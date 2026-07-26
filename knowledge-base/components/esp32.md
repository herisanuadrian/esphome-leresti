# ESPHome component: `esp32`

Source: `esphome/components/esp32/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `gpio.h`

**class `ESP32InternalGPIOPin` — public interface:**
```cpp
void set_pin(gpio_num_t pin) { this->pin_ = static_cast<uint8_t>(pin); }
void set_inverted(bool inverted) { this->pin_flags_.inverted = inverted; }
void set_drive_strength(gpio_drive_cap_t drive_strength) { this->pin_flags_.drive_strength = static_cast<uint8_t>(drive_strength); }
void set_flags(gpio::Flags flags) { this->flags_ = flags; }
void setup() override;
void pin_mode(gpio::Flags flags) override;
bool digital_read() override;
void digital_write(bool value) override;
size_t dump_summary(char *buffer, size_t len) const override;
void detach_interrupt() const override;
ISRInternalGPIOPin to_isr() const override;
uint8_t get_pin() const override { return this->pin_; }
gpio::Flags get_flags() const override { return this->flags_; }
bool is_inverted() const override { return this->pin_flags_.inverted; }
gpio_num_t get_pin_num() const { return static_cast<gpio_num_t>(this->pin_); }
gpio_drive_cap_t get_drive_strength() const { return static_cast<gpio_drive_cap_t>(this->pin_flags_.drive_strength); }
```

## `preference_backend.h`

**class `ESP32PreferenceBackend` — public interface:**
```cpp
bool save(const uint8_t *data, size_t len);
bool load(uint8_t *data, size_t len);
uint32_t key{0}
uint32_t nvs_handle{0}
uint16_t rtc_offset{0}
uint8_t length_words{0}
bool in_flash{true}
```

## `preferences.h`

**class `ESP32Preferences` — public interface:**
```cpp
using PreferencesMixin<ESP32Preferences>::make_preference;
void open();
ESPPreferenceObject make_preference(size_t length, uint32_t type, bool in_flash);
ESPPreferenceObject make_preference(size_t length, uint32_t type);
bool sync();
bool reset();
uint32_t nvs_handle;
```
