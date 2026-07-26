# ESPHome component: `font`

Source: `esphome/components/font/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `font.h`

**class `Glyph` — public interface:**
```cpp
constexpr Glyph(uint32_t code_point, const uint8_t *data, int advance, int offset_x, int offset_y, int width, int height) : code_point(code_point), data(data), advance(advance), offset_x(offset_x), offset_y(offset_y), width(width), height(height) {}
bool is_less_or_equal(uint32_t other) const { return this->code_point <= other; }
const uint32_t code_point;
const uint8_t *data;
int advance;
int offset_x;
int offset_y;
int width;
int height;
```
