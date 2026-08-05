# Hardware — Overview

Low-level I2S bus configuration. This board (303ESP32S3-AI) has no I2C control bus,
codec, or PA-enable GPIO — the INMP441 mic and MAX98357A amp are both pure I2S
devices with no register interface, unlike the previous ES8311-based board.

## Files

**i2s_bus.yaml** — two independent `i2s_audio:` buses, `id: i2s_mic` and
`id: i2s_spk`. Unlike the previous board (one shared bus for mic+speaker), this
board wires the INMP441 and MAX98357A to separate I2S peripherals.

## Exposes

- `i2s_audio.i2s_mic` — consumed by `audio/microphone.yaml`.
- `i2s_audio.i2s_spk` — consumed by `audio/speaker.yaml`.

## Dependencies

None. Pins are hardcoded literals in `i2s_bus.yaml` (no `substitutions:` layer).
