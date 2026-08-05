# Logging — Overview

## Files

**logger.yaml** — `logger: level: INFO`, no per-component log overrides. Lowered
from DEBUG on 2026-08-05: DEBUG-level UART logging was blocking the main loop long
enough to overflow `micro_wake_word`'s ring buffer ("Not enough free bytes in ring
buffer" warning) — see `packages/voice/NOTES.md`.

## Exposes

None.

## Dependencies

None.
