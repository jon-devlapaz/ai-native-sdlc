# Tight handoff evaluation

Completed within the approved nine-turn cap. [Results](results.md): no demonstrated
overall improvement; candidate not accepted for reliability, main assets unchanged.

- [Authorization](authorization.json), [plan and stop rules](plan.md)
- [Actual usage and source revisions](run-summary.json)
- [Cases](cases.json), [final model review](final-assessment.json)
- [Candidate patch](candidate.patch), [mechanical checks](candidate-checks.json)
- [Portable redacted evidence](evidence.tar.gz), [checksum](evidence.tar.gz.sha256),
  [raw/portable file hashes](evidence-manifest.json)

Original raw replies stay unchanged locally. Archive copies redact unsupported
email identifiers; they do not include dependencies or authentication state.
Original response pilot and calibration remain in `../stage01-2026-10-02/` unchanged.

Future work should start from these results and change only what a reproduced
failure warrants. Do not repeat model runs or ship this candidate by default.
Issue 1 and the owner-paused issue 34 await their separate dispositions.
