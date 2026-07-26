# ESPHome component: `binary_sensor`

Source: `esphome/components/binary_sensor/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `PressTrigger` — public interface:**
```cpp
explicit PressTrigger(BinarySensor *parent) { parent->add_on_state_callback([this](bool state) { if (state) this->trigger(); }); }
```

**class `ReleaseTrigger` — public interface:**
```cpp
explicit ReleaseTrigger(BinarySensor *parent) { parent->add_on_state_callback([this](bool state) { if (!state) this->trigger(); }); }
```

**class `ClickTrigger` — public interface:**
```cpp
explicit ClickTrigger(BinarySensor *parent, uint32_t min_length, uint32_t max_length) : min_length_(min_length), max_length_(max_length) { parent->add_on_state_callback([this](bool state) { if (state) { this->start_time_ = millis(); } else { const uint32_t length = millis() - this->start_time_; if (match_interval(this->min_length_, this->max_length_, length)) this->trigger(); } }); }
```

**class `DoubleClickTrigger` — public interface:**
```cpp
explicit DoubleClickTrigger(BinarySensor *parent, uint32_t min_length, uint32_t max_length) : min_length_(min_length), max_length_(max_length) { parent->add_on_state_callback([this](bool state) { const uint32_t now = millis(); if (state && this->start_time_ != 0 && this->end_time_ != 0) { if (match_interval(this->min_length_, this->max_length_, this->end_time_ - this->start_time_) && match_interval(this->min_length_, this->max_length_, now - this->end_time_)) { this->trigger(); this->start_time_ = 0; this->end_time_ = 0; return; } } this->start_time_ = this->end_time_; this->end_time_ = now; }); }
```

**class `MultiClickTriggerBase` — public interface:**
```cpp
explicit MultiClickTriggerBase(BinarySensor *parent) : parent_(parent) {}
void setup() override { this->last_state_ = this->parent_->get_state_default(false); this->parent_->add_on_state_callback([this](bool state) { this->on_state_(state); }); }
float get_setup_priority() const override { return setup_priority::HARDWARE; }
void set_invalid_cooldown(uint32_t invalid_cooldown) { this->invalid_cooldown_ = invalid_cooldown; }
void cancel();
MultiClickTriggerBase(const MultiClickTriggerBase &) = delete;
MultiClickTriggerBase &operator=(const MultiClickTriggerBase &) = delete;
```

**class `MultiClickTrigger` — public interface:**
```cpp
MultiClickTrigger(BinarySensor *parent, std::initializer_list<MultiClickTriggerEvent> timing) : MultiClickTriggerBase(parent) { init_array_from(this->timing_storage_, timing); this->timing_ = this->timing_storage_.data(); this->timing_count_ = N; }
```

**class `StateTrigger` — public interface:**
```cpp
explicit StateTrigger(BinarySensor *parent) { parent->add_on_state_callback([this](bool state) { this->trigger(state); }); }
```

**class `StateChangeTrigger` — public interface:**
```cpp
explicit StateChangeTrigger(BinarySensor *parent) { parent->add_full_state_callback( [this](optional<bool> old_state, optional<bool> state) { this->trigger(old_state, state); }); }
```

**class `BinarySensorCondition` — public interface:**
```cpp
BinarySensorCondition(BinarySensor *parent, bool state) : parent_(parent), state_(state) {}
bool check(const Ts &...x) override { return this->parent_->state == this->state_; }
```

**class `BinarySensorPublishAction` — public interface:**
```cpp
explicit BinarySensorPublishAction(BinarySensor *sensor) : sensor_(sensor) {}
TEMPLATABLE_VALUE(bool, state) void play(const Ts &...x) override { auto val = this->state_.value(x...); this->sensor_->publish_state(val); }
```

**class `BinarySensorInvalidateAction` — public interface:**
```cpp
explicit BinarySensorInvalidateAction(BinarySensor *sensor) : sensor_(sensor) {}
void play(const Ts &...x) override { this->sensor_->invalidate_state(); }
```

## `binary_sensor.h`

**class `BinarySensor` — public interface:**
```cpp
explicit BinarySensor() = default;
const bool &get_state() const override { return this->state; }
void set_trigger_on_initial_state(bool value) { this->trigger_on_initial_state_ = value; }
void publish_state(bool new_state);
void publish_initial_state(bool new_state);
#ifdef USE_BINARY_SENSOR_FILTER void add_filter(Filter *filter);
void add_filters(std::initializer_list<Filter *> filters);
#endif void send_state_internal(bool new_state) { if (this->flags_.has_state && this->state == new_state) return; this->set_new_state(new_state); }
virtual bool is_status_binary_sensor() const;
bool state{}
```

**class `BinarySensorInitiallyOff` — public interface:**
```cpp
BinarySensorInitiallyOff() { this->set_has_state(true); }
```

## `filter.h`

**class `Filter` — public interface:**
```cpp
virtual optional<bool> new_value(bool value) = 0;
virtual void input(bool value);
void output(bool value);
```

**class `TimeoutFilter` — public interface:**
```cpp
optional<bool> new_value(bool value) override { return value; }
void input(bool value) override;
template<typename T> void set_timeout_value(T timeout) { this->timeout_delay_ = timeout; }
```

**class `DelayedOnOffFilter` — public interface:**
```cpp
optional<bool> new_value(bool value) override;
template<typename T> void set_on_delay(T delay) { this->on_delay_ = delay; }
template<typename T> void set_off_delay(T delay) { this->off_delay_ = delay; }
```

**class `DelayedOnFilter` — public interface:**
```cpp
optional<bool> new_value(bool value) override;
template<typename T> void set_delay(T delay) { this->delay_ = delay; }
```

**class `DelayedOffFilter` — public interface:**
```cpp
optional<bool> new_value(bool value) override;
template<typename T> void set_delay(T delay) { this->delay_ = delay; }
```

**class `InvertFilter` — public interface:**
```cpp
optional<bool> new_value(bool value) override;
```

**class `AutorepeatFilterBase` — public interface:**
```cpp
optional<bool> new_value(bool value) override;
AutorepeatFilterBase(const AutorepeatFilterBase &) = delete;
AutorepeatFilterBase &operator=(const AutorepeatFilterBase &) = delete;
```

**class `AutorepeatFilter` — public interface:**
```cpp
explicit AutorepeatFilter(std::initializer_list<AutorepeatFilterTiming> timings) { init_array_from(this->timings_storage_, timings); this->timings_ = this->timings_storage_.data(); this->timings_count_ = N; }
```

**class `LambdaFilter` — public interface:**
```cpp
explicit LambdaFilter(std::function<optional<bool>(bool)> f);
optional<bool> new_value(bool value) override;
```

**class `StatelessLambdaFilter` — public interface:**
```cpp
explicit StatelessLambdaFilter(optional<bool> (*f)(bool)) : f_(f) {}
optional<bool> new_value(bool value) override { return this->f_(value); }
```

**class `SettleFilter` — public interface:**
```cpp
optional<bool> new_value(bool value) override;
template<typename T> void set_delay(T delay) { this->delay_ = delay; }
```
