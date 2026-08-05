# Network — Overview

Wireless connectivity, remote API (also the HA Assist voice-satellite transport), and
firmware update mechanism.

## Files

**wifi.yaml** — 3 WiFi networks, reusing the same shared `!secret` credentials as
`esp32-monitor` (`wifi_ssid_ext`/`wifi_password`/`wifi_ssid_nou`/`wifi_password_nou`/
`wifi_ssid_ext_nou`).

**api.yaml** — ESPHome Native API. No custom `services:` — this device registers as a
Home Assistant Assist voice satellite automatically once `api:` + `voice_assistant:`
are both present; no explicit wiring needed here. `encryption.key` is a literal,
pre-existing value (matches the `esp32-monitor` convention) — never touch it, see
top-level `NOTES.md`.

**ota.yaml** — classic dashboard push OTA only (`platform: esphome`). `password` is a
literal, pre-existing value — never touch it, see top-level `NOTES.md`.

## Exposes

None as named ESPHome entities — the device shows up in Home Assistant as an Assist
satellite, not via `api: services:`.

## Dependencies

None.
