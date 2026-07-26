# Network — Overview

Wireless connectivity, remote API, and firmware update mechanisms.

## Files

**wifi.yaml** — 3 WiFi networks, all credentials via `!secret`.

**api.yaml** — ESPHome Native API. Defines 7 custom services (`alarma_picaturi`, `buton_panica`, `prezenta_curte`, `prezenta_gradina`, `usa_acces`, `usa_acces_2`, `buzzer_melodie`), each invoked by Home Assistant automations external to this repo. Every service calls `script.execute: show_notification` (`automations/script.yaml`) then `rtttl.play` (`actuators/rtttl.yaml`) to show a notification banner and play an alert melody. `encryption.key` is a literal, pre-existing value — never touch it (see top-level `NOTES.md`).

**ota.yaml** — classic dashboard push OTA only (`platform: esphome`). `password` is a literal, pre-existing value — never touch it.

## Exposes

- 7 API services (see api.yaml above), exposed as `esphome.esp32_monitor_*` service calls from Home Assistant.

## Dependencies

`api.yaml` depends on `automations/script.yaml`'s `show_notification` and `actuators/rtttl.yaml`'s `rtttl.play`. Otherwise: none.

## Hardware Notes

- WiFi: ESP32 built-in WiFi module.
