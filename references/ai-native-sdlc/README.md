# The AI-Native SDLC Playbook

> Technical guide from Anthropic's Applied AI team on transforming the software development lifecycle (SDLC) with AI.
> **Source:** [Claude Academy](https://academy.claude.com/courses/ai-native-sdlc-playbook)

---

Many engineering teams still have the same approval gates, reviews, handoffs, and policies, stalling productivity gains made by using agentic coding solutions like Claude Code.

In this guide, we walk through several of our Applied AI team's best practices for integrating Claude internally across each stage of the SDLC to accelerate development and make processes run faster, inspired by working with our customers.

## Who this course is for

This course is for engineering, platform, and security leads whose organization already uses Claude Code and whose approval gates, reviews, and handoffs still run at human speed. It is written for large enterprises, and especially regulated ones, where the review queue cannot be allowed to build and code cannot ship under-reviewed. The plays assume you can change how your organization plans, reviews, tests, and deploys, not only how it writes code.

## Prerequisites

You should be comfortable working in Claude Code day to day, and have a Git repository and CI pipeline you are allowed to change. Each play names its own prerequisites under Getting started, and several have none.

---

## Course Table of Contents

### Introduction

- [Lesson 1: Introduction](./01-introduction.md) (4 min)
### Stage 1: Plan

- [Lesson 2: Capture as intent.md](./02-stage-1-plan-capture-intent.md) (4 min)
### Stage 2: Design

- [Lesson 3: Requirements and design](./03-stage-2-design-requirements-and-design.md) (4 min)
### Stage 3: Build

- [Lesson 4: Claude Code plan mode as the default starting point](./04-stage-3-build-plan-mode.md) (4 min)
- [Lesson 5: The CLAUDE.md](./05-stage-3-build-claude-md.md) (2 min)
- [Lesson 6: Skills as institutional knowledge](./06-stage-3-build-skills-as-institutional-knowledge.md) (3 min)
- [Lesson 7: Parallel sessions and subagents](./07-stage-3-build-parallel-sessions-and-subagents.md) (3 min)
### Stage 4: Test

- [Lesson 8: Give Claude a feedback loop](./08-stage-4-test-give-claude-a-feedback-loop.md) (3 min)
- [Lesson 9: Continuous evals in CI](./09-stage-4-test-continuous-evals-in-ci.md) (2 min)
### Stage 5: Deploy

- [Lesson 10: AI in the PR review loop](./10-stage-5-deploy-ai-in-the-pr-review-loop.md) (4 min)
- [Lesson 11: Hooks as approval gates](./11-stage-5-deploy-hooks-as-approval-gates.md) (4 min)
- [Lesson 12: CI/CD integration and deployment](./12-stage-5-deploy-ci-cd-integration-and-deployment.md) (3 min)
### Stage 6: Maintain

- [Lesson 13: Closing the loop on metrics](./13-stage-6-maintain-closing-the-loop-on-metrics.md) (5 min)
### Closing

- [Lesson 14: Closing thoughts and resources](./14-closing-thoughts-and-resources.md) (2 min)


---

## The Artifact Chain Summary

An AI-native SDLC ties stages together through committed, version-controlled artifacts:

| Stage | Artifact | Author / Instigator | Gate & Approval |
|---|---|---|---|
| **1. Plan** | `intent.md` | Originator & Claude | Product Owner review & commit |
| **2. Design** | `spec.md` | Claude (constrained by policy skills) | Product Owner & Tech Lead |
| **3. Build** | `plan.md`, `CLAUDE.md`, skills | Engineer in Plan Mode | Engineer / Architecture sign-off |
| **4. Test** | Test suite, locked fix tests, CI Evals | Engineer & Claude | Deterministic CI suite & locked test hooks |
| **5. Deploy** | `REVIEW.md`, PR review findings, hooks | Claude multi-pass review | Human Code Owner + Release Gate Hook |
| **6. Maintain** | `bands.yaml`, automated diagnosis `intent.md` | Deterministic monitor / Claude Tag | Service Owner triage into Stage 1 |
