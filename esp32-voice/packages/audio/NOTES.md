# Audio — Overview

Microphone capture and speaker playback components, both `platform: i2s_audio`.

## Files

**microphone.yaml** — `id: mic_es8311`, `adc_type: external`, `i2s_mode: secondary`
(shares the I2S bus with the speaker — see `hardware/i2s_bus.yaml`). `channel: left`
and the primary/secondary assignment are unconfirmed hardware-behavior guesses, both
schema-valid — see top-level `NOTES.md`.

**speaker.yaml** — `id: spk_es8311`, `dac_type: external`, `i2s_mode: primary`,
references `hardware/codec.yaml`'s `es8311_dac` via `audio_dac:` for volume/mute
passthrough. `sample_rate: 16000` matches the codec's own `sample_rate`.

## Exposes

- `microphone.mic_es8311` — consumed by `voice/wake_word.yaml`, `voice/assistant.yaml`.
- `speaker.spk_es8311` — consumed by `voice/assistant.yaml`.

## Dependencies

Both depend on `hardware/i2s_bus.yaml`'s `i2s_bus_audio` hub. `speaker.yaml` also
depends on `hardware/codec.yaml`'s `es8311_dac`.
