# Sensors — Overview

Diagnostic sensors, reset-reason reporting, and the physical buttons/PIR exposed by
this board.

## Files

**sensor.yaml** — 3 HA-facing diagnostic sensors (`uptime`, `wifi_signal`,
`internal_temperature`, all unnamed ids) plus a `text_sensor` template,
`id: reset_reason`, published by `esp32-voice.yaml`'s top-level `on_boot:`
(priority 600) lambda that decodes `esp_reset_reason()`.

**binary_sensor.yaml** — `status` sensor ("VA Online"), plus 4 `platform: gpio`
sensors: `vol_down` (GPIO39), `vol_up` (GPIO40), `wifi_btn` (GPIO1) — all
`INPUT_PULLUP`/`inverted: true` — and `pir_motion` (GPIO8, `device_class: motion`,
HC-SR501-compatible). None have HA automations wired from this config yet.

## Exposes

- `sensor.VA_Uptime`, `sensor.VA_WiFi_RSSI`, `sensor.VA_Temperature` (diagnostic).
- `text_sensor.reset_reason` — HA entity "VA Reset Reason"; written by
  `esp32-voice.yaml`'s `on_boot:` lambda (cross-file id coupling — see top-level
  `NOTES.md`).
- `binary_sensor.VA_Online`, `vol_down`, `vol_up`, `wifi_btn`, `pir_motion`.

## Dependencies

None component-wise. `reset_reason` is written from outside this package (see
Exposes above).
