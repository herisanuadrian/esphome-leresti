# ESPHome component: `one_wire`

Source: `esphome/components/one_wire/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `one_wire.h`

**class `OneWireDevice` — public interface:**
```cpp
void set_address(uint64_t address);
void set_index(uint8_t index) { this->index_ = index; }
void set_one_wire_bus(OneWireBus *bus) { this->bus_ = bus; }
const std::string &get_address_name();
```

## `one_wire_bus.h`

**class `OneWireBus` — public interface:**
```cpp
virtual void write8(uint8_t val) = 0;
virtual void write64(uint64_t val) = 0;
bool skip();
virtual uint8_t read8() = 0;
virtual uint64_t read64() = 0;
bool select(uint64_t address);
const std::vector<uint64_t> &get_devices();
void search();
const LogString *get_model_str(uint8_t model);
```
