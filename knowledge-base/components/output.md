# ESPHome component: `output`

Source: `esphome/components/output/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `TurnOffAction` — public interface:**
```cpp
TurnOffAction(BinaryOutput *output) : output_(output) {}
void play(const Ts &...x) override { this->output_->turn_off(); }
```

**class `TurnOnAction` — public interface:**
```cpp
TurnOnAction(BinaryOutput *output) : output_(output) {}
void play(const Ts &...x) override { this->output_->turn_on(); }
```

**class `SetLevelAction` — public interface:**
```cpp
SetLevelAction(FloatOutput *output) : output_(output) {}
TEMPLATABLE_VALUE(float, level) void play(const Ts &...x) override { this->output_->set_level(this->level_.value(x...)); }
```

**class `SetMinPowerAction` — public interface:**
```cpp
SetMinPowerAction(FloatOutput *output) : output_(output) {}
TEMPLATABLE_VALUE(float, min_power) void play(const Ts &...x) override { this->output_->set_min_power(this->min_power_.value(x...)); }
```

**class `SetMaxPowerAction` — public interface:**
```cpp
SetMaxPowerAction(FloatOutput *output) : output_(output) {}
TEMPLATABLE_VALUE(float, max_power) void play(const Ts &...x) override { this->output_->set_max_power(this->max_power_.value(x...)); }
```

## `binary_output.h`

**class `BinaryOutput` — public interface:**
```cpp
void set_inverted(bool inverted) { this->inverted_ = inverted; }
#ifdef USE_POWER_SUPPLY void set_power_supply(power_supply::PowerSupply *power_supply) { this->power_.set_parent(power_supply); }
#endif virtual void set_state(bool state) { if (state) { this->turn_on(); } else { this->turn_off(); } }
virtual void turn_on() { #ifdef USE_POWER_SUPPLY this->power_.request(); #endif this->write_state(!this->inverted_); }
virtual void turn_off() { #ifdef USE_POWER_SUPPLY this->power_.unrequest(); #endif this->write_state(this->inverted_); }
bool is_inverted() const { return this->inverted_; }
```

## `button/output_button.h`

**class `OutputButton` — public interface:**
```cpp
void dump_config() override;
void set_output(BinaryOutput *output) { output_ = output; }
void set_duration(uint32_t duration) { duration_ = duration; }
```

## `float_output.h`

**class `FloatOutput` — public interface:**
```cpp
#ifdef USE_OUTPUT_FLOAT_POWER_SCALING void set_max_power(float max_power);
void set_min_power(float min_power);
void set_zero_means_zero(bool zero_means_zero) { this->zero_means_zero_ = zero_means_zero; }
#else template<bool _use_output_float_power_scaling = false> void set_max_power(float max_power) { static_assert(_use_output_float_power_scaling, "set_max_power() requires USE_OUTPUT_FLOAT_POWER_SCALING. " "To enable it, add 'max_power: 100%' (or any value) to one output entry in your YAML — " "the codegen will then keep the scaling fields. " "See https: }
template<bool _use_output_float_power_scaling = false> void set_min_power(float min_power) { static_assert(_use_output_float_power_scaling, "set_min_power() requires USE_OUTPUT_FLOAT_POWER_SCALING. " "To enable it, add 'min_power: 0%' (or any value) to one output entry in your YAML — " "the codegen will then keep the scaling fields. " "See https: }
template<bool _use_output_float_power_scaling = false> void set_zero_means_zero(bool zero_means_zero) { static_assert(_use_output_float_power_scaling, "set_zero_means_zero() requires USE_OUTPUT_FLOAT_POWER_SCALING. " "To enable it, add 'zero_means_zero: true' to one output entry in your YAML."); }
#endif void set_level(float state);
virtual void update_frequency(float frequency) {}
#ifdef USE_OUTPUT_FLOAT_POWER_SCALING float get_max_power() const { return this->max_power_; }
float get_min_power() const { return this->min_power_; }
#else float get_max_power() const { return 1.0f; }
float get_min_power() const { return 0.0f; }
#endif protected: void write_state(bool state) override;
virtual void write_state(float state) = 0;
#ifdef USE_OUTPUT_FLOAT_POWER_SCALING float max_power_{1.0f}
float min_power_{0.0f}
bool zero_means_zero_{false}
```

## `lock/output_lock.h`

**class `OutputLock` — public interface:**
```cpp
void set_output(BinaryOutput *output) { output_ = output; }
float get_setup_priority() const override { return setup_priority::HARDWARE - 1.0f; }
void dump_config() override;
```

## `switch/output_switch.h`

**class `OutputSwitch` — public interface:**
```cpp
void set_output(BinaryOutput *output) { output_ = output; }
void setup() override;
float get_setup_priority() const override { return setup_priority::HARDWARE - 1.0f; }
void dump_config() override;
```
