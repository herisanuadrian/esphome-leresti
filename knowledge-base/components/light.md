# ESPHome component: `light`

Source: `esphome/components/light/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `addressable_light.h`

**class `AddressableLight` — public interface:**
```cpp
virtual int32_t size() const = 0;
ESPColorView operator[](int32_t index) const { return this->get_view_internal(interpret_index(index, this->size())); }
ESPColorView get(int32_t index) { return this->get_view_internal(interpret_index(index, this->size())); }
virtual void clear_effect_data() = 0;
ESPRangeView range(int32_t from, int32_t to) { from = interpret_index(from, this->size()); to = interpret_index(to, this->size()); return ESPRangeView(this, from, to); }
ESPRangeView all() { return ESPRangeView(this, 0, this->size()); }
ESPRangeIterator begin() { return this->all().begin(); }
ESPRangeIterator end() { return this->all().end(); }
void shift_left(int32_t amnt) { if (amnt < 0) { this->shift_right(-amnt); return; } if (amnt > this->size()) amnt = this->size(); this->range(0, -amnt) = this->range(amnt, this->size()); }
void shift_right(int32_t amnt) { if (amnt < 0) { this->shift_left(-amnt); return; } if (amnt > this->size()) amnt = this->size(); this->range(amnt, this->size()) = this->range(0, -amnt); }
bool is_effect_active() const { return this->effect_active_; }
void set_effect_active(bool effect_active) { this->effect_active_ = effect_active; }
std::unique_ptr<LightTransformer> create_default_transition() override;
void set_correction(float red, float green, float blue, float white = 1.0f) { this->correction_.set_max_brightness( Color(to_uint8_scale(red), to_uint8_scale(green), to_uint8_scale(blue), to_uint8_scale(white))); }
void setup_state(LightState *state) override { #ifdef USE_LIGHT_GAMMA_LUT this->correction_.set_gamma_table(state->get_gamma_table()); #endif this->state_parent_ = state; }
void update_state(LightState *state) override;
void schedule_show() { this->state_parent_->schedule_write_(); }
#ifdef USE_POWER_SUPPLY void set_power_supply(power_supply::PowerSupply *power_supply) { this->power_.set_parent(power_supply); }
#endif void call_setup() override;
```

**class `AddressableLightTransformer` — public interface:**
```cpp
AddressableLightTransformer(AddressableLight &light) : light_(light) {}
void start() override;
optional<LightColorValues> apply() override;
```

## `addressable_light_effect.h`

**class `AddressableLightEffect` — public interface:**
```cpp
explicit AddressableLightEffect(const char *name) : LightEffect(name) {}
void start_internal() override { this->get_addressable_()->set_effect_active(true); this->get_addressable_()->clear_effect_data(); this->start(); }
void stop() override { this->get_addressable_()->set_effect_active(false); }
virtual void apply(AddressableLight &it, const Color &current_color) = 0;
void apply() override { Color current_color = color_from_light_color_values(this->state_->remote_values); this->apply(*this->get_addressable_(), current_color); }
uint32_t get_effect_index() const { return this->get_index(); }
bool is_current_effect() const { return this->is_active() && this->get_addressable_()->is_effect_active(); }
```

**class `AddressableLambdaLightEffect` — public interface:**
```cpp
AddressableLambdaLightEffect(const char *name, void (*f)(AddressableLight &, Color, bool initial_run), uint32_t update_interval) : AddressableLightEffect(name), f_(f), update_interval_(update_interval) {}
void start() override { this->initial_run_ = true; }
void apply(AddressableLight &it, const Color &current_color) override { const uint32_t now = millis(); if (now - this->last_run_ >= this->update_interval_ || this->initial_run_) { this->last_run_ = now; this->f_(it, current_color, this->initial_run_); this->initial_run_ = false; it.schedule_show(); } }
```

**class `AddressableRainbowLightEffect` — public interface:**
```cpp
explicit AddressableRainbowLightEffect(const char *name) : AddressableLightEffect(name) {}
void apply(AddressableLight &it, const Color &current_color) override { ESPHSVColor hsv; hsv.value = 255; hsv.saturation = 240; uint16_t hue = (millis() * this->speed_) % 0xFFFF; const uint16_t add = 0xFFFF / this->width_; for (auto var : it) { hsv.hue = hue >> 8; var = hsv; hue += add; } it.schedule_show(); }
void set_speed(uint32_t speed) { this->speed_ = speed; }
void set_width(uint16_t width) { this->width_ = width; }
```

**class `AddressableColorWipeEffect` — public interface:**
```cpp
explicit AddressableColorWipeEffect(const char *name) : AddressableLightEffect(name) {}
void set_colors(const std::initializer_list<AddressableColorWipeEffectColor> &colors) { this->colors_ = colors; }
void set_add_led_interval(uint32_t add_led_interval) { this->add_led_interval_ = add_led_interval; }
void set_reverse(bool reverse) { this->reverse_ = reverse; }
void apply(AddressableLight &it, const Color &current_color) override { const uint32_t now = millis(); if (now - this->last_add_ < this->add_led_interval_) return; this->last_add_ = now; if (this->reverse_) { it.shift_left(1); } else { it.shift_right(1); } const AddressableColorWipeEffectColor &color = this->colors_[this->at_color_]; Color esp_color = Color(color.r, color.g, color.b, color.w); if (color.gradient) { size_t next_color_index = (this->at_color_ + 1) % this->colors_.size(); const AddressableColorWipeEffectColor &next_color = this->colors_[next_color_index]; const Color next_esp_color = Color(next_color.r, next_color.g, next_color.b, next_color.w); uint8_t gradient = 255 * ((float) this->leds_added_ / color.num_leds); esp_color = esp_color.gradient(next_esp_color, gradient); } if (this->reverse_) { it[-1] = esp_color; } else { it[0] = esp_color; } if (++this->leds_added_ >= color.num_leds) { this->leds_added_ = 0; this->at_color_ = (this->at_color_ + 1) % this->colors_.size(); AddressableColorWipeEffectColor &new_color = this->colors_[this->at_color_]; if (new_color.random) { Color c = Color::random_color(); new_color.r = c.r; new_color.g = c.g; new_color.b = c.b; } } it.schedule_show(); }
```

**class `AddressableScanEffect` — public interface:**
```cpp
explicit AddressableScanEffect(const char *name) : AddressableLightEffect(name) {}
void set_move_interval(uint32_t move_interval) { this->move_interval_ = move_interval; }
void set_scan_width(uint32_t scan_width) { this->scan_width_ = scan_width; }
void apply(AddressableLight &it, const Color &current_color) override { const uint32_t now = millis(); if (now - this->last_move_ < this->move_interval_) return; const auto num_leds = static_cast<uint32_t>(it.size()); if (this->scan_width_ >= num_leds) { it.all() = current_color; it.schedule_show(); this->last_move_ = now; return; } const uint32_t max_pos = num_leds - this->scan_width_; if (this->at_led_ >= max_pos) { this->at_led_ = max_pos; this->direction_ = false; } if (this->direction_) { this->at_led_++; if (this->at_led_ >= max_pos) this->direction_ = false; } else { if (this->at_led_ > 0) this->at_led_--; if (this->at_led_ == 0) this->direction_ = true; } this->last_move_ = now; it.all() = Color::BLACK; for (uint32_t i = 0; i < this->scan_width_; i++) { it[this->at_led_ + i] = current_color; } it.schedule_show(); }
```

**class `AddressableTwinkleEffect` — public interface:**
```cpp
explicit AddressableTwinkleEffect(const char *name) : AddressableLightEffect(name) {}
void apply(AddressableLight &addressable, const Color &current_color) override { const uint32_t now = millis(); uint8_t pos_add = 0; if (now - this->last_progress_ > this->progress_interval_) { const uint32_t pos_add32 = (now - this->last_progress_) / this->progress_interval_; pos_add = pos_add32; this->last_progress_ += pos_add32 * this->progress_interval_; } for (auto view : addressable) { if (view.get_effect_data() != 0) { const uint8_t sine = half_sin8(view.get_effect_data()); view = current_color * sine; const uint8_t new_pos = view.get_effect_data() + pos_add; if (new_pos < view.get_effect_data()) { view.set_effect_data(0); } else { view.set_effect_data(new_pos); } } else { view = Color::BLACK; } } while (random_float() < this->twinkle_probability_) { const size_t pos = random_uint32() % addressable.size(); if (addressable[pos].get_effect_data() != 0) continue; addressable[pos].set_effect_data(1); } addressable.schedule_show(); }
void set_twinkle_probability(float twinkle_probability) { this->twinkle_probability_ = twinkle_probability; }
void set_progress_interval(uint32_t progress_interval) { this->progress_interval_ = progress_interval; }
```

**class `AddressableRandomTwinkleEffect` — public interface:**
```cpp
explicit AddressableRandomTwinkleEffect(const char *name) : AddressableLightEffect(name) {}
void apply(AddressableLight &it, const Color &current_color) override { const uint32_t now = millis(); uint8_t pos_add = 0; if (now - this->last_progress_ > this->progress_interval_) { pos_add = (now - this->last_progress_) / this->progress_interval_; this->last_progress_ = now; } uint8_t subsine = ((8 * (now - this->last_progress_)) / this->progress_interval_) & 0b111; for (auto view : it) { if (view.get_effect_data() != 0) { const uint8_t x = (view.get_effect_data() >> 3) & 0b11111; const uint8_t color = view.get_effect_data() & 0b111; const uint16_t sine = half_sin8((x << 3) | subsine); if (color == 0) { view = current_color * sine; } else { view = Color(((color >> 2) & 1) * sine, ((color >> 1) & 1) * sine, ((color >> 0) & 1) * sine); } const uint8_t new_x = x + pos_add; if (new_x > 0b11111) { view.set_effect_data(0); } else { view.set_effect_data((new_x << 3) | color); } } else { view = Color(0, 0, 0, 0); } } while (random_float() < this->twinkle_probability_) { const size_t pos = random_uint32() % it.size(); if (it[pos].get_effect_data() != 0) continue; const uint8_t color = random_uint32() & 0b111; it[pos].set_effect_data(0b1000 | color); } it.schedule_show(); }
void set_twinkle_probability(float twinkle_probability) { this->twinkle_probability_ = twinkle_probability; }
void set_progress_interval(uint32_t progress_interval) { this->progress_interval_ = progress_interval; }
```

**class `AddressableFireworksEffect` — public interface:**
```cpp
explicit AddressableFireworksEffect(const char *name) : AddressableLightEffect(name) {}
void start() override { auto &it = *this->get_addressable_(); it.all() = Color::BLACK; }
void apply(AddressableLight &it, const Color &current_color) override { const uint32_t now = millis(); if (now - this->last_update_ < this->update_interval_) return; this->last_update_ = now; const uint8_t fade_out_mult = 255u - this->fade_out_rate_; for (auto view : it) { Color target = view.get() * fade_out_mult; if (target.r < 64) target *= 170; view = target; } if (it.size() < 2) return; int last = it.size() - 1; it[0].set(it[0].get() + (it[1].get() * 128)); for (int i = 1; i < last; i++) { it[i] = (it[i - 1].get() * 64) + it[i].get() + (it[i + 1].get() * 64); } it[last] = it[last].get() + (it[last - 1].get() * 128); if (random_float() < this->spark_probability_) { const size_t pos = random_uint32() % it.size(); if (this->use_random_color_) { it[pos] = Color::random_color(); } else { it[pos] = current_color; } } it.schedule_show(); }
void set_update_interval(uint32_t update_interval) { this->update_interval_ = update_interval; }
void set_spark_probability(float spark_probability) { this->spark_probability_ = spark_probability; }
void set_use_random_color(bool random_color) { this->use_random_color_ = random_color; }
void set_fade_out_rate(uint8_t fade_out_rate) { this->fade_out_rate_ = fade_out_rate; }
```

**class `AddressableFlickerEffect` — public interface:**
```cpp
explicit AddressableFlickerEffect(const char *name) : AddressableLightEffect(name) {}
void apply(AddressableLight &it, const Color &current_color) override { const uint32_t now = millis(); const uint8_t intensity = this->intensity_; const uint8_t inv_intensity = 255 - intensity; if (now - this->last_update_ < this->update_interval_) return; this->last_update_ = now; uint32_t rng_state = random_uint32(); for (auto var : it) { rng_state = (rng_state * 0x9E3779B9) + 0x9E37; const uint8_t flicker = (rng_state & 0xFF) % intensity; var = var.get() * (255 - flicker); var = (var.get() * inv_intensity) + (current_color * intensity); } it.schedule_show(); }
void set_update_interval(uint32_t update_interval) { this->update_interval_ = update_interval; }
void set_intensity(float intensity) { this->intensity_ = to_uint8_scale(intensity); }
```

## `addressable_light_wrapper.h`

**class `AddressableLightWrapper` — public interface:**
```cpp
explicit AddressableLightWrapper(light::LightState *light_state) : light_state_(light_state) {}
int32_t size() const override { return 1; }
void clear_effect_data() override { this->wrapper_state_[4] = 0; }
light::LightTraits get_traits() override { LightTraits traits; ColorMode color_mode_precedence[] = {ColorMode::RGB_WHITE, ColorMode::RGB_COLD_WARM_WHITE, ColorMode::RGB_COLOR_TEMPERATURE, ColorMode::RGB, ColorMode::WHITE, ColorMode::COLD_WARM_WHITE, ColorMode::COLOR_TEMPERATURE, ColorMode::BRIGHTNESS, ColorMode::ON_OFF, ColorMode::UNKNOWN}; LightTraits parent_traits = this->light_state_->get_traits(); for (auto cm : color_mode_precedence) { if (parent_traits.supports_color_mode(cm)) { this->color_mode_ = cm; break; } } switch (this->color_mode_) { case ColorMode::RGB_WHITE: case ColorMode::RGB_COLD_WARM_WHITE: case ColorMode::RGB_COLOR_TEMPERATURE: traits.set_supported_color_modes({light::ColorMode::RGB_WHITE}); break; case ColorMode::RGB: traits.set_supported_color_modes({light::ColorMode::RGB}); break; case ColorMode::WHITE: case ColorMode::COLD_WARM_WHITE: case ColorMode::COLOR_TEMPERATURE: case ColorMode::BRIGHTNESS: traits.set_supported_color_modes({light::ColorMode::BRIGHTNESS}); break; case ColorMode::ON_OFF: traits.set_supported_color_modes({light::ColorMode::ON_OFF}); break; default: traits.set_supported_color_modes({light::ColorMode::UNKNOWN}); } return traits; }
void write_state(light::LightState *state) override { if (this->light_state_->remote_values.is_on()) { this->mark_shown_(); return; } float r = this->light_state_->gamma_uncorrect_lut(this->wrapper_state_[0] / 255.0f); float g = this->light_state_->gamma_uncorrect_lut(this->wrapper_state_[1] / 255.0f); float b = this->light_state_->gamma_uncorrect_lut(this->wrapper_state_[2] / 255.0f); float w = this->light_state_->gamma_uncorrect_lut(this->wrapper_state_[3] / 255.0f); auto call = this->light_state_->make_call(); float color_brightness = fmaxf(r, fmaxf(g, b)); float brightness = fmaxf(color_brightness, w); if (brightness == 0.0f) { call.set_state(false); } else { color_brightness /= brightness; w /= brightness; call.set_state(true); call.set_color_mode_if_supported(this->color_mode_); call.set_brightness_if_supported(brightness); call.set_color_brightness_if_supported(color_brightness); call.set_red_if_supported(r); call.set_green_if_supported(g); call.set_blue_if_supported(b); call.set_white_if_supported(w); call.set_warm_white_if_supported(w); call.set_cold_white_if_supported(w); } call.set_transition_length_if_supported(0); call.set_publish(false); call.set_save(false); call.perform(); this->mark_shown_(); }
```

## `automation.h`

**Enums:**
```cpp
enum class LimitMode { CLAMP, DO_NOTHING };
```

**class `ToggleAction` — public interface:**
```cpp
explicit ToggleAction(LightState *state) : state_(state) {}
template<typename V> void set_transition_length(V value) requires(HasTransitionLength) { this->transition_length_ = value; }
void play(const Ts &...x) override { auto call = this->state_->toggle(); if constexpr (HasTransitionLength) { call.set_transition_length(this->transition_length_.optional_value(x...)); } call.perform(); }
```

**class `LightControlAction` — public interface:**
```cpp
using ApplyFn = void (*)(LightState *, LightCall &, const std::remove_cvref_t<Ts> &...);
LightControlAction(LightState *parent, ApplyFn apply) : parent_(parent), apply_(apply) {}
void play(const Ts &...x) override { auto call = this->parent_->make_call(); this->apply_(this->parent_, call, x...); call.perform(); }
```

**class `DimRelativeAction` — public interface:**
```cpp
explicit DimRelativeAction(LightState *parent) : parent_(parent) {}
TEMPLATABLE_VALUE(float, relative_brightness) template<typename V> void set_transition_length(V value) requires(HasTransitionLength) { this->transition_length_ = value; }
void play(const Ts &...x) override { auto call = this->parent_->make_call(); float rel = this->relative_brightness_.value(x...); float cur; this->parent_->remote_values.as_brightness(&cur); if ((limit_mode_ == LimitMode::DO_NOTHING) && ((cur < min_brightness_) || (cur > max_brightness_))) { return; } float new_brightness = clamp(cur + rel, min_brightness_, max_brightness_); call.set_state(new_brightness != 0.0f); call.set_brightness(new_brightness); if constexpr (HasTransitionLength) { call.set_transition_length(this->transition_length_.optional_value(x...)); } call.perform(); }
void set_min_max_brightness(float min, float max) { this->min_brightness_ = min; this->max_brightness_ = max; }
void set_limit_mode(LimitMode limit_mode) { this->limit_mode_ = limit_mode; }
```

**class `LightEffectCycleAction` — public interface:**
```cpp
explicit LightEffectCycleAction(LightState *parent) : parent_(parent) {}
void set_include_none(bool include_none) { this->include_none_ = include_none; }
void play(const Ts &...) override { size_t count = this->parent_->get_effect_count(); if (count == 0) { return; } uint32_t current = this->parent_->get_current_effect_index(); uint32_t next; if (this->include_none_) { uint32_t total = static_cast<uint32_t>(count) + 1; if constexpr (Forward) { next = (current + 1) % total; } else { next = (current + total - 1) % total; } } else { if constexpr (Forward) { next = (current % static_cast<uint32_t>(count)) + 1; } else { next = (current <= 1) ? static_cast<uint32_t>(count) : current - 1; } } auto call = this->parent_->turn_on(); call.set_effect(next); call.perform(); }
```

**class `LightIsOnCondition` — public interface:**
```cpp
explicit LightIsOnCondition(LightState *state) : state_(state) {}
bool check(const Ts &...x) override { return this->state_->current_values.is_on(); }
```

**class `LightIsOffCondition` — public interface:**
```cpp
explicit LightIsOffCondition(LightState *state) : state_(state) {}
bool check(const Ts &...x) override { return !this->state_->current_values.is_on(); }
```

**class `LightTurnOnTrigger` — public interface:**
```cpp
explicit LightTurnOnTrigger(LightState *a_light) : light_(a_light) { a_light->add_remote_values_listener(this); this->last_on_ = a_light->current_values.is_on(); }
void on_light_remote_values_update() override { auto is_on = this->light_->remote_values.is_on(); auto should_trigger = is_on && !this->last_on_; this->last_on_ = is_on; if (should_trigger) { this->trigger(); } }
```

**class `LightTurnOffTrigger` — public interface:**
```cpp
explicit LightTurnOffTrigger(LightState *a_light) : light_(a_light) { a_light->add_target_state_reached_listener(this); }
void on_light_target_state_reached() override { auto is_on = this->light_->current_values.is_on(); if (!is_on) { this->trigger(); } }
```

**class `LightStateTrigger` — public interface:**
```cpp
explicit LightStateTrigger(LightState *a_light) { a_light->add_remote_values_listener(this); }
void on_light_remote_values_update() override { this->trigger(); }
```

**class `AddressableSet` — public interface:**
```cpp
explicit AddressableSet(LightState *parent) : parent_(parent) {}
TEMPLATABLE_VALUE(int32_t, range_from) TEMPLATABLE_VALUE(int32_t, range_to) TEMPLATABLE_VALUE(float, color_brightness) TEMPLATABLE_VALUE(float, red) TEMPLATABLE_VALUE(float, green) TEMPLATABLE_VALUE(float, blue) TEMPLATABLE_VALUE(float, white) void play(const Ts &...x) override { auto *out = (AddressableLight *) this->parent_->get_output(); int32_t range_from = interpret_index(this->range_from_.value_or(x..., 0), out->size()); if (range_from < 0 || range_from >= out->size()) range_from = 0; int32_t range_to = interpret_index(this->range_to_.value_or(x..., out->size() - 1) + 1, out->size()); if (range_to < 0 || range_to >= out->size()) range_to = out->size(); uint8_t color_brightness = to_uint8_scale(this->color_brightness_.value_or(x..., this->parent_->remote_values.get_color_brightness())); auto range = out->range(range_from, range_to); if (this->red_.has_value()) range.set_red(esp_scale8(to_uint8_compat(this->red_.value(x...), "red"), color_brightness)); if (this->green_.has_value()) range.set_green(esp_scale8(to_uint8_compat(this->green_.value(x...), "green"), color_brightness)); if (this->blue_.has_value()) range.set_blue(esp_scale8(to_uint8_compat(this->blue_.value(x...), "blue"), color_brightness)); if (this->white_.has_value()) range.set_white(to_uint8_compat(this->white_.value(x...), "white")); out->schedule_show(); }
```

## `base_light_effects.h`

**class `PulseLightEffect` — public interface:**
```cpp
explicit PulseLightEffect(const char *name) : LightEffect(name) {}
void apply() override { const uint32_t now = millis(); if (now - this->last_color_change_ < this->update_interval_) { return; } auto call = this->state_->turn_on(); float out = this->on_ ? this->max_brightness_ : this->min_brightness_; call.set_brightness_if_supported(out); call.set_transition_length_if_supported(this->on_ ? this->transition_on_length_ : this->transition_off_length_); this->on_ = !this->on_; call.set_publish(false); call.set_save(false); call.perform(); this->last_color_change_ = now; }
void set_transition_on_length(uint32_t transition_length) { this->transition_on_length_ = transition_length; }
void set_transition_off_length(uint32_t transition_length) { this->transition_off_length_ = transition_length; }
void set_update_interval(uint32_t update_interval) { this->update_interval_ = update_interval; }
void set_min_max_brightness(float min, float max) { this->min_brightness_ = min; this->max_brightness_ = max; }
```

**class `RandomLightEffect` — public interface:**
```cpp
explicit RandomLightEffect(const char *name) : LightEffect(name) {}
void apply() override { const uint32_t now = millis(); if (now - this->last_color_change_ < this->update_interval_) { return; } auto color_mode = this->state_->remote_values.get_color_mode(); auto call = this->state_->turn_on(); bool changed = false; if (color_mode & ColorCapability::RGB) { call.set_red(random_float()); call.set_green(random_float()); call.set_blue(random_float()); changed = true; } if (color_mode & ColorCapability::COLOR_TEMPERATURE) { float min = this->state_->get_traits().get_min_mireds(); float max = this->state_->get_traits().get_max_mireds(); call.set_color_temperature(min + random_float() * (max - min)); changed = true; } if (color_mode & ColorCapability::COLD_WARM_WHITE) { call.set_cold_white(random_float()); call.set_warm_white(random_float()); changed = true; } if (!changed) { call.set_brightness(random_float()); } call.set_transition_length_if_supported(this->transition_length_); call.set_publish(true); call.set_save(false); call.perform(); this->last_color_change_ = now; }
void set_transition_length(uint32_t transition_length) { this->transition_length_ = transition_length; }
void set_update_interval(uint32_t update_interval) { this->update_interval_ = update_interval; }
```

**class `LambdaLightEffect` — public interface:**
```cpp
LambdaLightEffect(const char *name, void (*f)(LightState &, bool initial_run), uint32_t update_interval) : LightEffect(name), f_(f), update_interval_(update_interval) {}
void start() override { this->initial_run_ = true; }
void apply() override { const uint32_t now = millis(); if (now - this->last_run_ >= this->update_interval_ || this->initial_run_) { this->last_run_ = now; this->f_(*this->state_, this->initial_run_); this->initial_run_ = false; } }
uint32_t get_current_index() const { return this->get_index(); }
```

**class `AutomationLightEffect` — public interface:**
```cpp
AutomationLightEffect(const char *name) : LightEffect(name) {}
void stop() override { this->trig_.stop_action(); }
void apply() override { if (!this->trig_.is_action_running()) { this->trig_.trigger(); } }
Trigger<> *get_trig() { return &this->trig_; }
uint32_t get_current_index() const { return this->get_index(); }
```

**class `StrobeLightEffect` — public interface:**
```cpp
explicit StrobeLightEffect(const char *name) : LightEffect(name) {}
void apply() override { const uint32_t now = millis(); if (now - this->last_switch_ < this->colors_[this->at_color_].duration) return; this->at_color_ = (this->at_color_ + 1) % this->colors_.size(); auto color = this->colors_[this->at_color_].color; auto call = this->state_->turn_on(); call.from_light_color_values(this->colors_[this->at_color_].color); if (!color.is_on()) { call.set_brightness(0.0f); call.set_state(true); } call.set_publish(false); call.set_save(false); call.set_transition_length_if_supported(this->colors_[this->at_color_].transition_length); call.perform(); this->last_switch_ = now; }
void set_colors(const std::initializer_list<StrobeLightEffectColor> &colors) { this->colors_ = colors; }
```

**class `FlickerLightEffect` — public interface:**
```cpp
explicit FlickerLightEffect(const char *name) : LightEffect(name) {}
void apply() override { LightColorValues remote = this->state_->remote_values; LightColorValues current = this->state_->current_values; LightColorValues out; const float alpha = this->alpha_; const float beta = 1.0f - alpha; out.set_state(true); out.set_brightness(remote.get_brightness() * beta + current.get_brightness() * alpha + (random_cubic_float() * this->intensity_)); out.set_red(remote.get_red() * beta + current.get_red() * alpha + (random_cubic_float() * this->intensity_)); out.set_green(remote.get_green() * beta + current.get_green() * alpha + (random_cubic_float() * this->intensity_)); out.set_blue(remote.get_blue() * beta + current.get_blue() * alpha + (random_cubic_float() * this->intensity_)); out.set_white(remote.get_white() * beta + current.get_white() * alpha + (random_cubic_float() * this->intensity_)); out.set_cold_white(remote.get_cold_white() * beta + current.get_cold_white() * alpha + (random_cubic_float() * this->intensity_)); out.set_warm_white(remote.get_warm_white() * beta + current.get_warm_white() * alpha + (random_cubic_float() * this->intensity_)); auto call = this->state_->make_call(); call.set_publish(false); call.set_save(false); call.set_transition_length_if_supported(0); call.from_light_color_values(out); call.set_state(true); call.perform(); }
void set_alpha(float alpha) { this->alpha_ = alpha; }
void set_intensity(float intensity) { this->intensity_ = intensity; }
```

## `color_mode.h`

**Enums:**
```cpp
enum class ColorCapability : uint8_t {
  ON_OFF = 1 << 0,
  BRIGHTNESS = 1 << 1,
  WHITE = 1 << 2,
  COLOR_TEMPERATURE = 1 << 3,
  COLD_WARM_WHITE = 1 << 4,
  RGB = 1 << 5
};
enum class ColorMode : uint8_t {
  UNKNOWN = 0,
  ON_OFF = (uint8_t) ColorCapability::ON_OFF,
  BRIGHTNESS = (uint8_t) (ColorCapability::ON_OFF | ColorCapability::BRIGHTNESS),
  WHITE = (uint8_t) (ColorCapability::ON_OFF | ColorCapability::BRIGHTNESS | ColorCapability::WHITE),
  COLOR_TEMPERATURE =
      (uint8_t) (ColorCapability::ON_OFF | ColorCapability::BRIGHTNESS | ColorCapability::COLOR_TEMPERATURE),
  COLD_WARM_WHITE =
      (uint8_t) (ColorCapability::ON_OFF | ColorCapability::BRIGHTNESS | ColorCapability::COLD_WARM_WHITE),
  RGB = (uint8_t) (ColorCapability::ON_OFF | ColorCapability::BRIGHTNESS | ColorCapability::RGB),
  RGB_WHITE =
      (uint8_t) (ColorCapability::ON_OFF | ColorCapability::BRIGHTNESS | ColorCapability::RGB | ColorCapability::WHITE),
  RGB_COLOR_TEMPERATURE = (uint8_t) (ColorCapability::ON_OFF | ColorCapability::BRIGHTNESS | ColorCapability::RGB |
                                     ColorCapability::WHITE | ColorCapability::COLOR_TEMPERATURE),
  RGB_COLD_WARM_WHITE = (uint8_t) (ColorCapability::ON_OFF | ColorCapability::BRIGHTNESS | ColorCapability::RGB |
                                   ColorCapability::COLD_WARM_WHITE),
};
```

**Constants:**
```cpp
constexpr int COLOR_CAPABILITY_COUNT = 6;
```

**class `ColorCapabilityHelper` — public interface:**
```cpp
constexpr ColorCapabilityHelper(ColorCapability val) : val_(val) {}
constexpr operator ColorCapability() const { return val_; }
constexpr operator uint8_t() const { return static_cast<uint8_t>(val_); }
constexpr operator bool() const { return static_cast<uint8_t>(val_) != 0; }
```

**class `ColorModeHelper` — public interface:**
```cpp
constexpr ColorModeHelper(ColorMode val) : val_(val) {}
constexpr operator ColorMode() const { return val_; }
constexpr operator uint8_t() const { return static_cast<uint8_t>(val_); }
constexpr operator bool() const { return static_cast<uint8_t>(val_) != 0; }
```

## `esp_color_correction.h`

**class `ESPColorCorrection` — public interface:**
```cpp
void set_max_brightness(const Color &max_brightness) { this->max_brightness_ = max_brightness; }
void set_local_brightness(uint8_t local_brightness) { this->local_brightness_ = local_brightness; }
void set_gamma_table(const uint16_t *table) { this->gamma_table_ = table; }
inline Color color_correct(Color color) const ESPHOME_ALWAYS_INLINE { return Color(this->color_correct_red(color.red), this->color_correct_green(color.green), this->color_correct_blue(color.blue), this->color_correct_white(color.white)); }
inline uint8_t color_correct_red(uint8_t red) const ESPHOME_ALWAYS_INLINE { uint8_t res = esp_scale8_twice(red, this->max_brightness_.red, this->local_brightness_); return this->gamma_correct_(res); }
inline uint8_t color_correct_green(uint8_t green) const ESPHOME_ALWAYS_INLINE { uint8_t res = esp_scale8_twice(green, this->max_brightness_.green, this->local_brightness_); return this->gamma_correct_(res); }
inline uint8_t color_correct_blue(uint8_t blue) const ESPHOME_ALWAYS_INLINE { uint8_t res = esp_scale8_twice(blue, this->max_brightness_.blue, this->local_brightness_); return this->gamma_correct_(res); }
inline uint8_t color_correct_white(uint8_t white) const ESPHOME_ALWAYS_INLINE { uint8_t res = esp_scale8_twice(white, this->max_brightness_.white, this->local_brightness_); return this->gamma_correct_(res); }
Color color_uncorrect(Color color) const;
inline uint8_t color_uncorrect_red(uint8_t red) const ESPHOME_ALWAYS_INLINE { return this->color_uncorrect_channel_(red, this->max_brightness_.red); }
inline uint8_t color_uncorrect_green(uint8_t green) const ESPHOME_ALWAYS_INLINE { return this->color_uncorrect_channel_(green, this->max_brightness_.green); }
inline uint8_t color_uncorrect_blue(uint8_t blue) const ESPHOME_ALWAYS_INLINE { return this->color_uncorrect_channel_(blue, this->max_brightness_.blue); }
inline uint8_t color_uncorrect_white(uint8_t white) const ESPHOME_ALWAYS_INLINE { return this->color_uncorrect_channel_(white, this->max_brightness_.white); }
```

## `esp_color_view.h`

**class `ESPColorSettable` — public interface:**
```cpp
virtual void set(const Color &color) = 0;
virtual void set_red(uint8_t red) = 0;
virtual void set_green(uint8_t green) = 0;
virtual void set_blue(uint8_t blue) = 0;
virtual void set_white(uint8_t white) = 0;
virtual void set_effect_data(uint8_t effect_data) = 0;
virtual void fade_to_white(uint8_t amnt) = 0;
virtual void fade_to_black(uint8_t amnt) = 0;
virtual void lighten(uint8_t delta) = 0;
virtual void darken(uint8_t delta) = 0;
void set(const ESPHSVColor &color) { this->set_hsv(color); }
void set_hsv(const ESPHSVColor &color) { Color rgb = color.to_rgb(); this->set_rgb(rgb.r, rgb.g, rgb.b); }
void set_rgb(uint8_t red, uint8_t green, uint8_t blue) { this->set_red(red); this->set_green(green); this->set_blue(blue); }
void set_rgbw(uint8_t red, uint8_t green, uint8_t blue, uint8_t white) { this->set_rgb(red, green, blue); this->set_white(white); }
```

**class `ESPColorView` — public interface:**
```cpp
ESPColorView(uint8_t *red, uint8_t *green, uint8_t *blue, uint8_t *white, uint8_t *effect_data, const ESPColorCorrection *color_correction) : red_(red), green_(green), blue_(blue), white_(white), effect_data_(effect_data), color_correction_(color_correction) {}
ESPColorView &operator=(const Color &rhs) { this->set(rhs); return *this; }
ESPColorView &operator=(const ESPHSVColor &rhs) { this->set_hsv(rhs); return *this; }
void set(const Color &color) override { this->set_rgbw(color.r, color.g, color.b, color.w); }
void set_red(uint8_t red) override { *this->red_ = this->color_correction_->color_correct_red(red); }
void set_green(uint8_t green) override { *this->green_ = this->color_correction_->color_correct_green(green); }
void set_blue(uint8_t blue) override { *this->blue_ = this->color_correction_->color_correct_blue(blue); }
void set_white(uint8_t white) override { if (this->white_ == nullptr) return; *this->white_ = this->color_correction_->color_correct_white(white); }
void set_effect_data(uint8_t effect_data) override { if (this->effect_data_ == nullptr) return; *this->effect_data_ = effect_data; }
void fade_to_white(uint8_t amnt) override { this->set(this->get().fade_to_white(amnt)); }
void fade_to_black(uint8_t amnt) override { this->set(this->get().fade_to_black(amnt)); }
void lighten(uint8_t delta) override { this->set(this->get().lighten(delta)); }
void darken(uint8_t delta) override { this->set(this->get().darken(delta)); }
Color get() const { return Color(this->get_red(), this->get_green(), this->get_blue(), this->get_white()); }
uint8_t get_red() const { return this->color_correction_->color_uncorrect_red(*this->red_); }
uint8_t get_red_raw() const { return *this->red_; }
uint8_t get_green() const { return this->color_correction_->color_uncorrect_green(*this->green_); }
uint8_t get_green_raw() const { return *this->green_; }
uint8_t get_blue() const { return this->color_correction_->color_uncorrect_blue(*this->blue_); }
uint8_t get_blue_raw() const { return *this->blue_; }
uint8_t get_white() const { if (this->white_ == nullptr) return 0; return this->color_correction_->color_uncorrect_white(*this->white_); }
uint8_t get_white_raw() const { if (this->white_ == nullptr) return 0; return *this->white_; }
uint8_t get_effect_data() const { if (this->effect_data_ == nullptr) return 0; return *this->effect_data_; }
void raw_set_color_correction(const ESPColorCorrection *color_correction) { this->color_correction_ = color_correction; }
```

## `esp_range_view.h`

**class `ESPRangeView` — public interface:**
```cpp
ESPRangeView(AddressableLight *parent, int32_t begin, int32_t end) : parent_(parent), begin_(begin), end_(end < begin ? begin : end) {}
ESPRangeView(const ESPRangeView &) = default;
int32_t size() const { return this->end_ - this->begin_; }
ESPColorView operator[](int32_t index) const;
ESPRangeIterator begin();
ESPRangeIterator end();
void set(const Color &color) override;
void set(const ESPHSVColor &color) { this->set(color.to_rgb()); }
void set_red(uint8_t red) override;
void set_green(uint8_t green) override;
void set_blue(uint8_t blue) override;
void set_white(uint8_t white) override;
void set_effect_data(uint8_t effect_data) override;
void fade_to_white(uint8_t amnt) override;
void fade_to_black(uint8_t amnt) override;
void lighten(uint8_t delta) override;
void darken(uint8_t delta) override;
ESPRangeView &operator=(const Color &rhs) { this->set(rhs); return *this; }
ESPRangeView &operator=(const ESPColorView &rhs) { this->set(rhs.get()); return *this; }
ESPRangeView &operator=(const ESPHSVColor &rhs) { this->set_hsv(rhs); return *this; }
ESPRangeView &operator=(const ESPRangeView &rhs);
```

**class `ESPRangeIterator` — public interface:**
```cpp
ESPRangeIterator(const ESPRangeView &range, int32_t i) : range_(range), i_(i) {}
ESPRangeIterator(const ESPRangeIterator &) = default;
ESPRangeIterator operator++() { this->i_++; return *this; }
bool operator!=(const ESPRangeIterator &other) const { return this->i_ != other.i_; }
ESPColorView operator*() const;
```

## `light_call.h`

**Enums:**
```cpp
enum FieldFlags : uint16_t {
    FLAG_HAS_BRIGHTNESS = 1 << 0,
    FLAG_HAS_COLOR_BRIGHTNESS = 1 << 1,
    FLAG_HAS_RED = 1 << 2,
    FLAG_HAS_GREEN = 1 << 3,
    FLAG_HAS_BLUE = 1 << 4,
    FLAG_HAS_WHITE = 1 << 5,
    FLAG_HAS_COLD_WHITE = 1 << 6,
    FLAG_HAS_WARM_WHITE = 1 << 7,
    FLAG_HAS_COLOR_TEMPERATURE = 1 << 8,
    FLAG_HAS_STATE = 1 << 9,
    FLAG_HAS_TRANSITION = 1 << 10,
    FLAG_HAS_FLASH = 1 << 11,
    FLAG_HAS_EFFECT = 1 << 12,
    FLAG_HAS_COLOR_MODE = 1 << 13,
    FLAG_PUBLISH = 1 << 14,
    FLAG_SAVE = 1 << 15,
  };
```

**class `LightCall` — public interface:**
```cpp
explicit LightCall(LightState *parent) : parent_(parent) {}
LightCall &set_state(optional<bool> state);
LightCall &set_state(bool state);
LightCall &set_transition_length(optional<uint32_t> transition_length);
LightCall &set_transition_length(uint32_t transition_length);
LightCall &set_transition_length_if_supported(uint32_t transition_length);
LightCall &set_flash_length(optional<uint32_t> flash_length);
LightCall &set_flash_length(uint32_t flash_length);
LightCall &set_brightness(optional<float> brightness);
LightCall &set_brightness(float brightness);
LightCall &set_brightness_if_supported(float brightness);
LightCall &set_color_mode(optional<ColorMode> color_mode);
LightCall &set_color_mode(ColorMode color_mode);
LightCall &set_color_mode_if_supported(ColorMode color_mode);
LightCall &set_color_brightness(optional<float> brightness);
LightCall &set_color_brightness(float brightness);
LightCall &set_color_brightness_if_supported(float brightness);
LightCall &set_red(optional<float> red);
LightCall &set_red(float red);
LightCall &set_red_if_supported(float red);
LightCall &set_green(optional<float> green);
LightCall &set_green(float green);
LightCall &set_green_if_supported(float green);
LightCall &set_blue(optional<float> blue);
LightCall &set_blue(float blue);
LightCall &set_blue_if_supported(float blue);
LightCall &set_white(optional<float> white);
LightCall &set_white(float white);
LightCall &set_white_if_supported(float white);
LightCall &set_color_temperature(optional<float> color_temperature);
LightCall &set_color_temperature(float color_temperature);
LightCall &set_color_temperature_if_supported(float color_temperature);
LightCall &set_cold_white(optional<float> cold_white);
LightCall &set_cold_white(float cold_white);
LightCall &set_cold_white_if_supported(float cold_white);
LightCall &set_warm_white(optional<float> warm_white);
LightCall &set_warm_white(float warm_white);
LightCall &set_warm_white_if_supported(float warm_white);
LightCall &set_effect(optional<std::string> effect);
LightCall &set_effect(const std::string &effect) { return this->set_effect(effect.data(), effect.size()); }
LightCall &set_effect(const char *effect) { return this->set_effect(effect, strlen(effect)); }
LightCall &set_effect(const char *effect, size_t len);
LightCall &set_effect(uint32_t effect_number);
LightCall &set_effect(optional<uint32_t> effect_number);
LightCall &set_publish(bool publish);
LightCall &set_save(bool save);
bool has_state() const { return (flags_ & FLAG_HAS_STATE) != 0; }
bool has_brightness() const { return (flags_ & FLAG_HAS_BRIGHTNESS) != 0; }
bool has_color_brightness() const { return (flags_ & FLAG_HAS_COLOR_BRIGHTNESS) != 0; }
bool has_red() const { return (flags_ & FLAG_HAS_RED) != 0; }
bool has_green() const { return (flags_ & FLAG_HAS_GREEN) != 0; }
bool has_blue() const { return (flags_ & FLAG_HAS_BLUE) != 0; }
bool has_white() const { return (flags_ & FLAG_HAS_WHITE) != 0; }
bool has_color_temperature() const { return (flags_ & FLAG_HAS_COLOR_TEMPERATURE) != 0; }
bool has_cold_white() const { return (flags_ & FLAG_HAS_COLD_WHITE) != 0; }
bool has_warm_white() const { return (flags_ & FLAG_HAS_WARM_WHITE) != 0; }
bool has_color_mode() const { return (flags_ & FLAG_HAS_COLOR_MODE) != 0; }
LightCall &set_rgb(float red, float green, float blue);
LightCall &set_rgbw(float red, float green, float blue, float white);
LightCall &from_light_color_values(const LightColorValues &values);
void perform();
```

## `light_color_values.h`

**class `LightColorValues` — public interface:**
```cpp
LightColorValues() : state_(0.0f), brightness_(1.0f), color_brightness_(1.0f), red_(1.0f), green_(1.0f), blue_(1.0f), white_(1.0f), cold_white_{1.0f}
, warm_white_{1.0f}
, color_temperature_{0.0f}
, color_mode_(ColorMode::UNKNOWN) {}
LightColorValues(ColorMode color_mode, float state, float brightness, float color_brightness, float red, float green, float blue, float white, float color_temperature, float cold_white, float warm_white) { this->set_color_mode(color_mode); this->set_state(state); this->set_brightness(brightness); this->set_color_brightness(color_brightness); this->set_red(red); this->set_green(green); this->set_blue(blue); this->set_white(white); this->set_color_temperature(color_temperature); this->set_cold_white(cold_white); this->set_warm_white(warm_white); }
static LightColorValues lerp(const LightColorValues &start, const LightColorValues &end, float completion);
void normalize_color() { if (this->color_mode_ & ColorCapability::RGB) { float max_value = fmaxf(this->red_, fmaxf(this->green_, this->blue_)); if (max_value == 0.0f) { this->red_ = 1.0f; this->green_ = 1.0f; this->blue_ = 1.0f; } else { float inv = 1.0f / max_value; this->red_ *= inv; this->green_ *= inv; this->blue_ *= inv; } } }
void as_binary(bool *binary) const { *binary = this->state_ == 1.0f; }
void as_brightness(float *brightness) const { *brightness = this->state_ * this->brightness_; }
void as_rgb(float *red, float *green, float *blue) const { if (this->color_mode_ & ColorCapability::RGB) { float brightness = this->state_ * this->brightness_ * this->color_brightness_; *red = brightness * this->red_; *green = brightness * this->green_; *blue = brightness * this->blue_; } else { *red = *green = *blue = 0; } }
void as_rgbw(float *red, float *green, float *blue, float *white) const { this->as_rgb(red, green, blue); if (this->color_mode_ & ColorCapability::WHITE) { *white = this->state_ * this->brightness_ * this->white_; } else { *white = 0; } }
void as_rgbww(float *red, float *green, float *blue, float *cold_white, float *warm_white, bool constant_brightness = false) const { this->as_rgb(red, green, blue); this->as_cwww(cold_white, warm_white, constant_brightness); }
void as_rgbct(float color_temperature_cw, float color_temperature_ww, float *red, float *green, float *blue, float *color_temperature, float *white_brightness) const { this->as_rgb(red, green, blue); this->as_ct(color_temperature_cw, color_temperature_ww, color_temperature, white_brightness); }
void as_cwww(float *cold_white, float *warm_white, bool constant_brightness = false) const { if (this->color_mode_ & ColorCapability::COLD_WARM_WHITE) { const float cw_level = this->cold_white_; const float ww_level = this->warm_white_; const float white_level = this->state_ * this->brightness_; if (!constant_brightness) { *cold_white = white_level * cw_level; *warm_white = white_level * ww_level; } else { const float sum = cw_level > 0 || ww_level > 0 ? cw_level + ww_level : 1; *cold_white = white_level * std::max(cw_level, ww_level) * cw_level / sum; *warm_white = white_level * std::max(cw_level, ww_level) * ww_level / sum; } } else { *cold_white = *warm_white = 0; } }
void as_ct(float color_temperature_cw, float color_temperature_ww, float *color_temperature, float *white_brightness) const { const float white_level = this->color_mode_ & ColorCapability::RGB ? this->white_ : 1; if (this->color_mode_ & ColorCapability::COLOR_TEMPERATURE) { *color_temperature = (this->color_temperature_ - color_temperature_cw) / (color_temperature_ww - color_temperature_cw); *white_brightness = this->state_ * this->brightness_ * white_level; } else { *white_brightness = 0; } }
bool operator==(const LightColorValues &rhs) const { return color_mode_ == rhs.color_mode_ && state_ == rhs.state_ && brightness_ == rhs.brightness_ && color_brightness_ == rhs.color_brightness_ && red_ == rhs.red_ && green_ == rhs.green_ && blue_ == rhs.blue_ && white_ == rhs.white_ && color_temperature_ == rhs.color_temperature_ && cold_white_ == rhs.cold_white_ && warm_white_ == rhs.warm_white_; }
bool operator!=(const LightColorValues &rhs) const { return !(rhs == *this); }
ColorMode get_color_mode() const { return this->color_mode_; }
void set_color_mode(ColorMode color_mode) { this->color_mode_ = color_mode; }
float get_state() const { return this->state_; }
bool is_on() const { return this->get_state() != 0.0f; }
void set_state(float state) { this->state_ = clamp_unit_float(state); }
void set_state(bool state) { this->state_ = state ? 1.0f : 0.0f; }
float get_brightness() const { return this->brightness_; }
void set_brightness(float brightness) { this->brightness_ = clamp_unit_float(brightness); }
float get_color_brightness() const { return this->color_brightness_; }
void set_color_brightness(float brightness) { this->color_brightness_ = clamp_unit_float(brightness); }
float get_red() const { return this->red_; }
void set_red(float red) { this->red_ = clamp_unit_float(red); }
float get_green() const { return this->green_; }
void set_green(float green) { this->green_ = clamp_unit_float(green); }
float get_blue() const { return this->blue_; }
void set_blue(float blue) { this->blue_ = clamp_unit_float(blue); }
float get_white() const { return white_; }
void set_white(float white) { this->white_ = clamp_unit_float(white); }
float get_color_temperature() const { return this->color_temperature_; }
void set_color_temperature(float color_temperature) { this->color_temperature_ = color_temperature; }
float get_color_temperature_kelvin() const { if (this->color_temperature_ <= 0) { return this->color_temperature_; } return 1000000.0f / this->color_temperature_; }
void set_color_temperature_kelvin(float color_temperature) { if (color_temperature <= 0) { return; } this->color_temperature_ = 1000000.0f / color_temperature; }
float get_cold_white() const { return this->cold_white_; }
void set_cold_white(float cold_white) { this->cold_white_ = clamp_unit_float(cold_white); }
float get_warm_white() const { return this->warm_white_; }
void set_warm_white(float warm_white) { this->warm_white_ = clamp_unit_float(warm_white); }
```

## `light_effect.h`

**class `LightEffect` — public interface:**
```cpp
explicit LightEffect(const char *name) : name_(name) {}
virtual void start() {}
virtual void start_internal() { this->start(); }
virtual void stop() {}
virtual void apply() = 0;
StringRef get_name() const { return StringRef(this->name_); }
virtual void init() {}
void init_internal(LightState *state) { this->state_ = state; this->init(); }
uint32_t get_index() const;
bool is_active() const;
LightState *get_light_state() const { return this->state_; }
```

## `light_json_schema.h`

**class `LightJSONSchema` — public interface:**
```cpp
static void dump_json(LightState &state, JsonObject root);
static void parse_json(LightState &state, LightCall &call, JsonObject root);
```

## `light_output.h`

**class `LightOutput` — public interface:**
```cpp
virtual LightTraits get_traits() = 0;
virtual std::unique_ptr<LightTransformer> create_default_transition();
virtual void setup_state(LightState *state) {}
virtual void update_state(LightState *state) {}
virtual void write_state(LightState *state) = 0;
```

## `light_state.h`

**Enums:**
```cpp
enum LightRestoreMode : uint8_t {
  LIGHT_RESTORE_DEFAULT_OFF,
  LIGHT_RESTORE_DEFAULT_ON,
  LIGHT_ALWAYS_OFF,
  LIGHT_ALWAYS_ON,
  LIGHT_RESTORE_INVERTED_DEFAULT_OFF,
  LIGHT_RESTORE_INVERTED_DEFAULT_ON,
  LIGHT_RESTORE_AND_OFF,
  LIGHT_RESTORE_AND_ON,
};
```

**class `LightRemoteValuesListener` — public interface:**
```cpp
virtual void on_light_remote_values_update() = 0;
```

**class `LightTargetStateReachedListener` — public interface:**
```cpp
virtual void on_light_target_state_reached() = 0;
```

**class `LightState` — public interface:**
```cpp
LightState(LightOutput *output);
LightTraits get_traits();
LightCall turn_on();
LightCall turn_off();
LightCall toggle();
LightCall make_call();
void setup() override;
void dump_config() override;
void loop() override;
float get_setup_priority() const override;
LightColorValues current_values;
LightColorValues remote_values;
void publish_state();
LightOutput *get_output() const;
StringRef get_effect_name();
void add_remote_values_listener(LightRemoteValuesListener *listener);
void add_target_state_reached_listener(LightTargetStateReachedListener *listener);
void set_default_transition_length(uint32_t default_transition_length);
uint32_t get_default_transition_length() const;
void set_flash_transition_length(uint32_t flash_transition_length);
uint32_t get_flash_transition_length() const;
void set_gamma_correct(float gamma_correct);
float get_gamma_correct() const { return this->gamma_correct_; }
#ifdef USE_LIGHT_GAMMA_LUT void set_gamma_table(const uint16_t *forward) { this->gamma_table_ = forward; }
const uint16_t *get_gamma_table() const { return this->gamma_table_; }
float gamma_correct_lut(float value) const;
float gamma_uncorrect_lut(float value) const;
#else float gamma_correct_lut(float value) const { return value; }
float gamma_uncorrect_lut(float value) const { return value; }
#endif void set_restore_mode(LightRestoreMode restore_mode);
void set_initial_state(void (*callback)(LightStateRTCState &));
bool supports_effects();
const FixedVector<LightEffect *> &get_effects() const;
void add_effects(const std::initializer_list<LightEffect *> &effects);
size_t get_effect_count() const { return this->effects_.size(); }
uint32_t get_current_effect_index() const { return this->active_effect_index_; }
uint32_t get_effect_index(const std::string &effect_name) const { if (str_equals_case_insensitive(effect_name, "none")) { return 0; } for (size_t i = 0; i < this->effects_.size(); i++) { if (str_equals_case_insensitive(effect_name, this->effects_[i]->get_name())) { return i + 1; } } return 0; }
uint32_t get_effect_index(const char *name, size_t len) const { if (len == 4 && ESPHOME_strncasecmp_P(name, ESPHOME_PSTR("none"), 4) == 0) { return 0; } StringRef ref(name, len); for (size_t i = 0; i < this->effects_.size(); i++) { if (str_equals_case_insensitive(ref, this->effects_[i]->get_name())) { return i + 1; } } return 0; }
LightEffect *get_effect_by_index(uint32_t index) const { if (index == 0 || index > this->effects_.size()) { return nullptr; } return this->effects_[index - 1]; }
std::string get_effect_name_by_index(uint32_t index) const { if (index == 0) { return "None"; } if (index > this->effects_.size()) { return ""; } return std::string(this->effects_[index - 1]->get_name()); }
void current_values_as_binary(bool *binary);
void current_values_as_brightness(float *brightness);
void current_values_as_rgb(float *red, float *green, float *blue);
void current_values_as_rgbw(float *red, float *green, float *blue, float *white);
void current_values_as_rgbww(float *red, float *green, float *blue, float *cold_white, float *warm_white, bool constant_brightness = false);
void current_values_as_rgbct(float *red, float *green, float *blue, float *color_temperature, float *white_brightness);
void current_values_as_cwww(float *cold_white, float *warm_white, bool constant_brightness = false);
void current_values_as_ct(float *color_temperature, float *white_brightness);
bool is_transformer_active();
```

## `light_traits.h`

**class `LightTraits` — public interface:**
```cpp
LightTraits() = default;
ColorModeMask get_supported_color_modes() const { return this->supported_color_modes_; }
void set_supported_color_modes(ColorModeMask supported_color_modes) { this->supported_color_modes_ = supported_color_modes; }
void set_supported_color_modes(std::initializer_list<ColorMode> modes) { this->supported_color_modes_ = ColorModeMask(modes); }
bool supports_color_mode(ColorMode color_mode) const { return this->supported_color_modes_.count(color_mode) > 0; }
bool supports_color_capability(ColorCapability color_capability) const { return has_capability(this->supported_color_modes_, color_capability); }
float get_min_mireds() const { return this->min_mireds_; }
void set_min_mireds(float min_mireds) { this->min_mireds_ = min_mireds; }
float get_max_mireds() const { return this->max_mireds_; }
void set_max_mireds(float max_mireds) { this->max_mireds_ = max_mireds; }
```

## `light_transformer.h`

**class `LightTransformer` — public interface:**
```cpp
virtual ~LightTransformer() = default;
void setup(const LightColorValues &start_values, const LightColorValues &target_values, uint32_t length) { this->start_time_ = millis(); this->length_ = length; this->start_values_ = start_values; this->target_values_ = target_values; this->start(); }
virtual bool is_finished() { return this->get_progress_() >= 1.0f; }
virtual void start() {}
virtual optional<LightColorValues> apply() = 0;
virtual void stop() {}
const LightColorValues &get_start_values() const { return this->start_values_; }
const LightColorValues &get_target_values() const { return this->target_values_; }
```

## `transformers.h`

**class `LightTransitionTransformer` — public interface:**
```cpp
void start() override { if (!this->start_values_.is_on() && this->target_values_.is_on()) { this->start_values_ = LightColorValues(this->target_values_); this->start_values_.set_brightness(0.0f); } if (this->start_values_.is_on() && !this->target_values_.is_on()) { this->end_values_ = LightColorValues(this->start_values_); this->end_values_.set_brightness(0.0f); } else { this->end_values_ = LightColorValues(this->target_values_); } if (this->start_values_.get_color_mode() != this->end_values_.get_color_mode()) { this->changing_color_mode_ = true; this->intermediate_values_ = this->start_values_; this->intermediate_values_.set_state(false); } }
optional<LightColorValues> apply() override { float p = this->get_progress_(); if (this->changing_color_mode_ && p > 0.5f && this->intermediate_values_.get_color_mode() != this->end_values_.get_color_mode()) { this->intermediate_values_ = this->end_values_; this->intermediate_values_.set_state(false); } LightColorValues &start = this->changing_color_mode_ && p > 0.5f ? this->intermediate_values_ : this->start_values_; LightColorValues &end = this->changing_color_mode_ && p < 0.5f ? this->intermediate_values_ : this->end_values_; if (this->changing_color_mode_) p = p < 0.5f ? p * 2 : (p - 0.5f) * 2; float v = LightTransformer::smoothed_progress(p); return LightColorValues::lerp(start, end, v); }
```

**class `LightFlashTransformer` — public interface:**
```cpp
LightFlashTransformer(LightState &state) : state_(state) {}
void start() override { this->transition_length_ = this->state_.get_flash_transition_length(); if (this->transition_length_ * 2 > this->length_) this->transition_length_ = this->length_ / 2; this->begun_lightstate_restore_ = false; this->transformer_ = this->state_.get_output()->create_default_transition(); this->transformer_->setup(this->state_.current_values, this->target_values_, this->transition_length_); }
optional<LightColorValues> apply() override { optional<LightColorValues> result = {}; if (this->transformer_ == nullptr && millis() - this->start_time_ > this->length_ - this->transition_length_) { this->transformer_ = this->state_.get_output()->create_default_transition(); this->transformer_->setup(this->state_.current_values, this->get_start_values(), this->transition_length_); this->begun_lightstate_restore_ = true; } if (this->transformer_ != nullptr) { result = this->transformer_->apply(); if (this->transformer_->is_finished()) { this->transformer_->stop(); this->transformer_ = nullptr; } } return result; }
void stop() override { if (this->transformer_ != nullptr) { this->transformer_->stop(); this->transformer_ = nullptr; } this->state_.current_values = this->get_start_values(); this->state_.remote_values = this->get_start_values(); this->state_.publish_state(); }
bool is_finished() override { return this->begun_lightstate_restore_ && LightTransformer::is_finished(); }
```
