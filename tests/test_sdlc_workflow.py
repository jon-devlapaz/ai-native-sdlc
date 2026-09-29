import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import unittest
from unittest.mock import patch
from types import SimpleNamespace

SOURCE = Path(__file__).resolve().parents[1] / 'assets/_system/scripts/sdlc.py'
spec = importlib.util.spec_from_file_location('workflow', SOURCE)
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        shutil.copytree(SOURCE.parents[2] / '_shared', self.root / '_shared')
        (self.root / '_system/scripts').mkdir(parents=True)
        shutil.copyfile(SOURCE, self.root / '_system/scripts/sdlc.py')
        (self.root / 'stages/01-plan').mkdir(parents=True)
        (self.root / 'stages/01-plan/CONTEXT.md').write_text('contract')
        (self.root / 'code.py').write_text('original')
        self.config([{'argv': ['python3', '-c', 'print("real check")'], 'timeout_seconds': 5}])
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@local', 'commit', '-qm', 'baseline')

    def git(self, *args):
        subprocess.run(['git', '-C', str(self.root), *args], check=True, capture_output=True)

    def config(self, checks, require_tink=False):
        (self.root / '_system/verification.json').write_text(json.dumps({'checks': checks, 'require_tink': require_tink}))

    def cli(self, *args, ok=True):
        result = subprocess.run(['python3', str(self.root / '_system/scripts/sdlc.py'), *args], cwd='/', capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def approve(self, stage='3'):
        self.cli('decide', 'example', stage, 'approved', '--reviewer', 'human', '--source', 'review:1', '--reason', 'accepted')

    def create_ready(self, *args):
        self.cli('new', 'example', *args)
        (self.root / 'runs/example/checklist.json').unlink()  # legacy run: no checklist enforcement
        self.approve()

    def test_slug_and_no_overwrite(self):
        self.cli('new', '../escape', ok=False)
        self.cli('new', 'example')
        brief = self.root / 'runs/example/brief.md'
        brief.write_text('human work')
        self.cli('new', 'example', ok=False)
        self.assertEqual(brief.read_text(), 'human work')

    def test_concurrent_creation(self):
        command = ['python3', str(self.root / '_system/scripts/sdlc.py'), 'new', 'race']
        a = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        b = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        a.communicate(); b.communicate()
        self.assertEqual(sorted([a.returncode, b.returncode]), [0, 1])
        self.assertTrue((self.root / 'runs/race/run.json').exists())

    def test_text_is_not_approval_or_verification(self):
        self.cli('new', 'example')
        (self.root / 'runs/example/brief.md').write_text('**Status:** approved')
        directory = self.root / 'runs/example/04-test/output'
        directory.mkdir(parents=True)
        (directory / 'test-log.md').write_text('all passed')
        out = self.cli('status', 'example')
        self.assertIn('Stage 3: pending', out)
        self.assertIn('Verification: not run (implementation may be pending; a text log is not passing evidence)', out)
        self.cli('verify', 'example', ok=False)

    def test_verification_wrapper_requires_run_id(self):
        wrapper = self.root / '_system/scripts/verify.sh'
        wrapper.write_text(
            '#!/usr/bin/env bash\n'
            'set -euo pipefail\n'
            'SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"\n'
            'if [ "$#" -ne 1 ]; then\n'
            '  echo "Usage: $0 <run-id>" >&2\n'
            '  echo "Create a run first with: ${SCRIPT_DIR}/new-run.sh <run-id>" >&2\n'
            '  exit 2\n'
            'fi\n'
            'exec python3 "${SCRIPT_DIR}/sdlc.py" verify "$@"\n'
        )
        wrapper.chmod(0o755)
        result = subprocess.run(['bash', str(wrapper)], cwd='/', capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('Usage:', result.stderr)
        self.assertIn('new-run.sh', result.stderr)

    def test_stale_approval_and_rejection(self):
        self.create_ready()
        (self.root / 'runs/example/brief.md').write_text('new requirements')
        self.assertIn('Stage 3: stale', self.cli('status', 'example'))
        self.approve()
        self.cli('decide', 'example', '3', 'changes-requested', '--reviewer', 'human', '--source', 'review:2', '--reason', 'scope')
        self.assertIn('changes-requested', self.cli('status', 'example'))
        self.cli('verify', 'example', ok=False)

    def test_full_dependency_chain(self):
        self.cli('new', 'example', '--profile', 'full')
        self.cli('decide', 'example', '2', 'approved', '--reviewer', 'human', '--source', 'review:1', '--reason', 'yes', ok=False)
        (self.root / 'runs/example/checklist.json').unlink()  # legacy run
        for stage in ['1', '2', '3']:
            self.approve(stage)
        (self.root / 'runs/example/01-plan/output/intent.md').write_text('changed intent')
        out = self.cli('status', 'example')
        self.assertIn('Stage 2: stale', out)
        self.assertIn('Stage 3: stale', out)

    def test_evidence_bound_to_code_and_log(self):
        self.create_ready()
        self.cli('verify', 'example')
        self.assertIn('Verification: current', self.cli('status', 'example'))
        (self.root / 'code.py').write_text('different')
        self.assertIn('stale', self.cli('status', 'example'))
        self.cli('verify', 'example')
        (self.root / 'runs/example/04-test/output/test-log.md').write_text('edited')
        self.assertIn('stale', self.cli('status', 'example'))

    def test_untracked_python_cache_does_not_fail_passing_suite(self):
        self.create_ready()
        (self.root / 'tests').mkdir()
        (self.root / 'tests/test_real.py').write_text('import unittest\nclass Check(unittest.TestCase):\n def test_ok(self): self.assertEqual(2 + 2, 4)\n')
        self.config([{'argv': ['python3', '-m', 'unittest', 'discover', '-s', 'tests'], 'timeout_seconds': 5}])
        self.cli('verify', 'example')
        self.assertTrue(list((self.root / 'tests/__pycache__').glob('*.pyc')))
        self.assertIn('Verification: current', self.cli('status', 'example'))

    def test_tracked_cache_remains_covered(self):
        self.create_ready()
        (self.root / 'tracked.pyc').write_bytes(b'original')
        self.git('add', 'tracked.pyc')
        self.cli('verify', 'example')
        (self.root / 'tracked.pyc').write_bytes(b'changed')
        self.assertIn('stale', self.cli('status', 'example'))

    def test_evidence_commit_preserves_content_verification(self):
        self.create_ready()
        self.cli('verify', 'example')
        self.git('add', 'runs')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@local', 'commit', '-qm', 'record evidence')
        self.assertIn('Verification: current', self.cli('status', 'example'))
        (self.root / 'code.py').write_text('changed source')
        self.git('add', 'code.py')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@local', 'commit', '-qm', 'change source')
        self.assertIn('stale', self.cli('status', 'example'))

    def test_missing_empty_failed_and_timeout_checks(self):
        self.create_ready()
        for checks in [[], [{'argv': ['missing-executable-sdlc'], 'timeout_seconds': 1}],
                       [{'argv': ['python3', '-c', 'raise SystemExit(1)'], 'timeout_seconds': 1}],
                       [{'argv': ['python3', '-c', 'import time; time.sleep(3)'], 'timeout_seconds': 1}]]:
            self.config(checks)
            self.cli('verify', 'example', ok=False)
            self.assertNotIn('Verification: current', self.cli('status', 'example'))

    def test_required_tink_is_not_optional(self):
        self.create_ready()
        self.config([{'argv': ['true'], 'timeout_seconds': 1}], True)
        original_run = workflow.subprocess.run
        def missing_tink(argv, **kwargs):
            if argv[0] == 'tink':
                raise FileNotFoundError('tink unavailable')
            return original_run(argv, **kwargs)
        with patch.object(workflow, 'ROOT', self.root), patch.object(workflow.subprocess, 'run', side_effect=missing_tink):
            with self.assertRaises(FileNotFoundError):
                workflow.verify(SimpleNamespace(run='example'))
        receipt = json.loads((self.root / 'runs/example/04-test/output/verification.json').read_text())
        self.assertEqual(receipt['result'], 'failed')

    def test_tink_lock_path_formula_pinned(self):
        expected_hash = hashlib.sha256(str(self.root.resolve()).encode()).hexdigest()[:12]
        expected = Path(tempfile.gettempdir()) / f'sdlc-tink-{os.getuid()}-{expected_hash}.lock'
        self.assertEqual(workflow.tink_lock_path(self.root), expected)

    def test_lock_file_created_with_restricted_permissions(self):
        lock = Path(self.temp.name) / 'perms.lock'
        old_umask = os.umask(0o022)
        try:
            with workflow.locked(lock):
                self.assertEqual(os.stat(lock).st_mode & 0o777, 0o600 & ~0o022)
        finally:
            os.umask(old_umask)

    def test_locked_times_out_while_flock_held(self):
        lock = Path(self.temp.name) / 'contention.lock'
        lock.touch()
        fd = os.open(lock, os.O_CREAT | os.O_RDWR)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            start = time.monotonic()
            with self.assertRaises(ValueError):
                with workflow.locked(lock, timeout=0.1, poll_interval=0.02):
                    pass
            self.assertGreaterEqual(time.monotonic() - start, 0.1)
        finally:
            try:
                fcntl.flock(fd, fcntl.LOCK_UN)
            except OSError:
                pass
            os.close(fd)

    def test_skills_under_flock_fails_without_running(self):
        with patch.object(workflow.tempfile, 'gettempdir', return_value=str(self.root)):
            lock = workflow.tink_lock_path(self.root)
        lock.touch()
        fd = os.open(lock, os.O_CREAT | os.O_RDWR)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            args = SimpleNamespace(tool='tink', arguments=['skill', 'check'])
            with patch.object(workflow, 'ROOT', self.root), patch.object(workflow.tempfile, 'gettempdir', return_value=str(self.root)):
                with patch.object(workflow.subprocess, 'run', side_effect=AssertionError('subprocess must not run')) as run_mock:
                    with self.assertRaises(ValueError):
                        workflow.skills(args)
                    run_mock.assert_not_called()
        finally:
            try:
                fcntl.flock(fd, fcntl.LOCK_UN)
            except OSError:
                pass
            os.close(fd)

    def test_locked_rejects_stale_directory(self):
        lock = Path(self.temp.name) / 'stale-dir.lock'
        lock.mkdir()
        with self.assertRaisesRegex(ValueError, 'Stale directory lock'):
            with workflow.locked(lock):
                pass

    def test_locked_rejects_symlink(self):
        target = Path(self.temp.name) / 'real.lock'
        target.touch()
        link = Path(self.temp.name) / 'link.lock'
        if link.exists() or link.is_symlink():
            link.unlink()
        link.symlink_to(target)
        with self.assertRaisesRegex(ValueError, 'must not be a symlink'):
            with workflow.locked(link):
                pass

    def test_locked_acquires_after_flock_released(self):
        lock = Path(self.temp.name) / 'release.lock'
        lock.touch()
        fd = os.open(lock, os.O_CREAT | os.O_RDWR)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)
        with workflow.locked(lock, timeout=1.0, poll_interval=0.02):
            pass

    def test_skill_wrapper_rejects_symlink(self):
        args = SimpleNamespace(tool='tink', arguments=['skill', 'check'])
        with patch.object(workflow, 'ROOT', self.root), patch.object(workflow.tempfile, 'gettempdir', return_value=str(self.root)):
            (self.root / '.agents').symlink_to(self.root, target_is_directory=True)
            with self.assertRaises(ValueError):
                workflow.skills(args)

    def test_skill_wrapper_tool_exit_codes(self):
        cases = [
            ('tink', 0, False),
            ('tink', 1, True),
            ('tink-route', 0, False),
            ('tink-route', 1, False),
            ('tink-route', 2, True),
        ]
        with patch.object(workflow, 'ROOT', self.root), patch.object(workflow.tempfile, 'gettempdir', return_value=str(self.root)):
            for tool, returncode, should_raise in cases:
                with self.subTest(tool=tool, returncode=returncode):
                    args = SimpleNamespace(tool=tool, arguments=['check'])
                    with patch.object(workflow.subprocess, 'run', return_value=subprocess.CompletedProcess([tool, 'check'], returncode)):
                        if should_raise:
                            with self.assertRaises(ValueError):
                                workflow.skills(args)
                        else:
                            self.assertIsNone(workflow.skills(args))
            with self.subTest(tool='unknown-tool'):
                args = SimpleNamespace(tool='unknown-tool', arguments=['check'])
                with patch.object(workflow.subprocess, 'run', return_value=subprocess.CompletedProcess(['unknown-tool', 'check'], 0)):
                    with self.assertRaises(ValueError):
                        workflow.skills(args)

    def test_skill_wrapper_cli_normalizes_unrouted(self):
        argv = ['sdlc.py', 'skills', 'tink-route', '--', 'check']
        run = subprocess.CompletedProcess(['tink-route', 'check'], 1)
        with patch.object(workflow, 'ROOT', self.root), patch.object(workflow.tempfile, 'gettempdir', return_value=str(self.root)), patch.object(workflow.subprocess, 'run', return_value=run), patch.object(workflow.sys, 'argv', argv):
            self.assertEqual(workflow.main(), 0)

    def test_candidate_mutation_during_check(self):
        self.create_ready()
        self.config([{'argv': ['python3', '-c', 'from pathlib import Path; Path("code.py").write_text("modified")'], 'timeout_seconds': 2}])
        self.assertIn('changed during verification', self.cli('verify', 'example', ok=False))

    def test_bug_requires_unchanged_test_baseline(self):
        self.create_ready('--kind', 'bug')
        self.cli('verify', 'example', ok=False)
        (self.root / 'regression.py').write_text('assert True')
        self.cli('lock-tests', 'example', 'regression.py', '--source', 'review:3', '--failure-evidence', 'ci:failed-reproduction')
        self.cli('verify', 'example')
        (self.root / 'regression.py').write_text('weakened')
        self.cli('verify', 'example', ok=False)

    def test_symlink_run_rejected(self):
        (self.root / 'runs').mkdir()
        (self.root / 'runs/link').symlink_to(self.root, target_is_directory=True)
        self.cli('status', 'link', ok=False)

    # ---- JSON checklist ----

    def checklist_path(self):
        return self.root / 'runs/example/checklist.json'

    def write_checklist(self, items, raw=None):
        text = raw if raw is not None else json.dumps({'schema': 1, 'items': items})
        self.checklist_path().write_text(text)

    def item(self, ident, **extra):
        return {'id': ident, 'description': f'do {ident}', 'verify': f'check {ident}', **extra}

    def checklist_ready(self, ids=('alpha',), *args):
        self.cli('new', 'example', *args)
        self.write_checklist([self.item(i) for i in ids])
        self.approve()

    def mark(self, item, result='passed', evidence='observed', ok=True):
        return self.cli('mark', 'example', item, result, '--evidence', evidence, ok=ok)

    def receipts(self):
        return sorted((self.root / 'runs/example/marks').glob('*.json'))

    def test_new_run_has_empty_valid_checklist(self):
        for profile in ['light', 'full']:
            with self.subTest(profile=profile):
                shutil.rmtree(self.root / 'runs', ignore_errors=True)
                self.cli('new', 'example', '--profile', profile)
                self.assertEqual(json.loads(self.checklist_path().read_text()), {'schema': 1, 'items': []})
                self.assertIn('Checklist: 0/0 passed', self.cli('status', 'example'))

    def test_approval_requires_nonempty_valid_checklist(self):
        self.cli('new', 'example')
        args = ('decide', 'example', '3', 'approved', '--reviewer', 'h', '--source', 's', '--reason', 'r')
        self.assertIn('at least one checklist item', self.cli(*args, ok=False))
        self.cli('decide', 'example', '3', 'changes-requested', '--reviewer', 'h', '--source', 's', '--reason', 'r')
        self.write_checklist([], raw='{not json')
        self.cli(*args, ok=False)
        self.cli('decide', 'example', '3', 'changes-requested', '--reviewer', 'h', '--source', 's', '--reason', 'r')
        self.write_checklist([self.item('alpha')])
        self.cli(*args)
        self.assertIn('Stage 3: approved', self.cli('status', 'example'))

    def test_invalid_checklists_rejected(self):
        self.cli('new', 'example')
        bad = {
            'extra key passes': [self.item('alpha', passes=True)],
            'extra key status': [self.item('alpha', status='done')],
            'duplicate ids': [self.item('alpha'), self.item('alpha')],
            'uppercase id': [self.item('Alpha')],
            'leading hyphen': [self.item('-alpha')],
            'long id': [self.item('a' * 41)],
            'blank description': [{'id': 'alpha', 'description': '  ', 'verify': 'x'}],
            'missing verify': [{'id': 'alpha', 'description': 'x'}],
        }
        for name, items in bad.items():
            with self.subTest(name):
                self.write_checklist(items)
                out = self.cli('decide', 'example', '3', 'approved', '--reviewer', 'h', '--source', 's', '--reason', 'r', ok=False)
                self.assertIn('Error:', out)
        self.write_checklist([], raw=json.dumps({'schema': 2, 'items': [self.item('alpha')]}))
        self.cli('decide', 'example', '3', 'approved', '--reviewer', 'h', '--source', 's', '--reason', 'r', ok=False)
        self.write_checklist([], raw='[]')
        self.cli('decide', 'example', '3', 'approved', '--reviewer', 'h', '--source', 's', '--reason', 'r', ok=False)
        self.write_checklist([self.item('alpha', passes=True)])
        self.assertIn('alpha', self.cli('decide', 'example', '3', 'approved', '--reviewer', 'h', '--source', 's', '--reason', 'r', ok=False))

    def test_checklist_definition_edit_stales_approval_but_reformat_does_not(self):
        self.checklist_ready()
        self.assertIn('Stage 3: approved', self.cli('status', 'example'))
        data = json.loads(self.checklist_path().read_text())
        self.checklist_path().write_text(json.dumps({'items': [dict(reversed(list(data['items'][0].items())))], 'schema': 1}, indent=8))
        self.assertIn('Stage 3: approved', self.cli('status', 'example'))
        self.write_checklist([{**self.item('alpha'), 'verify': 'weaker'}])
        self.assertIn('Stage 3: stale', self.cli('status', 'example'))
        self.approve()
        self.write_checklist([self.item('alpha'), self.item('beta')])
        self.assertIn('Stage 3: stale', self.cli('status', 'example'))
        self.approve()
        self.checklist_path().unlink()
        self.assertIn('Stage 3: stale', self.cli('status', 'example'))

    def test_full_profile_checklist_binds_stage_three_only(self):
        self.cli('new', 'example', '--profile', 'full')
        self.write_checklist([self.item('alpha')])
        for stage in ['1', '2', '3']:
            self.approve(stage)
        self.write_checklist([self.item('alpha'), self.item('beta')])
        out = self.cli('status', 'example')
        self.assertIn('Stage 1: approved', out)
        self.assertIn('Stage 2: approved', out)
        self.assertIn('Stage 3: stale', out)
        self.approve()
        self.assertIn('Checklist: 0/2 passed', self.cli('status', 'example'))

    def test_mark_preconditions(self):
        self.cli('new', 'example')
        self.write_checklist([self.item('alpha')])
        self.mark('alpha', ok=False)  # gate not approved
        self.approve()
        self.mark('nope', ok=False)
        self.mark('alpha', evidence='   ', ok=False)
        self.cli('mark', 'example', 'alpha', 'passed', ok=False)
        self.cli('mark', 'example', 'alpha', 'maybe', '--evidence', 'x', ok=False)
        self.assertEqual(self.receipts(), [])
        self.write_checklist([self.item('alpha')], raw='{bad')
        self.mark('alpha', ok=False)
        self.write_checklist([self.item('alpha')])
        self.mark('alpha')
        self.cli('mark', 'missing-run', 'alpha', 'passed', '--evidence', 'x', ok=False)

    def test_mark_requires_current_approval(self):
        self.checklist_ready()
        self.write_checklist([self.item('alpha'), self.item('beta')])  # stale
        self.mark('alpha', ok=False)

    def test_mark_appends_receipts_and_never_rewrites(self):
        self.checklist_ready(('alpha', 'beta'))
        self.mark('alpha', evidence='first')
        first = self.receipts()[0]
        before = (first.read_bytes(), first.stat().st_mtime_ns)
        self.mark('alpha', 'failed', evidence='second')
        self.mark('beta')
        self.assertEqual(len(self.receipts()), 3)
        self.assertEqual((first.read_bytes(), first.stat().st_mtime_ns), before)
        record = json.loads(first.read_text())
        self.assertEqual(set(record), {'item', 'result', 'evidence', 'candidate', 'time_ns'})
        self.assertEqual((record['item'], record['result'], record['evidence']), ('alpha', 'passed', 'first'))
        self.assertEqual(record['candidate'], workflow_tree(self.root))
        self.assertTrue(first.name.startswith(f"alpha-{record['time_ns']}-"))

    def test_latest_mark_wins(self):
        self.checklist_ready()
        self.mark('alpha')
        self.assertIn('Checklist: 1/1 passed', self.cli('status', 'example'))
        self.mark('alpha', 'failed', evidence='regressed')
        out = self.cli('status', 'example')
        self.assertIn('Checklist: 0/1 passed', out)
        self.assertIn('  - alpha: failed', out)
        self.mark('alpha')
        self.assertIn('Checklist: 1/1 passed', self.cli('status', 'example'))

    def test_orphan_marks_ignored(self):
        self.checklist_ready(('alpha', 'beta'))
        self.mark('beta')
        self.write_checklist([self.item('alpha')])
        self.approve()
        out = self.cli('status', 'example')
        self.assertIn('Checklist: 0/1 passed', out)
        self.assertNotIn('beta', out)

    def test_status_checklist_lines(self):
        self.checklist_ready(('alpha', 'beta', 'gamma'))
        out = self.cli('status', 'example')
        self.assertIn('Checklist: 0/3 passed\n  - alpha: pending\n  - beta: pending\n  - gamma: pending\n', out)
        self.assertLess(out.index('Stage 3'), out.index('Checklist:'))
        self.assertLess(out.index('Checklist:'), out.index('Verification'))
        self.mark('alpha')
        self.mark('beta', 'failed', evidence='broken')
        out = self.cli('status', 'example')
        self.assertIn('Checklist: 1/3 passed', out)
        self.assertNotIn('  - alpha:', out)
        self.assertIn('  - beta: failed', out)
        self.assertIn('  - gamma: pending', out)
        (self.root / 'code.py').write_text('changed after mark')
        out = self.cli('status', 'example')
        self.assertIn('Checklist: 1/3 passed', out)
        self.assertIn('  - alpha: passed on an older candidate (re-mark after changes)', out)
        self.mark('alpha')
        self.assertNotIn('older candidate', self.cli('status', 'example'))

    def test_status_survives_snapshot_failure(self):
        self.checklist_ready()
        self.mark('alpha')
        shutil.rmtree(self.root / '.git')
        out = self.cli('status', 'example')
        self.assertIn('Checklist: 1/1 passed', out)

    def test_verify_requires_all_items_passed(self):
        self.checklist_ready(('alpha', 'beta'))
        out = self.cli('verify', 'example', ok=False)
        self.assertIn('Checklist incomplete: alpha, beta', out)
        receipt = self.root / 'runs/example/04-test/output/verification.json'
        self.assertEqual(json.loads(receipt.read_text())['result'], 'failed')
        self.mark('alpha')
        self.mark('beta', 'failed', evidence='no')
        self.assertIn('Checklist incomplete: beta', self.cli('verify', 'example', ok=False))
        self.mark('beta')
        self.cli('verify', 'example')
        passed = json.loads(receipt.read_text())
        self.assertEqual(passed['result'], 'passed')
        self.assertEqual(passed['checklist'], workflow_checklist_digest(self.checklist_path()))
        self.assertIn('Verification: current', self.cli('status', 'example'))

    def test_verify_does_not_require_marks_on_current_tree(self):
        self.checklist_ready()
        self.mark('alpha')
        (self.root / 'code.py').write_text('changed after mark')
        self.cli('verify', 'example')
        self.assertIn('older candidate', self.cli('status', 'example'))

    def test_checklist_change_stales_verification(self):
        self.checklist_ready()
        self.mark('alpha')
        self.cli('verify', 'example')
        receipt = self.root / 'runs/example/04-test/output/verification.json'
        record = json.loads(receipt.read_text())
        # Definitions changed but approval renewed: receipt digest must differ.
        self.write_checklist([{**self.item('alpha'), 'verify': 'stricter'}])
        self.approve()
        self.assertNotIn('Verification: current', self.cli('status', 'example'))
        self.assertIn('checklist', record)

    def test_legacy_run_without_checklist_unaffected(self):
        self.cli('new', 'example')
        self.checklist_path().unlink()
        self.approve()
        out = self.cli('status', 'example')
        self.assertIn('Checklist: none (legacy run)', out)
        self.assertIn('Stage 3: approved', out)
        self.mark('alpha', ok=False)
        self.cli('verify', 'example')
        receipt = json.loads((self.root / 'runs/example/04-test/output/verification.json').read_text())
        self.assertNotIn('checklist', receipt)
        self.assertIn('Verification: current', self.cli('status', 'example'))

    def test_concurrent_marks_leave_valid_receipts(self):
        self.checklist_ready(('alpha', 'beta'))
        script = str(self.root / '_system/scripts/sdlc.py')
        procs = [subprocess.Popen(['python3', script, 'mark', 'example', ['alpha', 'beta'][i % 2], 'passed',
                                   '--evidence', f'proc {i}'], cwd='/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                 for i in range(6)]
        for proc in procs:
            proc.communicate()
            self.assertEqual(proc.returncode, 0)
        receipts = self.receipts()
        self.assertEqual(len(receipts), 6)
        self.assertEqual(len({r.name for r in receipts}), 6)
        for receipt in receipts:
            self.assertEqual(json.loads(receipt.read_text())['result'], 'passed')
        self.assertIn('Checklist: 2/2 passed', self.cli('status', 'example'))


def workflow_tree(root):
    with patch.object(workflow, 'ROOT', root):
        return workflow.snapshot()['tree']


def workflow_checklist_digest(path):
    return hashlib.sha256(json.dumps(json.loads(path.read_text()), sort_keys=True).encode()).hexdigest()


if __name__ == '__main__':
    unittest.main()
