# Hardware — Overview

Low-level bus and touch-input configuration.

## Files

**spi.yaml** — SPI bus (clk/mosi/miso pins from substitutions), used by the ILI9xxx display in `ui/display.yaml`.

**touchscreen.yaml** — XPT2046 resistive touch controller, `id: my_touch`, with calibration values and an `on_touch` debug lambda that logs raw x/y at `ESP_LOGI` (visible since `logging/logger.yaml` sets `xpt2046: DEBUG`).

## Exposes

- `touchscreen.my_touch` — consumed by `ui/lvgl_base.yaml`'s `touchscreens:` list.

## Dependencies

None (pins come from `esp32-monitor.yaml`'s `substitutions:`).

## Hardware Notes

- Touch calibration (`x_min`/`x_max`/`y_min`/`y_max`) is device-specific — recalibrating requires touching the physical screen's corners, not a config-only change.
