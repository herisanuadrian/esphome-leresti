# Network — Overview

Wireless connectivity, remote API (also the HA Assist voice-satellite transport), and
firmware update mechanism.

## Files

**wifi.yaml** — 3 WiFi networks, reusing the same shared `!secret` credentials as
`esp32-monitor` (`wifi_ssid_ext`/`wifi_password`/`wifi_ssid_nou`/`wifi_password_nou`/
`wifi_ssid_ext_nou`).

**api.yaml** — ESPHome Native API. No custom `services:` — this device registers as a
Home Assistant Assist voice satellite automatically once `api:` + `voice_assistant:`
are both present; no explicit wiring needed here. `encryption.key` is a new
`!secret api_encryption_key_esp32_voice`, generated for this device specifically (not
shared with other devices, unlike the WiFi credentials).

**ota.yaml** — classic dashboard push OTA only (`platform: esphome`). Uses a new
`!secret ota_password_esp32_voice` — unlike other devices in this repo (which use a
literal, pre-existing OTA password), this device follows the task's explicit
"secrets go in secrets.yaml" instruction since there was no pre-existing literal to
preserve.

## Exposes

None as named ESPHome entities — the device shows up in Home Assistant as an Assist
satellite, not via `api: services:`.

## Dependencies

None beyond the two new secrets noted above.
