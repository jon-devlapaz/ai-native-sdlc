#!/usr/bin/env python3
"""Local workflow evidence. Human identity and release authority belong to the forge."""
import argparse
import contextlib
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import uuid

ROOT = Path(__file__).resolve().parents[2]
ITEM_ID = re.compile(r'[a-z0-9][a-z0-9-]{0,39}')
ITEM_KEYS = {'id', 'description', 'verify'}
CHECK_KEYS = {'argv', 'timeout_seconds'}
ARTIFACTS = ['01-plan/output/intent.md', '02-design/output/spec.md', '03-build/output/plan.md']


def digest(value):
    return hashlib.sha256(value).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True).encode()


def read_json(path):
    return json.loads(path.read_text())


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(value, stream, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def run_path(slug):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,79}', slug):
        raise ValueError('Run name must be 1–80 lowercase letters, digits, or hyphens; start with a letter or digit.')
    path = ROOT / 'runs' / slug
    if path.resolve() != path.absolute():
        raise ValueError('Run paths must not contain symlinks.')
    return path


def tink_lock_path(root=ROOT):
    repo_id = digest(str(root.resolve()).encode())[:12]
    return Path(tempfile.gettempdir()) / f'sdlc-tink-{os.getuid()}-{repo_id}.lock'


@contextlib.contextmanager
def locked(path, timeout=5.0, poll_interval=0.05):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    except OSError as error:
        if error.errno == errno.ELOOP:
            raise ValueError(f'Lock path must not be a symlink: {path}') from error
        if error.errno == errno.EISDIR:
            raise ValueError(f'Stale directory lock found at {path}. Remove it to allow file flock.') from error
        raise
    st = os.fstat(fd)
    if not stat.S_ISREG(st.st_mode):
        os.close(fd)
        raise ValueError(f'Lock path must be a regular file: {path}')
    with open(fd, 'a+b', closefd=True) as handle:
        start = time.monotonic()
        while True:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError as error:
                if error.errno not in (errno.EAGAIN, errno.EACCES):
                    raise
                if time.monotonic() - start >= timeout:
                    raise ValueError(f'Busy or interrupted operation: {path}. Confirm no writer remains before removing this lock.')
                time.sleep(poll_interval)
        yield


def require_run(path):
    if not path.is_dir() or not (path / 'run.json').is_file():
        raise ValueError('Run is missing or legacy. Create a new run; legacy artifacts remain readable but are not approved evidence.')
    return read_json(path / 'run.json')


def validate_check(check, exact=False):
    """Shared argv/timeout rules for verification.json checks and checklist item checks."""
    if not isinstance(check, dict):
        raise ValueError('A check must be an object with argv and timeout_seconds.')
    if exact and set(check) != CHECK_KEYS:
        raise ValueError('A check must have exactly the keys argv, timeout_seconds.')
    argv = check.get('argv')
    if not isinstance(argv, list) or not argv or not all(isinstance(a, str) and a for a in argv):
        raise ValueError('Every check requires a nonempty argv array.')
    timeout = check.get('timeout_seconds')
    if not isinstance(timeout, int) or isinstance(timeout, bool) or timeout <= 0:
        raise ValueError('Every check requires a positive timeout_seconds.')


def validate_checklist(value):
    """Return the item list of a checklist definition, or raise ValueError naming the problem."""
    if not isinstance(value, dict) or set(value) != {'schema', 'items'}:
        raise ValueError('Checklist must be an object with exactly "schema" and "items".')
    if value['schema'] != 1 or isinstance(value['schema'], bool):
        raise ValueError('Checklist schema must be 1.')
    items = value['items']
    if not isinstance(items, list):
        raise ValueError('Checklist items must be a list.')
    seen = set()
    for index, item in enumerate(items):
        name = item.get('id') if isinstance(item, dict) and isinstance(item.get('id'), str) else f'#{index + 1}'
        if not isinstance(item, dict) or not ITEM_KEYS <= set(item) <= ITEM_KEYS | {'check'}:
            raise ValueError(f'Checklist item {name} must have the keys id, description, verify, and optionally check.')
        if not ITEM_ID.fullmatch(item['id']):
            raise ValueError(f'Checklist item {name} has an invalid id (use [a-z0-9][a-z0-9-]{{0,39}}).')
        if item['id'] in seen:
            raise ValueError(f'Checklist item {name} has a duplicate id.')
        seen.add(item['id'])
        for key in ('description', 'verify'):
            if not isinstance(item[key], str) or not item[key].strip():
                raise ValueError(f'Checklist item {name} needs a nonempty {key}.')
        if 'check' in item:
            try:
                validate_check(item['check'], exact=True)
            except ValueError as error:
                raise ValueError(f'Checklist item {name} has an invalid check: {error}') from error
    return items


