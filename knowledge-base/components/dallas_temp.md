# ESPHome component: `dallas_temp`

Source: `esphome/components/dallas_temp/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `dallas_temp.h`

**class `DallasTemperatureSensor` — public interface:**
```cpp
void setup() override;
void update() override;
void dump_config() override;
void set_resolution(uint8_t resolution) { this->resolution_ = resolution; }
```
