# Automations — Overview

Notification script and periodic UI-refresh intervals — the most cross-coupled domain in this split (see top-level `esp32-monitor/NOTES.md`).

## Files

**script.yaml** — `show_notification`: updates the notification label/box on all 3 lvgl pages, shows them, waits 5s, hides them. Called by all 7 services in `network/api.yaml`.

**interval.yaml** — 4 intervals:
- 60s: reads `ha_time`, turns `backlight` on (06:00–21:00) or off (otherwise).
- 6s: `lvgl.page.next` — auto-advances the visible page (order-dependent, see top-level NOTES.md).
- 1s: updates clock/seconds/date labels on `page_clock` and the compact time label on `page_dormitor`, all from `ha_time`.
- 30s: updates wifi-signal labels on all 3 pages, and temperature/humidity/lux labels on `page_clock` (dormitor mirror) and `page_exterior`/`page_dormitor` (exterior + dormitor temp/humidity), from `sensors/sensor.yaml`'s ids.

## Exposes

- `script.show_notification`.

## Dependencies

Full cross-file id list is in the top-level `esp32-monitor/NOTES.md` "Cross-file id coupling" section — this domain is the heaviest consumer of ids from `time/`, `sensors/`, `actuators/light.yaml`, and all three `ui/lvgl_page_*.yaml` files.