def load_checklist(path):
    """None for legacy runs without checklist.json; otherwise the validated item list."""
    target = path / 'checklist.json'
    if not target.exists():
        return None
    try:
        return validate_checklist(read_json(target))
    except json.JSONDecodeError as error:
        raise ValueError(f'checklist.json is not valid JSON: {error}') from error


def checklist_digest(path):
    """Digest of canonical definitions (whitespace/key order insensitive); None when absent."""
    target = path / 'checklist.json'
    if not target.exists():
        return None
    try:
        return digest(encoded(read_json(target)))
    except ValueError:
        return digest(target.read_bytes())


def marks(path, items):
    """Latest valid receipt per current item id; receipts for removed items are ignored."""
    ids = {item['id'] for item in items}
    latest_marks = {}
    for receipt in (path / 'marks').glob('*.json') if (path / 'marks').is_dir() else []:
        try:
            record = read_json(receipt)
            key = (record['time_ns'], receipt.name)
            if record['item'] in ids and record['result'] in ('passed', 'failed') and isinstance(record['time_ns'], int):
                if record['item'] not in latest_marks or key > latest_marks[record['item']][0]:
                    latest_marks[record['item']] = (key, record)
        except (ValueError, KeyError, TypeError, OSError):
            continue
    return {item: record for item, (_, record) in latest_marks.items()}


def inputs(path, stage):
    metadata = require_run(path)
    files = [path / 'brief.md'] if metadata['profile'] == 'light' else [path / p for p in ARTIFACTS[:stage]]
    files += sorted((ROOT / 'stages').glob('*/CONTEXT.md'))
    values = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in files}
    if stage == 3 and checklist_digest(path) is not None:
        values[str((path / 'checklist.json').relative_to(ROOT))] = checklist_digest(path)
    return digest(encoded(values))


def latest(path, stage):
    records = sorted((path / 'decisions').glob(f'{stage}-*.json'))
    return read_json(records[-1]) if records else None


def gate(path, stage):
    record = latest(path, stage)
    if record is None:
        return 'pending'
    if record['inputs'] != inputs(path, stage):
        return 'stale'
    return record['decision']


def stages(path):
    return [3] if require_run(path)['profile'] == 'light' else [1, 2, 3]


def ready(path):
    for stage in stages(path):
        if gate(path, stage) != 'approved':
            raise ValueError(f'Stage {stage} needs a current approval receipt.')


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], stderr=subprocess.PIPE)


def snapshot():
    head = git('rev-parse', 'HEAD').decode().strip()
    tracked = set(git('ls-files', '-z', '--cached').split(b'\0'))
    names = tracked | set(git('ls-files', '-z', '--others', '--exclude-standard').split(b'\0'))
    files = {}
    for name in names:
        if not name:
            continue
        relative = os.fsdecode(name)
        if relative.startswith('runs/'):
            continue
        # Ignore disposable Python caches only when untracked. Tracked files
        # remain covered even when their name resembles generated output.
        parts = Path(relative).parts
        if name not in tracked and (any(part in {'__pycache__', '.pytest_cache', '.ruff_cache'} for part in parts)
                                    or Path(relative).suffix in {'.pyc', '.pyo'}):
            continue
        path = ROOT / relative
        if path.is_symlink():
            value = os.readlink(path).encode()
        elif path.is_file():
            value = path.read_bytes()
        elif not path.exists():
            value = b'<deleted>'
        else:
            raise ValueError(f'Unsupported candidate path: {relative}')
        files[relative] = [digest(value), path.lstat().st_mode if path.exists() or path.is_symlink() else 0]
    return {'head': head, 'tree': digest(encoded(files))}


def checks_config():
    config = read_json(ROOT / '_system/verification.json')
    checks = config.get('checks')
    if not isinstance(config.get('require_tink'), bool) or not isinstance(checks, list) or not checks:
        raise ValueError('Verification requires an explicit Tink policy and a nonempty check list.')
    for check in checks:
        validate_check(check)
    return config


