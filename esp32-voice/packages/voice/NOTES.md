# Voice — Overview

On-device wake word detection and the Home Assistant voice-assistant pipeline.

## Files

**wake_word.yaml** — `micro_wake_word:`, `id: mww`, single model (`okay_nabu`), plus
the default `vad:` model. `stop_after_detection: true` is the chosen mechanism for
avoiding wake-word false-triggers during TTS playback (see top-level `NOTES.md`'s
"No AEC/beamforming coprocessor" section) — this is the ONLY gating mechanism used;
no separate `on_tts_start`/`on_tts_end` hooks were added, to keep this minimal.
`on_wake_word_detected` calls `voice_assistant.start` with the detected `wake_word`
lambda variable.

**assistant.yaml** — `voice_assistant:`, `id: va`. Uses `speaker:` (not `media_player:`
— these are mutually exclusive as `voice_assistant:`'s own audio-output key). Re-arms
`micro_wake_word` via `micro_wake_word.start`/`.stop` on `on_client_connected`/
`on_client_disconnected`/`on_end`/`on_error`.

Note: a separate, standalone `media_player` entity exists in
`audio/media_player.yaml` (HA entity `esp_speaker`) for announcements — it wraps
`spk_es8311` directly and is unrelated to `voice_assistant:`'s own `speaker:` key
above.

## Cross-file id coupling

**wake_word.yaml → assistant.yaml**: `on_wake_word_detected` calls
`voice_assistant.start` (targets the `va` id implicitly — only one `voice_assistant:`
instance exists, so no explicit id needed in the action).

**assistant.yaml → wake_word.yaml**: `micro_wake_word: mww` key, plus 4 automations
(`micro_wake_word.start`/`.stop: { id: mww }`).

Before renaming `mww` or `va`, grep both files — the coupling is bidirectional and not
visible from either file in isolation.

## Exposes

Neither file exposes a named HA entity — `api:` + `voice_assistant:` together make the
device register as an HA Assist satellite automatically.

## Dependencies

Both depend on `audio/microphone.yaml`'s `mic_es8311`; `assistant.yaml` also depends on
`audio/speaker.yaml`'s `spk_es8311`.
