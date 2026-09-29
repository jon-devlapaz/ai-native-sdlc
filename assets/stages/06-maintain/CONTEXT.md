# Maintenance intake (optional)

This is a producer of new work, not a mandatory final stage for each feature.
Inputs: telemetry and an explicitly configured, tested monitoring policy.
No monitoring job or bands policy is provisioned by this scaffold.

Before enabling automation, define suitable metric-specific thresholds, stable
baselines, incident deduplication keys, cooldowns, and active-run limits. Do not
assume universal 2-sigma/3-sigma thresholds are appropriate.

Output: a new write run from `new-run.sh`, with observed evidence and affected
systems in its brief or intent. Repeated alerts update the existing incident
instead of spawning duplicate work.
Gate: service owner triages, dismisses, schedules, or approves the draft through
the normal definition gate. Telemetry never fabricates approval or releases code.

## Skills

Skillset: `maintenance-skillset` (pin: `.tink/skillsets/maintenance-skillset.json`). This stage is optional, like maintenance itself; skip this section unless you run it.
- Once per machine/library, after reviewing the pin (it selects exact upstream code):
  `tink library fetch .tink/skillsets/maintenance-skillset.json`
- At stage open, compile the required disciplines, then start a NEW session so
  `AGENTS.md` is re-read: `tink use maintenance-skillset --snapshot runs/<slug>/06-maintain`
- For a capability gap: `tink-route --skillset maintenance-skillset --receipt runs/<slug>/skills.jsonl "<what you need>"`
  (prints the skill on stdout; exit 1 or 2 means continue without a skill).
