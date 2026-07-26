# ESPHome component: `number`

Source: `esphome/components/number/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `NumberStateTrigger` — public interface:**
```cpp
explicit NumberStateTrigger(Number *parent) { parent->add_on_state_callback([this](float value) { this->trigger(value); }); }
```

**class `NumberSetAction` — public interface:**
```cpp
NumberSetAction(Number *number) : number_(number) {}
TEMPLATABLE_VALUE(float, value) void play(const Ts &...x) override { auto call = this->number_->make_call(); call.set_value(this->value_.value(x...)); call.perform(); }
```

**class `NumberOperationAction` — public interface:**
```cpp
explicit NumberOperationAction(Number *number) : number_(number) {}
TEMPLATABLE_VALUE(NumberOperation, operation) TEMPLATABLE_VALUE(bool, cycle) void play(const Ts &...x) override { auto call = this->number_->make_call(); call.with_operation(this->operation_.value(x...)); if (this->cycle_.has_value()) { call.with_cycle(this->cycle_.value(x...)); } call.perform(); }
```

**class `ValueRangeTrigger` — public interface:**
```cpp
explicit ValueRangeTrigger(Number *parent) : parent_(parent) {}
template<typename V> void set_min(V min) { this->min_ = min; }
template<typename V> void set_max(V max) { this->max_ = max; }
void setup() override;
float get_setup_priority() const override;
```

**class `NumberInRangeCondition` — public interface:**
```cpp
NumberInRangeCondition(Number *parent) : parent_(parent) {}
void set_min(float min) { this->min_ = min; }
void set_max(float max) { this->max_ = max; }
bool check(const Ts &...x) override { const float state = this->parent_->state; if (std::isnan(this->min_)) { return state <= this->max_; } else if (std::isnan(this->max_)) { return state >= this->min_; } else { return this->min_ <= state && state <= this->max_; } }
```

## `number.h`

**class `Number` — public interface:**
```cpp
float state;
void publish_state(float state);
NumberCall make_call() { return NumberCall(this); }
template<typename F> void add_on_state_callback(F &&callback) { this->state_callback_.add(std::forward<F>(callback)); }
NumberTraits traits;
```

## `number_call.h`

**Enums:**
```cpp
enum NumberOperation : uint8_t {
  NUMBER_OP_NONE,
  NUMBER_OP_SET,
  NUMBER_OP_INCREMENT,
  NUMBER_OP_DECREMENT,
  NUMBER_OP_TO_MIN,
  NUMBER_OP_TO_MAX,
};
```

**class `NumberCall` — public interface:**
```cpp
explicit NumberCall(Number *parent) : parent_(parent) {}
void perform();
NumberCall &set_value(float value);
NumberCall &number_increment(bool cycle);
NumberCall &number_decrement(bool cycle);
NumberCall &number_to_min();
NumberCall &number_to_max();
NumberCall &with_operation(NumberOperation operation);
NumberCall &with_value(float value);
NumberCall &with_cycle(bool cycle);
```

## `number_traits.h`

**Enums:**
```cpp
enum NumberMode : uint8_t {
  NUMBER_MODE_AUTO = 0,
  NUMBER_MODE_BOX = 1,
  NUMBER_MODE_SLIDER = 2,
};
```

**class `NumberTraits` — public interface:**
```cpp
void set_min_value(float min_value) { min_value_ = min_value; }
float get_min_value() const { return min_value_; }
void set_max_value(float max_value) { max_value_ = max_value; }
float get_max_value() const { return max_value_; }
void set_step(float step) { step_ = step; }
float get_step() const { return step_; }
void set_mode(NumberMode mode) { this->mode_ = mode; }
NumberMode get_mode() const { return this->mode_; }
```

## `sensor/number_sensor.h`

**class `NumberSensor` — public interface:**
```cpp
explicit NumberSensor(Number *source) : source_(source) {}
void setup() override;
void dump_config() override;
```
