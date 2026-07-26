#!/usr/bin/env python3
"""
kb_build.py — Lazily builds a markdown knowledge base of ESPHome component
public C++ interfaces, sourced directly from the esphome/esphome repo.

Design goals:
  - Never re-download more than needed. Uses a single persistent sparse
    git checkout and only adds new component paths to it on demand.
  - Deterministic extraction (regex/brace-tracking), not LLM guesswork.
  - Pins to one esphome ref so lambda code stays compatible across a session.
  - Safe to call repeatedly / incrementally from Claude Code as new
    components show up in your YAML.

Typical usage (run from your config/esphome folder):

    # one-time / whenever you add new YAML files or components:
    python3 scripts/kb_build.py --scan .

    # force-pull specific components explicitly:
    python3 scripts/kb_build.py --component pca9685 ads1115 daikin_onecta

    # see what's already known vs missing, without pulling anything:
    python3 scripts/kb_build.py --scan . --dry-run

    # re-pin to a new esphome release and refresh existing components:
    python3 scripts/kb_build.py --ref 2026.7.0 --refresh-all

Layout produced under ./knowledge-base/:
    _meta/pinned_ref.txt        <- esphome git ref this KB is built against
    _meta/index.json            <- per-component: ref pulled at, files, status
    _meta/esphome-src/          <- persistent sparse git checkout (source cache)
    components/<name>.md        <- one file per component, ready for Claude to read
    components/_unresolved.md   <- log of names seen in YAML but not found upstream
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_URL = "https://github.com/esphome/esphome.git"

# Common top-level YAML keys that are not esphome "components" in the
# repo-folder sense (core, board configs, generic sections) — skip these
# during auto-scan so we don't waste a lookup on them.
SKIP_KEYS = {
    "esphome", "wifi", "ethernet", "api", "ota", "logger", "web_server",
    "captive_portal", "improv_serial", "substitutions", "packages",
    "globals", "script", "interval", "time", "mdns", "debug", "external_components",
}


# --------------------------------------------------------------------------
# Repo management (lazy, incremental sparse checkout)
# --------------------------------------------------------------------------

def run(cmd, cwd=None, check=True):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{result.stderr}")
    return result.stdout.strip()


CALVER_TAG_RE = re.compile(r"^20\d{2}\.\d{1,2}\.\d{1,2}$")


def latest_stable_tag():
    """Get the newest stable esphome release tag without hitting API rate limits.

    ESPHome moved to CalVer (YYYY.M.P) years ago but the repo still carries
    legacy pre-CalVer `v1.x` tags. A plain `--sort=-v:refname` across both
    schemes sorts lexically by scheme first (letters vs digits), NOT by
    actual recency -- so we filter to CalVer tags explicitly before sorting.
    """
    out = run(["git", "ls-remote", "--tags", "--sort=-v:refname", REPO_URL])
    for line in out.splitlines():
        ref = line.split("refs/tags/")[-1]
        if ref.endswith("^{}"):
            continue
        if not CALVER_TAG_RE.match(ref):
            continue  # skip betas (YYYY.M.PbN), rcs, and legacy v1.x tags
        return ref
    return "dev"


def ensure_src_repo(meta_dir: Path, ref: str):
    """Create the persistent sparse checkout once; otherwise reuse it."""
    src = meta_dir / "esphome-src"
    if not (src / ".git").exists():
        src.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--filter=blob:none", "--sparse", "--depth", "1",
             "--branch", ref, REPO_URL, str(src)])
        run(["git", "sparse-checkout", "init", "--cone"], cwd=src)
        run(["git", "sparse-checkout", "set"], cwd=src)  # start empty (cone root only)
    else:
        current_ref = run(["git", "describe", "--tags", "--exact-match"], cwd=src, check=False)
        if current_ref != ref:
            run(["git", "fetch", "--depth", "1", "origin", "tag", ref], cwd=src)
            run(["git", "checkout", f"tags/{ref}"], cwd=src)
    return src


def pull_component_dir(src: Path, component: str) -> Path | None:
    """Add a single component folder to the sparse checkout if not already present."""
    target = src / "esphome" / "components" / component
    if target.exists():
        return target
    sparse_list_file = src / ".git" / "info" / "sparse-checkout"
    existing = sparse_list_file.read_text().splitlines() if sparse_list_file.exists() else []
    path_spec = f"esphome/components/{component}"
    if path_spec not in existing:
        run(["git", "sparse-checkout", "add", path_spec], cwd=src)
    return target if target.exists() else None


def load_external_repos(meta_dir: Path) -> dict:
    """Optional mapping for HACS-style external components that don't live in
    esphome/esphome core (e.g. daikin_onecta, comfoconnect). Populate
    knowledge-base/_meta/external_repos.json like:

        {
          "daikin_onecta": {"repo": "https://github.com/lourencorodrigues/daikin_onecta.git", "path": "components/daikin_onecta"},
          "comfoconnect":  {"repo": "https://github.com/marconett/esphome-comfoconnect.git", "path": "components/comfoconnect"}
        }

    Each maps a component name to its own repo + the path to the component
    folder within it (paths vary by author, so this isn't guessable).
    """
    f = meta_dir / "external_repos.json"
    if f.exists():
        return json.loads(f.read_text())
    return {}


def pull_external_component_dir(meta_dir: Path, component: str, spec: dict) -> Path | None:
    """Sparse-checkout a single external (non-core) component repo, cached
    per-repo under _meta/external-src/<slug>/ just like the core repo."""
    repo_url = spec["repo"]
    comp_path = spec["path"]
    slug = re.sub(r"[^A-Za-z0-9_-]", "_", repo_url.rstrip("/").rsplit("/", 1)[-1].removesuffix(".git"))
    ext_root = meta_dir / "external-src"
    ext_root.mkdir(parents=True, exist_ok=True)
    repo_dir = ext_root / slug

    if not (repo_dir / ".git").exists():
        run(["git", "clone", "--filter=blob:none", "--sparse", "--depth", "1", repo_url, str(repo_dir)])
        run(["git", "sparse-checkout", "init", "--cone"], cwd=repo_dir)
        run(["git", "sparse-checkout", "set"], cwd=repo_dir)

    target = repo_dir / comp_path
    if not target.exists():
        run(["git", "sparse-checkout", "add", comp_path], cwd=repo_dir)
    return target if target.exists() else None


# --------------------------------------------------------------------------
# YAML scanning (lightweight, no PyYAML dependency required)
# --------------------------------------------------------------------------

PLATFORM_RE = re.compile(r"^\s*-?\s*platform:\s*([A-Za-z0-9_]+)")
TOPLEVEL_KEY_RE = re.compile(r"^([A-Za-z0-9_]+):\s*$")
TOPLEVEL_KEY_INLINE_RE = re.compile(r"^([A-Za-z0-9_]+):")
INCLUDE_RE = re.compile(r"!include(_dir_\w+)?\s+([^\s#]+)")


def scan_yaml_text(text: str) -> set[str]:
    found = set()
    for line in text.splitlines():
        if line.startswith("  ") or line.startswith("\t"):
            m = PLATFORM_RE.match(line)
            if m:
                found.add(m.group(1))
            continue
        m = TOPLEVEL_KEY_RE.match(line) or TOPLEVEL_KEY_INLINE_RE.match(line)
        if m:
            key = m.group(1)
            if key not in SKIP_KEYS:
                found.add(key)
    return found


def scan_yaml_dir(root: Path) -> set[str]:
    """Repo-wide scan. Fine for initial bootstrap; avoid for routine use in a
    multi-device repo -- it pulls components for devices you're not touching.
    Prefer scan_yaml_files() scoped to the file(s) actually in session."""
    found = set()
    for yaml_file in list(root.rglob("*.yaml")) + list(root.rglob("*.yml")):
        try:
            found |= scan_yaml_text(yaml_file.read_text(errors="ignore"))
        except OSError:
            continue
    return found


def scan_yaml_files(paths: list[Path]) -> set[str]:
    """Scan only the given file(s), following !include / !include_dir_*
    references (the esp-tourbillon packages: mechanism) so a single entry
    file like esp-tourbillon.yaml still resolves its real package tree --
    without touching any other device's config in the repo."""
    found = set()
    visited = set()
    queue = [Path(p).resolve() for p in paths]

    while queue:
        f = queue.pop()
        if f in visited or not f.exists():
            continue
        visited.add(f)
        try:
            text = f.read_text(errors="ignore")
        except OSError:
            continue
        found |= scan_yaml_text(text)

        for m in INCLUDE_RE.finditer(text):
            dir_suffix, ref_path = m.group(1), m.group(2)
            resolved = (f.parent / ref_path).resolve()
            if dir_suffix:  # !include_dir_* -> a directory of yaml files
                if resolved.is_dir():
                    queue.extend(resolved.rglob("*.yaml"))
                    queue.extend(resolved.rglob("*.yml"))
            else:
                queue.append(resolved)

    return found


# --------------------------------------------------------------------------
# C++ header interface extraction (brace-depth tracker, not a full parser —
# good enough to surface public method signatures / enums / constants)
# --------------------------------------------------------------------------

COMMENT_LINE_RE = re.compile(r"//.*$")


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    lines = [COMMENT_LINE_RE.sub("", ln) for ln in text.splitlines()]
    return "\n".join(lines)


def extract_top_level_constants(text: str) -> list[str]:
    out = []
    for m in re.finditer(r"^(?:inline\s+)?constexpr\s+.+?;", text, flags=re.M):
        out.append(m.group(0).strip())
    return out


def extract_enums(text: str) -> list[str]:
    out = []
    for m in re.finditer(r"enum(?:\s+class)?\s+\w+[^{]*\{.*?\};", text, flags=re.S):
        out.append(re.sub(r"\n\s*\n", "\n", m.group(0).strip()))
    return out


def extract_classes(text: str) -> list[dict]:
    """Brace-depth walk: find each `class X ... { ... };` block, then within
    it collect statements that fall under a top-level `public:` label."""
    classes = []
    for m in re.finditer(r"class\s+(\w+)(?:\s+final)?\s*(?::\s*[^{]+)?\{", text):
        name = m.group(1)
        start = m.end() - 1  # position of the opening brace
        depth = 0
        end = None
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end is None:
            continue
        body = text[start + 1:end]

        # Walk body tracking brace depth so nested { } inside inline method
        # bodies don't confuse the public/protected/private detector.
        # Statements can end three ways at depth 0: `;` (declarations), a
        # closing `}` (inline method bodies have no trailing `;`), or `:`
        # (access-specifier labels).
        public_stmts = []
        buf = ""
        access = "private"  # default for `class`, matches C++ semantics
        local_depth = 0

        def flush(stmt: str):
            stmt = stmt.strip()
            if not stmt or not re.search(r"[A-Za-z0-9_]", stmt):
                return
            am = re.match(r"^(public|protected|private)\s*:?$", stmt.rstrip(";").strip())
            if am:
                nonlocal access
                access = am.group(1)
                return
            if access == "public" and not stmt.startswith("friend"):
                public_stmts.append(re.sub(r"\s+", " ", stmt))

        i = 0
        while i < len(body):
            ch = body[i]
            if ch == "{":
                local_depth += 1
                buf += ch
            elif ch == "}":
                local_depth -= 1
                buf += ch
                if local_depth == 0:
                    flush(buf)
                    buf = ""
            elif ch == ";" and local_depth == 0:
                flush(buf + ";")
                buf = ""
            elif ch == ":" and local_depth == 0 and re.match(r"^\s*(public|protected|private)\s*$", buf):
                flush(buf + ":")
                buf = ""
            else:
                buf += ch
            i += 1

        classes.append({"name": name, "public": public_stmts})
    return classes


def build_component_markdown(component: str, src_dir: Path, ref: str, source_note: str = None) -> str:
    # Recurse: many components split platform-specific headers into
    # subfolders (e.g. ads1115/sensor/ads1115_sensor.h).
    files = sorted(src_dir.rglob("*.h"))
    if not files:
        return None

    if source_note is None:
        source_note = f"esphome/components/{component}/ at ref {ref}"

    lines = [
        f"# ESPHome component: `{component}`",
        "",
        f"Source: `{source_note}`",
        "",
        "> Auto-extracted public C++ interface. Not exhaustive — for anything",
        "> not covered here, check the `.py` config schema in the same folder",
        "> or the source file directly before guessing a lambda call.",
        "",
    ]

    any_content = False
    for f in files:
        raw = f.read_text(errors="ignore")
        text = strip_comments(raw)
        consts = extract_top_level_constants(text)
        enums = extract_enums(text)
        classes = extract_classes(text)

        if not (consts or enums or classes):
            continue
        any_content = True
        rel = f.relative_to(src_dir)
        lines.append(f"## `{rel}`")
        lines.append("")

        if enums:
            lines.append("**Enums:**")
            lines.append("```cpp")
            lines.extend(enums)
            lines.append("```")
            lines.append("")

        if consts:
            lines.append("**Constants:**")
            lines.append("```cpp")
            lines.extend(consts)
            lines.append("```")
            lines.append("")

        for c in classes:
            if not c["public"]:
                continue
            lines.append(f"**class `{c['name']}` — public interface:**")
            lines.append("```cpp")
            lines.extend(c["public"])
            lines.append("```")
            lines.append("")

    if not any_content:
        return None
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def load_index(meta_dir: Path) -> dict:
    idx_file = meta_dir / "index.json"
    if idx_file.exists():
        return json.loads(idx_file.read_text())
    return {}


def save_index(meta_dir: Path, index: dict):
    (meta_dir / "index.json").write_text(json.dumps(index, indent=2, sort_keys=True))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scan", metavar="DIR", help="Repo-wide scan of every YAML in DIR. Fine for initial bootstrap; avoid routinely in a multi-device repo (use --files instead).")
    ap.add_argument("--files", nargs="+", metavar="FILE", help="Scan only these specific YAML file(s), following !include/!include_dir_* references. Use this for day-to-day work scoped to the device(s) actually in session.")
    ap.add_argument("--component", nargs="+", metavar="NAME", help="Explicit component name(s) to pull/build")
    ap.add_argument("--kb-dir", default="knowledge-base", help="Knowledge base output directory (default: ./knowledge-base)")
    ap.add_argument("--ref", help="esphome git ref/tag to pin to (default: reuse pinned ref, or latest stable tag)")
    ap.add_argument("--refresh-all", action="store_true", help="Rebuild every already-known component against the current pinned ref")
    ap.add_argument("--dry-run", action="store_true", help="Report what's missing/stale without pulling or writing anything")
    args = ap.parse_args()

    kb_dir = Path(args.kb_dir).resolve()
    meta_dir = kb_dir / "_meta"
    comp_dir = kb_dir / "components"
    meta_dir.mkdir(parents=True, exist_ok=True)
    comp_dir.mkdir(parents=True, exist_ok=True)

    pinned_file = meta_dir / "pinned_ref.txt"
    if args.ref:
        ref = args.ref
    elif pinned_file.exists():
        ref = pinned_file.read_text().strip()
    else:
        print("No pinned ref yet — resolving latest stable esphome release...", file=sys.stderr)
        ref = latest_stable_tag()

    wanted = set(args.component or [])
    if args.scan:
        wanted |= scan_yaml_dir(Path(args.scan).resolve())
    if args.files:
        wanted |= scan_yaml_files([Path(p) for p in args.files])
    if args.refresh_all:
        index = load_index(meta_dir)
        wanted |= set(index.keys())

    if not wanted:
        print("Nothing to do: pass --files FILE ... (scoped) or --scan DIR (repo-wide) and/or --component NAME ...", file=sys.stderr)
        sys.exit(1)

    index = load_index(meta_dir)
    needed = []
    for name in sorted(wanted):
        entry = index.get(name)
        if entry and entry.get("ref") == ref and not args.refresh_all:
            continue  # already up to date for this ref
        needed.append(name)

    print(f"Pinned ref: {ref}")
    print(f"Requested: {len(wanted)} component(s). Already up to date: {len(wanted) - len(needed)}. Need work: {len(needed)}.")
    if needed:
        print("  -> " + ", ".join(needed))

    if args.dry_run:
        return

    pinned_file.write_text(ref)

    if not needed:
        print("Knowledge base already current for all requested components.")
        return

    src = ensure_src_repo(meta_dir, ref)
    external_repos = load_external_repos(meta_dir)
    unresolved = []

    for name in needed:
        comp_src = pull_component_dir(src, name)
        source_note = f"esphome/components/{name}/ at ref {ref}"
        if (comp_src is None or not comp_src.exists()) and name in external_repos:
            spec = external_repos[name]
            try:
                comp_src = pull_external_component_dir(meta_dir, name, spec)
                source_note = f"{spec['repo']} :: {spec['path']}"
            except RuntimeError as e:
                comp_src = None
                print(f"  [!] {name}: external repo clone failed ({spec['repo']}) -- {str(e).splitlines()[-1] if str(e).splitlines() else e}")

        if comp_src is None or not comp_src.exists():
            unresolved.append(name)
            hint = " (not in esphome core -- if this is a HACS/external component, add it to _meta/external_repos.json)" if name not in external_repos else ""
            index[name] = {"ref": ref, "status": "not_found"}
            print(f"  [!] {name}: not found{hint}")
            continue

        md = build_component_markdown(name, comp_src, ref, source_note)
        if md is None:
            unresolved.append(name)
            index[name] = {"ref": ref, "status": "no_extractable_headers"}
            print(f"  [!] {name}: no .h files with an extractable public interface (check .py schema manually)")
            continue

        out_file = comp_dir / f"{name}.md"
        out_file.write_text(md)
        index[name] = {
            "ref": ref,
            "status": "ok",
            "source": source_note,
            "files": [str(f.relative_to(comp_src)) for f in sorted(comp_src.rglob("*.h"))],
        }
        print(f"  [ok] {name} -> {out_file.relative_to(kb_dir.parent) if kb_dir.parent in out_file.parents else out_file}")

    if unresolved:
        unresolved_file = comp_dir / "_unresolved.md"
        existing = unresolved_file.read_text() if unresolved_file.exists() else "# Unresolved components\n\n"
        for name in unresolved:
            if name not in existing:
                existing += f"- `{name}` — not found / no extractable interface at ref `{ref}` (check manually)\n"
        unresolved_file.write_text(existing)

    save_index(meta_dir, index)
    print(f"\nDone. {len(needed) - len(unresolved)} component(s) written, {len(unresolved)} unresolved.")


if __name__ == "__main__":
    main()
