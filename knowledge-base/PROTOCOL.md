# ESPHome Knowledge Base — Protocol

Read this in full only when you've been triggered here from CLAUDE.md (lambda work, or a new component). Otherwise you shouldn't be reading this file at all.

## What this is

`knowledge-base/components/*.md` — auto-extracted public C++ interfaces (methods, enums, constants) from the real `esphome/esphome` source, pinned to one release. Ground truth for what a `lambda:` block can call via `id(x).method(...)`. Not YAML examples, not memory.

## Steps

1. Identify the component(s) the current task touches.
2. `ls knowledge-base/components/<component>.md` — if present, read it, use it, stop here.
3. If missing:
   ```
   python3 scripts/kb_build.py --component <name> [<name> ...]
   ```
   No-ops instantly if already cached at the pinned ref — safe to call, but batch multiple components in one call rather than looping.
4. If it reports "not found" (`knowledge-base/components/_unresolved.md`): likely external/HACS, not core ESPHome. Check `knowledge-base/_meta/external_repos.json` for a mapping; if absent and you know the repo, add an entry (`{"repo": "...", "path": "..."}`) and retry step 3. If you don't know the repo, say so — do not guess method names.
5. New component appears in a config not yet scanned — scope this to the
   file(s) actually in the current session, not the whole repo (per
   CLAUDE.md: one domain per session, touch the smallest number of files
   possible). Pass the specific device file(s); `!include` /
   `!include_dir_*` references (the esp-tourbillon packages mechanism) are
   followed automatically, so a single entry file resolves its real
   package tree without pulling in unrelated devices:
   ```
   python3 scripts/kb_build.py --files esp-tourbillon.yaml
   ```
   or, for a single-file device config:
   ```
   python3 scripts/kb_build.py --files s2-ventilation.yaml
   ```
   `--scan <dir>` (repo-wide) exists for initial bootstrap only — avoid it
   in routine work, since it pulls components for every device in the
   repo, not just the one in scope.
6. Write the lambda using only what's actually documented. Extractor is regex-based, not a full C++ parser — if a method you need isn't listed, say so and check the source path in the markdown's "Source:" line before inventing anything.

## Version pinning

`knowledge-base/_meta/pinned_ref.txt` — the ESPHome release this KB targets. Do not pass `--ref` / `--refresh-all` unless explicitly asked to move the ESPHome version; per CLAUDE.md, version bumps require explicit instruction regardless.
