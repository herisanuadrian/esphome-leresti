# ESPHome component: `text_sensor`

Source: `esphome/components/text_sensor/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `TextSensorStateTrigger` — public interface:**
```cpp
explicit TextSensorStateTrigger(TextSensor *parent) { parent->add_on_state_callback([this](const std::string &value) { this->trigger(value); }); }
```

**class `TextSensorStateRawTrigger` — public interface:**
```cpp
explicit TextSensorStateRawTrigger(TextSensor *parent) { parent->add_on_raw_state_callback([this](const std::string &value) { this->trigger(value); }); }
```

**class `TextSensorStateCondition` — public interface:**
```cpp
explicit TextSensorStateCondition(TextSensor *parent) : parent_(parent) {}
TEMPLATABLE_VALUE(std::string, state) bool check(const Ts &...x) override { return this->parent_->state == this->state_.value(x...); }
```

**class `TextSensorPublishAction` — public interface:**
```cpp
TextSensorPublishAction(TextSensor *sensor) : sensor_(sensor) {}
TEMPLATABLE_VALUE(std::string, state) void play(const Ts &...x) override { this->sensor_->publish_state(this->state_.value(x...)); }
```

## `filter.h`

**class `Filter` — public interface:**
```cpp
virtual bool new_value(std::string &value) = 0;
virtual void initialize(TextSensor *parent, Filter *next);
void input(std::string value);
void output(std::string &value);
```

**class `LambdaFilter` — public interface:**
```cpp
explicit LambdaFilter(lambda_filter_t lambda_filter);
bool new_value(std::string &value) override;
const lambda_filter_t &get_lambda_filter() const;
void set_lambda_filter(const lambda_filter_t &lambda_filter);
```

**class `StatelessLambdaFilter` — public interface:**
```cpp
explicit StatelessLambdaFilter(optional<std::string> (*lambda_filter)(std::string)) : lambda_filter_(lambda_filter) {}
bool new_value(std::string &value) override { auto result = this->lambda_filter_(value); if (result.has_value()) { value = std::move(*result); return true; } return false; }
```

**class `ToUpperFilter` — public interface:**
```cpp
bool new_value(std::string &value) override;
```

**class `ToLowerFilter` — public interface:**
```cpp
bool new_value(std::string &value) override;
```

**class `AppendFilter` — public interface:**
```cpp
explicit AppendFilter(const char *suffix) : suffix_(suffix) {}
bool new_value(std::string &value) override;
```

**class `PrependFilter` — public interface:**
```cpp
explicit PrependFilter(const char *prefix) : prefix_(prefix) {}
bool new_value(std::string &value) override;
```

**class `SubstituteFilter` — public interface:**
```cpp
explicit SubstituteFilter(const std::initializer_list<Substitution> &substitutions) { init_array_from(this->substitutions_, substitutions); }
bool new_value(std::string &value) override { return substitute_filter_apply(this->substitutions_.data(), N, value); }
```

**class `MapFilter` — public interface:**
```cpp
explicit MapFilter(const std::initializer_list<Substitution> &mappings) { init_array_from(this->mappings_, mappings); }
bool new_value(std::string &value) override { return map_filter_apply(this->mappings_.data(), N, value); }
```

## `text_sensor.h`

**class `TextSensor` — public interface:**
```cpp
std::string state;
TextSensor() = default;
~TextSensor() = default;
const std::string &get_state() const;
const std::string &get_raw_state() const;
void publish_state(const std::string &state);
void publish_state(const char *state);
void publish_state(const char *state, size_t len);
#ifdef USE_TEXT_SENSOR_FILTER void add_filter(Filter *filter);
void add_filters(std::initializer_list<Filter *> filters);
void set_filters(std::initializer_list<Filter *> filters);
void clear_filters();
#endif template<typename F> void add_on_state_callback(F &&callback) { this->callback_.add(std::forward<F>(callback)); }
template<typename F> void add_on_raw_state_callback(F &&callback) { #ifdef USE_TEXT_SENSOR_FILTER this->raw_callback_.add(std::forward<F>(callback)); #else this->callback_.add(std::forward<F>(callback)); #endif }
void internal_send_state_to_frontend(const std::string &state);
void internal_send_state_to_frontend(const char *state, size_t len);
```
