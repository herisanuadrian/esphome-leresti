# ESPHome component: `power_supply`

Source: `esphome/components/power_supply/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `power_supply.h`

**class `PowerSupply` — public interface:**
```cpp
void set_pin(GPIOPin *pin) { pin_ = pin; }
void set_enable_time(uint32_t enable_time) { enable_time_ = enable_time; }
void set_keep_on_time(uint32_t keep_on_time) { keep_on_time_ = keep_on_time; }
void set_enable_on_boot(bool enable_on_boot) { enable_on_boot_ = enable_on_boot; }
bool is_enabled() const;
void request_high_power();
void unrequest_high_power();
void setup() override;
void dump_config() override;
float get_setup_priority() const override;
void on_powerdown() override;
```

**class `PowerSupplyRequester` — public interface:**
```cpp
void set_parent(PowerSupply *parent) { parent_ = parent; }
void request() { if (!this->requested_ && this->parent_ != nullptr) { this->parent_->request_high_power(); this->requested_ = true; } }
void unrequest() { if (this->requested_ && this->parent_ != nullptr) { this->parent_->unrequest_high_power(); this->requested_ = false; } }
```
