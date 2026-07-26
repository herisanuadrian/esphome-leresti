# ESPHome component: `template`

Source: `esphome/components/template/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `alarm_control_panel/template_alarm_control_panel.h`

**Enums:**
```cpp
enum BinarySensorFlags : uint8_t {
  BINARY_SENSOR_MODE_NORMAL = 1 << 0,
  BINARY_SENSOR_MODE_BYPASS_ARMED_HOME = 1 << 1,
  BINARY_SENSOR_MODE_BYPASS_ARMED_NIGHT = 1 << 2,
  BINARY_SENSOR_MODE_CHIME = 1 << 3,
  BINARY_SENSOR_MODE_BYPASS_AUTO = 1 << 4,
};
enum AlarmSensorType : uint8_t {
  ALARM_SENSOR_TYPE_DELAYED = 0,
  ALARM_SENSOR_TYPE_INSTANT,
  ALARM_SENSOR_TYPE_DELAYED_FOLLOWER,
  ALARM_SENSOR_TYPE_INSTANT_ALWAYS,
};
enum TemplateAlarmControlPanelRestoreMode {
  ALARM_CONTROL_PANEL_ALWAYS_DISARMED,
  ALARM_CONTROL_PANEL_RESTORE_DEFAULT_DISARMED,
};
```

**class `TemplateAlarmControlPanel` — public interface:**
```cpp
TemplateAlarmControlPanel();
void dump_config() override;
void setup() override;
void loop() override;
uint32_t get_supported_features() const override;
bool get_requires_code() const override { return !this->codes_.empty(); }
bool get_requires_code_to_arm() const override { return this->requires_code_to_arm_; }
bool get_all_sensors_ready() { return this->sensors_ready_; }
void set_restore_mode(TemplateAlarmControlPanelRestoreMode restore_mode) { this->restore_mode_ = restore_mode; }
ESPDEPRECATED("bypass_before_arming() is deprecated and will be removed in 2026.10.0", "2026.4.0") void bypass_before_arming() { this->auto_bypass_sensors_(); }
#ifdef USE_BINARY_SENSOR void init_sensors(size_t capacity) { this->sensors_.init(capacity); }
void add_sensor(binary_sensor::BinarySensor *sensor, uint8_t flags = 0, AlarmSensorType type = ALARM_SENSOR_TYPE_DELAYED);
#endif void set_codes(std::initializer_list<const char *> codes) { this->codes_ = codes; }
void set_codes(std::initializer_list<std::string> codes) = delete;
void set_requires_code_to_arm(bool code_to_arm) { this->requires_code_to_arm_ = code_to_arm; }
void set_arming_away_time(uint32_t time) { this->arming_away_time_ = time; }
void set_arming_home_time(uint32_t time) { this->arming_home_time_ = time; }
void set_arming_night_time(uint32_t time) { this->arming_night_time_ = time; }
void set_pending_time(uint32_t time) { this->pending_time_ = time; }
void set_trigger_time(uint32_t time) { this->trigger_time_ = time; }
void set_supports_arm_home(bool supports_arm_home) { supports_arm_home_ = supports_arm_home; }
void set_supports_arm_night(bool supports_arm_night) { supports_arm_night_ = supports_arm_night; }
```

## `binary_sensor/template_binary_sensor.h`

**class `TemplateBinarySensor` — public interface:**
```cpp
template<typename F> void set_template(F &&f) { this->f_.set(std::forward<F>(f)); }
void setup() override;
void loop() override;
void dump_config() override;
float get_setup_priority() const override { return setup_priority::HARDWARE; }
```

## `button/template_button.h`

**class `TemplateButton` — public interface:**
```cpp
void press_action() override{}
```

## `cover/template_cover.h`

**Enums:**
```cpp
enum TemplateCoverRestoreMode {
  COVER_NO_RESTORE,
  COVER_RESTORE,
  COVER_RESTORE_AND_CALL,
};
```

**class `TemplateCover` — public interface:**
```cpp
TemplateCover();
template<typename F> void set_state_lambda(F &&f) { this->state_f_.set(std::forward<F>(f)); }
template<typename F> void set_tilt_lambda(F &&f) { this->tilt_f_.set(std::forward<F>(f)); }
Trigger<> *get_open_trigger();
Trigger<> *get_close_trigger();
Trigger<> *get_stop_trigger();
Trigger<> *get_toggle_trigger();
Trigger<float> *get_position_trigger();
Trigger<float> *get_tilt_trigger();
void set_optimistic(bool optimistic);
void set_assumed_state(bool assumed_state);
void set_has_stop(bool has_stop);
void set_has_position(bool has_position);
void set_has_tilt(bool has_tilt);
void set_has_toggle(bool has_toggle);
void set_restore_mode(TemplateCoverRestoreMode restore_mode) { restore_mode_ = restore_mode; }
void setup() override;
void loop() override;
void dump_config() override;
float get_setup_priority() const override;
```

## `datetime/template_date.h`

**class `TemplateDate` — public interface:**
```cpp
template<typename F> void set_template(F &&f) { this->f_.set(std::forward<F>(f)); }
void setup() override;
void update() override;
void dump_config() override;
float get_setup_priority() const override { return setup_priority::HARDWARE; }
Trigger<ESPTime> *get_set_trigger() { return &this->set_trigger_; }
void set_optimistic(bool optimistic) { this->optimistic_ = optimistic; }
void set_initial_value(ESPTime initial_value) { this->initial_value_ = initial_value; }
void set_restore_value(bool restore_value) { this->restore_value_ = restore_value; }
```

## `datetime/template_datetime.h`

**class `TemplateDateTime` — public interface:**
```cpp
template<typename F> void set_template(F &&f) { this->f_.set(std::forward<F>(f)); }
void setup() override;
void update() override;
void dump_config() override;
float get_setup_priority() const override { return setup_priority::HARDWARE; }
Trigger<ESPTime> *get_set_trigger() { return &this->set_trigger_; }
void set_optimistic(bool optimistic) { this->optimistic_ = optimistic; }
void set_initial_value(ESPTime initial_value) { this->initial_value_ = initial_value; }
void set_restore_value(bool restore_value) { this->restore_value_ = restore_value; }
```

## `datetime/template_time.h`

**class `TemplateTime` — public interface:**
```cpp
template<typename F> void set_template(F &&f) { this->f_.set(std::forward<F>(f)); }
void setup() override;
void update() override;
void dump_config() override;
float get_setup_priority() const override { return setup_priority::HARDWARE; }
Trigger<ESPTime> *get_set_trigger() { return &this->set_trigger_; }
void set_optimistic(bool optimistic) { this->optimistic_ = optimistic; }
void set_initial_value(ESPTime initial_value) { this->initial_value_ = initial_value; }
void set_restore_value(bool restore_value) { this->restore_value_ = restore_value; }
```

## `event/template_event.h`

## `fan/template_fan.h`

**class `TemplateFan` — public interface:**
```cpp
TemplateFan() {}
void setup() override;
void dump_config() override;
void set_has_direction(bool has_direction) { this->has_direction_ = has_direction; }
void set_has_oscillating(bool has_oscillating) { this->has_oscillating_ = has_oscillating; }
void set_speed_count(int count) { this->speed_count_ = count; }
void set_preset_modes(std::initializer_list<const char *> presets) { this->set_supported_preset_modes(presets); }
fan::FanTraits get_traits() override { this->wire_preset_modes_(this->traits_); return this->traits_; }
```

## `lock/automation.h`

**class `TemplateLockPublishAction` — public interface:**
```cpp
TEMPLATABLE_VALUE(lock::LockState, state) void play(const Ts &...x) override { this->parent_->publish_state(this->state_.value(x...)); }
```

## `lock/template_lock.h`

**class `TemplateLock` — public interface:**
```cpp
TemplateLock();
void setup() override;
void dump_config() override;
template<typename F> void set_state_lambda(F &&f) { this->f_.set(std::forward<F>(f)); }
Trigger<> *get_lock_trigger() { return &this->lock_trigger_; }
Trigger<> *get_unlock_trigger() { return &this->unlock_trigger_; }
Trigger<> *get_open_trigger() { return &this->open_trigger_; }
void set_optimistic(bool optimistic);
void loop() override;
float get_setup_priority() const override;
```

## `number/template_number.h`

**class `TemplateNumber` — public interface:**
```cpp
template<typename F> void set_template(F &&f) { this->f_.set(std::forward<F>(f)); }
void setup() override;
void update() override;
void dump_config() override;
float get_setup_priority() const override { return setup_priority::HARDWARE; }
Trigger<float> *get_set_trigger() { return &this->set_trigger_; }
void set_optimistic(bool optimistic) { optimistic_ = optimistic; }
void set_initial_value(float initial_value) { initial_value_ = initial_value; }
void set_restore_value(bool restore_value) { this->restore_value_ = restore_value; }
```

## `output/template_output.h`

**class `TemplateBinaryOutput` — public interface:**
```cpp
Trigger<bool> *get_trigger() { return &this->trigger_; }
```

**class `TemplateFloatOutput` — public interface:**
```cpp
Trigger<float> *get_trigger() { return &this->trigger_; }
```

## `select/template_select.h`

**class `TemplateSelect` — public interface:**
```cpp
template<typename F> void set_lambda(F &&f) { if constexpr (HAS_LAMBDA) { this->f_.set(std::forward<F>(f)); } }
void setup() override { if constexpr (!HAS_LAMBDA) { if constexpr (RESTORE_VALUE) { this->pref_ = this->template make_entity_preference<size_t>(); setup_with_restore(this, this->pref_, INITIAL_OPTION_INDEX); } else { setup_initial(this, INITIAL_OPTION_INDEX); } } }
void update() override { if constexpr (HAS_LAMBDA) { update_lambda(this, this->f_()); } }
void dump_config() override { dump_config_helper(this, OPTIMISTIC, HAS_LAMBDA, INITIAL_OPTION_INDEX, RESTORE_VALUE); }
float get_setup_priority() const override { return setup_priority::HARDWARE; }
```

**class `TemplateSelectWithSetAction` — public interface:**
```cpp
Trigger<StringRef> *get_set_trigger() { return &this->set_trigger_; }
```

## `sensor/template_sensor.h`

**class `TemplateSensor` — public interface:**
```cpp
template<typename F> void set_template(F &&f) { this->f_.set(std::forward<F>(f)); }
void update() override;
void dump_config() override;
float get_setup_priority() const override;
```

## `switch/template_switch.h`

**class `TemplateSwitch` — public interface:**
```cpp
TemplateSwitch();
void setup() override;
void dump_config() override;
template<typename F> void set_state_lambda(F &&f) { this->f_.set(std::forward<F>(f)); }
Trigger<> *get_turn_on_trigger();
Trigger<> *get_turn_off_trigger();
void set_optimistic(bool optimistic);
void set_assumed_state(bool assumed_state);
void loop() override;
float get_setup_priority() const override;
```

## `text/template_text.h`

**class `TemplateTextSaverBase` — public interface:**
```cpp
virtual bool save(const std::string &value) { return true; }
virtual void setup(uint32_t id, std::string &value) {}
```

**class `TextSaver` — public interface:**
```cpp
bool save(const std::string &value) override { if (value == this->prev_) { return true; } int size = value.size(); if (size > SZ) { return false; } unsigned char temp[SZ + 1]; memcpy(temp + 1, value.c_str(), size); temp[0] = ((unsigned char) size); this->pref_.save(&temp); this->prev_.assign(value); return true; }
void setup(uint32_t id, std::string &value) override { this->pref_ = global_preferences->make_preference<uint8_t[SZ + 1]>(id); char temp[SZ + 1]; bool hasdata = this->pref_.load(&temp); if (hasdata) { size_t len = static_cast<uint8_t>(temp[0]); if (len > SZ) { len = SZ; } value.assign(temp + 1, len); } this->prev_.assign(value); }
```

**class `TemplateText` — public interface:**
```cpp
template<typename F> void set_template(F &&f) { this->f_.set(std::forward<F>(f)); }
void setup() override;
void update() override;
void dump_config() override;
float get_setup_priority() const override { return setup_priority::HARDWARE; }
Trigger<std::string> *get_set_trigger() { return &this->set_trigger_; }
void set_optimistic(bool optimistic) { this->optimistic_ = optimistic; }
void set_initial_value(const char *initial_value) { this->initial_value_ = initial_value; }
void set_initial_value(const std::string &initial_value) = delete;
void set_value_saver(TemplateTextSaverBase *restore_value_saver) { this->pref_ = restore_value_saver; }
```

## `text_sensor/template_text_sensor.h`

**class `TemplateTextSensor` — public interface:**
```cpp
template<typename F> void set_template(F &&f) { this->f_.set(std::forward<F>(f)); }
void update() override;
float get_setup_priority() const override;
void dump_config() override;
```

## `valve/automation.h`

## `valve/template_valve.h`

**Enums:**
```cpp
enum TemplateValveRestoreMode {
  VALVE_NO_RESTORE,
  VALVE_RESTORE,
  VALVE_RESTORE_AND_CALL,
};
```

**class `TemplateValve` — public interface:**
```cpp
TemplateValve();
template<typename F> void set_state_lambda(F &&f) { this->state_f_.set(std::forward<F>(f)); }
Trigger<> *get_open_trigger();
Trigger<> *get_close_trigger();
Trigger<> *get_stop_trigger();
Trigger<> *get_toggle_trigger();
Trigger<float> *get_position_trigger();
void set_optimistic(bool optimistic);
void set_assumed_state(bool assumed_state);
void set_has_stop(bool has_stop);
void set_has_position(bool has_position);
void set_has_toggle(bool has_toggle);
void set_restore_mode(TemplateValveRestoreMode restore_mode) { restore_mode_ = restore_mode; }
void setup() override;
void loop() override;
void dump_config() override;
float get_setup_priority() const override;
```

## `water_heater/automation.h`

**class `TemplateWaterHeaterPublishAction` — public interface:**
```cpp
TEMPLATABLE_VALUE(float, current_temperature) TEMPLATABLE_VALUE(float, target_temperature) TEMPLATABLE_VALUE(water_heater::WaterHeaterMode, mode) TEMPLATABLE_VALUE(bool, away) TEMPLATABLE_VALUE(bool, is_on) void play(const Ts &...x) override { if (this->current_temperature_.has_value()) { this->parent_->set_current_temperature(this->current_temperature_.value(x...)); } bool needs_call = this->target_temperature_.has_value() || this->mode_.has_value() || this->away_.has_value() || this->is_on_.has_value(); if (needs_call) { auto call = this->parent_->make_call(); if (this->target_temperature_.has_value()) { call.set_target_temperature(this->target_temperature_.value(x...)); } if (this->mode_.has_value()) { call.set_mode(this->mode_.value(x...)); } if (this->away_.has_value()) { call.set_away(this->away_.value(x...)); } if (this->is_on_.has_value()) { call.set_on(this->is_on_.value(x...)); } call.perform(); } else { this->parent_->publish_state(); } }
```

## `water_heater/template_water_heater.h`

**Enums:**
```cpp
enum TemplateWaterHeaterRestoreMode {
  WATER_HEATER_NO_RESTORE,
  WATER_HEATER_RESTORE,
  WATER_HEATER_RESTORE_AND_CALL,
};
```

**class `TemplateWaterHeater` — public interface:**
```cpp
TemplateWaterHeater();
template<typename F> void set_current_temperature_lambda(F &&f) { this->current_temperature_f_.set(std::forward<F>(f)); }
template<typename F> void set_target_temperature_lambda(F &&f) { this->target_temperature_f_.set(std::forward<F>(f)); }
template<typename F> void set_mode_lambda(F &&f) { this->mode_f_.set(std::forward<F>(f)); }
template<typename F> void set_away_lambda(F &&f) { this->away_f_.set(std::forward<F>(f)); }
template<typename F> void set_is_on_lambda(F &&f) { this->is_on_f_.set(std::forward<F>(f)); }
void set_optimistic(bool optimistic) { this->optimistic_ = optimistic; }
void set_restore_mode(TemplateWaterHeaterRestoreMode restore_mode) { this->restore_mode_ = restore_mode; }
void set_supported_modes(const std::initializer_list<water_heater::WaterHeaterMode> &modes) { this->supported_modes_ = modes; }
Trigger<> *get_set_trigger() { return &this->set_trigger_; }
void setup() override;
void loop() override;
void dump_config() override;
float get_setup_priority() const override;
water_heater::WaterHeaterCallInternal make_call() override;
```
