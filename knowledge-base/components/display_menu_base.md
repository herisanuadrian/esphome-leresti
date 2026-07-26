# ESPHome component: `display_menu_base`

Source: `esphome/components/display_menu_base/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `UpAction` — public interface:**
```cpp
explicit UpAction(DisplayMenuComponent *menu) : menu_(menu) {}
void play(const Ts &...x) override { this->menu_->up(); }
```

**class `DownAction` — public interface:**
```cpp
explicit DownAction(DisplayMenuComponent *menu) : menu_(menu) {}
void play(const Ts &...x) override { this->menu_->down(); }
```

**class `LeftAction` — public interface:**
```cpp
explicit LeftAction(DisplayMenuComponent *menu) : menu_(menu) {}
void play(const Ts &...x) override { this->menu_->left(); }
```

**class `RightAction` — public interface:**
```cpp
explicit RightAction(DisplayMenuComponent *menu) : menu_(menu) {}
void play(const Ts &...x) override { this->menu_->right(); }
```

**class `EnterAction` — public interface:**
```cpp
explicit EnterAction(DisplayMenuComponent *menu) : menu_(menu) {}
void play(const Ts &...x) override { this->menu_->enter(); }
```

**class `ShowAction` — public interface:**
```cpp
explicit ShowAction(DisplayMenuComponent *menu) : menu_(menu) {}
void play(const Ts &...x) override { this->menu_->show(); }
```

**class `HideAction` — public interface:**
```cpp
explicit HideAction(DisplayMenuComponent *menu) : menu_(menu) {}
void play(const Ts &...x) override { this->menu_->hide(); }
```

**class `ShowMainAction` — public interface:**
```cpp
explicit ShowMainAction(DisplayMenuComponent *menu) : menu_(menu) {}
void play(const Ts &...x) override { this->menu_->show_main(); }
```

**class `IsActiveCondition` — public interface:**
```cpp
explicit IsActiveCondition(DisplayMenuComponent *menu) : menu_(menu) {}
bool check(const Ts &...x) override { return this->menu_->is_active(); }
```

**class `DisplayMenuOnEnterTrigger` — public interface:**
```cpp
explicit DisplayMenuOnEnterTrigger(MenuItem *parent) : parent_(parent) { parent->add_on_enter_callback([this]() { this->trigger(this->parent_); }); }
```

**class `DisplayMenuOnLeaveTrigger` — public interface:**
```cpp
explicit DisplayMenuOnLeaveTrigger(MenuItem *parent) : parent_(parent) { parent->add_on_leave_callback([this]() { this->trigger(this->parent_); }); }
```

**class `DisplayMenuOnValueTrigger` — public interface:**
```cpp
explicit DisplayMenuOnValueTrigger(MenuItem *parent) : parent_(parent) { parent->add_on_value_callback([this]() { this->trigger(this->parent_); }); }
```

**class `DisplayMenuOnNextTrigger` — public interface:**
```cpp
explicit DisplayMenuOnNextTrigger(MenuItemCustom *parent) : parent_(parent) { parent->add_on_next_callback([this]() { this->trigger(this->parent_); }); }
```

**class `DisplayMenuOnPrevTrigger` — public interface:**
```cpp
explicit DisplayMenuOnPrevTrigger(MenuItemCustom *parent) : parent_(parent) { parent->add_on_prev_callback([this]() { this->trigger(this->parent_); }); }
```

## `display_menu_base.h`

**Enums:**
```cpp
enum MenuMode {
  MENU_MODE_ROTARY,
  MENU_MODE_JOYSTICK,
};
```

**class `DisplayMenuComponent` — public interface:**
```cpp
void set_root_item(MenuItemMenu *item) { this->displayed_item_ = this->root_item_ = item; }
void set_active(bool active) { this->active_ = active; }
void set_mode(MenuMode mode) { this->mode_ = mode; }
void set_rows(uint8_t rows) { this->rows_ = rows; }
float get_setup_priority() const override { return setup_priority::PROCESSOR; }
void up();
void down();
void left();
void right();
void enter();
void show_main();
void show();
void hide();
void draw();
bool is_active() const { return this->active_; }
```

## `menu_item.h`

**Enums:**
```cpp
enum MenuItemType {
  MENU_ITEM_LABEL,
  MENU_ITEM_MENU,
  MENU_ITEM_BACK,
  MENU_ITEM_SELECT,
  MENU_ITEM_NUMBER,
  MENU_ITEM_SWITCH,
  MENU_ITEM_COMMAND,
  MENU_ITEM_CUSTOM,
};
```

**class `MenuItem` — public interface:**
```cpp
explicit MenuItem(MenuItemType t) : item_type_(t) {}
void set_parent(MenuItemMenu *parent) { this->parent_ = parent; }
MenuItemMenu *get_parent() { return this->parent_; }
MenuItemType get_type() const { return this->item_type_; }
template<typename V> void set_text(V val) { this->text_ = val; }
template<typename F> void add_on_enter_callback(F &&cb) { this->on_enter_callbacks_.add(std::forward<F>(cb)); }
template<typename F> void add_on_leave_callback(F &&cb) { this->on_leave_callbacks_.add(std::forward<F>(cb)); }
template<typename F> void add_on_value_callback(F &&cb) { this->on_value_callbacks_.add(std::forward<F>(cb)); }
std::string get_text() const { return const_cast<MenuItem *>(this)->text_.value(this); }
virtual bool get_immediate_edit() const { return false; }
virtual bool has_value() const { return false; }
virtual std::string get_value_text() const { return ""; }
virtual bool select_next() { return false; }
virtual bool select_prev() { return false; }
void on_enter();
void on_leave();
```

**class `MenuItemMenu` — public interface:**
```cpp
explicit MenuItemMenu() : MenuItem(MENU_ITEM_MENU) {}
void add_item(MenuItem *item) { item->set_parent(this); this->items_.push_back(item); }
size_t items_size() const { return this->items_.size(); }
MenuItem *get_item(size_t i) { return this->items_[i]; }
```

**class `MenuItemEditable` — public interface:**
```cpp
explicit MenuItemEditable(MenuItemType t) : MenuItem(t) {}
void set_immediate_edit(bool val) { this->immediate_edit_ = val; }
bool get_immediate_edit() const override { return this->immediate_edit_; }
void set_value_lambda(value_getter_t &&getter) { this->value_getter_ = getter; }
```

**class `MenuItemSelect` — public interface:**
```cpp
explicit MenuItemSelect() : MenuItemEditable(MENU_ITEM_SELECT) {}
void set_select_variable(select::Select *var) { this->select_var_ = var; }
bool has_value() const override { return true; }
std::string get_value_text() const override;
bool select_next() override;
bool select_prev() override;
```

**class `MenuItemNumber` — public interface:**
```cpp
explicit MenuItemNumber() : MenuItemEditable(MENU_ITEM_NUMBER) {}
void set_number_variable(number::Number *var) { this->number_var_ = var; }
void set_format(const std::string &fmt) { this->format_ = fmt; }
bool has_value() const override { return true; }
std::string get_value_text() const override;
bool select_next() override;
bool select_prev() override;
```

**class `MenuItemSwitch` — public interface:**
```cpp
explicit MenuItemSwitch() : MenuItemEditable(MENU_ITEM_SWITCH) {}
void set_switch_variable(switch_::Switch *var) { this->switch_var_ = var; }
void set_on_text(const std::string &t) { this->switch_on_text_ = t; }
void set_off_text(const std::string &t) { this->switch_off_text_ = t; }
bool has_value() const override { return true; }
std::string get_value_text() const override;
bool select_next() override;
bool select_prev() override;
```

**class `MenuItemCommand` — public interface:**
```cpp
explicit MenuItemCommand() : MenuItem(MENU_ITEM_COMMAND) {}
bool select_next() override;
bool select_prev() override;
```

**class `MenuItemCustom` — public interface:**
```cpp
explicit MenuItemCustom() : MenuItemEditable(MENU_ITEM_CUSTOM) {}
template<typename F> void add_on_next_callback(F &&cb) { this->on_next_callbacks_.add(std::forward<F>(cb)); }
template<typename F> void add_on_prev_callback(F &&cb) { this->on_prev_callbacks_.add(std::forward<F>(cb)); }
bool has_value() const override { return this->value_getter_.has_value(); }
std::string get_value_text() const override;
bool select_next() override;
bool select_prev() override;
```
