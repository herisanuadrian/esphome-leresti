# esp32-voice — Top-Level Notes

Xiaozhi ESP32-S3 Audio module (1.54" LCD board), voice-assistant scope only.
Package split follows the `esp32-monitor` pattern from day one — read
`esp32-voice/packages/INDEX.md` first for orientation.

## Scope

This config covers ONLY: mic capture, speaker playback, on-device wake word
(`micro_wake_word`), and the HA `voice_assistant` pipeline. Display, battery,
buttons, and LEDs are explicitly deferred — do not add them without a new task.

## Hardware — confirmed pins

Confirmed by two independent sources (hardware teardown + upstream `78/xiaozhi-esp32`
PR #1930 `config.h` for this exact board). See `substitutions:` in `esp32-voice.yaml`.
GPIO0 (BOOT button), GPIO11/12 (4G add-on), GPIO19/20 (native USB) are reserved/unused
in this scope.

## No AEC/beamforming coprocessor

Unlike Home Assistant's Voice PE (XMOS chip), this board has no hardware echo
cancellation. Wake word may false-trigger or fail to detect while the speaker is
playing. Gated via `micro_wake_word`'s `stop_after_detection: true` (halts wake-word
evaluation for the full duration of a `voice_assistant` pipeline run, including TTS
playback) — see `packages/voice/wake_word.yaml` and `packages/voice/NOTES.md`.

## Open hardware-verification items (schema-valid, not yet compile/flash-verified)

- `hardware/pa_enable.yaml` — PA enable polarity (active-high assumed).
- `esp32-voice.yaml`'s `psram:` — octal vs quad PSRAM chip (assumed octal).
- `audio/microphone.yaml` — mic `channel:` (left vs right).
- `audio/microphone.yaml` / `audio/speaker.yaml` — which side of the shared I2S bus
  should be `i2s_mode: secondary` vs `primary` (mic is currently secondary).

None of these are caught by `./validate.sh` (schema-only) — they need a real
`esphome compile` + flash to confirm. Run by the user, not by this agent.

## Cross-file id coupling

`voice/wake_word.yaml` and `voice/assistant.yaml` reference each other's ids
(`mww` calls `voice_assistant.start`; `assistant.yaml` references `mww` in its own
`micro_wake_word:` key and re-arms it via `micro_wake_word.start`/`.stop`). See
`packages/voice/NOTES.md`.

## Secrets

New secrets added to `secrets.yaml` (gitignored, not committed): `api_encryption_key_esp32_voice`,
`ota_password_esp32_voice`. WiFi reuses the existing shared secrets.

## No MANUAL.md

No on-device control surface yet (no display/buttons/LEDs in scope) — nothing to
document for an end user beyond this NOTES.md. Revisit once those land.
