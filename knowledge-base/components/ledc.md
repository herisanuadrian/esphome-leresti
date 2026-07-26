# ESPHome component: `ledc`

Source: `esphome/components/ledc/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `ledc_output.h`

**class `LEDCOutput` — public interface:**
```cpp
explicit LEDCOutput(InternalGPIOPin *pin) : pin_(pin) { this->channel_ = next_ledc_channel++; }
void set_channel(uint8_t channel) { this->channel_ = channel; }
void set_frequency(float frequency) { this->frequency_ = frequency; }
void set_phase_angle(float angle) { this->phase_angle_ = angle; }
void update_frequency(float frequency) override;
void setup() override;
void dump_config() override;
float get_setup_priority() const override { return setup_priority::HARDWARE; }
void write_state(float state) override;
```

**class `SetFrequencyAction` — public interface:**
```cpp
SetFrequencyAction(LEDCOutput *parent) : parent_(parent) {}
TEMPLATABLE_VALUE(float, frequency);
void play(const Ts &...x) { float freq = this->frequency_.value(x...); this->parent_->update_frequency(freq); }
```
