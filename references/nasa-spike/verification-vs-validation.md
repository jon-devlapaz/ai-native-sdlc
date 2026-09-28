# Verification vs Validation

Verification and validation must stay separate in router outputs.

## Verification

Verification proves compliance with specified requirements or specifications. In coding work, it maps each requirement to reproducible evidence such as a test, inspection, analysis, demonstration, command output, screenshot, trace, or review artifact.

Primary context: `.agents/skills/verification-planner/references/source-grounding.md`, Section 5.3 pages `extraction/pages/page_098.md` through `extraction/pages/page_109.md`, and Appendix D pages `extraction/pages/page_211.md` through `extraction/pages/page_212.md`.

## Validation

Validation checks whether the right thing was built for the intended user, environment, workflow, operational need, or ConOps. Passing verification does not prove validation.

Primary context: `.agents/skills/validation-planner/references/source-grounding.md`, Section 5.4 pages `extraction/pages/page_109.md` through `extraction/pages/page_115.md`, and Appendix E pages `extraction/pages/page_213.md` through `extraction/pages/page_214.md`.

## Required Router Behavior

- If the user asks "does it meet the requirements?", route to verification.
- If the user asks "does it solve the user's problem?", route to validation.
- If tests pass but the workflow fails, route to validation plus technical assessment.
- If intended use is unclear, route to ConOps before validation.
