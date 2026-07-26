# ESPHome component: `cwww`

Source: `esphome/components/cwww/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `cwww_light_output.h`

**class `CWWWLightOutput` — public interface:**
```cpp
void set_cold_white(output::FloatOutput *cold_white) { cold_white_ = cold_white; }
void set_warm_white(output::FloatOutput *warm_white) { warm_white_ = warm_white; }
void set_cold_white_temperature(float cold_white_temperature) { cold_white_temperature_ = cold_white_temperature; }
void set_warm_white_temperature(float warm_white_temperature) { warm_white_temperature_ = warm_white_temperature; }
void set_constant_brightness(bool constant_brightness) { constant_brightness_ = constant_brightness; }
light::LightTraits get_traits() override { auto traits = light::LightTraits(); traits.set_supported_color_modes({light::ColorMode::COLD_WARM_WHITE}); traits.set_min_mireds(this->cold_white_temperature_); traits.set_max_mireds(this->warm_white_temperature_); return traits; }
void write_state(light::LightState *state) override { float cwhite, wwhite; state->current_values_as_cwww(&cwhite, &wwhite, this->constant_brightness_); this->cold_white_->set_level(cwhite); this->warm_white_->set_level(wwhite); }
```