def test_lock(path):
    lock = path / 'test-lock.json'
    if not lock.exists():
        if require_run(path)['kind'] == 'bug':
            raise ValueError('Bug runs require a reproduction test lock.')
        return None
    record = read_json(lock)
    for name, expected in record['files'].items():
        target = ROOT / name
        if target.is_symlink() or not target.is_file() or digest(target.read_bytes()) != expected:
            raise ValueError(f'Locked test input changed or disappeared: {name}')
    return digest(lock.read_bytes())


def evidence_inputs(path):
    return {'candidate': snapshot(), 'inputs': inputs(path, 3),
            'policy': digest((ROOT / '_system/verification.json').read_bytes()),
            'test_lock': test_lock(path),
            **({'checklist': checklist_digest(path)} if checklist_digest(path) is not None else {})}


def create(args):
    path = run_path(args.run)
    path.parent.mkdir(exist_ok=True)
    with locked(path.parent / f'.{args.run}.lock'):
        if path.exists():
            raise ValueError('Run already exists; nothing overwritten.')
        temporary = Path(tempfile.mkdtemp(prefix=f'.{args.run}-', dir=path.parent))
        try:
            write_json(temporary / 'run.json', {'profile': args.profile, 'kind': args.kind, 'schema': 1})
            write_json(temporary / 'checklist.json', {'schema': 1, 'items': []})
            if args.profile == 'light':
                shutil.copyfile(ROOT / '_shared/brief-template.md', temporary / 'brief.md')
            else:
                for target, template in zip(ARTIFACTS, ['intent', 'spec', 'plan']):
                    dest = temporary / target
                    dest.parent.mkdir(parents=True)
                    shutil.copyfile(ROOT / '_shared' / f'{template}-template.md', dest)
            temporary.rename(path)
        finally:
            if temporary.exists():
                shutil.rmtree(temporary)
    print(f'Created {path}. Next: define the change and obtain a human review.')


def decide(args):
    path = run_path(args.run)
    require_run(path)
    with locked(path / '.writer-lock'):
        if args.stage not in stages(path):
            raise ValueError('Light runs use stage 3 for their combined definition gate.')
        if args.decision == 'approved' and args.stage == 3 and load_checklist(path) == []:
            raise ValueError('Define at least one checklist item before approval.')
        if args.decision == 'approved':
            for stage in stages(path):
                if stage < args.stage and gate(path, stage) != 'approved':
                    raise ValueError(f'Approve stage {stage} first.')
        write_json(path / 'decisions' / f'{args.stage}-{time.time_ns()}-{uuid.uuid4().hex}.json', {
            'inputs': inputs(path, args.stage), 'decision': args.decision,
            **({'has_checklist': True} if args.stage == 3 and (path / 'checklist.json').exists() else {}),
            'reviewer': args.reviewer, 'source': args.source, 'reason': args.reason})
    print('Recorded local review receipt. Release approval must be independently authenticated by the forge.')


def verify(args):
    path = run_path(args.run)
    require_run(path)
    with locked(path / '.writer-lock'):
        output = path / '04-test/output'
        output.mkdir(parents=True, exist_ok=True)
        receipt = output / 'verification.json'
        write_json(receipt, {'result': 'running'})
        try:
            ready(path)
            config = checks_config()
            before = evidence_inputs(path)
            items = load_checklist(path)
            checks = list(config['checks'])
            if config['require_tink']:
                checks.insert(0, {'argv': ['tink', 'skill', 'check'], 'timeout_seconds': 120})
            with (output / 'test-log.md').open('w') as log:
                for check in checks:
                    log.write(f"\n$ {json.dumps(check['argv'])}\n")
                    log.flush()
                    result = subprocess.run(check['argv'], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                            timeout=check['timeout_seconds'])
                    if result.returncode:
                        raise ValueError(f"Check failed ({result.returncode}): {check['argv']}")
                for item in items or []:
                    if 'check' not in item:
                        continue
                    check = item['check']
                    log.write(f"\n# checklist item {item['id']}\n$ {json.dumps(check['argv'])}\n")
                    log.flush()
                    try:
                        result = subprocess.run(check['argv'], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                                timeout=check['timeout_seconds'])
                    except (subprocess.TimeoutExpired, OSError) as error:
                        log.write(f'{type(error).__name__}: {error}\n')
                        raise ValueError(f"Checklist check failed: {item['id']}") from error
                    if result.returncode:
                        raise ValueError(f"Checklist check failed: {item['id']}")
            if before != evidence_inputs(path):
                raise ValueError('Candidate or inputs changed during verification; rerun against stable inputs.')
            ready(path)
            proof = {}
            if items is not None:
                marked = marks(path, items)
                attested = [item['id'] for item in items if 'check' not in item]
                missing = [i for i in attested if marked.get(i, {}).get('result') != 'passed']
                if missing:
                    raise ValueError(f"Checklist incomplete: {', '.join(missing)}")
                proof = {'checklist_items': {item['id']: 'proven' if 'check' in item else 'attested' for item in items}}
            write_json(receipt, {'result': 'passed', **before, **proof, 'log': digest((output / 'test-log.md').read_bytes())})
        except Exception as error:
            write_json(receipt, {'result': 'failed', 'error': str(error)})
            raise
    print('Configured checks passed for the recorded candidate. Human release review remains required.')


