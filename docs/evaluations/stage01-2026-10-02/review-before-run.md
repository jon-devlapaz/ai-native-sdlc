# Stage 01 pilot record

Completed 2026-10-02 for the requested quality comparison. The [results](results.md) recommend keeping current guidance unchanged. The active framework is [promptfoo](https://www.promptfoo.dev/), used in [Anthropic's evaluation course](https://github.com/anthropics/courses/blob/master/prompt_evaluations/README.md). It suits a fixed comparison of three instruction versions. Bloom and Petri are aimed at broader behavioral investigations.

## Inputs and calls

The [frozen task source](long/evals/tasks.jsonl) contains four synthetic requests and their criteria. A separate author prepared these in a fresh context; the author saw the candidate instruction. These are development cases, with no independently controlled holdout. Each request supplies the planning format, existing permission rules, and all project context.

Compare the control with the [26-word](short/SKILL.md) and [53-word](long/SKILL.md) additions. Only instruction bodies are delivered, without skill metadata. Each answer receives the same supplied task and the same basic system instruction. The control therefore represents existing guidance in a simplified response-only setting, not a complete production skill invocation.

The [configuration](promptfooconfig.json) specifies 12 Claude answers and 12 separate Codex judgments: four requests, three versions, one sample per combination. Claude uses the locally configured Sonnet alias at medium effort, without tools or loaded settings. The requested judge is `gpt-6.1-sol` at medium effort, in an empty read-only workspace without network/search. Each judge sees the original request, the fixed rubric, and one answer; version labels and extra instructions are withheld.

The [runner](run-promptfoo.mjs) uses promptfoo's native providers and evaluator. It records each raw provider response and rendered prompt, caps individual calls at 120 seconds, stops on call errors, and disables Codex provider retries and promptfoo cache. Internal behavior of the native model runtimes remains outside this wrapper. Existing subscription logins are used; inherited API credentials and alternate provider settings are removed. No billable API fallback is configured.

The prior 43-call skill-eval-loop plan and unused local Claude skill workflow were superseded when Jon selected an online framework. Their unexecuted plans are preserved outside the repository under `/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/`. Proposed calibration labels were never human-approved and are not evidence. Current automated judgments are explicitly uncalibrated against human labels.

## Actual execution

The corrected run completed twelve answers and twelve usable judgments. An earlier judging template omitted the original request: six completed judgments are invalid, and a seventh judge turn was interrupted. Seven completed writer answers were reused unchanged, and only the five remaining answers were generated. Thus 31 native provider turns were started and 30 completed; this is not an exact count of auxiliary model/HTTP requests. All errors and unused scores are preserved. A pre-call check now rejects an empty original request, and process signals explicitly abort the evaluator.

Two initial startup failures and an incorrect expected reuse count made no model calls. The completed configuration, actual rendered prompts, and responses are frozen in the external runtime's `run-2/` directory. The precise corrected-run command was:

```sh
STAGE01_EVAL_RUNTIME=/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo \
STAGE01_EVAL_RUN=run-2 \
STAGE01_REUSE_TARGETS=/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/run-1 \
node docs/evaluations/stage01-2026-10-02/run-promptfoo.mjs
```

The runner refuses to overwrite either existing run. These commands document what happened; intentionally start new trials under new names while preserving existing evidence.

## Assessment and selection

Check four dimensions against each original request: grounding, constraints, permission, and usefulness. Every dimension must pass. Retain exact errors and explanations; do not compensate for a critical failure with an average. Report answer lengths without treating verbosity as quality.

Keep existing guidance if neither addition demonstrates a useful improvement. Prefer the shorter addition if both fix the same observed failure without new harms. Consider the longer addition only if it fixes a consequential failure the shorter one retains. With four requests and one sample each, apparent differences need repetition and independent cases before changing canonical guidance. This pilot cannot complete #37's full producer/consumer/reviewer evaluation.

## Reproduction and evidence

Dependencies are isolated under `/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/`: promptfoo 0.123.1, Claude Agent SDK 0.3.287, and Codex SDK 0.160.0, with a package lock. Native provider resolution may load nested SDK versions; the actual package tree is retained.

```sh
STAGE01_EVAL_RUNTIME=/path/to/isolated/runtime node docs/evaluations/stage01-2026-10-02/run-promptfoo.mjs
```

The runtime requires a local authenticated Claude binary and Codex binary at the configured paths. The runner refuses to overwrite `run-1`; preserve prior evidence before intentionally starting another trial. The runtime retains inputs, hashes, raw calls, promptfoo results, errors, and account-usage metadata. SDK dollar estimates do not establish a subscription charge.

See the [research and results record](../../stage-01-evidence-review.md) for findings and limits. No canonical guidance has changed.
