"""One entry point: agents run `python3 _system/scripts/sdlc.py <command>`; no wrapper scripts ship.

Written before the change. A wrapper is a second command form, and each form is another permission prompt
and another string for an agent to get wrong.
"""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
INIT = ROOT / 'scripts/init.py'
WRAPPER = re.compile(r'\b(status|verify|new-run)\.sh\b')


def shipped_text_files():
    files = [p for p in ASSETS.rglob('*') if p.is_file() and p.suffix in {'.md', '.py', '.json'} and p.name != 'manifest.json'
             and '__pycache__' not in p.parts]
    return files + [INIT, ROOT / 'README.md']


class EntryPoint(unittest.TestCase):
    def test_no_wrapper_script_ships(self):
        self.assertEqual(sorted(p.name for p in (ASSETS / '_system/scripts').glob('*.sh')), [])
        manifest = json.loads((ASSETS / 'manifest.json').read_text())['files']
        self.assertEqual([name for name in manifest if name.endswith('.sh')], [])

    def test_no_shipped_text_names_a_wrapper(self):
        for path in shipped_text_files():
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertIsNone(WRAPPER.search(path.read_text()), WRAPPER.search(path.read_text()))

    def test_docs_name_the_one_command_form(self):
        sdlc = (ASSETS / '_system/SDLC.md').read_text()
        for command in ('new', 'status', 'verify'):
            self.assertIn(f'python3 _system/scripts/sdlc.py {command}', sdlc, command)
        self.assertIn('python3 _system/scripts/sdlc.py verify <slug>', (ASSETS / 'stages/04-test/CONTEXT.md').read_text())
        self.assertIn('python3 _system/scripts/sdlc.py status', (ASSETS / 'stages/01-plan/CONTEXT.md').read_text())
        router = re.search(r"ROUTER = '''(.*?)'''", INIT.read_text(), re.S).group(1)
        self.assertIn('python3 _system/scripts/sdlc.py status', router)

    def test_install_creates_no_wrapper_and_upgrade_removes_an_unmodified_one(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run([sys.executable, str(INIT), str(root)], capture_output=True, text=True, check=True)
            self.assertEqual(list((root / '_system/scripts').glob('*.sh')), [])
            wrapper = root / '_system/scripts/status.sh'
            wrapper.write_text('#!/usr/bin/env bash\nexec python3 "$(dirname "$0")/sdlc.py" status "$@"\n')
            import hashlib
            scaffold = json.loads((root / '_system/scaffold.json').read_text())
            scaffold['files']['_system/scripts/status.sh'] = hashlib.sha256(wrapper.read_bytes()).hexdigest()
            scaffold['version'] = '1.0.0'
            (root / '_system/scaffold.json').write_text(json.dumps(scaffold, indent=2))
            done = subprocess.run([sys.executable, str(INIT), str(root), '--upgrade'], capture_output=True, text=True)
            self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
            self.assertFalse(wrapper.exists())


if __name__ == '__main__':
    unittest.main()
