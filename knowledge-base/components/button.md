# ESPHome component: `button`

Source: `esphome/components/button/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `PressAction` — public interface:**
```cpp
explicit PressAction(Button *button) : button_(button) {}
void play(const Ts &...x) override { this->button_->press(); }
```

**class `ButtonPressTrigger` — public interface:**
```cpp
ButtonPressTrigger(Button *button) { button->add_on_press_callback([this]() { this->trigger(); }); }
```

## `button.h`

**class `Button` — public interface:**
```cpp
void press();
template<typename F> void add_on_press_callback(F &&callback) { this->press_callback_.add(std::forward<F>(callback)); }
```
