# ESPHome lazy knowledge base — setup

## What this is

A local `knowledge-base/` folder of markdown files, one per ESPHome
component you actually use, containing the real public C++ interface
(methods, enums, constants) extracted directly from the pinned ESPHome
source. Claude Code (running on Haiku) reads these instead of guessing
lambda syntax from memory or from random YAML found online.

Everything is built lazily and incrementally — nothing is pre-downloaded,
nothing is re-fetched once cached.

## Files in this delivery

- `scripts/kb_build.py` — the extraction engine. Run it directly, or let
  Claude Code call it per `knowledge-base-prompt.md`.
- `knowledge-base-prompt.md` — paste this into (or append it to) your
  `CLAUDE.md` in `config/esphome/`. It tells Claude Code when and how to
  use the script.

## One-time setup

1. Copy `scripts/` into your `config/esphome/` folder (so it sits next to
   your YAML files).
2. Append the contents of `knowledge-base-prompt.md` to your existing
   `CLAUDE.md` (or drop it in as `CLAUDE.md` if you don't have one yet).
3. Bootstrap the initial knowledge base from whatever you already have:
   ```bash
   cd config/esphome
   python3 scripts/kb_build.py --scan .
   ```
   This scans every `*.yaml`/`*.yml` file for `platform:` values and
   top-level component keys, resolves the latest stable ESPHome release
   automatically, and pulls + extracts each one. First run takes a few
   seconds per component (sparse git checkout); subsequent runs for the
   same components are instant no-ops.

4. (Optional) If you use external/HACS components like `daikin_onecta` or
   `comfoconnect` that don't live in `esphome/esphome` core, create
   `knowledge-base/_meta/external_repos.json`:
   ```json
   {
     "daikin_onecta": {"repo": "https://github.com/<author>/daikin_onecta.git", "path": "components/daikin_onecta"},
     "comfoconnect":  {"repo": "https://github.com/<author>/esphome-comfoconnect.git", "path": "components/comfoconnect"}
   }
   ```
   Then re-run `--scan .` — those two entries won't resolve automatically
   since they're not part of ESPHome core and the repo paths vary by
   author, but once mapped they'll pull the same way core components do.

## Day to day

You generally don't run the script yourself — Claude Code does, per the
protocol in `knowledge-base-prompt.md`, whenever it hits a component it
doesn't have documented yet. You can also run it manually:

```bash
# check what's missing without pulling anything
python3 scripts/kb_build.py --scan . --dry-run

# pull specific components explicitly
python3 scripts/kb_build.py --component pca9685 ads1115

# see the ESPHome version this KB is pinned to
cat knowledge-base/_meta/pinned_ref.txt

# upgrade the pin and refresh everything already known (only when you
# actually want to move to a newer ESPHome release)
python3 scripts/kb_build.py --ref 2026.7.0 --refresh-all
```

## Known limitation

The extractor is a brace-depth/regex walker, not a real C++ parser. It's
been tested against `pca9685`, `ads1115`, and `esp32_camera_web_server` and
produces clean, correctly-scoped public interfaces, but on more unusually
formatted headers it can occasionally miss a declaration. Each generated
markdown file links back to its exact source path/ref so this is easy to
spot-check when a lambda call doesn't compile.
