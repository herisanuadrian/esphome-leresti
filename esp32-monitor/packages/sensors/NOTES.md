# Sensors — Overview

Diagnostic sensors and Home Assistant sensor mirrors used to drive the dashboard's exterior/dormitor panels.

## Files

**sensor.yaml** — 3 HA-facing diagnostic sensors (`sensor_psram`, `sensor_heap`, `sensor_wifi`) plus 4 internal-only `platform: homeassistant` mirrors (no `name:`, so no HA entity of their own): `ha_statie_temp` (reads `sensor.statie_meteo_temperatura`), `ha_statie_lux` (reads `sensor.statie_meteo_luminozitate`), `ha_dorm_temp` (reads `sensor.temp_dormitor_1`), `ha_dorm_umid` (reads `sensor.umid_dormitor_1`).

## Exposes

- `sensor.sensor_psram`, `sensor.sensor_heap`, `sensor.sensor_wifi` (diagnostic, HA-facing).
- Internal-only (no HA entity): `ha_statie_temp`, `ha_statie_lux`, `ha_dorm_temp`, `ha_dorm_umid` — consumed by `automations/interval.yaml`'s 30s label-refresh lambda.

## Dependencies

Reads 4 external HA entities (see Files above). Otherwise: none.
