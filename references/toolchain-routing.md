# Toolchain routing for a run

1. Load mandatory policy skills deterministically. Reuse an appropriate loaded
   skill before routing. Route only a real capability gap; ranking is evidence of
   fit, not trust.
2. Ask the active stage's shelf and record a receipt:
   ```sh
   tink-route --receipt runs/<slug>/skills.jsonl "<capability needed>"
   ```
   The phase decides the shelf: the skillset named in the `tink:rules` block that
   `tink use` compiled into `AGENTS.md` (project pin `.tink/skillsets/<name>.json`,
   minus its `required` disciplines). The answer is strict: nothing on the shelf
   means exit 1, and a `Hint:` line may name a skill on another shelf that was not
   delivered. `--skillset NAME` overrides the shelf and `--anywhere` searches the
   whole library. Default behavior verifies the mount and prints the skill on
   stdout. Exit 0 delivered, 1 no specialist skill applies, 2 could not deliver or
   usage; on any non-zero, continue without a skill. `--pick` decides only and
   writes nothing.
3. Read the delivered skill before relying on it. Mounts land in the git-ignored
   `.tink/.active/` and need no pruning; `tink-route` never rewrites
   `.tink/skills.toml` or `.tink/skills.lock`.
4. Preserve the receipt with the run. Keep baseline manifests under reviewed
   dependency management and restore baseline skills through Tink:
   ```sh
   python3 _system/scripts/sdlc.py skills tink -- skill check
   ```

The `sdlc.py skills tink --` wrapper serializes cooperating `tink` operations
using a local user/temp-directory lock. It does not isolate shared home-library
state, or coordinate direct CLI calls, different lock namespaces, or multiple hosts.
It does not wrap `tink-route`.
