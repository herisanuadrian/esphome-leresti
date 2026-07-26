# ESPHome component: `esp32_rmt_led_strip`

Source: `esphome/components/esp32_rmt_led_strip/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `led_strip.h`

**Enums:**
```cpp
enum RGBOrder : uint8_t {
  ORDER_RGB,
  ORDER_RBG,
  ORDER_GRB,
  ORDER_GBR,
  ORDER_BGR,
  ORDER_BRG,
};
```

**class `ESP32RMTLEDStripLightOutput` — public interface:**
```cpp
void setup() override;
void write_state(light::LightState *state) override;
float get_setup_priority() const override;
int32_t size() const override { return this->num_leds_; }
light::LightTraits get_traits() override { auto traits = light::LightTraits(); if (this->is_rgbw_ || this->is_wrgb_) { traits.set_supported_color_modes({light::ColorMode::RGB_WHITE, light::ColorMode::WHITE}); } else { traits.set_supported_color_modes({light::ColorMode::RGB}); } return traits; }
void set_pin(uint8_t pin) { this->pin_ = pin; }
void set_inverted(bool inverted) { this->invert_out_ = inverted; }
void set_num_leds(uint16_t num_leds) { this->num_leds_ = num_leds; }
void set_is_rgbw(bool is_rgbw) { this->is_rgbw_ = is_rgbw; }
void set_is_wrgb(bool is_wrgb) { this->is_wrgb_ = is_wrgb; }
void set_use_dma(bool use_dma) { this->use_dma_ = use_dma; }
void set_use_psram(bool use_psram) { this->use_psram_ = use_psram; }
void set_max_refresh_rate(uint32_t interval_us) { this->max_refresh_rate_ = interval_us; }
void set_led_params(uint32_t bit0_high, uint32_t bit0_low, uint32_t bit1_high, uint32_t bit1_low, uint32_t reset_time_high, uint32_t reset_time_low);
void set_rgb_order(RGBOrder rgb_order) { this->rgb_order_ = rgb_order; }
void set_rmt_symbols(uint32_t rmt_symbols) { this->rmt_symbols_ = rmt_symbols; }
void clear_effect_data() override { for (int i = 0; i < this->size(); i++) this->effect_data_[i] = 0; }
void dump_config() override;
```
