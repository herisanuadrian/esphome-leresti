# ESPHome component: `lvgl`

Source: `esphome/components/lvgl/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `animation.h`

**Enums:**
```cpp
enum class AnimationState {
  STOPPED,
  STARTED,
  RUNNING,
};
```

**class `LvAnimationTiming` — public interface:**
```cpp
virtual float map_progress(float value) = 0;
```

**class `LvAnimationTimingRoundTrip` — public interface:**
```cpp
float map_progress(float value) override { value *= 2.0f; if (value > 1.0f) return 2.0f - value; return value; }
```

**class `LvAnimationTimingGravity` — public interface:**
```cpp
LvAnimationTimingGravity(float acceleration, float bounce) : acceleration_(acceleration), bounce_(bounce) {}
float map_progress(float value) override { if (value == 0.0f) { this->initial_position_ = 0.0f; this->initial_speed_ = 0.0f; this->initial_time_ = 0.0f; } auto position = this->calc_pos_(value); if (position > 1.0f) { auto initial_time = this->calc_end_time_(); this->initial_speed_ = -this->calc_speed_(initial_time) * this->bounce_; this->initial_position_ = 1.0f; this->initial_time_ = initial_time; position = calc_pos_(value); if (position > 1.0f) { position = 1.0f; } } return position; }
```

**class `LvAnimationTimingEaseInOut` — public interface:**
```cpp
LvAnimationTimingEaseInOut(float slope) : slope_(slope) {}
float map_progress(float value) override { float sqr = value * value; sqr = sqr / (2.0f * (sqr - value) + 1.0f); return this->slope_ * sqr + (1.0 - this->slope_) * value; }
```

**class `LvAnimation` — public interface:**
```cpp
LvAnimation(void (*update_callback)(const lv_coord_t *data), std::vector<TemplatableValue<lv_coord_t>> from, std::vector<TemplatableValue<lv_coord_t>> to) : update_callback_(update_callback) { std::copy(from.begin(), from.end(), this->from_); std::copy(to.begin(), to.end(), this->to_); }
void start() { if (this->state_ > AnimationState::STOPPED) this->stop(); if (this->duration_ == 0) return; for (size_t i = 0; i != DATA_SIZE; i++) { this->data_from_[i] = this->from_[i].value(); this->data_to_[i] = this->to_[i].value(); } this->start_time_ = millis(); this->state_ = AnimationState::STARTED; this->loop(); this->start_callback_.call(); }
void stop() { if (this->state_ == AnimationState::STOPPED) return; this->state_ = AnimationState::STOPPED; this->stop_callback_.call(); }
void setup() override { if constexpr (AUTO_START) this->start(); }
void loop() override { if (this->state_ == AnimationState::STOPPED) return; uint32_t elapsed = millis() - this->start_time_; float progress = static_cast<float>(elapsed) / static_cast<float>(this->duration_); switch (this->state_) { case AnimationState::STARTED: if (elapsed < this->start_delay_) return; this->state_ = AnimationState::RUNNING; this->start_time_ = millis(); progress = 0.0f; break; case AnimationState::RUNNING: if (progress >= 1.0f) { progress = 1.0f; this->stop(); if (this->loop_) this->start(); } break; default: return; } for (auto *timing : this->timings_) { progress = timing->map_progress(progress); } lv_coord_t data[DATA_SIZE]; for (size_t i = 0; i != DATA_SIZE; i++) { data[i] = static_cast<lv_coord_t>( roundf(this->data_from_[i] + static_cast<lv_coord_t>(this->data_to_[i] - this->data_from_[i]) * progress)); } this->update_callback_(data); }
float get_setup_priority() const override { return setup_priority::PROCESSOR - 20.0; }
void set_duration(uint32_t duration) { this->duration_ = duration; }
void set_start_delay(uint32_t start_delay) { this->start_delay_ = start_delay; }
void add_timing(LvAnimationTiming *timing) { this->timings_.push_back(timing); }
void set_loop(bool loop) { this->loop_ = loop; }
template<typename F> void add_on_start_callback(F &&callback) { this->start_callback_.add(std::forward<F>(callback)); }
template<typename F> void add_on_stop_callback(F &&callback) { this->stop_callback_.add(std::forward<F>(callback)); }
```

## `light/lvgl_light.h`

**class `LVLight` — public interface:**
```cpp
light::LightTraits get_traits() override { auto traits = light::LightTraits(); traits.set_supported_color_modes({light::ColorMode::RGB}); return traits; }
void write_state(light::LightState *state) override { float red, green, blue; state->current_values_as_rgb(&red, &green, &blue); auto color = lv_color_make(red * 255, green * 255, blue * 255); if (this->obj_ != nullptr) { this->set_value_(color); } else { this->initial_value_ = color; } }
void set_obj(lv_obj_t *obj) { this->obj_ = obj; if (this->initial_value_) { lv_led_set_color(obj, this->initial_value_.value()); lv_led_on(obj); this->initial_value_.reset(); } }
```

## `lvgl_esphome.h`

**Enums:**
```cpp
enum RotationType : uint8_t {
  ROTATION_UNUSED,
  ROTATION_SOFTWARE,
  ROTATION_HARDWARE,
};
enum class Orientation : uint8_t {
  UNKNOWN,
  LANDSCAPE,
  PORTRAIT,
};
```

**class `LvCompound` — public interface:**
```cpp
virtual ~LvCompound() = default;
virtual void set_obj(lv_obj_t *lv_obj) { this->obj = lv_obj; }
lv_obj_t *obj{}
```

**class `LvPageType` — public interface:**
```cpp
LvPageType(bool skip) : skip(skip) {}
void setup(size_t index) { this->index = index; this->obj = lv_obj_create(nullptr); }
bool is_showing() const;
lv_obj_t *obj{}
size_t index{}
bool skip;
```

**class `LvLambdaComponent` — public interface:**
```cpp
LvLambdaComponent(void (*callback)()) : callback_(callback) {}
void setup() override { this->callback_(); }
float get_setup_priority() const override { return setup_priority::PROCESSOR - 5; }
```

**class `ObjUpdateAction` — public interface:**
```cpp
explicit ObjUpdateAction(std::function<void(Ts...)> &&lamb) : lamb_(std::move(lamb)) {}
```

**class `LvglComponent` — public interface:**
```cpp
LvglComponent(std::vector<display::Display *> displays, float buffer_frac, bool full_refresh, int draw_rounding, bool resume_on_input, bool update_when_display_idle, RotationType rotation_type);
static void static_flush_cb(lv_display_t *disp_drv, const lv_area_t *area, uint8_t *color_p);
static lv_point_t get_touch_relative_to_obj(lv_obj_t *obj);
float get_setup_priority() const override { return setup_priority::PROCESSOR; }
void setup() override;
void update() override;
void loop() override;
template<typename F> void add_on_idle_callback(F &&callback) { this->idle_callbacks_.add(std::forward<F>(callback)); }
static void render_end_cb(lv_event_t *event);
static void render_start_cb(lv_event_t *event);
void dump_config() override;
lv_display_t *get_disp() { return this->disp_; }
lv_obj_t *get_screen_active() { return lv_display_get_screen_active(this->disp_); }
void set_paused(bool paused, bool show_snow);
void set_refresh_interval(uint32_t period) { this->refr_timer_period_ = period; if (this->refr_timer_ != nullptr) lv_timer_set_period(this->refr_timer_, period); }
bool is_paused() const { return this->paused_; }
void maybe_wakeup() { if (this->paused_ && this->resume_on_input_) { this->set_paused(false, false); } }
static void esphome_lvgl_init();
static void add_event_cb(lv_obj_t *obj, event_callback_t callback, lv_event_code_t event);
static void add_event_cb(lv_obj_t *obj, event_callback_t callback, lv_event_code_t event1, lv_event_code_t event2);
static void add_event_cb(lv_obj_t *obj, event_callback_t callback, lv_event_code_t event1, lv_event_code_t event2, lv_event_code_t event3);
static void lv_obj_set_state_value(lv_obj_t *obj, lv_state_t state, bool value) { if (value != lv_obj_has_state(obj, state)) { if (value) { lv_obj_add_state(obj, state); } else { lv_obj_remove_state(obj, state); } if (state == LV_STATE_CHECKED) lv_obj_send_event(obj, lv_update_event, nullptr); } }
#ifdef USE_LVGL_BUTTONMATRIX static void lv_buttonmatrix_set_button_ctrl_value(lv_obj_t *obj, uint32_t index, lv_buttonmatrix_ctrl_t ctrl, bool value) { if (value != lv_buttonmatrix_has_button_ctrl(obj, index, ctrl)) { if (value) { lv_buttonmatrix_set_button_ctrl(obj, index, ctrl); } else { lv_buttonmatrix_clear_button_ctrl(obj, index, ctrl); } if (ctrl == LV_BUTTONMATRIX_CTRL_CHECKED) lv_obj_send_event(obj, lv_update_event, nullptr); } }
#endif void add_page(LvPageType *page);
void show_page(size_t index, lv_screen_load_anim_t anim, uint32_t time);
void show_next_page(lv_screen_load_anim_t anim, uint32_t time);
void show_prev_page(lv_screen_load_anim_t anim, uint32_t time);
void set_page_wrap(bool wrap) { this->page_wrap_ = wrap; }
void set_big_endian(bool big_endian) { this->big_endian_ = big_endian; }
size_t get_current_page() const;
void set_focus_mark(lv_group_t *group) { this->focus_marks_[group] = lv_group_get_focused(group); }
void restore_focus_mark(lv_group_t *group) { auto *mark = this->focus_marks_[group]; if (mark != nullptr) { lv_group_focus_obj(mark); } }
size_t draw_rounding{2}
void set_pause_trigger(Trigger<> *trigger) { this->pause_callback_ = trigger; }
void set_resume_trigger(Trigger<> *trigger) { this->resume_callback_ = trigger; }
void set_draw_start_trigger(Trigger<> *trigger) { this->draw_start_callback_ = trigger; }
void set_draw_end_trigger(Trigger<> *trigger) { this->draw_end_callback_ = trigger; }
void set_landscape_trigger(Trigger<> *trigger) { this->landscape_callback_ = trigger; }
void set_portrait_trigger(Trigger<> *trigger) { this->portrait_callback_ = trigger; }
void set_rotation(display::DisplayRotation rotation);
void set_rotation(int angle);
display::DisplayRotation get_rotation() const { return this->rotation_; }
void rotate_coordinates(int32_t &x, int32_t &y) const;
uint16_t get_width() const { return lv_display_get_horizontal_resolution(this->disp_); }
uint16_t get_height() const { return lv_display_get_vertical_resolution(this->disp_); }
```

**class `IdleTrigger` — public interface:**
```cpp
explicit IdleTrigger(LvglComponent *parent, TemplatableFn<uint32_t> timeout);
```

**class `LvglAction` — public interface:**
```cpp
explicit LvglAction(std::function<void(LvglComponent *)> &&lamb) : action_(std::move(lamb)) {}
```

**class `LvglCondition` — public interface:**
```cpp
LvglCondition(std::function<bool(Tc *)> &&condition_lambda) : condition_lambda_(std::move(condition_lambda)) {}
bool check(const Ts &...x) override { return this->condition_lambda_(this->parent_); }
```

**class `LVTouchListener` — public interface:**
```cpp
LVTouchListener(uint16_t long_press_time, uint16_t long_press_repeat_time, LvglComponent *parent);
void update(const touchscreen::TouchPoints_t &tpoints) override;
void release() override { touch_pressed_ = false; this->parent_->maybe_wakeup(); }
lv_indev_t *get_drv() { return this->drv_; }
```

**class `IndicatorLine` — public interface:**
```cpp
IndicatorLine() = default;
void set_obj(lv_obj_t *lv_obj) override;
void set_value(int value);
```

**class `LVEncoderListener` — public interface:**
```cpp
LVEncoderListener(lv_indev_type_t type, uint16_t long_press_time, uint16_t long_press_repeat_time);
#ifdef USE_BINARY_SENSOR void add_button(binary_sensor::BinarySensor *button, lv_key_t key) { button->add_on_state_callback([this, key](bool state) { this->event(key, state); }); }
#endif #ifdef USE_LVGL_ROTARY_ENCODER void set_sensor(rotary_encoder::RotaryEncoderSensor *sensor) { sensor->register_listener([this](int32_t count) { this->set_count(count); }); }
#endif void event(int key, bool pressed) { if (!this->parent_->is_paused()) { this->pressed_ = pressed; this->key_ = key; } else if (!pressed) { this->parent_->maybe_wakeup(); } }
void set_count(int32_t count) { if (!this->parent_->is_paused()) { this->count_ = count; } else { this->parent_->maybe_wakeup(); } }
lv_indev_t *get_drv() { return this->drv_; }
```

**class `LvLineType` — public interface:**
```cpp
void set_points(FixedVector<lv_point_precise_t> points) { this->points_ = std::move(points); lv_line_set_points(this->obj, this->points_.begin(), this->points_.size()); }
```

**class `LvSelectable` — public interface:**
```cpp
virtual size_t get_selected_index() = 0;
virtual void set_selected_index(size_t index, lv_anim_enable_t anim) = 0;
void set_selected_text(const std::string &text, lv_anim_enable_t anim);
std::string get_selected_text();
const std::vector<std::string> &get_options() { return this->options_; }
void set_options(std::vector<std::string> options);
```

**class `LvDropdownType` — public interface:**
```cpp
size_t get_selected_index() override { return lv_dropdown_get_selected(this->obj); }
void set_selected_index(size_t index, lv_anim_enable_t anim) override { lv_dropdown_set_selected(this->obj, index); }
```

**class `LvRollerType` — public interface:**
```cpp
size_t get_selected_index() override { return lv_roller_get_selected(this->obj); }
void set_selected_index(size_t index, lv_anim_enable_t anim) override { lv_roller_set_selected(this->obj, index, anim); }
void set_mode(lv_roller_mode_t mode) { this->mode_ = mode; }
```

**class `LvButtonMatrixType` — public interface:**
```cpp
void set_obj(lv_obj_t *lv_obj) override;
uint16_t get_selected() { return lv_buttonmatrix_get_selected_button(this->obj); }
void set_key(size_t idx, uint8_t key) { this->key_map_[idx] = key; }
```

**class `LvKeyboardType` — public interface:**
```cpp
void set_obj(lv_obj_t *lv_obj) override;
```

## `number/lvgl_number.h`

**class `LVGLNumber` — public interface:**
```cpp
LVGLNumber(std::function<void(float)> control_lambda, std::function<float()> value_lambda, bool restore) : control_lambda_(std::move(control_lambda)), value_lambda_(std::move(value_lambda)), restore_(restore) {}
void setup() override { float value = this->value_lambda_(); if (this->restore_) { this->pref_ = this->make_entity_preference<float>(); if (this->pref_.load(&value)) { this->control_lambda_(value); } } this->publish_state(value); }
void on_value() { this->publish_(this->value_lambda_()); }
```

## `select/lvgl_select.h`

**class `LVGLSelect` — public interface:**
```cpp
LVGLSelect(LvSelectable *widget, lv_anim_enable_t anim, bool restore) : widget_(widget), anim_(anim), restore_(restore) {}
void setup() override { this->set_options_(); if (this->restore_) { size_t index; this->pref_ = this->make_entity_preference<size_t>(); if (this->pref_.load(&index)) this->widget_->set_selected_index(index, LV_ANIM_OFF); } this->publish(); lv_obj_add_event_cb( this->widget_->obj, [](lv_event_t *e) { auto *it = static_cast<LVGLSelect *>(lv_event_get_user_data(e)); it->set_options_(); }, LV_EVENT_REFRESH, this); auto lamb = [](lv_event_t *e) { auto *self = static_cast<LVGLSelect *>(lv_event_get_user_data(e)); self->publish(); }; lv_obj_add_event_cb(this->widget_->obj, lamb, LV_EVENT_VALUE_CHANGED, this); lv_obj_add_event_cb(this->widget_->obj, lamb, lv_update_event, this); }
void publish() { auto index = this->widget_->get_selected_index(); this->publish_state(index); if (this->restore_) { this->pref_.save(&index); } }
```

## `switch/lvgl_switch.h`

**class `LVGLSwitch` — public interface:**
```cpp
LVGLSwitch(std::function<void(bool)> state_lambda) : state_lambda_(std::move(state_lambda)) {}
void setup() override { this->write_state(this->get_initial_state_with_restore_mode().value_or(false)); }
```

## `text/lvgl_text.h`

**class `LVGLText` — public interface:**
```cpp
void set_control_lambda(const std::function<void(std::string)> &control_lambda) { this->control_lambda_ = control_lambda; if (this->initial_state_.has_value()) { this->control_lambda_(this->initial_state_.value()); this->initial_state_.reset(); } }
```
