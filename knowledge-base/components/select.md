# ESPHome component: `select`

Source: `esphome/components/select/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `SelectStateTrigger` — public interface:**
```cpp
explicit SelectStateTrigger(Select *parent) : parent_(parent) { parent->add_on_state_callback( [this](size_t index) { this->trigger(StringRef(this->parent_->option_at(index)), index); }); }
```

**class `SelectSetAction` — public interface:**
```cpp
explicit SelectSetAction(Select *select) : select_(select) {}
TEMPLATABLE_VALUE(std::string, option) void play(const Ts &...x) override { auto call = this->select_->make_call(); call.set_option(this->option_.value(x...)); call.perform(); }
```

**class `SelectSetIndexAction` — public interface:**
```cpp
explicit SelectSetIndexAction(Select *select) : select_(select) {}
TEMPLATABLE_VALUE(size_t, index) void play(const Ts &...x) override { auto call = this->select_->make_call(); call.set_index(this->index_.value(x...)); call.perform(); }
```

**class `SelectOperationAction` — public interface:**
```cpp
explicit SelectOperationAction(Select *select) : select_(select) {}
TEMPLATABLE_VALUE(bool, cycle) TEMPLATABLE_VALUE(SelectOperation, operation) void play(const Ts &...x) override { auto call = this->select_->make_call(); call.with_operation(this->operation_.value(x...)); if (this->cycle_.has_value()) { call.with_cycle(this->cycle_.value(x...)); } call.perform(); }
```

**class `SelectIsCondition` — public interface:**
```cpp
SelectIsCondition(Select *parent, const char *const *option_list) : parent_(parent), option_list_(option_list) {}
bool check(const Ts &...x) override { auto current = this->parent_->current_option(); for (size_t i = 0; i != N; i++) { if (current == this->option_list_[i]) { return true; } } return false; }
```

## `select.h`

**class `Select` — public interface:**
```cpp
SelectTraits traits;
Select() = default;
~Select() = default;
void publish_state(const std::string &state);
void publish_state(const char *state);
void publish_state(size_t index);
StringRef current_option() const;
SelectCall make_call() { return SelectCall(this); }
bool has_option(const std::string &option) const;
bool has_option(const char *option) const;
bool has_index(size_t index) const;
size_t size() const;
optional<size_t> index_of(const char *option, size_t len) const;
optional<size_t> index_of(const std::string &option) const { return this->index_of(option.data(), option.size()); }
optional<size_t> index_of(const char *option) const { return this->index_of(option, strlen(option)); }
optional<size_t> active_index() const;
optional<std::string> at(size_t index) const;
const char *option_at(size_t index) const;
template<typename F> void add_on_state_callback(F &&callback) { this->state_callback_.add(std::forward<F>(callback)); }
```

## `select_call.h`

**Enums:**
```cpp
enum SelectOperation {
  SELECT_OP_NONE,
  SELECT_OP_SET,
  SELECT_OP_NEXT,
  SELECT_OP_PREVIOUS,
  SELECT_OP_FIRST,
  SELECT_OP_LAST
};
```

**class `SelectCall` — public interface:**
```cpp
explicit SelectCall(Select *parent) : parent_(parent) {}
void perform();
SelectCall &set_option(const char *option, size_t len);
SelectCall &set_option(const std::string &option) { return this->set_option(option.data(), option.size()); }
SelectCall &set_option(const char *option) { return this->set_option(option, strlen(option)); }
SelectCall &set_index(size_t index);
SelectCall &select_next(bool cycle);
SelectCall &select_previous(bool cycle);
SelectCall &select_first();
SelectCall &select_last();
SelectCall &with_operation(SelectOperation operation);
SelectCall &with_cycle(bool cycle);
SelectCall &with_option(const char *option, size_t len);
SelectCall &with_option(const std::string &option) { return this->with_option(option.data(), option.size()); }
SelectCall &with_option(const char *option) { return this->with_option(option, strlen(option)); }
SelectCall &with_index(size_t index);
```

## `select_traits.h`

**class `SelectTraits` — public interface:**
```cpp
void set_options(const std::initializer_list<const char *> &options);
void set_options(const FixedVector<const char *> &options);
const FixedVector<const char *> &get_options() const;
```
