# esp32-monitor — Top-Level Notes

Package split introduced 2026-07-26, following the `esp-tourbillon` pattern from the sibling `/Users/adrian/tools/esphome` repo. Config is composed from `esp32-monitor/packages/<domain>/<feature>.yaml` files via `packages:` in `esp32-monitor.yaml`. Orientation: read `esp32-monitor/packages/INDEX.md` first.

## lvgl page order — do not reorder without checking

`ui/lvgl_page_clock.yaml`, `ui/lvgl_page_exterior.yaml`, and `ui/lvgl_page_dormitor.yaml` each contribute one entry to `lvgl.pages:` (a list, concatenated by ESPHome's package merge in the order their `packages:` keys appear in `esp32-monitor.yaml`). The 6s auto-advance interval (`automations/interval.yaml`) calls `lvgl.page.next`, which cycles pages in that assembled order, not by id. **The `packages:` block in `esp32-monitor.yaml` must keep `ui/lvgl_page_clock` → `ui/lvgl_page_exterior` → `ui/lvgl_page_dormitor` in that exact order** to preserve the current clock → exterior → dormitor cycle. Re-validate with `./validate.sh esp32-monitor` after touching this ordering.

## Cross-file id coupling

`automations/interval.yaml` and `automations/script.yaml` are the most coupled files in this split — they reference ids defined across nearly every other domain:
- `time/time.yaml`: `ha_time`
- `sensors/sensor.yaml`: `sensor_wifi`, `ha_dorm_temp`, `ha_dorm_umid`, `ha_statie_temp`, `ha_statie_lux`
- `actuators/light.yaml`: `backlight`
- `ui/lvgl_page_clock.yaml`: `p1_wifi`, `p1_time`, `p1_seconds`, `p1_date`, `p1_dorm_temp`, `p1_dorm_umid`, `p1_notif_box`, `p1_notif_text`
- `ui/lvgl_page_exterior.yaml`: `p2_wifi`, `p2_temp`, `p2_lux`, `p2_notif_box`, `p2_notif_text`
- `ui/lvgl_page_dormitor.yaml`: `p3_wifi`, `p3_temp`, `p3_umid`, `p3_time`, `p3_notif_box`, `p3_notif_text`

Before renaming any of these ids, grep the whole `esp32-monitor/` tree first — a rename in one file silently breaks a lambda in another.

## Literal (non-`!secret`) credentials — never touch the values

`network/api.yaml`'s `encryption.key` and `network/ota.yaml`'s `password` are literal strings, pre-existing before this split (not introduced by it, and not converted to `!secret`). Never replace, regenerate, or print these values in any report.

## No MANUAL.md

This device is a straightforward dashboard (no on-device menu/control surface like esp-tourbillon's motor/LED system), so no user-facing manual was created. Revisit if the device grows a control surface worth documenting.

## Fixed during the split: rotation moved from display: to lvgl:

The original monolithic file had `rotation: 90` under `display:` (confirmed pre-existing via `git show HEAD:esp32-monitor.yaml`), which ESPHome rejects when `lvgl:` is also configured ("use of 'rotation' in the display config is not compatible with LVGL"). Fixed by moving `rotation: 90` from `ui/display.yaml`'s `display:` block to `ui/lvgl_base.yaml`'s `lvgl:` block.
