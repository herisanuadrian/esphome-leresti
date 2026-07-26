# Time — Overview

Clock source for the on-screen clock/date labels.

## Files

**time.yaml** — single `platform: homeassistant` time source, `id: ha_time`. Has no `name:`, so it's internal-only (no HA-facing entity); its value is read via `id(ha_time)` in `automations/script.yaml`'s and `automations/interval.yaml`'s lambdas to populate the clock/date labels on all three lvgl pages.

## Exposes

(nothing HA-facing — internal time source only)

## Dependencies

None (consumed by `automations/interval.yaml`, `actuators/light.yaml`'s backlight schedule indirectly via the interval).
