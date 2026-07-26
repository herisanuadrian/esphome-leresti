# ESPHome component: `fan`

Source: `esphome/components/fan/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `TurnOnAction` — public interface:**
```cpp
using ApplyFn = void (*)(FanCall &, const std::remove_cvref_t<Ts> &...);
TurnOnAction(Fan *state, ApplyFn apply) : state_(state), apply_(apply) {}
void play(const Ts &...x) override { auto call = this->state_->turn_on(); this->apply_(call, x...); call.perform(); }
Fan *state_;
ApplyFn apply_;
```

**class `TurnOffAction` — public interface:**
```cpp
explicit TurnOffAction(Fan *state) : state_(state) {}
void play(const Ts &...x) override { this->state_->turn_off().perform(); }
Fan *state_;
```

**class `ToggleAction` — public interface:**
```cpp
explicit ToggleAction(Fan *state) : state_(state) {}
void play(const Ts &...x) override { this->state_->toggle().perform(); }
Fan *state_;
```

**class `CycleSpeedAction` — public interface:**
```cpp
explicit CycleSpeedAction(Fan *state) : state_(state) {}
TEMPLATABLE_VALUE(bool, no_off_cycle) void play(const Ts &...x) override { if (this->state_->get_traits().supported_speed_count()) { if (this->state_->state) { int speed = this->state_->speed + 1; int supported_speed_count = this->state_->get_traits().supported_speed_count(); bool off_speed_cycle = no_off_cycle_.value(x...); if (speed > supported_speed_count && off_speed_cycle) { speed = 1; auto call = this->state_->turn_off(); call.set_speed(speed); call.perform(); } else if (speed > supported_speed_count && !off_speed_cycle) { auto call = this->state_->turn_on(); call.set_speed(1); call.perform(); } else { auto call = this->state_->turn_on(); call.set_speed(speed); call.perform(); } } else { auto call = this->state_->turn_on(); call.set_speed(1); call.perform(); } } else { this->state_->toggle().perform(); } }
Fan *state_;
```

**class `FanIsOnCondition` — public interface:**
```cpp
explicit FanIsOnCondition(Fan *state) : state_(state) {}
bool check(const Ts &...x) override { return this->state_->state; }
```

**class `FanIsOffCondition` — public interface:**
```cpp
explicit FanIsOffCondition(Fan *state) : state_(state) {}
bool check(const Ts &...x) override { return !this->state_->state; }
```

**class `FanStateTrigger` — public interface:**
```cpp
FanStateTrigger(Fan *state) : fan_(state) { state->add_on_state_callback([this]() { this->trigger(this->fan_); }); }
```

**class `FanTurnOnTrigger` — public interface:**
```cpp
FanTurnOnTrigger(Fan *state) : fan_(state) { state->add_on_state_callback([this]() { auto is_on = this->fan_->state; auto should_trigger = is_on && !this->last_on_; this->last_on_ = is_on; if (should_trigger) { this->trigger(); } }); this->last_on_ = state->state; }
```

**class `FanTurnOffTrigger` — public interface:**
```cpp
FanTurnOffTrigger(Fan *state) : fan_(state) { state->add_on_state_callback([this]() { auto is_on = this->fan_->state; auto should_trigger = !is_on && this->last_on_; this->last_on_ = is_on; if (should_trigger) { this->trigger(); } }); this->last_on_ = state->state; }
```

**class `FanDirectionSetTrigger` — public interface:**
```cpp
FanDirectionSetTrigger(Fan *state) : fan_(state) { state->add_on_state_callback([this]() { auto direction = this->fan_->direction; auto should_trigger = direction != this->last_direction_; this->last_direction_ = direction; if (should_trigger) { this->trigger(direction); } }); this->last_direction_ = state->direction; }
```

**class `FanOscillatingSetTrigger` — public interface:**
```cpp
FanOscillatingSetTrigger(Fan *state) : fan_(state) { state->add_on_state_callback([this]() { auto oscillating = this->fan_->oscillating; auto should_trigger = oscillating != this->last_oscillating_; this->last_oscillating_ = oscillating; if (should_trigger) { this->trigger(oscillating); } }); this->last_oscillating_ = state->oscillating; }
```

**class `FanSpeedSetTrigger` — public interface:**
```cpp
FanSpeedSetTrigger(Fan *state) : fan_(state) { state->add_on_state_callback([this]() { auto speed = this->fan_->speed; auto should_trigger = speed != this->last_speed_; this->last_speed_ = speed; if (should_trigger) { this->trigger(speed); } }); this->last_speed_ = state->speed; }
```

**class `FanPresetSetTrigger` — public interface:**
```cpp
FanPresetSetTrigger(Fan *state) : fan_(state) { state->add_on_state_callback([this]() { auto preset_mode = this->fan_->get_preset_mode(); auto should_trigger = preset_mode != this->last_preset_mode_; this->last_preset_mode_ = preset_mode; if (should_trigger) { this->trigger(preset_mode); } }); this->last_preset_mode_ = state->get_preset_mode(); }
```

## `fan.h`

**Enums:**
```cpp
enum class FanDirection { FORWARD = 0, REVERSE = 1 };
enum class FanRestoreMode {
  NO_RESTORE,
  ALWAYS_OFF,
  ALWAYS_ON,
  RESTORE_DEFAULT_OFF,
  RESTORE_DEFAULT_ON,
  RESTORE_INVERTED_DEFAULT_OFF,
  RESTORE_INVERTED_DEFAULT_ON,
};
```

**class `FanCall` — public interface:**
```cpp
explicit FanCall(Fan &parent) : parent_(parent) {}
FanCall &set_state(bool binary_state) { this->binary_state_ = binary_state; return *this; }
FanCall &set_state(optional<bool> binary_state) { this->binary_state_ = binary_state; return *this; }
optional<bool> get_state() const { return this->binary_state_; }
FanCall &set_oscillating(bool oscillating) { this->oscillating_ = oscillating; return *this; }
FanCall &set_oscillating(optional<bool> oscillating) { this->oscillating_ = oscillating; return *this; }
optional<bool> get_oscillating() const { return this->oscillating_; }
FanCall &set_speed(int speed) { this->speed_ = speed; return *this; }
optional<int> get_speed() const { return this->speed_; }
FanCall &set_direction(FanDirection direction) { this->direction_ = direction; return *this; }
FanCall &set_direction(optional<FanDirection> direction) { this->direction_ = direction; return *this; }
optional<FanDirection> get_direction() const { return this->direction_; }
FanCall &set_preset_mode(const std::string &preset_mode);
FanCall &set_preset_mode(const char *preset_mode);
FanCall &set_preset_mode(const char *preset_mode, size_t len);
const char *get_preset_mode() const { return this->preset_mode_; }
bool has_preset_mode() const { return this->preset_mode_ != nullptr; }
void perform();
```

**class `Fan` — public interface:**
```cpp
bool state{false}
bool oscillating{false}
int speed{0}
FanDirection direction{FanDirection::FORWARD}
FanCall turn_on();
FanCall turn_off();
FanCall toggle();
FanCall make_call();
template<typename F> void add_on_state_callback(F &&callback) { this->state_callback_.add(std::forward<F>(callback)); }
void publish_state();
virtual FanTraits get_traits() = 0;
void set_supported_preset_modes(std::initializer_list<const char *> preset_modes) { this->ensure_preset_modes_().assign(preset_modes.begin(), preset_modes.end()); }
void set_supported_preset_modes(const std::vector<const char *> &preset_modes) { this->ensure_preset_modes_() = preset_modes; }
void set_restore_mode(FanRestoreMode restore_mode) { this->restore_mode_ = restore_mode; }
StringRef get_preset_mode() const { return StringRef::from_maybe_nullptr(this->preset_mode_); }
bool has_preset_mode() const { return this->preset_mode_ != nullptr; }
```

## `fan_traits.h`

**class `FanTraits` — public interface:**
```cpp
FanTraits() = default;
FanTraits(bool oscillation, bool speed, bool direction, int speed_count) : oscillation_(oscillation), speed_(speed), direction_(direction), speed_count_(speed_count) {}
bool supports_oscillation() const { return this->oscillation_; }
void set_oscillation(bool oscillation) { this->oscillation_ = oscillation; }
bool supports_speed() const { return this->speed_; }
void set_speed(bool speed) { this->speed_ = speed; }
int supported_speed_count() const { return this->speed_count_; }
void set_supported_speed_count(int speed_count) { this->speed_count_ = speed_count; }
bool supports_direction() const { return this->direction_; }
void set_direction(bool direction) { this->direction_ = direction; }
const std::vector<const char *> &supported_preset_modes() const;
ESPDEPRECATED("Call set_supported_preset_modes() on the Fan entity instead. Removed in 2026.11.0", "2026.5.0") void set_supported_preset_modes(std::initializer_list<const char *> preset_modes) { this->compat_preset_modes_ = preset_modes; }
ESPDEPRECATED("Call set_supported_preset_modes() on the Fan entity instead. Removed in 2026.11.0", "2026.5.0") void set_supported_preset_modes(const std::vector<const char *> &preset_modes) { this->compat_preset_modes_ = preset_modes; }
void set_supported_preset_modes(const std::vector<std::string> &preset_modes) = delete;
void set_supported_preset_modes(std::initializer_list<std::string> preset_modes) = delete;
bool supports_preset_modes() const { if (this->preset_modes_) { return !this->preset_modes_->empty(); } return !this->compat_preset_modes_.empty(); }
const char *find_preset_mode(const char *preset_mode) const { return this->find_preset_mode(preset_mode, preset_mode ? strlen(preset_mode) : 0); }
const char *find_preset_mode(const char *preset_mode, size_t len) const { if (preset_mode == nullptr || len == 0) { return nullptr; } const auto &modes = this->preset_modes_ ? *this->preset_modes_ : this->compat_preset_modes_; for (const char *mode : modes) { if (strncmp(mode, preset_mode, len) == 0 && mode[len] == '\0') { return mode; } } return nullptr; }
```
