# ESPHome component: `status`

Source: `esphome/components/status/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `status_binary_sensor.h`

**class `StatusBinarySensor` — public interface:**
```cpp
void update() override;
void setup() override;
void dump_config() override;
bool is_status_binary_sensor() const override { return true; }
```
