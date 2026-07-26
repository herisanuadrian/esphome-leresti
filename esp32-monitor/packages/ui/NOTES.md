# UI — Overview

Display hardware, styling primitives (colors/fonts), and the 3-page LVGL touch UI.

## Files

**display.yaml** — bundles `color:` (12 colors), `font:` (5 Roboto sizes), and `display:` (ILI9xxx ST7796 480x320, `id: my_display`) together, mirroring the esp-tourbillon precedent of keeping a display's styling primitives in one file. All three lvgl page files and `lvgl_base.yaml` reference these color/font ids by name.

**lvgl_base.yaml** — top-level lvgl config only: `displays:`, `touchscreens:`, `rotation:`, `buffer_size:`, `theme:`. Contributes no `pages:` entries itself. `rotation: 90` lives here rather than under `display.yaml`'s `display:` block — ESPHome rejects `rotation` under `display:` once `lvgl:` is configured.

**lvgl_page_clock.yaml**, **lvgl_page_exterior.yaml**, **lvgl_page_dormitor.yaml** — one file per page, each contributing a single entry to the `lvgl.pages:` list (ESPHome package merge concatenates lists, so this is safe). **Order matters**: see the top-level `esp32-monitor/NOTES.md` "lvgl page order" section — these three files' `packages:` keys must stay in clock → exterior → dormitor order in `esp32-monitor.yaml` for the 6s auto-advance interval to cycle correctly.

## Exposes

- `display.my_display`, 12 `color.*` ids, 5 `font.*` ids (display.yaml).
- lvgl pages `page_clock`, `page_exterior`, `page_dormitor` and their label/widget ids (see each page file's own `# EXPOSES:` header).

## Dependencies

`display.yaml` depends on `hardware/spi.yaml`'s SPI bus. `lvgl_base.yaml` depends on `display.yaml`'s `my_display` and `hardware/touchscreen.yaml`'s `my_touch`. All three page files depend on `display.yaml`'s colors/fonts and are read by `automations/script.yaml` and `automations/interval.yaml`.
