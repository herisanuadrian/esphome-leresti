# esp32-voice — Top-Level Notes

303ESP32S3-AI v2.3 board (INMP441 mic + MAX98357A amp), voice-assistant scope.
Package split follows the `esp32-monitor` pattern — read
`esp32-voice/packages/INDEX.md` first for orientation.

## Board history

This device previously ran on a different, ES8311-codec-based board (I2C control
bus, shared I2S bus between mic/speaker, `okay_nabu` wake word). That board was
replaced (2026-08-06) with the current 303ESP32S3-AI hardware — a known-working
flat config was split into this package layout. The full board reference (GPIO
map, chip/FCC/board IDs) lives in the header comment of `esp32-voice.yaml`.

## Scope

Mic capture, speaker playback, on-device wake word (`micro_wake_word`, `hey_jarvis`
model), the HA `voice_assistant` pipeline, a standalone announcement `media_player`,
plus buttons (Vol Up/Down, WiFi), a PIR motion sensor, and diagnostic
sensors/reset-reason reporting. No display present on this board variant.

## No AEC/beamforming coprocessor

Unlike Home Assistant's Voice PE (XMOS chip), this board has no hardware echo
cancellation. Note: unlike the previous board's config, this one does **not** set
`stop_after_detection` or an explicit `vad:` on `micro_wake_word` — carried over
as-is from the known-working flat config; not changed as part of the packages
split. If wake word false-triggers during TTS playback, that gating is the first
thing to revisit.

## Cross-file id coupling

`esp32-voice.yaml`'s top-level `on_boot:` (priority 600) publishes to
`text_sensor.reset_reason`, defined in `packages/sensors/sensor.yaml` — and its
`on_boot:` (priority -100) and `packages/voice/assistant.yaml`'s `on_end`/`on_error`
all call `micro_wake_word.start` (single instance, no id, defined in
`packages/voice/wake_word.yaml`), which itself calls `voice_assistant.start`
(single instance, id `va`, defined in `packages/voice/assistant.yaml`).

## Literal (non-`!secret`) credentials — never touch the values

`network/api.yaml`'s `encryption.key` and `network/ota.yaml`'s `password` are literal
strings, matching the pre-existing `esp32-monitor` convention. WiFi uses the shared
`!secret` credentials (`wifi_ssid_nou`/`wifi_password_nou`/`ap_password`).

## No MANUAL.md

Buttons/PIR exist but have no HA automations wired from this config yet (volume
buttons and WiFi button are exposed as `binary_sensor`s only) — revisit once
automations land.
