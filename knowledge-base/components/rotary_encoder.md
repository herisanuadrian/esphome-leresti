# ESPHome component: `rotary_encoder`

Source: `esphome/components/rotary_encoder/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `rotary_encoder.h`

**Enums:**
```cpp
enum RotaryEncoderRestoreMode {
  ROTARY_ENCODER_RESTORE_DEFAULT_ZERO,  
  ROTARY_ENCODER_ALWAYS_ZERO,           
};
enum RotaryEncoderResolution {
  ROTARY_ENCODER_1_PULSE_PER_CYCLE =
      0x4400,  
  ROTARY_ENCODER_2_PULSES_PER_CYCLE = 0x2200,  
  ROTARY_ENCODER_4_PULSES_PER_CYCLE = 0x1100,  
};
```

**class `RotaryEncoderSensor` — public interface:**
```cpp
void set_pin_a(InternalGPIOPin *pin_a) { pin_a_ = pin_a; }
void set_pin_b(InternalGPIOPin *pin_b) { pin_b_ = pin_b; }
void set_restore_mode(RotaryEncoderRestoreMode restore_mode);
void set_resolution(RotaryEncoderResolution mode);
void set_value(int value) { this->store_.counter = value; this->loop(); }
void set_reset_pin(GPIOPin *pin_i) { this->pin_i_ = pin_i; }
void set_min_value(int32_t min_value);
void set_max_value(int32_t max_value);
void set_publish_initial_value(bool publish_initial_value) { publish_initial_value_ = publish_initial_value; }
void setup() override;
void dump_config() override;
void loop() override;
template<typename F> void add_on_clockwise_callback(F &&callback) { this->on_clockwise_callback_.add(std::forward<F>(callback)); }
template<typename F> void add_on_anticlockwise_callback(F &&callback) { this->on_anticlockwise_callback_.add(std::forward<F>(callback)); }
template<typename F> void register_listener(F &&listener) { this->listeners_.add(std::forward<F>(listener)); }
```

**class `RotaryEncoderSetValueAction` — public interface:**
```cpp
RotaryEncoderSetValueAction(RotaryEncoderSensor *encoder) : encoder_(encoder) {}
TEMPLATABLE_VALUE(int, value) void play(const Ts &...x) override { this->encoder_->set_value(this->value_.value(x...)); }
```
