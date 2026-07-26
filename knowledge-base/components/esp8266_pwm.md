# ESPHome component: `esp8266_pwm`

Source: `esphome/components/esp8266_pwm/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `esp8266_pwm.h`

**class `ESP8266PWM` — public interface:**
```cpp
void set_pin(InternalGPIOPin *pin) { pin_ = pin; }
void set_frequency(float frequency) { this->frequency_ = frequency; }
void update_frequency(float frequency) override { this->set_frequency(frequency); this->write_state(this->last_output_); }
void setup() override;
void dump_config() override;
float get_setup_priority() const override { return setup_priority::HARDWARE; }
```

**class `SetFrequencyAction` — public interface:**
```cpp
SetFrequencyAction(ESP8266PWM *parent) : parent_(parent) {}
TEMPLATABLE_VALUE(float, frequency);
void play(const Ts &...x) { float freq = this->frequency_.value(x...); this->parent_->update_frequency(freq); }
ESP8266PWM *parent_;
```
