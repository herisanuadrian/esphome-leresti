# ESPHome component: `text`

Source: `esphome/components/text/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `TextStateTrigger` — public interface:**
```cpp
explicit TextStateTrigger(Text *parent) { parent->add_on_state_callback([this](const std::string &value) { this->trigger(value); }); }
```

**class `TextSetAction` — public interface:**
```cpp
explicit TextSetAction(Text *text) : text_(text) {}
TEMPLATABLE_VALUE(std::string, value) void play(const Ts &...x) override { auto call = this->text_->make_call(); call.set_value(this->value_.value(x...)); call.perform(); }
```

## `text.h`

**class `Text` — public interface:**
```cpp
std::string state;
TextTraits traits;
void publish_state(const std::string &state);
void publish_state(const char *state);
void publish_state(const char *state, size_t len);
TextCall make_call() { return TextCall(this); }
template<typename F> void add_on_state_callback(F &&callback) { this->state_callback_.add(std::forward<F>(callback)); }
```

## `text_call.h`

**class `TextCall` — public interface:**
```cpp
explicit TextCall(Text *parent) : parent_(parent) {}
void perform();
TextCall &set_value(const std::string &value);
TextCall &set_value(const char *value, size_t len);
```

## `text_sensor/text_text_sensor.h`

**class `TextTextSensor` — public interface:**
```cpp
explicit TextTextSensor(Text *source) : source_(source) {}
void setup() override;
void dump_config() override;
```

## `text_traits.h`

**Enums:**
```cpp
enum TextMode : uint8_t {
  TEXT_MODE_TEXT = 0,
  TEXT_MODE_PASSWORD = 1,
};
```

**class `TextTraits` — public interface:**
```cpp
void set_min_length(int min_length) { this->min_length_ = min_length; }
int get_min_length() const { return this->min_length_; }
void set_max_length(int max_length) { this->max_length_ = max_length; }
int get_max_length() const { return this->max_length_; }
void set_pattern(const char *pattern) { this->pattern_ = pattern; }
std::string get_pattern() const { return std::string(this->pattern_); }
const char *get_pattern_c_str() const { return this->pattern_; }
StringRef get_pattern_ref() const { return StringRef(this->pattern_); }
void set_mode(TextMode mode) { this->mode_ = mode; }
TextMode get_mode() const { return this->mode_; }
```
