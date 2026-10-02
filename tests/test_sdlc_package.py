import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'scripts').mkdir()
        shutil.copyfile(ROOT / 'scripts/package.py', self.root / 'scripts/package.py')
        self.assets = self.root / 'assets'
        self.assets.mkdir()
        self.payload = self.assets / 'example.md'
        self.payload.write_text('original payload\n')
        self.manifest = self.assets / 'manifest.json'
        self.initial = {
            'version': '1.18.2',
            'files': {'example.md': hashlib.sha256(self.payload.read_bytes()).hexdigest()},
            'projectOwned': [],
        }
        self.write_manifest(self.initial)

    def write_manifest(self, manifest):
        self.manifest.write_text(json.dumps(manifest, indent=2) + '\n')

    def cli(self, *args):
        return subprocess.run(
            [sys.executable, str(self.root / 'scripts/package.py'), *args],
            capture_output=True, text=True,
        )

    def assert_refused_without_writes(self, args, message):
        before = {str(p.relative_to(self.root)): p.read_bytes()
                  for p in self.root.rglob('*') if p.is_file()}
        result = self.cli(*args)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(message, result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        after = {str(p.relative_to(self.root)): p.read_bytes()
                 for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_malformed_release_versions_refused_without_writes(self):
        versions = ('', '1', '1.2', 'v1.19.0', '1.19.0rc1', '1.19.0+build',
                    '-1.19.0', '1.19.0\n', '١.١٩.٠')
        for version in versions:
            for mode in ((), ('--check',)):
                with self.subTest(version=version, mode=mode):
                    self.write_manifest(self.initial)
                    self.assert_refused_without_writes(
                        (*mode, f'--version={version}'), 'expected numeric X.Y.Z')

    def test_downgrades_refused_without_writes(self):
        for version in ('1.0.1', '1.18.1', '0.99.0'):
            for mode in ((), ('--check',)):
                with self.subTest(version=version, mode=mode):
                    self.write_manifest(self.initial)
                    self.assert_refused_without_writes(
                        (*mode, '--version', version), 'Downgrade refused')

    def test_malformed_manifest_versions_refused_without_writes(self):
        for version in (None, 1182, '1.18', 'bad'):
            for args in ((), ('--check',), ('--version', '1.19.0')):
                with self.subTest(version=version, args=args):
                    self.write_manifest({**self.initial, 'version': version})
                    self.assert_refused_without_writes(args, 'expected numeric X.Y.Z')

    def test_missing_manifest_version_refused_without_traceback(self):
        self.write_manifest({key: value for key, value in self.initial.items() if key != 'version'})
        self.assert_refused_without_writes(('--check',), 'expected numeric X.Y.Z')

    def test_release_upgrade_uses_numeric_order_and_refreshes_hashes(self):
        self.payload.write_text('new payload\n')
        for version in ('1.19.0', '1.100.0', '2.0.0'):
            with self.subTest(version=version):
                self.write_manifest(self.initial)
                result = self.cli('--version', version)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                manifest = json.loads(self.manifest.read_text())
                self.assertEqual(manifest['version'], version)
                self.assertEqual(manifest['files']['example.md'],
                                 hashlib.sha256(self.payload.read_bytes()).hexdigest())
                self.assertEqual(self.cli('--check').returncode, 0)

    def test_same_version_and_implicit_manifest_refresh_remain_supported(self):
        for args in ((), ('--version', '1.18.2')):
            with self.subTest(args=args):
                self.write_manifest(self.initial)
                self.payload.write_text('refreshed payload\n')
                result = self.cli(*args)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                manifest = json.loads(self.manifest.read_text())
                self.assertEqual(manifest['version'], '1.18.2')
                self.assertEqual(manifest['files']['example.md'],
                                 hashlib.sha256(self.payload.read_bytes()).hexdigest())

    def test_check_is_read_only(self):
        before = self.manifest.read_bytes()
        for args in (('--check',), ('--check', '--version', '1.18.2')):
            result = self.cli(*args)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(self.manifest.read_bytes(), before)
        result = self.cli('--check', '--version', '1.19.0')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Manifest does not match', result.stderr)
        self.assertEqual(self.manifest.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
