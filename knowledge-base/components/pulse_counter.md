# ESPHome component: `pulse_counter`

Source: `esphome/components/pulse_counter/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `SetTotalPulsesAction` — public interface:**
```cpp
SetTotalPulsesAction(PulseCounterSensor *pulse_counter) : pulse_counter_(pulse_counter) {}
TEMPLATABLE_VALUE(uint32_t, total_pulses) void play(const Ts &...x) override { this->pulse_counter_->set_total_pulses(this->total_pulses_.value(x...)); }
```

## `pulse_counter_sensor.h`

**Enums:**
```cpp
enum PulseCounterCountMode {
  PULSE_COUNTER_DISABLE = 0,
  PULSE_COUNTER_INCREMENT,
  PULSE_COUNTER_DECREMENT,
};
```

**class `PulseCounterSensor` — public interface:**
```cpp
explicit PulseCounterSensor(bool hw_pcnt = false) : storage_(*get_storage(hw_pcnt)) {}
void set_pin(InternalGPIOPin *pin) { pin_ = pin; }
void set_rising_edge_mode(PulseCounterCountMode mode) { storage_.rising_edge_mode = mode; }
void set_falling_edge_mode(PulseCounterCountMode mode) { storage_.falling_edge_mode = mode; }
void set_filter_us(uint32_t filter) { storage_.filter_us = filter; }
void set_total_sensor(sensor::Sensor *total_sensor) { total_sensor_ = total_sensor; }
void set_total_pulses(uint32_t pulses);
void setup() override;
void update() override;
void dump_config() override;
```
