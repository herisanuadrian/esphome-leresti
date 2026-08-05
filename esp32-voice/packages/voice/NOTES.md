# Voice — Overview

On-device wake word detection and the Home Assistant voice-assistant pipeline.

## Files

**wake_word.yaml** — `micro_wake_word:`, no `id:` (single instance, matches the
known-working flat config this was split from). Single model (`hey_jarvis`), no
`vad:` or `stop_after_detection:` (see top-level `NOTES.md`'s "No AEC/beamforming
coprocessor" section — carried over as-is, not added during the packages split).
`on_wake_word_detected` waits 300ms then calls `voice_assistant.start` (no explicit
wake_word lambda, unlike the previous board's config).

**assistant.yaml** — `voice_assistant:`, `id: va`. Uses `speaker:` (not
`media_player:`). Re-arms `micro_wake_word` via `micro_wake_word.start` on `on_end`
and `on_error` only (no `on_client_connected`/`on_client_disconnected` hooks, unlike
the previous board's config) — initial arming instead happens once via
`esp32-voice.yaml`'s top-level `on_boot:` (priority -100, after a boot delay and
`wait_until: api.connected`).

Note: a separate, standalone `media_player` entity exists in
`audio/media_player.yaml` (HA entity `esp_speaker`) for announcements — it wraps
`va_speaker` directly and is unrelated to `voice_assistant:`'s own `speaker:` key.

## Cross-file id coupling

**wake_word.yaml → assistant.yaml**: `on_wake_word_detected` calls
`voice_assistant.start` (targets the `va` id implicitly — only one `voice_assistant:`
instance exists).

**assistant.yaml → wake_word.yaml**: `on_end`/`on_error` call `micro_wake_word.start`
(targets the single `micro_wake_word:` instance implicitly — it has no id).

**esp32-voice.yaml → wake_word.yaml**: top-level `on_boot:` (priority -100) also
calls `micro_wake_word.start` once, after boot + API connect.

Before adding an `id:` to either `micro_wake_word:` or `voice_assistant:`, grep all
three call sites above — the coupling relies on there being exactly one instance of
each.

## Exposes

Neither file exposes a named HA entity — `api:` + `voice_assistant:` together make the
device register as an HA Assist satellite automatically.

## Dependencies

Both depend on `audio/microphone.yaml`'s `va_mic`; `assistant.yaml` also depends on
`audio/speaker.yaml`'s `va_speaker`.
