# Stage 01 research and comparison

Prepared 2026-10-02 for #36 and #37. The proposed instruction remains unproven. Research supports checking meaning against source material, measuring failures, and controlling evaluation bias. It does not establish that 53 extra words improve this workflow.

## What the research supports

These primary sources were opened on 2026-10-02. This is a focused review of relevant mechanisms and contrary evidence, not a systematic literature review. The links identify the inspected versions; no paper percentage becomes our acceptance threshold.

| Primary source | Finding and scope | Consequence for our comparison |
|---|---|---|
| [Maynez et al., ACL 2020](https://aclanthology.org/2020.acl-main.173.pdf), abstract and sections 3–5 | Human evaluation of neural abstractive summaries found content unsupported by the source. Standard overlap scores were insufficient to establish faithfulness. These are older summarization systems, not current Stage 01 agents. | Compare each claim and retained constraint with the original request and available facts. Heading counts and fluency are insufficient. Label this transfer to planning as an inference. |
| [Liu et al., Lost in the Middle](https://arxiv.org/html/2307.03172v3), sections 2–4 | Several tested models varied in retrieval/QA performance with information position and irrelevant context. Some models performed nearly perfectly on synthetic retrieval; a prompting change helped retrieval substantially but had little effect on multi-document QA. | Include irrelevant context and misleading cues. Keep delivery and context equal across arms. This motivates a stress case; it does not prove a short instruction fixes context loss or characterize current GPT-6 performance. |
| [Huang et al., ICLR 2024](https://arxiv.org/html/2310.01798v2), sections 4 and 7 | On studied reasoning tasks, intrinsic self-correction without external feedback often failed or degraded results. The authors explicitly distinguish task types and feedback conditions. | My own rereading cannot establish quality. Use separately authored cases, source-based grading, and human assessment. A fresh model judge is additional evidence, not an accountable owner or guaranteed independent truth. |
| [Kumar et al., SCoRe](https://arxiv.org/abs/2409.12917), abstract | Reinforcement learning improved self-correction on the evaluated math/code tasks. The intervention changes training rather than merely requesting self-review. | Reject the broad claim that models cannot self-correct. The useful question is whether this specific model, intervention, and feedback improve these tasks. This is counterevidence to universalizing the older result. |
| [Dubois et al., Length-Controlled AlpacaEval](https://arxiv.org/html/2404.04475v2), sections 4–5 | Automated preference judgments can reward response length. Their correction was tested on AlpacaEval with specific English instructions and judge prompts; it does not solve every judging bias. | Judge correctness before style and length. Blind arm labels, report output lengths, and retain disagreements. We are not reproducing their statistical correction or borrowing its effect size. |

No inspected study directly tests our 53-word instruction, Seed Me-to-SDLC handoffs, mandatory planning headings, or a required Jev validator. Those remain local hypotheses or policy choices. The research supports the method of measurement more strongly than any particular wording.

## What the first review got wrong

“Smallest proposed change” implied more evidence than we had. The [scope review](stage-01-scope-review.md) now calls it a small candidate. Missing explicit guidance is observable; the necessity of adding it is unproven. The original finding table also groups documentary gaps and behavioral hypotheses, so each recommendation must retain its classification and limit.

The first proposed cases were visible to the instruction author and therefore development cases. A separate author now creates the initial four-case suite from the instruction fixture and a fixed task contract, without this conversation or model outputs. That provides a fresh authoring context. Because the author sees the intervention, and we inspect the tasks, it does not create an independent promotion holdout. A real holdout still requires separate custody.

## Comparison using promptfoo

Jon asked for the best suited online evaluation framework. Use [promptfoo](https://www.promptfoo.dev/), which appears in [Anthropic's evaluation course](https://github.com/anthropics/courses/blob/master/prompt_evaluations/README.md). It supports the fixed request/answer comparison we need. Bloom and Petri target broader behavioral investigations; this pilot does not need their task-generation machinery. This framework choice is a judgment about fit, not a research finding about our instruction's effectiveness.

| Version | Additional guidance | Purpose |
|---|---|---|
| Control | None; existing format and permission policy are supplied in each request. | Check whether current guidance already succeeds. |
| Short | 26 words. | Check whether less wording is sufficient. |
| Long | 53 words. | Check whether added detail earns its cost. |

The [pilot record](evaluations/stage01-2026-10-02/review-before-run.md) links the frozen four-case source, actual configuration, and runner. One answer per version per case gives 12 target answers. The requested writer is Claude's locally configured Sonnet alias at medium effort; a separate `gpt-6.1-sol` Codex turn judges each answer against the original request and four fixed dimensions. The judge does not receive the version label or extra instruction. Existing subscription logins are used, without inherited API credentials or configured paid fallback. SDK usage and dollar estimates are not confirmed subscription charges.

All necessary project context is supplied. The writer has no tools or loaded custom settings. The judge works in an empty read-only directory with network/search disabled. The control uses a simplified rendering of existing guidance; this is not a complete production skill invocation. These cases assess planning text, not repository investigation, tool use, downstream implementation, runtime gates, or the full SDLC. Case order and version order are fixed, and each version has one sample. No result can establish equivalence or complete #37's producer/consumer/reviewer evaluation.

A separate author wrote the cases in a fresh context before outputs existed. The author saw the candidate instruction, and the cases were inspected. This is a development suite, not an independent holdout. The model judge is from another provider but is uncalibrated against human labels. Human assessment and independently controlled cases remain necessary before promotion.

Raw requests, provider responses, traces supplied by the SDK, errors, hashes, usage, and promptfoo results remain under `/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/`. The obsolete 43-call skill-eval-loop plan and unused local Claude skill workflow were not executed. Their proposed human labels were never approved and contribute no evidence.

## Execution faults and corrections

Two startup failures occurred before any model execution: a CommonJS logging incompatibility and optional SDK package resolution from the repository instead of the isolated runtime. Their logs are preserved.

The first live judging prompt used `{{vars.task}}`, which rendered the original request empty. Those judgments are invalid. SIGTERM was consumed by native runtime signal handling; the process tree was then forcibly stopped. Seven completed writer answers and six completed invalid judgments were saved, with one further judge turn interrupted. The corrected run uses `{{task}}` and checks that the rendered original request is present before any judge call. It reuses all seven completed answers unchanged, generating only the remaining five. Task criteria and instruction bodies were not changed in response to scores. Abort signals are now explicitly bound to SIGTERM and SIGINT.

These are evaluation setup defects, not workflow behavior failures. They consumed account usage and prevent treating the originally announced 24 calls as the actual total. The final accounting must include the invalid and interrupted turns; none may disappear from the evidence record.

## Results and recommendation

The [completed results](evaluations/stage01-2026-10-02/results.md) retain every answer, automated judgment, reviewer disagreement, word count, and execution receipt. The uncalibrated judge passed control on 3/4 cases, short on 3/4, and long on 2/4. All versions were flagged on the build-investigation case for avoidable owner questions; the long version was also flagged for calling supplied facts inspected. Some flags are disputed: all three build answers preserve the authorized read-only next step, and the long version defers asking until after inspection. Listing a future decision and stopping work to demand an answer must be distinguished before larger judging.

**Keep canonical wording unchanged.** This pilot shows no reliable improvement from either added instruction. It does not prove existing guidance is sufficient in production or that the additions can never help. The most useful next step is to resolve the grading ambiguity using the exact retained answers, then assess actual producer/consumer/reviewer handoffs with independent cases. #37 remains open.

Actual accounting is 31 native provider turns started, 30 completed: twelve writer answers, twelve usable judgments, six invalid completed judgments, and one interrupted judgment. Native runtimes can make auxiliary requests, so this is not an exact HTTP/model-request count. The corrected evaluation includes 47,442 writer tokens and 220,044 grading tokens; the additional invalid/interrupted usage is excluded from those totals. The results record explains model identity limits and retains the raw usage. Setup repairs did not change the task criteria or instruction bodies.

Eight existing mechanical checks passed at the reviewed main revision, with a [receipt](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/mechanical/receipt.json). They verify existing gate and contract behavior, not the semantic quality measured here.

## Selection rule and next evidence

Inspect grounding, constraints, permission, and usefulness against each fixed request. Retain omissions, invented evidence, authorization errors, avoidable questions, and reviewer rationale individually. A critical error defeats acceptance regardless of average score. Include the fully specified task so extra caution or needless questions can count as regressions.

If unchanged guidance succeeds and neither addition has a demonstrated benefit, retain unchanged guidance. If both additions resolve the same failure without new harms, prefer the shorter one. If the long version resolves a consequential failure that persists with the short version, preserve the exact outputs before considering it. With four tasks and one trial, any apparent difference is a screening result requiring repetition and independently controlled cases before promotion. No significance, general safety, or minimum-possible-wording claim follows from this pilot.

Implementation remains conditional on demonstrated need and reviewed evidence. Current wording stays unchanged while the comparison is assessed.
