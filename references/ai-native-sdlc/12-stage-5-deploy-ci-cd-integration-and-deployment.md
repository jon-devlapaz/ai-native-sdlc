# CI/CD integration and deployment

> **Course:** The AI-Native SDLC Playbook  
> **Stage:** Stage 5: Deploy  
> **Lesson:** 12 of 14 (3 min read)  
> **Source:** [Claude Academy](https://academy.claude.com/courses/ai-native-sdlc-playbook/ci-cd-integration-and-deployment)

---

Run Claude Code non-interactively inside the CI/CD pipeline, sandbox the execution so long-running agents run safely, expose deployment through MCP integrations, and rehearse the rollback paths before the agent ever needs them.

## What changes

| Traditional | AI-native |
| --- | --- |
| Pipelines run deterministic scripts, and anything that needs judgment waits for a human: for example, triaging the flaky test, writing the changelog, or working out why the build broke. Deployment and rollback are runbooks a human follows under pressure. | Claude runs non-interactively inside the pipeline for the judgment steps, in a sandbox with scoped credentials. Deployment tooling is exposed to the agent through MCP, so the workflow that wrote and tested the change can also ship it and roll it back, inside gates the organization defines per environment. |

## Getting started

* **Prerequisites**: AI in the PR review loop and hooks as approval gates, because the gates must exist before automation accelerates anything through them.
* **Infrastructure**: A CI platform with the claude-code-action installed, or any runner that can call `claude -p`; model access through the API, or Amazon Bedrock, Microsoft Foundry, or Vertex AI where traffic must stay on the organization's cloud agreement; MCP servers for the deployment targets; a sandbox profile for agent jobs with no standing production credentials.

## How to execute it

1. The platform engineer starts with read-only judgment steps. Use `claude -p` in a pipeline job to triage a failed build, summarize a flaky test, or draft the changelog.
2. Add write steps behind the existing gates for jobs like fixing lint, updating generated docs, or addressing review comments via the `@claude` mentions. Anything the agent writes arrives as a PR through branch protection, and the agent has no route to push to main.
3. Execution is sandboxed. Agent jobs run in containers under a network policy with short-lived scoped tokens, and hold no production credentials by default.
4. Expose deployment through MCP. Deploy, status, and rollback become tools, scoped per environment, so the agent's deployment powers are an allowlist rather than a shell script with credentials.
5. Tier the autonomy by environment. In development, the agent deploys freely. In production, the agent prepares the release and the release manager authorizes it, and a hook enforces the production gate. Staging sits somewhere in the middle.
6. Rollback should be the most rehearsed path in the pipeline, a single command that the agent can run and that is exercised regularly in staging. The closing the loop play (**Stage 6: Maintain**) calls this rollback when a control band is breached, so it has to be proven in advance.

## What it looks like

Pipeline step:

```yaml
- name: Triage failed build
  if: failure()
  run: >
    claude -p "Read the build log at out/build.log. Identify the most
    likely cause, say whether the failure looks flaky or real, and write a
    three-line summary for the PR thread." >> triage.md
```

## Governance considerations

The governing principle is that the agent may act up to the production gate and cannot pass it. The controls below enforce this principle.

* **Branch protection** turns anything the agent writes into a PR, with no direct path to main.
* **The production deploy hook** blocks the release until a named release manager authorizes it. Each non-interactive run acts under the agent's own identity, so the pipeline log separates what the agent did from what the engineer who triggered it did.
* **Per-environment permission tiers** set how much the agent may do on the way to the gate.

## How to measure it

* **Leading indicator**: The share of pipeline failures triaged without paging a human, taken from the CI/CD pipeline logs.
* **Lagging indicator**: DevOps Research and Assessment (DORA) measures, which the CI system and deployment tooling already emit.
