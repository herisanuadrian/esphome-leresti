# ESPHome component: `speed`

Source: `esphome/components/speed/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `fan/speed_fan.h`

**class `SpeedFan` — public interface:**
```cpp
SpeedFan(int speed_count) : speed_count_(speed_count) {}
void setup() override;
void dump_config() override;
void set_output(output::FloatOutput *output) { this->output_ = output; }
void set_oscillating(output::BinaryOutput *oscillating) { this->oscillating_ = oscillating; }
void set_direction(output::BinaryOutput *direction) { this->direction_ = direction; }
void set_preset_modes(std::initializer_list<const char *> presets) { this->set_supported_preset_modes(presets); }
fan::FanTraits get_traits() override { this->wire_preset_modes_(this->traits_); return this->traits_; }
```
