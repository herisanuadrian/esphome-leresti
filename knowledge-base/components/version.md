# ESPHome component: `version`

Source: `esphome/components/version/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `version_text_sensor.h`

**class `VersionTextSensor` — public interface:**
```cpp
void set_hide_hash(bool hide_hash);
void set_hide_timestamp(bool hide_timestamp);
void setup() override;
void dump_config() override;
```
