# ESPHome component: `graphical_display_menu`

Source: `esphome/components/graphical_display_menu/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `graphical_display_menu.h`

**class `GraphicalDisplayMenu` — public interface:**
```cpp
void setup() override;
void dump_config() override;
void set_display(display::Display *display);
void set_font(display::BaseFont *font);
template<typename V> void set_menu_item_value(V menu_item_value) { this->menu_item_value_ = menu_item_value; }
void set_foreground_color(Color foreground_color);
void set_background_color(Color background_color);
template<typename F> void add_on_redraw_callback(F &&cb) { this->on_redraw_callbacks_.add(std::forward<F>(cb)); }
void draw(display::Display *display, const display::Rect *bounds);
```

**class `GraphicalDisplayMenuOnRedrawTrigger` — public interface:**
```cpp
explicit GraphicalDisplayMenuOnRedrawTrigger(GraphicalDisplayMenu *parent) : parent_(parent) { parent->add_on_redraw_callback([this]() { this->trigger(this->parent_); }); }
```