def lock_tests(args):
    path = run_path(args.run)
    require_run(path)
    with locked(path / '.writer-lock'):
        record = path / 'test-lock.json'
        if record.exists():
            raise ValueError('Test lock already exists. A corrected baseline requires a new run and independent review.')
        files = {}
        for name in args.paths:
            target = ROOT / name
            if target.resolve() != target.absolute() or not target.is_file() or not target.is_relative_to(ROOT) or '..' in Path(name).parts:
                raise ValueError('Lock only regular files inside the checkout.')
            files[str(target.relative_to(ROOT))] = digest(target.read_bytes())
        write_json(record, {'files': files, 'candidate': snapshot(), 'review_source': args.source,
                            'failure_evidence': args.failure_evidence})
    print('Local test baseline recorded. CI must independently validate the failing reproduction and protect the baseline.')


def mark(args):
    path = run_path(args.run)
    require_run(path)
    evidence = args.evidence.strip()
    if not evidence:
        raise ValueError('Evidence must be nonempty.')
    with locked(path / '.writer-lock'):
        items = load_checklist(path)
        if items is None:
            raise ValueError('Run has no checklist.json (legacy run); nothing to mark.')
        if args.item not in {item['id'] for item in items}:
            raise ValueError(f'Unknown checklist item: {args.item}')
        if any(item['id'] == args.item and 'check' in item for item in items):
            raise ValueError(f'item {args.item} has an executable check; run verify to prove it')
        if gate(path, 3) != 'approved':
            raise ValueError('Stage 3 needs a current approval receipt before items can be marked.')
        now = time.time_ns()
        write_json(path / 'marks' / f'{args.item}-{now}-{uuid.uuid4().hex}.json', {
            'item': args.item, 'result': args.result, 'evidence': evidence,
            'candidate': snapshot()['tree'], 'time_ns': now})
    print(f'Recorded {args.result} receipt for {args.item}.')


def print_checklist(path, verified=False):
    try:
        items = load_checklist(path)
    except ValueError as error:
        print(f'Checklist: invalid ({error})')
        return
    if items is None:
        decision = latest(path, 3)
        print('Checklist: MISSING (deleted after approval)' if decision and decision.get('has_checklist')
              else 'Checklist: none (legacy run)')
        return
    if not items:
        print('Checklist: no items defined')
        return
    try:
        tree = snapshot()['tree']
    except (ValueError, OSError, subprocess.SubprocessError):
        tree = None
    marked = marks(path, items)
    lines = []
    passed = 0
    for item in items:
        record = marked.get(item['id'])
        if 'check' in item:
            if verified:
                passed += 1
            else:
                lines.append(f"  - {item['id']}: pending (proved by verify)")
        elif record is None:
            lines.append(f"  - {item['id']}: pending")
        elif record['result'] != 'passed':
            lines.append(f"  - {item['id']}: failed")
        else:
            passed += 1
            if tree is not None and record.get('candidate') != tree:
                lines.append(f"  - {item['id']}: passed on an older candidate (re-mark after changes)")
    proven = sum('check' in item for item in items)
    summary = f'Checklist: {passed}/{len(items)} passed ({proven} proven by check, {len(items) - proven} attested)'
    print('\n'.join([summary] + lines))


