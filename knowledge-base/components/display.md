# ESPHome component: `display`

Source: `esphome/components/display/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `display.h`

**Enums:**
```cpp
enum class TextAlign {
  TOP = 0x00,
  CENTER_VERTICAL = 0x01,
  BASELINE = 0x02,
  BOTTOM = 0x04,
  LEFT = 0x00,
  CENTER_HORIZONTAL = 0x08,
  RIGHT = 0x10,
  TOP_LEFT = TOP | LEFT,
  TOP_CENTER = TOP | CENTER_HORIZONTAL,
  TOP_RIGHT = TOP | RIGHT,
  CENTER_LEFT = CENTER_VERTICAL | LEFT,
  CENTER = CENTER_VERTICAL | CENTER_HORIZONTAL,
  CENTER_RIGHT = CENTER_VERTICAL | RIGHT,
  BASELINE_LEFT = BASELINE | LEFT,
  BASELINE_CENTER = BASELINE | CENTER_HORIZONTAL,
  BASELINE_RIGHT = BASELINE | RIGHT,
  BOTTOM_LEFT = BOTTOM | LEFT,
  BOTTOM_CENTER = BOTTOM | CENTER_HORIZONTAL,
  BOTTOM_RIGHT = BOTTOM | RIGHT,
};
enum class ImageAlign {
  TOP = 0x00,
  CENTER_VERTICAL = 0x01,
  BOTTOM = 0x02,
  LEFT = 0x00,
  CENTER_HORIZONTAL = 0x04,
  RIGHT = 0x08,
  TOP_LEFT = TOP | LEFT,
  TOP_CENTER = TOP | CENTER_HORIZONTAL,
  TOP_RIGHT = TOP | RIGHT,
  CENTER_LEFT = CENTER_VERTICAL | LEFT,
  CENTER = CENTER_VERTICAL | CENTER_HORIZONTAL,
  CENTER_RIGHT = CENTER_VERTICAL | RIGHT,
  BOTTOM_LEFT = BOTTOM | LEFT,
  BOTTOM_CENTER = BOTTOM | CENTER_HORIZONTAL,
  BOTTOM_RIGHT = BOTTOM | RIGHT,
  HORIZONTAL_ALIGNMENT = LEFT | CENTER_HORIZONTAL | RIGHT,
  VERTICAL_ALIGNMENT = TOP | CENTER_VERTICAL | BOTTOM
};
enum DisplayType {
  DISPLAY_TYPE_BINARY = 1,
  DISPLAY_TYPE_GRAYSCALE = 2,
  DISPLAY_TYPE_COLOR = 3,
};
enum DisplayRotation {
  DISPLAY_ROTATION_0_DEGREES = 0,
  DISPLAY_ROTATION_90_DEGREES = 90,
  DISPLAY_ROTATION_180_DEGREES = 180,
  DISPLAY_ROTATION_270_DEGREES = 270,
};
enum RegularPolygonVariation {
  VARIATION_POINTY_TOP = 0,
  VARIATION_FLAT_TOP = 1,
};
enum RegularPolygonDrawing {
  DRAWING_OUTLINE = 0,
  DRAWING_FILLED = 1,
};
```

**Constants:**
```cpp
inline constexpr Color COLOR_OFF(0, 0, 0, 0);
inline constexpr Color COLOR_ON(255, 255, 255, 255);
```

**class `DisplayWriter` — public interface:**
```cpp
DisplayWriter() : type_(NONE) {}
template<typename F> DisplayWriter(F f) requires std::invocable<F, T &> && std::convertible_to<F, void (*)(T &)> : type_(STATELESS_LAMBDA) { this->stateless_f_ = f; }
template<typename F> DisplayWriter(F f) requires std::invocable<F, T &> &&(!std::convertible_to<F, void (*)(T &)>) : type_(LAMBDA) { this->f_ = new std::function<void(T &)>(std::move(f)); }
DisplayWriter(const DisplayWriter &other) : type_(other.type_) { if (type_ == LAMBDA) { this->f_ = new std::function<void(T &)>(*other.f_); } else if (type_ == STATELESS_LAMBDA) { this->stateless_f_ = other.stateless_f_; } }
DisplayWriter(DisplayWriter &&other) noexcept : type_(other.type_) { if (type_ == LAMBDA) { this->f_ = other.f_; other.f_ = nullptr; } else if (type_ == STATELESS_LAMBDA) { this->stateless_f_ = other.stateless_f_; } other.type_ = NONE; }
DisplayWriter &operator=(const DisplayWriter &other) { if (this != &other) { this->~DisplayWriter(); new (this) DisplayWriter(other); } return *this; }
DisplayWriter &operator=(DisplayWriter &&other) noexcept { if (this != &other) { this->~DisplayWriter(); new (this) DisplayWriter(std::move(other)); } return *this; }
~DisplayWriter() { if (type_ == LAMBDA) { delete this->f_; } }
bool has_value() const { return this->type_ != NONE; }
void call(T &display) const { switch (this->type_) { case STATELESS_LAMBDA: this->stateless_f_(display); break; case LAMBDA: (*this->f_)(display); break; case NONE: default: break; } }
void operator()(T &display) const { this->call(display); }
DisplayWriter &operator*() { return *this; }
const DisplayWriter &operator*() const { return *this; }
```

**class `BaseImage` — public interface:**
```cpp
virtual void draw(int x, int y, Display *display, Color color_on, Color color_off) = 0;
virtual int get_width() const = 0;
virtual int get_height() const = 0;
```

**class `BaseFont` — public interface:**
```cpp
virtual void print(int x, int y, Display *display, Color color, const char *text, Color background) = 0;
virtual void measure(const char *str, int *width, int *x_offset, int *baseline, int *height) = 0;
```

**class `Display` — public interface:**
```cpp
virtual void fill(Color color);
virtual void clear();
virtual int get_width() { return this->get_width_internal(); }
virtual int get_height() { return this->get_height_internal(); }
int get_native_width() { return this->get_width_internal(); }
int get_native_height() { return this->get_height_internal(); }
inline void draw_pixel_at(int x, int y) { this->draw_pixel_at(x, y, COLOR_ON); }
virtual void draw_pixel_at(int x, int y, Color color) = 0;
virtual void draw_pixels_at(int x_start, int y_start, int w, int h, const uint8_t *ptr, ColorOrder order, ColorBitness bitness, bool big_endian, int x_offset, int y_offset, int x_pad);
void draw_pixels_at(int x_start, int y_start, int w, int h, const uint8_t *ptr, ColorOrder order, ColorBitness bitness, bool big_endian) { this->draw_pixels_at(x_start, y_start, w, h, ptr, order, bitness, big_endian, 0, 0, 0); }
void line(int x1, int y1, int x2, int y2, Color color = COLOR_ON);
void line_at_angle(int x, int y, int angle, int length, Color color = COLOR_ON);
void line_at_angle(int x, int y, int angle, int start_radius, int stop_radius, Color color = COLOR_ON);
void horizontal_line(int x, int y, int width, Color color = COLOR_ON);
void vertical_line(int x, int y, int height, Color color = COLOR_ON);
void rectangle(int x1, int y1, int width, int height, Color color = COLOR_ON);
void filled_rectangle(int x1, int y1, int width, int height, Color color = COLOR_ON);
void circle(int center_x, int center_xy, int radius, Color color = COLOR_ON);
void filled_circle(int center_x, int center_y, int radius, Color color = COLOR_ON);
void filled_ring(int center_x, int center_y, int radius1, int radius2, Color color = COLOR_ON);
void filled_gauge(int center_x, int center_y, int radius1, int radius2, int progress, Color color = COLOR_ON);
void triangle(int x1, int y1, int x2, int y2, int x3, int y3, Color color = COLOR_ON);
void filled_triangle(int x1, int y1, int x2, int y2, int x3, int y3, Color color = COLOR_ON);
void get_regular_polygon_vertex(int vertex_id, int *vertex_x, int *vertex_y, int center_x, int center_y, int radius, int edges, RegularPolygonVariation variation = VARIATION_POINTY_TOP, float rotation_degrees = ROTATION_0_DEGREES);
void regular_polygon(int x, int y, int radius, int edges, RegularPolygonVariation variation = VARIATION_POINTY_TOP, float rotation_degrees = ROTATION_0_DEGREES, Color color = COLOR_ON, RegularPolygonDrawing drawing = DRAWING_OUTLINE);
void regular_polygon(int x, int y, int radius, int edges, RegularPolygonVariation variation, Color color, RegularPolygonDrawing drawing = DRAWING_OUTLINE);
void regular_polygon(int x, int y, int radius, int edges, Color color, RegularPolygonDrawing drawing = DRAWING_OUTLINE);
void filled_regular_polygon(int x, int y, int radius, int edges, RegularPolygonVariation variation = VARIATION_POINTY_TOP, float rotation_degrees = ROTATION_0_DEGREES, Color color = COLOR_ON);
void filled_regular_polygon(int x, int y, int radius, int edges, RegularPolygonVariation variation, Color color);
void filled_regular_polygon(int x, int y, int radius, int edges, Color color);
void print(int x, int y, BaseFont *font, Color color, TextAlign align, const char *text, Color background = COLOR_OFF);
void print(int x, int y, BaseFont *font, Color color, const char *text, Color background = COLOR_OFF);
void print(int x, int y, BaseFont *font, TextAlign align, const char *text);
void print(int x, int y, BaseFont *font, const char *text);
void printf(int x, int y, BaseFont *font, Color color, Color background, TextAlign align, const char *format, ...) __attribute__((format(printf, 8, 9)));
void printf(int x, int y, BaseFont *font, Color color, TextAlign align, const char *format, ...) __attribute__((format(printf, 7, 8)));
void printf(int x, int y, BaseFont *font, Color color, const char *format, ...) __attribute__((format(printf, 6, 7)));
void printf(int x, int y, BaseFont *font, TextAlign align, const char *format, ...) __attribute__((format(printf, 6, 7)));
void printf(int x, int y, BaseFont *font, const char *format, ...) __attribute__((format(printf, 5, 6)));
void strftime(int x, int y, BaseFont *font, Color color, Color background, TextAlign align, const char *format, ESPTime time) __attribute__((format(strftime, 8, 0)));
void strftime(int x, int y, BaseFont *font, Color color, TextAlign align, const char *format, ESPTime time) __attribute__((format(strftime, 7, 0)));
void strftime(int x, int y, BaseFont *font, Color color, const char *format, ESPTime time) __attribute__((format(strftime, 6, 0)));
void strftime(int x, int y, BaseFont *font, TextAlign align, const char *format, ESPTime time) __attribute__((format(strftime, 6, 0)));
void strftime(int x, int y, BaseFont *font, const char *format, ESPTime time) __attribute__((format(strftime, 5, 0)));
void image(int x, int y, BaseImage *image, Color color_on = COLOR_ON, Color color_off = COLOR_OFF);
void image(int x, int y, BaseImage *image, ImageAlign align, Color color_on = COLOR_ON, Color color_off = COLOR_OFF);
#ifdef USE_GRAPH void graph(int x, int y, graph::Graph *graph, Color color_on = COLOR_ON);
void legend(int x, int y, graph::Graph *graph, Color color_on = COLOR_ON);
#endif #ifdef USE_QR_CODE void qr_code(int x, int y, qr_code::QrCode *qr_code, Color color_on = COLOR_ON, int scale = 1);
#endif #ifdef USE_GRAPHICAL_DISPLAY_MENU void menu(int x, int y, graphical_display_menu::GraphicalDisplayMenu *menu, int width, int height);
#endif void get_text_bounds(int x, int y, const char *text, BaseFont *font, TextAlign align, int *x1, int *y1, int *width, int *height);
void set_writer(display_writer_t &&writer);
void show_page(DisplayPage *page);
void show_next_page();
void show_prev_page();
void set_pages(std::vector<DisplayPage *> pages);
const DisplayPage *get_active_page() const { return this->page_; }
void add_on_page_change_trigger(DisplayOnPageChangeTrigger *t) { this->on_page_change_triggers_.push_back(t); }
virtual void set_rotation(DisplayRotation rotation);
void set_auto_clear(bool auto_clear_enabled) { this->auto_clear_enabled_ = auto_clear_enabled; }
DisplayRotation get_rotation() const { return this->rotation_; }
virtual DisplayType get_display_type() = 0;
void start_clipping(Rect rect);
void start_clipping(int16_t left, int16_t top, int16_t right, int16_t bottom) { start_clipping(Rect(left, top, right - left, bottom - top)); }
void extend_clipping(Rect rect);
void extend_clipping(int16_t left, int16_t top, int16_t right, int16_t bottom) { this->extend_clipping(Rect(left, top, right - left, bottom - top)); }
void shrink_clipping(Rect rect);
void shrink_clipping(uint16_t left, uint16_t top, uint16_t right, uint16_t bottom) { this->shrink_clipping(Rect(left, top, right - left, bottom - top)); }
void end_clipping();
Rect get_clipping() const;
bool is_clipping() const { return !this->clipping_rectangle_.empty(); }
bool clip(int x, int y);
void test_card();
void show_test_card() { this->show_test_card_ = true; }
```

**class `DisplayPage` — public interface:**
```cpp
DisplayPage(display_writer_t writer);
void show();
void show_next();
void show_prev();
void set_parent(Display *parent);
void set_prev(DisplayPage *prev);
void set_next(DisplayPage *next);
const display_writer_t &get_writer() const;
```

**class `DisplayPageShowAction` — public interface:**
```cpp
TEMPLATABLE_VALUE(DisplayPage *, page) void play(const Ts &...x) override { auto *page = this->page_.value(x...); if (page != nullptr) { page->show(); } }
```

**class `DisplayPageShowNextAction` — public interface:**
```cpp
DisplayPageShowNextAction(Display *buffer) : buffer_(buffer) {}
void play(const Ts &...x) override { this->buffer_->show_next_page(); }
Display *buffer_;
```

**class `DisplayPageShowPrevAction` — public interface:**
```cpp
DisplayPageShowPrevAction(Display *buffer) : buffer_(buffer) {}
void play(const Ts &...x) override { this->buffer_->show_prev_page(); }
Display *buffer_;
```

**class `DisplayIsDisplayingPageCondition` — public interface:**
```cpp
DisplayIsDisplayingPageCondition(Display *parent) : parent_(parent) {}
void set_page(DisplayPage *page) { this->page_ = page; }
bool check(const Ts &...x) override { return this->parent_->get_active_page() == this->page_; }
```

**class `DisplayOnPageChangeTrigger` — public interface:**
```cpp
explicit DisplayOnPageChangeTrigger(Display *parent) { parent->add_on_page_change_trigger(this); }
void process(DisplayPage *from, DisplayPage *to);
void set_from(DisplayPage *p) { this->from_ = p; }
void set_to(DisplayPage *p) { this->to_ = p; }
```

## `display_buffer.h`

**class `DisplayBuffer` — public interface:**
```cpp
int get_width() override;
int get_height() override;
void draw_pixel_at(int x, int y, Color color) override;
```

## `display_color_utils.h`

**Enums:**
```cpp
enum ColorOrder : uint8_t { COLOR_ORDER_RGB = 0, COLOR_ORDER_BGR = 1, COLOR_ORDER_GRB = 2 };
enum ColorBitness : uint8_t { COLOR_BITNESS_888 = 0, COLOR_BITNESS_565 = 1, COLOR_BITNESS_332 = 2 };
```

**class `ColorUtil` — public interface:**
```cpp
static Color to_color(uint32_t colorcode, ColorOrder color_order, ColorBitness color_bitness = ColorBitness::COLOR_BITNESS_888, bool right_bit_aligned = true) { uint8_t first_color, second_color, third_color; uint8_t first_bits = 0; uint8_t second_bits = 0; uint8_t third_bits = 0; switch (color_bitness) { case COLOR_BITNESS_888: first_bits = 8; second_bits = 8; third_bits = 8; break; case COLOR_BITNESS_565: first_bits = 5; second_bits = 6; third_bits = 5; break; case COLOR_BITNESS_332: first_bits = 3; second_bits = 3; third_bits = 2; break; } first_color = right_bit_aligned ? esp_scale(((colorcode >> (second_bits + third_bits)) & ((1 << first_bits) - 1)), ((1 << first_bits) - 1)) : esp_scale(((colorcode >> 16) & 0xFF), (1 << first_bits) - 1); second_color = right_bit_aligned ? esp_scale(((colorcode >> third_bits) & ((1 << second_bits) - 1)), ((1 << second_bits) - 1)) : esp_scale(((colorcode >> 8) & 0xFF), ((1 << second_bits) - 1)); third_color = (right_bit_aligned ? esp_scale(((colorcode >> 0) & ((1 << third_bits) - 1)), ((1 << third_bits) - 1)) : esp_scale(((colorcode >> 0) & 0xFF), (1 << third_bits) - 1)); Color color_return; switch (color_order) { case COLOR_ORDER_RGB: color_return.r = first_color; color_return.g = second_color; color_return.b = third_color; break; case COLOR_ORDER_BGR: color_return.b = first_color; color_return.g = second_color; color_return.r = third_color; break; case COLOR_ORDER_GRB: color_return.g = first_color; color_return.r = second_color; color_return.b = third_color; break; } return color_return; }
static inline Color rgb332_to_color(uint8_t rgb332_color) { return to_color((uint32_t) rgb332_color, COLOR_ORDER_RGB, COLOR_BITNESS_332); }
static uint8_t color_to_332(Color color, ColorOrder color_order = ColorOrder::COLOR_ORDER_RGB) { uint16_t red_color, green_color, blue_color; red_color = esp_scale8(color.red, ((1 << 3) - 1)); green_color = esp_scale8(color.green, ((1 << 3) - 1)); blue_color = esp_scale8(color.blue, (1 << 2) - 1); switch (color_order) { case COLOR_ORDER_RGB: return red_color << 5 | green_color << 2 | blue_color; case COLOR_ORDER_BGR: return blue_color << 6 | green_color << 3 | red_color; case COLOR_ORDER_GRB: return green_color << 5 | red_color << 2 | blue_color; } return 0; }
static uint16_t color_to_565(Color color, ColorOrder color_order = ColorOrder::COLOR_ORDER_RGB) { uint16_t red_color, green_color, blue_color; red_color = esp_scale8(color.red, ((1 << 5) - 1)); green_color = esp_scale8(color.green, ((1 << 6) - 1)); blue_color = esp_scale8(color.blue, (1 << 5) - 1); switch (color_order) { case COLOR_ORDER_RGB: return red_color << 11 | green_color << 5 | blue_color; case COLOR_ORDER_BGR: return blue_color << 11 | green_color << 5 | red_color; case COLOR_ORDER_GRB: return green_color << 10 | red_color << 5 | blue_color; } return 0; }
static uint32_t color_to_grayscale4(Color color) { uint32_t gs4 = esp_scale8(color.white, 15); return gs4; }
static uint8_t color_to_index8_palette888(Color color, const uint8_t *palette) { uint8_t closest_index = 0; uint32_t minimum_dist2 = UINT32_MAX; int16_t tgt_r = color.r; int16_t tgt_g = color.g; int16_t tgt_b = color.b; uint16_t x, y, z; for (uint16_t i = 0; i < 256; i++) { int16_t plt_r = (int16_t) palette[i * 3 + 0]; int16_t plt_g = (int16_t) palette[i * 3 + 1]; int16_t plt_b = (int16_t) palette[i * 3 + 2]; x = (uint32_t) std::abs(tgt_r - plt_r); y = (uint32_t) std::abs(tgt_g - plt_g); z = (uint32_t) std::abs(tgt_b - plt_b); uint32_t dist2 = x * x + y * y + z * z; if (dist2 < minimum_dist2) { minimum_dist2 = dist2; closest_index = (uint8_t) i; } } return closest_index; }
static Color index8_to_color_palette888(uint8_t index, const uint8_t *palette) { Color color = Color(palette[index * 3 + 0], palette[index * 3 + 1], palette[index * 3 + 2], 0); return color; }
```

## `rect.h`

**class `Rect` — public interface:**
```cpp
int16_t x;
int16_t y;
int16_t w;
int16_t h;
Rect() : x(VALUE_NO_SET), y(VALUE_NO_SET), w(VALUE_NO_SET), h(VALUE_NO_SET) {}
inline Rect(int16_t x, int16_t y, int16_t w, int16_t h) ESPHOME_ALWAYS_INLINE : x(x), y(y), w(w), h(h) {}
inline int16_t x2() const { return this->x + this->w; }
inline int16_t y2() const { return this->y + this->h; }
inline bool is_set() const ESPHOME_ALWAYS_INLINE { return (this->h != VALUE_NO_SET) && (this->w != VALUE_NO_SET); }
void expand(int16_t horizontal, int16_t vertical);
void extend(Rect rect);
void shrink(Rect rect);
bool inside(Rect rect) const;
bool inside(int16_t test_x, int16_t test_y, bool absolute = true) const;
bool equal(Rect rect) const;
void info(const std::string &prefix = "rect info:");
```
