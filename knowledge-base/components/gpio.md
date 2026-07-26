# ESPHome component: `gpio`

Source: `esphome/components/gpio/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `binary_sensor/gpio_binary_sensor.h`

**class `GPIOBinarySensorStore` — public interface:**
```cpp
void setup(InternalGPIOPin *pin, Component *component);
static void gpio_intr(GPIOBinarySensorStore *arg);
bool get_state() const { return this->state_; }
bool is_changed() const { return this->changed_; }
void clear_changed() { this->changed_ = false; }
```

**class `GPIOBinarySensor` — public interface:**
```cpp
void set_pin(GPIOPin *pin) { this->pin_ = pin; }
void set_use_interrupt(bool use_interrupt) { this->store_.use_interrupt_ = use_interrupt; }
void set_interrupt_type(gpio::InterruptType type) { this->store_.interrupt_type_ = type; }
void setup() override;
void dump_config() override;
float get_setup_priority() const override;
void loop() override;
```

## `one_wire/gpio_one_wire.h`

**class `GPIOOneWireBus` — public interface:**
```cpp
void setup() override;
void dump_config() override;
float get_setup_priority() const override { return setup_priority::BUS; }
void set_pin(InternalGPIOPin *pin) { this->t_pin_ = pin; this->pin_ = pin->to_isr(); }
void write8(uint8_t val) override;
void write64(uint64_t val) override;
uint8_t read8() override;
uint64_t read64() override;
```

## `output/gpio_binary_output.h`

**class `GPIOBinaryOutput` — public interface:**
```cpp
void set_pin(GPIOPin *pin) { pin_ = pin; }
void setup() override { this->turn_off(); this->pin_->setup(); this->turn_off(); }
void dump_config() override;
float get_setup_priority() const override { return setup_priority::HARDWARE; }
```

## `switch/gpio_switch.h`

**class `GPIOSwitch` — public interface:**
```cpp
void set_pin(GPIOPin *pin) { pin_ = pin; }
float get_setup_priority() const override;
void setup() override;
void dump_config() override;
#ifdef USE_GPIO_SWITCH_INTERLOCK void set_interlock(const std::initializer_list<Switch *> &interlock);
void set_interlock_wait_time(uint32_t interlock_wait_time) { interlock_wait_time_ = interlock_wait_time; }
#endif protected: void write_state(bool state) override;
GPIOPin *pin_;
#ifdef USE_GPIO_SWITCH_INTERLOCK FixedVector<Switch *> interlock_;
uint32_t interlock_wait_time_{0}
```
