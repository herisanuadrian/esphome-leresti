#!/usr/bin/env python3
"""Extract ESPHome-generated entity IDs (domain.object_id) from device YAML files.

Regex/block-based, not a full YAML parser (this repo's YAML has custom tags
like !secret/!lambda that a strict parser would choke on, and lambdas are C++
text, not structure). Mirrors ESPHome's own object_id algorithm: normalize
unicode (strips accents: a-with-breve -> a, s-with-comma -> s, etc.), lowercase,
replace anything that isn't [a-z0-9] with "_", collapse/trim underscores.

Usage:
    python3 scripts/extract_entity_ids.py file1.yaml [file2.yaml ...]
    python3 scripts/extract_entity_ids.py *.yaml
    python3 scripts/extract_entity_ids.py --ids-only file1.yaml   # no name comments

Output per file:
    EXPOSES  - one "domain.object_id" per named entity this device publishes
               (comment shows the source name, unless --ids-only)
    CONSUMES - entity IDs read via `platform: homeassistant`, and entity IDs /
               service names written via `homeassistant.service:` calls

Entities with no `name:` (internal-only, e.g. a homeassistant mirror sensor
used only in a lambda) are not exposed entities and are omitted from EXPOSES.
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

# ESPHome top-level keys that create HA entities, mapped to their HA domain
# (only esp32_camera differs from its own YAML key).
ENTITY_DOMAINS = {
    "sensor": "sensor",
    "binary_sensor": "binary_sensor",
    "switch": "switch",
    "text_sensor": "text_sensor",
    "climate": "climate",
    "number": "number",
    "light": "light",
    "button": "button",
    "cover": "cover",
    "lock": "lock",
    "fan": "fan",
    "select": "select",
    "valve": "valve",
    "esp32_camera": "camera",
    "alarm_control_panel": "alarm_control_panel",
    "siren": "siren",
    "water_heater": "water_heater",
    "humidifier": "humidifier",
    "event": "event",
    "update": "update",
    "text": "text",
    "date": "date",
    "datetime": "datetime",
    "time": "time",  # only when it's a user-facing time entity, not the HA-clock-sync platform
}


def slugify(value: str) -> str:
    value = value.strip().strip("'\"").strip()
    normalized = unicodedata.normalize("NFKD", value)
    stripped = "".join(c for c in normalized if not unicodedata.combining(c))
    lowered = stripped.lower()
    sanitized = re.sub(r"[^a-z0-9]+", "_", lowered)
    return sanitized.strip("_")


def load_substitutions(text: str) -> dict:
    subs = {}
    m = re.search(r"^substitutions:\s*\n((?:[ \t]+.+\n?)*)", text, re.M)
    if not m:
        return subs
    block = m.group(1)
    for line in block.splitlines():
        km = re.match(r"\s*([A-Za-z_0-9]+):\s*(.+?)\s*(#.*)?$", line)
        if km:
            subs[km.group(1)] = km.group(2).strip().strip("'\"")
    return subs


def resolve_substitutions(value: str, subs: dict) -> str:
    for _ in range(5):
        new_value = re.sub(
            r"\$\{([A-Za-z_0-9]+)\}", lambda m: subs.get(m.group(1), m.group(0)), value
        )
        if new_value == value:
            break
        value = new_value
    return value


def iter_blocks(lines, top_indent_max=2):
    """Yield (domain, block_lines) for each top-level-key's list-item blocks."""
    domain = None
    block = []

    def is_top_level_key(line):
        return bool(re.match(r"^[A-Za-z_0-9]+:", line))

    for raw in lines:
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0 and is_top_level_key(line):
            if domain is not None and block:
                yield domain, block
            domain = line.split(":")[0]
            block = []
            continue
        if domain is None:
            continue
        stripped = line.lstrip(" ")
        if indent <= top_indent_max and stripped.startswith("- "):
            if block:
                yield domain, block
            block = [line]
        else:
            block.append(line)
    if domain is not None and block:
        yield domain, block


def extract_exposes(text: str, subs: dict):
    lines = text.splitlines()
    results = []
    for domain, block in iter_blocks(lines):
        ha_domain = ENTITY_DOMAINS.get(domain)
        if ha_domain is None:
            continue
        block_text = "\n".join(block)
        platform_m = re.search(r"^\s*-?\s*platform:\s*(\S+)", block_text, re.M)
        platform = platform_m.group(1) if platform_m else None
        if domain == "time" and platform == "homeassistant":
            continue  # clock-sync boilerplate, not a user-facing entity
        names = re.findall(r"^\s*-?\s*name:\s*(.+?)\s*$", block_text, re.M)
        for raw_name in names:
            name = resolve_substitutions(raw_name, subs)
            object_id = slugify(name)
            if not object_id:
                continue
            results.append((f"{ha_domain}.{object_id}", raw_name))
    return results


def extract_consumes(text: str):
    reads = []
    writes = []
    lines = text.splitlines()

    # Reads: platform: homeassistant blocks (sensor/binary_sensor) with entity_id.
    for domain, block in iter_blocks(lines):
        if domain not in ("sensor", "binary_sensor", "text_sensor"):
            continue
        block_text = "\n".join(block)
        if not re.search(r"^\s*-?\s*platform:\s*homeassistant", block_text, re.M):
            continue
        m = re.search(r"^\s*entity_id:\s*(\S+)", block_text, re.M)
        if m:
            reads.append(m.group(1))

    # Writes/calls: homeassistant.service: blocks anywhere (nested in automations).
    for m in re.finditer(r"homeassistant\.service:\s*\n((?:[ \t]*\n|[ \t]+.+\n)*)", text):
        block = m.group(1)
        base_indent = None
        block_lines = []
        for line in block.splitlines():
            if not line.strip():
                continue
            indent = len(line) - len(line.lstrip(" "))
            if base_indent is None:
                base_indent = indent
            if indent < base_indent:
                break
            block_lines.append(line)
        block_text = "\n".join(block_lines)
        service_m = re.search(r"^\s*service:\s*(\S+)", block_text, re.M)
        entity_m = re.search(r"^\s*entity_id:\s*(\S+)", block_text, re.M)
        if entity_m:
            service = service_m.group(1) if service_m else "?"
            writes.append(f"{entity_m.group(1)} (via {service})")
        elif service_m:
            writes.append(service_m.group(1))

    return reads, writes


def process_file(path: Path, ids_only: bool):
    text = path.read_text()
    subs = load_substitutions(text)
    exposes = extract_exposes(text, subs)
    reads, writes = extract_consumes(text)

    print(f"=== {path.name} ===")
    print("EXPOSES:")
    if not exposes:
        print("  (none)")
    for object_id, raw_name in exposes:
        if ids_only:
            print(f"  {object_id}")
        else:
            print(f"  {object_id}  # {raw_name.strip().strip(chr(39)+chr(34))}")
    print("CONSUMES:")
    if not reads and not writes:
        print("  (none)")
    for r in reads:
        print(f"  reads:  {r}")
    for w in writes:
        print(f"  writes: {w}")
    print()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+", help="YAML file(s) to scan")
    parser.add_argument("--ids-only", action="store_true", help="omit the source-name comment on EXPOSES lines")
    args = parser.parse_args()

    for file_arg in args.files:
        path = Path(file_arg)
        if not path.exists():
            print(f"=== {file_arg} ===\n  ! file not found\n", file=sys.stderr)
            continue
        if path.name == "secrets.yaml":
            continue
        process_file(path, args.ids_only)


if __name__ == "__main__":
    main()
