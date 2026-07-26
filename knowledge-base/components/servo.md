# ESPHome component: `servo`

Source: `esphome/components/servo/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `servo.h`

**Enums:**
```cpp
enum State {
    STATE_ATTACHED = 0,
    STATE_DETACHED = 1,
    STATE_TARGET_REACHED = 2,
  };
```

**class `Servo` — public interface:**
```cpp
void set_output(output::FloatOutput *output) { output_ = output; }
void loop() override;
void write(float value);
void internal_write(float value);
void detach();
void setup() override;
void dump_config() override;
void set_min_level(float min_level) { min_level_ = min_level; }
void set_idle_level(float idle_level) { idle_level_ = idle_level; }
void set_max_level(float max_level) { max_level_ = max_level; }
void set_restore(bool restore) { restore_ = restore; }
void set_auto_detach_time(uint32_t auto_detach_time) { auto_detach_time_ = auto_detach_time; }
void set_transition_length(uint32_t transition_length) { transition_length_ = transition_length; }
bool has_reached_target() { return this->current_value_ == this->target_value_; }
```

**class `ServoWriteAction` — public interface:**
```cpp
ServoWriteAction(Servo *servo) : servo_(servo) {}
TEMPLATABLE_VALUE(float, value) void play(const Ts &...x) override { this->servo_->write(this->value_.value(x...)); }
```

**class `ServoDetachAction` — public interface:**
```cpp
ServoDetachAction(Servo *servo) : servo_(servo) {}
void play(const Ts &...x) override { this->servo_->detach(); }
```
