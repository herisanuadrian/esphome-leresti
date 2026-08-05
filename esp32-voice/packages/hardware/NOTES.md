# Hardware — Overview

Low-level bus, codec, and amplifier-enable configuration for the ES8311 audio path.

## Files

**i2c.yaml** — I2C bus for ES8311 register control, `id: i2c_bus`, internal pull-ups
enabled (mirrors the reference firmware's `I2C_NUM_0` config per hardware source
notes).

**i2s_bus.yaml** — single shared `i2s_audio:` hub (`id: i2s_bus_audio`). Both the mic
(DIN) and speaker (DOUT) attach to this one hub via `i2s_audio_id` — this board wires
mic and speaker to a single I2S peripheral with shared BCLK/LRCK/MCLK, unlike designs
with two separate I2S ports. Pin values are bare GPIO numbers (confirmed via
`esphome config` dump, not a `number:` sub-key).

**codec.yaml** — ES8311 `audio_dac:`, `id: es8311_dac`. `use_microphone: true` since
this board has no separate mic-ADC chip — the ES8311's own ADC path handles mic input.
Referenced by `audio/speaker.yaml`'s `audio_dac:` key for volume/mute passthrough
(does not itself carry I2S pin wiring — that's on the mic/speaker platform entries).

**pa_enable.yaml** — GPIO8 speaker-amp enable, `switch: platform: gpio`,
`restore_mode: ALWAYS_ON`, `internal: true` (no HA entity yet). Polarity unconfirmed
(active-high assumed) — see top-level `NOTES.md`'s open-items list.

## Exposes

- `i2c.i2c_bus` — consumed by `codec.yaml`.
- `i2s_audio.i2s_bus_audio` — consumed by `audio/microphone.yaml`, `audio/speaker.yaml`.
- `audio_dac.es8311_dac` — consumed by `audio/speaker.yaml`.
- Internal-only `switch.pa_enable` — no HA entity.

## Dependencies

Pins come from `esp32-voice.yaml`'s `substitutions:`.

## Hardware Notes

- No AEC/beamforming coprocessor on this board — see top-level `NOTES.md`.
- PSRAM mode (octal assumed) and PA polarity are unconfirmed — flagged as
  `# TODO verify:` comments in the relevant files.
