# Interface Contracts Playbook

Use for module, API, tool, schema, generated-artifact, file-format, or external dependency boundaries where two sides must agree before integration.

## Steps

1. Name the interface, owner, producer, consumer, version, and change authority.
2. Define inputs, outputs, data shape, error behavior, side effects, idempotency, timing, and compatibility expectations.
3. Identify assumptions, constraints, security or privacy boundaries, and external dependency limits.
4. Define compatibility checks and verification evidence for the boundary.
5. Record migration, rollback, and deprecation expectations when the boundary can change.
6. Mark unresolved fields as open questions, not hidden assumptions.

## Output

Produce an interface contract with name, owner, producers/consumers, inputs, outputs, errors, version, compatibility rules, verification, rollback, and open questions.

## Guardrails

Do not treat an interface contract as proof that integration works. Hand integration sequence and cross-boundary proof to `integration-planning.md`.
