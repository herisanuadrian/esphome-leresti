# ESPHome component: `switch`

Source: `esphome/components/switch/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `TurnOnAction` — public interface:**
```cpp
explicit TurnOnAction(Switch *a_switch) : switch_(a_switch) {}
void play(const Ts &...x) override { this->switch_->turn_on(); }
```

**class `TurnOffAction` — public interface:**
```cpp
explicit TurnOffAction(Switch *a_switch) : switch_(a_switch) {}
void play(const Ts &...x) override { this->switch_->turn_off(); }
```

**class `ToggleAction` — public interface:**
```cpp
explicit ToggleAction(Switch *a_switch) : switch_(a_switch) {}
void play(const Ts &...x) override { this->switch_->toggle(); }
```

**class `ControlAction` — public interface:**
```cpp
explicit ControlAction(Switch *a_switch) : switch_(a_switch) {}
TEMPLATABLE_VALUE(bool, state) void play(const Ts &...x) override { auto state = this->state_.optional_value(x...); if (state.has_value()) { this->switch_->control(*state); } }
```

**class `SwitchCondition` — public interface:**
```cpp
SwitchCondition(Switch *parent, bool state) : parent_(parent), state_(state) {}
bool check(const Ts &...x) override { return this->parent_->state == this->state_; }
```

**class `SwitchStateTrigger` — public interface:**
```cpp
SwitchStateTrigger(Switch *a_switch) { a_switch->add_on_state_callback([this](bool state) { this->trigger(state); }); }
```

**class `SwitchTurnOnTrigger` — public interface:**
```cpp
SwitchTurnOnTrigger(Switch *a_switch) { a_switch->add_on_state_callback([this](bool state) { if (state) { this->trigger(); } }); }
```

**class `SwitchTurnOffTrigger` — public interface:**
```cpp
SwitchTurnOffTrigger(Switch *a_switch) { a_switch->add_on_state_callback([this](bool state) { if (!state) { this->trigger(); } }); }
```

**class `SwitchPublishAction` — public interface:**
```cpp
SwitchPublishAction(Switch *a_switch) : switch_(a_switch) {}
TEMPLATABLE_VALUE(bool, state) void play(const Ts &...x) override { this->switch_->publish_state(this->state_.value(x...)); }
```

## `binary_sensor/switch_binary_sensor.h`

**class `SwitchBinarySensor` — public interface:**
```cpp
void set_source(Switch *source) { source_ = source; }
void setup() override;
void dump_config() override;
```

## `switch.h`

**Enums:**
```cpp
enum SwitchRestoreMode : uint8_t {
  SWITCH_ALWAYS_OFF = !RESTORE_MODE_ON_MASK,
  SWITCH_ALWAYS_ON = RESTORE_MODE_ON_MASK,
  SWITCH_RESTORE_DEFAULT_OFF = RESTORE_MODE_PERSISTENT_MASK,
  SWITCH_RESTORE_DEFAULT_ON = RESTORE_MODE_PERSISTENT_MASK | RESTORE_MODE_ON_MASK,
  SWITCH_RESTORE_INVERTED_DEFAULT_OFF = RESTORE_MODE_PERSISTENT_MASK | RESTORE_MODE_INVERTED_MASK,
  SWITCH_RESTORE_INVERTED_DEFAULT_ON = RESTORE_MODE_PERSISTENT_MASK | RESTORE_MODE_INVERTED_MASK | RESTORE_MODE_ON_MASK,
  SWITCH_RESTORE_DISABLED = RESTORE_MODE_DISABLED_MASK,
};
```

**Constants:**
```cpp
constexpr int RESTORE_MODE_ON_MASK = 0x01;
constexpr int RESTORE_MODE_PERSISTENT_MASK = 0x02;
constexpr int RESTORE_MODE_INVERTED_MASK = 0x04;
constexpr int RESTORE_MODE_DISABLED_MASK = 0x08;
```

**class `Switch` — public interface:**
```cpp
explicit Switch();
void publish_state(bool state);
SwitchRestoreMode restore_mode{SWITCH_RESTORE_DEFAULT_OFF}
bool state;
void control(bool target_state);
void turn_on();
void turn_off();
void toggle();
void set_inverted(bool inverted);
template<typename F> void add_on_state_callback(F &&callback) { this->state_callback_.add(std::forward<F>(callback)); }
optional<bool> get_initial_state();
optional<bool> get_initial_state_with_restore_mode();
virtual bool assumed_state();
bool is_inverted() const;
void set_restore_mode(SwitchRestoreMode restore_mode) { this->restore_mode = restore_mode; }
```
