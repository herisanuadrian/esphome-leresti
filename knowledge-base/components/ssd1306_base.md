# ESPHome component: `ssd1306_base`

Source: `esphome/components/ssd1306_base/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `ssd1306_base.h`

**Enums:**
```cpp
enum SSD1306Model {
  SSD1306_MODEL_128_32 = 0,
  SSD1306_MODEL_128_64,
  SSD1306_MODEL_96_16,
  SSD1306_MODEL_64_48,
  SSD1306_MODEL_64_32,
  SSD1306_MODEL_72_40,
  SH1106_MODEL_128_32,
  SH1106_MODEL_128_64,
  SH1106_MODEL_96_16,
  SH1106_MODEL_64_48,
  SH1107_MODEL_128_64,
  SH1107_MODEL_128_128,
  SSD1305_MODEL_128_32,
  SSD1305_MODEL_128_64,
  SSD1306_MODEL_COUNT,  
};
```

**class `SSD1306` — public interface:**
```cpp
void setup() override;
void display();
void update() override;
void set_model(SSD1306Model model) { this->model_ = model; }
void set_reset_pin(GPIOPin *reset_pin) { this->reset_pin_ = reset_pin; }
void set_external_vcc(bool external_vcc) { this->external_vcc_ = external_vcc; }
void init_contrast(float contrast) { this->contrast_ = contrast; }
float get_contrast();
void set_contrast(float contrast);
float get_brightness();
void init_brightness(float brightness) { this->brightness_ = brightness; }
void set_brightness(float brightness);
void init_flip_x(bool flip_x) { this->flip_x_ = flip_x; }
void init_flip_y(bool flip_y) { this->flip_y_ = flip_y; }
void init_offset_x(uint8_t offset_x) { this->offset_x_ = offset_x; }
void init_offset_y(uint8_t offset_y) { this->offset_y_ = offset_y; }
void init_invert(bool invert) { this->invert_ = invert; }
void set_invert(bool invert);
bool is_on();
void turn_on();
void turn_off();
float get_setup_priority() const override { return setup_priority::PROCESSOR; }
void fill(Color color) override;
display::DisplayType get_display_type() override { return display::DisplayType::DISPLAY_TYPE_BINARY; }
```
