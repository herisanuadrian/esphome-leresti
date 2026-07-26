# ESPHome component: `network`

Source: `esphome/components/network/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `network_component.h`

**class `NetworkComponent` — public interface:**
```cpp
void setup() override;
float get_setup_priority() const override { return setup_priority::AFTER_BLUETOOTH; }
```
