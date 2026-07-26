# ESPHome component: `mipi_spi`

Source: `esphome/components/mipi_spi/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `mipi_spi.h`

**Enums:**
```cpp
enum PixelMode {
  PIXEL_MODE_8 = 1,
  PIXEL_MODE_16 = 2,
  PIXEL_MODE_18 = 3,
};
enum BusType {
  BUS_TYPE_SINGLE = 1,
  BUS_TYPE_QUAD = 4,
  BUS_TYPE_OCTAL = 8,
  BUS_TYPE_SINGLE_16 = 16,  
};
```

**Constants:**
```cpp
constexpr static const char *const TAG = "display.mipi_spi";
```

**class `MipiSpi` — public interface:**
```cpp
MipiSpi() = default;
void update() override { this->stop_poller(); }
void draw_pixel_at(int x, int y, Color color) override {}
void set_model(const char *model) { this->model_ = model; }
void set_reset_pin(GPIOPin *reset_pin) { this->reset_pin_ = reset_pin; }
void set_enable_pins(std::vector<GPIOPin *> enable_pins) { this->enable_pins_ = std::move(enable_pins); }
void set_dc_pin(GPIOPin *dc_pin) { this->dc_pin_ = dc_pin; }
void set_invert_colors(bool invert_colors) { this->invert_colors_ = invert_colors; this->reset_params_(); }
void set_brightness(uint8_t brightness) { this->brightness_ = brightness; this->reset_params_(); }
void set_rotation(display::DisplayRotation rotation) override { this->rotation_ = rotation; if constexpr (HAS_HARDWARE_ROTATION) { this->reset_params_(); } }
display::DisplayType get_display_type() override { return display::DisplayType::DISPLAY_TYPE_COLOR; }
int get_width() override { if (this->rotation_ == display::DISPLAY_ROTATION_90_DEGREES || this->rotation_ == display::DISPLAY_ROTATION_270_DEGREES) return HEIGHT; return WIDTH; }
int get_height() override { if (this->rotation_ == display::DISPLAY_ROTATION_90_DEGREES || this->rotation_ == display::DISPLAY_ROTATION_270_DEGREES) return WIDTH; return HEIGHT; }
void set_init_sequence(const std::vector<uint8_t> &sequence) { this->init_sequence_ = sequence; }
void setup() override { this->spi_setup(); if (this->dc_pin_ != nullptr) { this->dc_pin_->setup(); this->dc_pin_->digital_write(false); } for (auto *pin : this->enable_pins_) { pin->setup(); pin->digital_write(true); } if (this->reset_pin_ != nullptr) { this->reset_pin_->setup(); this->reset_pin_->digital_write(true); delay(5); this->reset_pin_->digital_write(false); delay(5); this->reset_pin_->digital_write(true); } auto when = millis() + 120; size_t index = 0; auto &vec = this->init_sequence_; while (index != vec.size()) { if (vec.size() - index < 2) { esph_log_e(TAG, "Malformed init sequence"); this->mark_failed(); return; } uint8_t cmd = vec[index++]; uint8_t x = vec[index++]; if (x == DELAY_FLAG) { if (cmd == 0) { cmd = clamp_at_least((int) (when - millis()), 0); } esph_log_d(TAG, "Delay %dms", cmd); delay(cmd); } else { uint8_t num_args = x & 0x7F; if (vec.size() - index < num_args) { esph_log_e(TAG, "Malformed init sequence"); this->mark_failed(); return; } const auto *ptr = vec.data() + index; this->write_command_(cmd, ptr, num_args); index += num_args; } } this->reset_params_(); this->init_sequence_.clear(); }
void draw_pixels_at(int x_start, int y_start, int w, int h, const uint8_t *ptr, display::ColorOrder order, display::ColorBitness bitness, bool big_endian, int x_offset, int y_offset, int x_pad) override { if (this->is_failed()) return; if (w <= 0 || h <= 0) return; if (get_pixel_mode(bitness) != BUFFERPIXEL || big_endian != IS_BIG_ENDIAN) { esph_log_e(TAG, "Unsupported color depth or bit order"); return; } this->write_to_display_(x_start, y_start, w, h, reinterpret_cast<const BUFFERTYPE *>(ptr), x_offset, y_offset, x_pad); }
void dump_config() override { internal_dump_config(this->model_, this->get_width(), this->get_height(), this->get_offset_width_(), this->get_offset_height_(), (uint8_t) MADCTL, this->invert_colors_, DISPLAYPIXEL * 8, IS_BIG_ENDIAN, this->brightness_, this->cs_, this->reset_pin_, this->dc_pin_, this->mode_, this->data_rate_, BUS_TYPE, HAS_HARDWARE_ROTATION); }
```

**class `MipiSpiBuffer` — public interface:**
```cpp
static constexpr size_t round_buffer(size_t size) { return (size + ROUNDING - 1) / ROUNDING * ROUNDING; }
MipiSpiBuffer() = default;
void dump_config() override { MipiSpi<BUFFERTYPE, BUFFERPIXEL, IS_BIG_ENDIAN, DISPLAYPIXEL, BUS_TYPE, WIDTH, HEIGHT, OFFSET_WIDTH, OFFSET_HEIGHT, PAD_WIDTH, PAD_HEIGHT, MADCTL, HAS_HARDWARE_ROTATION>::dump_config(); esph_log_config(TAG, " Rotation: %d°\n" " Buffer pixels: %d bits\n" " Buffer fraction: 1/%d\n" " Buffer bytes: %zu\n" " Draw rounding: %u", this->rotation_, BUFFERPIXEL * 8, FRACTION, sizeof(BUFFERTYPE) * round_buffer(WIDTH) * round_buffer(HEIGHT) / FRACTION, ROUNDING); }
void setup() override { MipiSpi<BUFFERTYPE, BUFFERPIXEL, IS_BIG_ENDIAN, DISPLAYPIXEL, BUS_TYPE, WIDTH, HEIGHT, OFFSET_WIDTH, OFFSET_HEIGHT, PAD_WIDTH, PAD_HEIGHT, MADCTL, HAS_HARDWARE_ROTATION>::setup(); RAMAllocator<BUFFERTYPE> allocator{}; this->buffer_ = allocator.allocate(round_buffer(WIDTH) * round_buffer(HEIGHT) / FRACTION); if (this->buffer_ == nullptr) { this->mark_failed(LOG_STR("Buffer allocation failed")); } }
void update() override { #if ESPHOME_LOG_LEVEL == ESPHOME_LOG_LEVEL_VERBOSE auto now = millis(); #endif if (this->is_failed()) { return; } auto increment = (this->get_height_internal() / FRACTION / ROUNDING) * ROUNDING; for (this->start_line_ = 0; this->start_line_ < this->get_height_internal(); this->start_line_ = this->end_line_) { #if ESPHOME_LOG_LEVEL == ESPHOME_LOG_LEVEL_VERBOSE auto lap = millis(); #endif this->end_line_ = clamp_at_most(this->start_line_ + increment, this->get_height_internal()); if (this->auto_clear_enabled_) { this->clear(); } if (this->page_ != nullptr) { this->page_->get_writer()(*this); } else if (this->writer_.has_value()) { (*this->writer_)(*this); } else { this->test_card(); } #if ESPHOME_LOG_LEVEL == ESPHOME_LOG_LEVEL_VERBOSE esph_log_v(TAG, "Drawing from line %d took %dms", this->start_line_, millis() - lap); lap = millis(); #endif if (this->x_low_ > this->x_high_ || this->y_low_ > this->y_high_) return; esph_log_v(TAG, "x_low %d, y_low %d, x_high %d, y_high %d", this->x_low_, this->y_low_, this->x_high_, this->y_high_); this->x_low_ = this->x_low_ / ROUNDING * ROUNDING; this->y_low_ = this->y_low_ / ROUNDING * ROUNDING; this->x_high_ = round_buffer(this->x_high_ + 1) - 1; this->y_high_ = clamp_at_most(round_buffer(this->y_high_ + 1) - 1, this->end_line_ - 1); int w = this->x_high_ - this->x_low_ + 1; int h = this->y_high_ - this->y_low_ + 1; this->write_to_display_(this->x_low_, this->y_low_, w, h, this->buffer_, this->x_low_, this->y_low_ - this->start_line_, round_buffer(this->get_width_internal()) - w - this->x_low_); this->x_low_ = this->get_width_internal(); this->y_low_ = this->get_height_internal(); this->x_high_ = 0; this->y_high_ = 0; #if ESPHOME_LOG_LEVEL == ESPHOME_LOG_LEVEL_VERBOSE esph_log_v(TAG, "Write to display took %dms", millis() - lap); lap = millis(); #endif } #if ESPHOME_LOG_LEVEL == ESPHOME_LOG_LEVEL_VERBOSE esph_log_v(TAG, "Total update took %dms", millis() - now); #endif }
void draw_pixel_at(int x, int y, Color color) override { if (!this->get_clipping().inside(x, y)) return; if constexpr (not HAS_HARDWARE_ROTATION) { if (this->rotation_ == display::DISPLAY_ROTATION_180_DEGREES) { x = WIDTH - x - 1; y = HEIGHT - y - 1; } else if (this->rotation_ == display::DISPLAY_ROTATION_90_DEGREES) { auto tmp = x; x = WIDTH - y - 1; y = tmp; } else if (this->rotation_ == display::DISPLAY_ROTATION_270_DEGREES) { auto tmp = y; y = HEIGHT - x - 1; x = tmp; } } if (x < 0 || x >= this->get_width_internal() || y < this->start_line_ || y >= this->end_line_) return; this->buffer_[(y - this->start_line_) * round_buffer(this->get_width_internal()) + x] = convert_color(color); if (x < this->x_low_) { this->x_low_ = x; } if (x > this->x_high_) { this->x_high_ = x; } if (y < this->y_low_) { this->y_low_ = y; } if (y > this->y_high_) { this->y_high_ = y; } }
void fill(Color color) override { if (this->get_clipping().is_set()) { display::Display::fill(color); return; } this->x_low_ = 0; this->y_low_ = this->start_line_; this->x_high_ = this->get_width_internal() - 1; this->y_high_ = this->end_line_ - 1; std::fill_n(this->buffer_, (this->end_line_ - this->start_line_) * round_buffer(this->get_width_internal()), convert_color(color)); }
```
