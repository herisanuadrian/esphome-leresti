# Actuators — Overview

Backlight and buzzer output hardware.

## Files

**output.yaml** — 2 raw `ledc` PWM outputs: `backlight_pwm` (drives `light.yaml`), `buzzer_out` (drives `rtttl.yaml`). No HA entities of their own.

**light.yaml** — `light.backlight`, a monochromatic light wrapping `backlight_pwm`. Turned on/off by `automations/interval.yaml`'s 60s scheduler (on 06:00–21:00, off otherwise) based on `time/time.yaml`'s `ha_time`.

**rtttl.yaml** — RTTTL buzzer melody player wrapping `buzzer_out`. `rtttl.play` is called directly from each of `network/api.yaml`'s 7 services — not from any script or interval.

## Exposes

- `light.backlight`.

## Dependencies

`light.yaml` and `rtttl.yaml` depend on `output.yaml`'s PWM outputs. `light.yaml` is driven by `automations/interval.yaml`; `rtttl.yaml` is driven by `network/api.yaml`.
