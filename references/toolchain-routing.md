# Toolchain routing for a run

1. Load mandatory policy skills deterministically. Reuse an appropriate loaded
   skill before routing. Route only a real capability gap; ranking is evidence of
   fit, not trust.
2. Scope routing to the active stage's skillset and record a receipt:
   ```sh
   tink-route --skillset <stage>-skillset --receipt runs/<slug>/skills.jsonl "<capability needed>"
   ```
   The project pin `.tink/skillsets/<name>.json` scopes candidates (minus its
   `required` disciplines), with a one-shot whole-library fallback; `--strict`
   disables the fallback. Default behavior verifies the mount and prints the skill
   on stdout. Exit 0 delivered, 1 no specialist skill applies, 2 could not
   deliver or usage; on any non-zero, continue without a skill. `--pick` decides
   only and writes nothing.
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
