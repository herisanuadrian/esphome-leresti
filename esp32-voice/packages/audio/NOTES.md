# Audio — Overview

Microphone capture and speaker playback components, both `platform: i2s_audio`,
each on its own dedicated I2S bus (see `hardware/i2s_bus.yaml`).

## Files

**microphone.yaml** — `id: va_mic`, INMP441 (`adc_type: external`, `channel: left`),
on the `i2s_mic` bus.

**speaker.yaml** — `id: va_speaker`, MAX98357A (`dac_type: external`,
`i2s_mode: primary`), on the `i2s_spk` bus. No `audio_dac:` reference — unlike the
previous ES8311 board, this amp has no separate codec component for volume/mute.

**media_player.yaml** — `id: external_media_player`, `platform: speaker`, HA entity
`esp_speaker`. Wraps `va_speaker` via `announcement_pipeline:` for a standalone
announcement/media entity, independent of `voice/assistant.yaml`'s `voice_assistant:`,
which feeds `va_speaker` directly via its own `speaker:` key.

## Exposes

- `microphone.va_mic` — consumed by `voice/assistant.yaml`.
- `speaker.va_speaker` — consumed by `voice/assistant.yaml`, `audio/media_player.yaml`.
- `media_player.external_media_player` — HA entity `esp_speaker`.

## Dependencies

`microphone.yaml` depends on `hardware/i2s_bus.yaml`'s `i2s_mic`. `speaker.yaml`
depends on `hardware/i2s_bus.yaml`'s `i2s_spk`. `media_player.yaml` depends on
`speaker.yaml`'s `va_speaker`.
