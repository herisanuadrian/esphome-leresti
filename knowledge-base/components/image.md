# ESPHome component: `image`

Source: `esphome/components/image/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `image.h`

**Enums:**
```cpp
enum ImageType {
  IMAGE_TYPE_BINARY = 0,
  IMAGE_TYPE_GRAYSCALE = 1,
  IMAGE_TYPE_RGB = 2,
  IMAGE_TYPE_RGB565 = 3,
};
enum Transparency {
  TRANSPARENCY_OPAQUE = 0,
  TRANSPARENCY_CHROMA_KEY = 1,
  TRANSPARENCY_ALPHA_CHANNEL = 2,
};
```

**class `Image` — public interface:**
```cpp
Image(const uint8_t *data_start, int width, int height, ImageType type, Transparency transparency);
Color get_pixel(int x, int y, Color color_on = display::COLOR_ON, Color color_off = display::COLOR_OFF) const;
int get_width() const override;
int get_height() const override;
const uint8_t *get_data_start() const { return this->data_start_; }
ImageType get_type() const;
int get_bpp() const { return this->bpp_; }
size_t get_width_stride() const { return (this->width_ * this->get_bpp() + 7u) / 8u; }
void draw(int x, int y, display::Display *display, Color color_on, Color color_off) override;
bool has_transparency() const { return this->transparency_ != TRANSPARENCY_OPAQUE; }
#ifdef USE_LVGL lv_image_dsc_t *get_lv_image_dsc();
#endif protected: bool get_binary_pixel_(int x, int y) const;
Color get_rgb_pixel_(int x, int y) const;
Color get_rgb565_pixel_(int x, int y) const;
Color get_grayscale_pixel_(int x, int y) const;
int width_;
int height_;
ImageType type_;
const uint8_t *data_start_;
Transparency transparency_;
size_t bpp_{}
size_t stride_{}
#ifdef USE_LVGL lv_img_dsc_t dsc_{}
```
