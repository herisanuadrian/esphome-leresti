# ESPHome component: `monochromatic`

Source: `esphome/components/monochromatic/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `monochromatic_light_output.h`

**class `MonochromaticLightOutput` — public interface:**
```cpp
void set_output(output::FloatOutput *output) { output_ = output; }
light::LightTraits get_traits() override { auto traits = light::LightTraits(); traits.set_supported_color_modes({light::ColorMode::BRIGHTNESS}); return traits; }
void write_state(light::LightState *state) override { float bright; state->current_values_as_brightness(&bright); this->output_->set_level(bright); }
```
