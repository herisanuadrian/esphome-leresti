# ESPHome component: `sensor`

Source: `esphome/components/sensor/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `SensorStateTrigger` — public interface:**
```cpp
explicit SensorStateTrigger(Sensor *parent) { parent->add_on_state_callback([this](float value) { this->trigger(value); }); }
```

**class `SensorRawStateTrigger` — public interface:**
```cpp
explicit SensorRawStateTrigger(Sensor *parent) { parent->add_on_raw_state_callback([this](float value) { this->trigger(value); }); }
```

**class `SensorPublishAction` — public interface:**
```cpp
SensorPublishAction(Sensor *sensor) : sensor_(sensor) {}
TEMPLATABLE_VALUE(float, state) void play(const Ts &...x) override { this->sensor_->publish_state(this->state_.value(x...)); }
```

**class `ValueRangeTrigger` — public interface:**
```cpp
explicit ValueRangeTrigger(Sensor *parent) : parent_(parent) {}
template<typename V> void set_min(V min) { this->min_ = min; }
template<typename V> void set_max(V max) { this->max_ = max; }
void setup() override { this->rtc_ = this->parent_->make_entity_preference<bool>(); bool initial_state; if (this->rtc_.load(&initial_state)) { this->previous_in_range_ = initial_state; } this->parent_->add_on_state_callback([this](float state) { this->on_state_(state); }); }
float get_setup_priority() const override { return setup_priority::HARDWARE; }
```

**class `SensorInRangeCondition` — public interface:**
```cpp
SensorInRangeCondition(Sensor *parent) : parent_(parent) {}
void set_min(float min) { this->min_ = min; }
void set_max(float max) { this->max_ = max; }
bool check(const Ts &...x) override { const float state = this->parent_->state; if (std::isnan(this->min_)) { return state <= this->max_; } else if (std::isnan(this->max_)) { return state >= this->min_; } else { return this->min_ <= state && state <= this->max_; } }
```

## `filter.h`

**class `Filter` — public interface:**
```cpp
virtual optional<float> new_value(float value) = 0;
virtual void initialize(Sensor *parent, Filter *next);
void input(float value);
void output(float value);
```

**class `SlidingWindowFilter` — public interface:**
```cpp
SlidingWindowFilter(uint16_t window_size, uint16_t send_every, uint16_t send_first_at);
optional<float> new_value(float value) final;
```

**class `MinMaxFilter` — public interface:**
```cpp
using SlidingWindowFilter::SlidingWindowFilter;
```

**class `SortedWindowFilter` — public interface:**
```cpp
using SlidingWindowFilter::SlidingWindowFilter;
```

**class `QuantileFilter` — public interface:**
```cpp
explicit QuantileFilter(size_t window_size, size_t send_every, size_t send_first_at, float quantile);
void set_quantile(float quantile) { this->quantile_ = quantile; }
```

**class `MedianFilter` — public interface:**
```cpp
using SortedWindowFilter::SortedWindowFilter;
```

**class `SkipInitialFilter` — public interface:**
```cpp
explicit SkipInitialFilter(size_t num_to_ignore);
optional<float> new_value(float value) override;
```

**class `MinFilter` — public interface:**
```cpp
using MinMaxFilter::MinMaxFilter;
```

**class `MaxFilter` — public interface:**
```cpp
using MinMaxFilter::MinMaxFilter;
```

**class `SlidingWindowMovingAverageFilter` — public interface:**
```cpp
using SlidingWindowFilter::SlidingWindowFilter;
```

**class `ExponentialMovingAverageFilter` — public interface:**
```cpp
ExponentialMovingAverageFilter(float alpha, uint16_t send_every, uint16_t send_first_at);
optional<float> new_value(float value) override;
void set_send_every(uint16_t send_every);
void set_alpha(float alpha);
```

**class `ThrottleAverageFilter` — public interface:**
```cpp
explicit ThrottleAverageFilter(uint32_t time_period);
void initialize(Sensor *parent, Filter *next) override;
optional<float> new_value(float value) override;
```

**class `LambdaFilter` — public interface:**
```cpp
explicit LambdaFilter(lambda_filter_t lambda_filter);
optional<float> new_value(float value) override;
const lambda_filter_t &get_lambda_filter() const;
void set_lambda_filter(const lambda_filter_t &lambda_filter);
```

**class `StatelessLambdaFilter` — public interface:**
```cpp
explicit StatelessLambdaFilter(optional<float> (*lambda_filter)(float)) : lambda_filter_(lambda_filter) {}
optional<float> new_value(float value) override { return this->lambda_filter_(value); }
```

**class `OffsetFilter` — public interface:**
```cpp
explicit OffsetFilter(TemplatableFn<float> offset);
optional<float> new_value(float value) override;
```

**class `MultiplyFilter` — public interface:**
```cpp
explicit MultiplyFilter(TemplatableFn<float> multiplier);
optional<float> new_value(float value) override;
```

**class `FilterOutValueFilter` — public interface:**
```cpp
explicit FilterOutValueFilter(std::initializer_list<TemplatableFn<float>> values_to_filter_out) : ValueListFilter<N>(values_to_filter_out) {}
optional<float> new_value(float value) override { if (this->value_matches_any_(value)) return {}; return value; }
```

**class `ThrottleFilter` — public interface:**
```cpp
explicit ThrottleFilter(uint32_t min_time_between_inputs);
optional<float> new_value(float value) override;
```

**class `ThrottleWithPriorityFilter` — public interface:**
```cpp
explicit ThrottleWithPriorityFilter(uint32_t min_time_between_inputs, std::initializer_list<TemplatableFn<float>> prioritized_values) : ValueListFilter<N>(prioritized_values), min_time_between_inputs_(min_time_between_inputs) {}
optional<float> new_value(float value) override { return throttle_with_priority_new_value(this->parent_, value, this->values_.data(), N, this->last_input_, this->min_time_between_inputs_); }
```

**class `ThrottleWithPriorityNanFilter` — public interface:**
```cpp
explicit ThrottleWithPriorityNanFilter(uint32_t min_time_between_inputs);
optional<float> new_value(float value) override;
```

**class `TimeoutFilterBase` — public interface:**
```cpp
void loop() override;
float get_setup_priority() const override;
```

**class `TimeoutFilterLast` — public interface:**
```cpp
explicit TimeoutFilterLast(uint32_t time_period) : TimeoutFilterBase(time_period) {}
optional<float> new_value(float value) override;
```

**class `TimeoutFilterConfigured` — public interface:**
```cpp
explicit TimeoutFilterConfigured(uint32_t time_period, const TemplatableFn<float> &new_value) : TimeoutFilterBase(time_period), value_(new_value) {}
optional<float> new_value(float value) override;
```

**class `DebounceFilter` — public interface:**
```cpp
explicit DebounceFilter(uint32_t time_period);
optional<float> new_value(float value) override;
```

**class `HeartbeatFilter` — public interface:**
```cpp
explicit HeartbeatFilter(uint32_t time_period);
void initialize(Sensor *parent, Filter *next) override;
optional<float> new_value(float value) override;
void set_optimistic(bool optimistic) { this->optimistic_ = optimistic; }
```

**class `DeltaFilter` — public interface:**
```cpp
explicit DeltaFilter(float min_a0, float min_a1, float max_a0, float max_a1);
void set_baseline(float (*fn)(float));
optional<float> new_value(float value) override;
```

**class `OrFilter` — public interface:**
```cpp
explicit OrFilter(std::initializer_list<Filter *> filters) { init_array_from(this->filters_, filters); }
void initialize(Sensor *parent, Filter *next) override { Filter::initialize(parent, next); or_filter_initialize(this->filters_.data(), N, parent, &this->phi_); }
optional<float> new_value(float value) override { return or_filter_new_value(this->filters_.data(), N, value, this->has_value_); }
```

**class `PhiNode` — public interface:**
```cpp
PhiNode(OrFilter *or_parent) : or_parent_(or_parent) {}
optional<float> new_value(float value) override { if (!this->or_parent_->has_value_) { this->or_parent_->output(value); this->or_parent_->has_value_ = true; } return {}; }
```

**class `CalibrateLinearFilter` — public interface:**
```cpp
explicit CalibrateLinearFilter(std::initializer_list<std::array<float, 3>> linear_functions) { init_array_from(this->linear_functions_, linear_functions); }
optional<float> new_value(float value) override { return calibrate_linear_compute(this->linear_functions_.data(), N, value); }
```

**class `CalibratePolynomialFilter` — public interface:**
```cpp
explicit CalibratePolynomialFilter(std::initializer_list<float> coefficients) { init_array_from(this->coefficients_, coefficients); }
optional<float> new_value(float value) override { return calibrate_polynomial_compute(this->coefficients_.data(), N, value); }
```

**class `ClampFilter` — public interface:**
```cpp
ClampFilter(float min, float max, bool ignore_out_of_range);
optional<float> new_value(float value) override;
```

**class `RoundFilter` — public interface:**
```cpp
explicit RoundFilter(uint8_t precision);
optional<float> new_value(float value) override;
```

**class `RoundMultipleFilter` — public interface:**
```cpp
explicit RoundMultipleFilter(float multiple);
optional<float> new_value(float value) override;
```

**class `RoundSignificantDigitsFilter` — public interface:**
```cpp
optional<float> new_value(float value) override { if (std::isfinite(value)) { if (value == 0.0f) return 0.0f; float factor = pow10_int(Digits - 1 - ilog10(value)); return roundf(value * factor) / factor; } return value; }
```

**class `ToNTCResistanceFilter` — public interface:**
```cpp
ToNTCResistanceFilter(double a, double b, double c) : a_(a), b_(b), c_(c) {}
optional<float> new_value(float value) override;
```

**class `ToNTCTemperatureFilter` — public interface:**
```cpp
ToNTCTemperatureFilter(double a, double b, double c) : a_(a), b_(b), c_(c) {}
optional<float> new_value(float value) override;
```

**class `StreamingFilter` — public interface:**
```cpp
StreamingFilter(uint16_t window_size, uint16_t send_first_at);
optional<float> new_value(float value) final;
```

**class `StreamingMinFilter` — public interface:**
```cpp
using StreamingFilter::StreamingFilter;
```

**class `StreamingMaxFilter` — public interface:**
```cpp
using StreamingFilter::StreamingFilter;
```

**class `StreamingMovingAverageFilter` — public interface:**
```cpp
using StreamingFilter::StreamingFilter;
```

## `sensor.h`

**Enums:**
```cpp
enum StateClass : uint8_t {
  STATE_CLASS_NONE = 0,
  STATE_CLASS_MEASUREMENT = 1,
  STATE_CLASS_TOTAL_INCREASING = 2,
  STATE_CLASS_TOTAL = 3,
  STATE_CLASS_MEASUREMENT_ANGLE = 4
};
```

**Constants:**
```cpp
constexpr uint8_t STATE_CLASS_LAST = static_cast<uint8_t>(STATE_CLASS_MEASUREMENT_ANGLE);
```

**class `Sensor` — public interface:**
```cpp
explicit Sensor();
int8_t get_accuracy_decimals();
void set_accuracy_decimals(int8_t accuracy_decimals);
bool has_accuracy_decimals() const { return this->sensor_flags_.has_accuracy_override; }
StateClass get_state_class();
void set_state_class(StateClass state_class);
bool get_force_update() const { return sensor_flags_.force_update; }
void set_force_update(bool force_update) { sensor_flags_.force_update = force_update; }
#ifdef USE_SENSOR_FILTER void add_filter(Filter *filter);
void add_filters(std::initializer_list<Filter *> filters);
void set_filters(std::initializer_list<Filter *> filters);
void clear_filters();
#endif float get_state() const { return this->state; }
float get_raw_state() const { #pragma GCC diagnostic push #pragma GCC diagnostic ignored "-Wdeprecated-declarations" return this->raw_state; #pragma GCC diagnostic pop }
void publish_state(float state);
template<typename F> void add_on_state_callback(F &&callback) { this->callback_.add(std::forward<F>(callback)); }
template<typename F> void add_on_raw_state_callback(F &&callback) { #ifdef USE_SENSOR_FILTER this->raw_callback_.add(std::forward<F>(callback)); #else this->callback_.add(std::forward<F>(callback)); #endif }
float state;
#pragma GCC diagnostic push #pragma GCC diagnostic ignored "-Wdeprecated-declarations" ESPDEPRECATED("Use get_raw_state() instead of .raw_state. Will be removed in 2026.10.0", "2026.4.0") float raw_state;
#pragma GCC diagnostic pop void internal_send_state_to_frontend(float state);
```