def evidence_matches(record, current):
    # HEAD records provenance. Evidence-only commits must not stale unchanged
    # candidate contents; CI still needs a check for the actual merge revision.
    return (record.get('candidate', {}).get('tree') == current['candidate']['tree']
            and all(record.get(key) == value for key, value in current.items() if key != 'candidate'))


def status(args):
    if not args.run:
        directory = ROOT / 'runs'
        print('\n'.join(p.name for p in sorted(directory.iterdir()) if p.is_dir() and not p.name.startswith('.')) if directory.exists() else 'No runs.')
        return
    path = run_path(args.run)
    require_run(path)
    blocked = False
    for stage in stages(path):
        state = gate(path, stage)
        print(f'Stage {stage}: {state}' + (' (blocked by upstream gate)' if blocked else ''))
        if state != 'approved' and not blocked:
            print(f'Next: revise/review stage {stage}; record the human decision.')
            blocked = True
    record_path = path / '04-test/output/verification.json'
    record = read_json(record_path) if record_path.exists() else None
    verified = False
    if record is not None and record.get('result') == 'passed':
        try:
            verified = evidence_matches(record, evidence_inputs(path)) and record['log'] == digest((record_path.parent / 'test-log.md').read_bytes())
        except (ValueError, OSError, subprocess.SubprocessError, KeyError):
            pass
    print_checklist(path, verified)
    if record is not None:
        print('Verification: ' + ('current' if verified and not blocked else 'failed, stale, or blocked'))
    else:
        print('Verification: not run (implementation may be pending; a text log is not passing evidence)')
    if not blocked:
        print('Next: independent PR review and release checks.' if verified else 'Next: implement the approved brief, then run verification.')
    print('Deployment: not inferred from local review files; consult the deployment system.')


# tink-route uses exit 1 to mean "no skill applies" — a successful no-op, not a failure.
TOOL_ACCEPTABLE_CODES = {
    'tink': (0,),
    'tink-route': (0, 1),
}


def skills(args):
    allowed = TOOL_ACCEPTABLE_CODES.get(args.tool)
    if allowed is None:
        raise ValueError(f'Unknown skill tool: {args.tool!r}')
    # All cooperating worktrees on this host share a mutation lock. This is not
    # a security boundary and cannot coordinate tools invoked outside this wrapper.
    for relative in ['.agents', '.agents/skills', '.tink']:
        target = ROOT / relative
        if target.resolve() != target.absolute():
            raise ValueError('Skill state must not be symlinked across worktrees.')
    arguments = list(args.arguments)
    if arguments[:1] == ['--']:
        arguments.pop(0)
    if not arguments:
        raise ValueError('Supply the authorized Tink/router operation.')
    lock = tink_lock_path(ROOT)
    with locked(lock):
        result = subprocess.run([args.tool, *arguments], cwd=ROOT)
        if result.returncode not in allowed:
            raise ValueError(f'{args.tool} failed with exit code {result.returncode}; inspect partial state before retrying.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    new = commands.add_parser('new')
    new.add_argument('run')
    new.add_argument('--profile', choices=['light', 'full'], default='light')
    new.add_argument('--kind', choices=['feature', 'bug'], default='feature')
    state = commands.add_parser('status')
    state.add_argument('run', nargs='?')
    decision = commands.add_parser('decide')
    decision.add_argument('run')
    decision.add_argument('stage', type=int, choices=[1, 2, 3])
    decision.add_argument('decision', choices=['approved', 'changes-requested'])
    for flag in ['reviewer', 'source', 'reason']:
        decision.add_argument('--' + flag, required=True)
    verification = commands.add_parser('verify')
    verification.add_argument('run')
    marking = commands.add_parser('mark')
    marking.add_argument('run')
    marking.add_argument('item')
    marking.add_argument('result', choices=['passed', 'failed'])
    marking.add_argument('--evidence', required=True)
    baseline = commands.add_parser('lock-tests')
    baseline.add_argument('run')
    baseline.add_argument('paths', nargs='+')
    baseline.add_argument('--source', required=True)
    baseline.add_argument('--failure-evidence', required=True)
    skill = commands.add_parser('skills')
    skill.add_argument('tool', choices=list(TOOL_ACCEPTABLE_CODES))
    skill.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        {'new': create, 'status': status, 'decide': decide, 'verify': verify, 'mark': mark, 'lock-tests': lock_tests, 'skills': skills}[args.command](args)
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
