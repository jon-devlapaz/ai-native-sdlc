"""Guard the operational docs against the 'review' -> 'parse' find/replace corruption.

The extraction commit replaced the word 'review' with 'parse' in several shipped
documents ('Stage 05: Parse and release', 'a model parse is not human approval').
These documents are instructions to agents, so the corruption changes their meaning.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# 'parse' is legitimate in code and in `git rev-parse`; the hyphen lookbehind keeps rev-parse out.
CORRUPTION = re.compile(r'(?<![\w-])parse[sd]?(?![\w-])', re.IGNORECASE)


def operational_docs():
    files = sorted((ROOT / 'assets' / 'stages').glob('*/CONTEXT.md'))
    files += sorted((ROOT / 'assets' / '_shared').glob('*.md'))
    files += [ROOT / 'assets' / '_system' / 'SDLC.md', ROOT / 'SKILL.md', ROOT / 'README.md',
              ROOT / 'references' / 'lifecycle-stages.md']
    return files


class WordingTests(unittest.TestCase):
    def test_no_parse_where_review_was_meant(self):
        offenders = []
        for path in operational_docs():
            for number, line in enumerate(path.read_text().splitlines(), 1):
                if CORRUPTION.search(line):
                    offenders.append(f'{path.relative_to(ROOT)}:{number}: {line.strip()[:80]}')
        self.assertEqual(offenders, [], "the word 'parse' appears where 'review' was meant")

    def test_stage_five_is_review_and_release(self):
        first = (ROOT / 'assets' / 'stages' / '05-deploy' / 'CONTEXT.md').read_text().splitlines()[0]
        self.assertEqual(first, '# Stage 05: Review and release')

    def test_light_run_gate_vocabulary(self):
        sentence = 'Light runs have ONE definition gate, recorded as stage 3'
        for rel in ['_system/SDLC.md', 'stages/01-plan/CONTEXT.md', 'stages/02-design/CONTEXT.md', 'stages/03-build/CONTEXT.md']:
            self.assertIn(sentence, (ROOT / 'assets' / rel).read_text(), rel)
        build = (ROOT / 'assets/stages/03-build/CONTEXT.md').read_text()
        self.assertNotIn('Inspect code, write the plan,', build)
        self.assertIn('For full runs, write the plan', build)

    def test_stage_boundary_ownership_section(self):
        text = (ROOT / 'assets/_system/SDLC.md').read_text()
        self.assertIn('## Who does what at a stage boundary', text)
        section = text.split('## Who does what at a stage boundary')[1].split('\n## ')[0]
        self.assertLess(len(section.strip().splitlines()), 25)
        for word in ['launcher', 'tink use', 'NEW session', 'never approves', 'sdlc.py mark', 'REVIEW-findings.md', 'commit before verifying']:
            self.assertIn(word.lower(), section.lower(), word)

    def test_generated_rules_excluded_from_fingerprint_documented(self):
        text = (ROOT / 'assets/_system/SDLC.md').read_text()
        self.assertIn('excluded from the candidate fingerprint', text)

    def test_review_guide_is_about_review(self):
        text = (ROOT / 'assets' / '_shared' / 'REVIEW.md').read_text()
        self.assertIn('Review logic and edge cases', text)
        self.assertIn('Automated review is advisory', text)


if __name__ == '__main__':
    unittest.main()
