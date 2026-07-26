# ESPHome component: `spi`

Source: `esphome/components/spi/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `spi.h`

**Enums:**
```cpp
enum SPIBitOrder {
  BIT_ORDER_LSB_FIRST,
  BIT_ORDER_MSB_FIRST,
};
enum SPIClockPolarity {
  CLOCK_POLARITY_LOW = false,
  CLOCK_POLARITY_HIGH = true,
};
enum SPIClockPhase {
  CLOCK_PHASE_LEADING,
  CLOCK_PHASE_TRAILING,
};
enum SPIMode {
  MODE0 = 0,
  MODE1 = 1,
  MODE2 = 2,
  MODE3 = 3,
};
enum SPIDataRate : uint32_t {
  DATA_RATE_1KHZ = 1000,
  DATA_RATE_75KHZ = 75000,
  DATA_RATE_200KHZ = 200000,
  DATA_RATE_1MHZ = 1000000,
  DATA_RATE_2MHZ = 2000000,
  DATA_RATE_4MHZ = 4000000,
  DATA_RATE_5MHZ = 5000000,
  DATA_RATE_8MHZ = 8000000,
  DATA_RATE_10MHZ = 10000000,
  DATA_RATE_20MHZ = 20000000,
  DATA_RATE_40MHZ = 40000000,
  DATA_RATE_80MHZ = 80000000,
};
```

**class `NullPin` — public interface:**
```cpp
void setup() override {}
void pin_mode(gpio::Flags flags) override {}
gpio::Flags get_flags() const override { return gpio::Flags::FLAG_NONE; }
bool digital_read() override { return false; }
void digital_write(bool value) override {}
size_t dump_summary(char *buffer, size_t len) const override { if (len > 0) buffer[0] = '\0'; return 0; }
```

**class `Utility` — public interface:**
```cpp
static int get_pin_no(GPIOPin *pin) { if (pin == nullptr || !pin->is_internal()) return -1; if (((InternalGPIOPin *) pin)->is_inverted()) return -1; return ((InternalGPIOPin *) pin)->get_pin(); }
static SPIMode get_mode(SPIClockPolarity polarity, SPIClockPhase phase) { if (polarity == CLOCK_POLARITY_HIGH) { return phase == CLOCK_PHASE_LEADING ? MODE2 : MODE3; } return phase == CLOCK_PHASE_LEADING ? MODE0 : MODE1; }
static SPIClockPhase get_phase(SPIMode mode) { switch (mode) { case MODE0: case MODE2: return CLOCK_PHASE_LEADING; default: return CLOCK_PHASE_TRAILING; } }
static SPIClockPolarity get_polarity(SPIMode mode) { switch (mode) { case MODE0: case MODE1: return CLOCK_POLARITY_LOW; default: return CLOCK_POLARITY_HIGH; } }
```

**class `SPIDelegate` — public interface:**
```cpp
SPIDelegate() = default;
SPIDelegate(uint32_t data_rate, SPIBitOrder bit_order, SPIMode mode, GPIOPin *cs_pin) : bit_order_(bit_order), data_rate_(data_rate), mode_(mode), cs_pin_(cs_pin) { if (this->cs_pin_ == nullptr) this->cs_pin_ = NullPin::NULL_PIN; this->cs_pin_->setup(); this->cs_pin_->digital_write(true); }
virtual ~SPIDelegate(){}
virtual void begin_transaction() { this->cs_pin_->digital_write(false); }
virtual void end_transaction() { this->cs_pin_->digital_write(true); }
virtual uint8_t transfer(uint8_t data) = 0;
virtual void transfer(uint8_t *ptr, size_t length) { this->transfer(ptr, ptr, length); }
virtual void transfer(const uint8_t *txbuf, uint8_t *rxbuf, size_t length) { for (size_t i = 0; i != length; i++) rxbuf[i] = this->transfer(txbuf[i]); }
virtual void write(uint16_t data, size_t num_bits) { esph_log_e("spi_device", "variable length write not implemented"); }
virtual void write_cmd_addr_data(size_t cmd_bits, uint32_t cmd, size_t addr_bits, uint32_t address, const uint8_t *data, size_t length, uint8_t bus_width) { esph_log_e("spi_device", "write_cmd_addr_data not implemented"); }
virtual void write16(uint16_t data) { if (this->bit_order_ == BIT_ORDER_MSB_FIRST) { uint16_t buffer; buffer = (data >> 8) | (data << 8); this->write_array(reinterpret_cast<const uint8_t *>(&buffer), 2); } else { this->write_array(reinterpret_cast<const uint8_t *>(&data), 2); } }
virtual void write_array16(const uint16_t *data, size_t length) { for (size_t i = 0; i != length; i++) { this->write16(data[i]); } }
virtual void write_array(const uint8_t *ptr, size_t length) { for (size_t i = 0; i != length; i++) this->transfer(ptr[i]); }
virtual void read_array(uint8_t *ptr, size_t length) { for (size_t i = 0; i != length; i++) ptr[i] = this->transfer(0); }
virtual bool is_ready();
```

**class `SPIDelegateDummy` — public interface:**
```cpp
SPIDelegateDummy() = default;
uint8_t transfer(uint8_t data) override { return 0; }
void end_transaction() override{}
void begin_transaction() override;
```

**class `SPIDelegateBitBash` — public interface:**
```cpp
SPIDelegateBitBash(uint32_t clock, SPIBitOrder bit_order, SPIMode mode, GPIOPin *cs_pin, GPIOPin *clk_pin, GPIOPin *sdo_pin, GPIOPin *sdi_pin) : SPIDelegate(clock, bit_order, mode, cs_pin), clk_pin_(clk_pin), sdo_pin_(sdo_pin), sdi_pin_(sdi_pin) { this->wait_cycle_ = uint32_t(arch_get_cpu_freq_hz()) / this->data_rate_ / 2ULL; this->clock_polarity_ = Utility::get_polarity(this->mode_); this->clock_phase_ = Utility::get_phase(this->mode_); }
uint8_t transfer(uint8_t data) override;
void write(uint16_t data, size_t num_bits) override;
void write16(uint16_t data) override { this->write(data, 16); }
```

**class `SPIBus` — public interface:**
```cpp
SPIBus() = default;
SPIBus(GPIOPin *clk, GPIOPin *sdo, GPIOPin *sdi) : clk_pin_(clk), sdo_pin_(sdo), sdi_pin_(sdi) {}
virtual SPIDelegate *get_delegate(uint32_t data_rate, SPIBitOrder bit_order, SPIMode mode, GPIOPin *cs_pin, bool release_device, bool write_only) { return new SPIDelegateBitBash(data_rate, bit_order, mode, cs_pin, this->clk_pin_, this->sdo_pin_, this->sdi_pin_); }
virtual bool is_hw() { return false; }
```

**class `SPIComponent` — public interface:**
```cpp
SPIDelegate *register_device(SPIClient *device, SPIMode mode, SPIBitOrder bit_order, uint32_t data_rate, GPIOPin *cs_pin, bool release_device, bool write_only);
void unregister_device(SPIClient *device);
void set_clk(GPIOPin *clk) { this->clk_pin_ = clk; }
void set_miso(GPIOPin *sdi) { this->sdi_pin_ = sdi; }
void set_mosi(GPIOPin *sdo) { this->sdo_pin_ = sdo; }
void set_data_pins(std::vector<uint8_t> pins) { this->data_pins_ = std::move(pins); }
void set_interface(SPIInterface interface) { this->interface_ = interface; this->using_hw_ = true; }
void set_interface_name(const char *name) { this->interface_name_ = name; }
float get_setup_priority() const override { return setup_priority::BUS; }
void setup() override;
void dump_config() override;
size_t get_bus_width() const { if (this->data_pins_.empty()) { return 1; } return this->data_pins_.size(); }
```

**class `SPIClient` — public interface:**
```cpp
SPIClient(SPIBitOrder bit_order, SPIMode mode, uint32_t data_rate) : bit_order_(bit_order), mode_(mode), data_rate_(data_rate) {}
virtual void spi_setup() { esph_log_d("spi_device", "mode %u, data_rate %ukHz", (unsigned) this->mode_, (unsigned) (this->data_rate_ / 1000)); this->delegate_ = this->parent_->register_device(this, this->mode_, this->bit_order_, this->data_rate_, this->cs_, this->release_device_, this->write_only_); }
virtual void spi_teardown() { this->parent_->unregister_device(this); this->delegate_ = SPIDelegate::NULL_DELEGATE; }
bool spi_is_ready() { return this->delegate_->is_ready(); }
void set_release_device(bool release) { this->release_device_ = release; }
void set_write_only(bool write_only) { this->write_only_ = write_only; }
```

**class `SPIDevice` — public interface:**
```cpp
SPIDevice() : SPIClient(BIT_ORDER, Utility::get_mode(CLOCK_POLARITY, CLOCK_PHASE), DATA_RATE) {}
SPIDevice(SPIComponent *parent, GPIOPin *cs_pin) { this->set_spi_parent(parent); this->set_cs_pin(cs_pin); }
void spi_setup() override { SPIClient::spi_setup(); }
void spi_teardown() override { SPIClient::spi_teardown(); }
void set_spi_parent(SPIComponent *parent) { this->parent_ = parent; }
void set_cs_pin(GPIOPin *cs) { this->cs_ = cs; }
void set_data_rate(uint32_t data_rate) { this->data_rate_ = data_rate; }
void set_bit_order(SPIBitOrder order) { this->bit_order_ = order; }
void set_mode(SPIMode mode) { this->mode_ = mode; }
uint8_t read_byte() { return this->delegate_->transfer(0); }
void read_array(uint8_t *data, size_t length) { this->delegate_->read_array(data, length); }
void write(uint16_t data, size_t num_bits) { this->delegate_->write(data, num_bits); }
void write_cmd_addr_data(size_t cmd_bits, uint32_t cmd, size_t addr_bits, uint32_t address, const uint8_t *data, size_t length, uint8_t bus_width = 1) { this->delegate_->write_cmd_addr_data(cmd_bits, cmd, addr_bits, address, data, length, bus_width); }
void write_byte(uint8_t data) { this->delegate_->write_array(&data, 1); }
void transfer_array(uint8_t *data, size_t length) { this->delegate_->transfer(data, length); }
uint8_t transfer_byte(uint8_t data) { return this->delegate_->transfer(data); }
void write_byte16(uint16_t data) { this->delegate_->write16(data); }
void write_array16(const uint16_t *data, size_t length) { this->delegate_->write_array16(data, length); }
void enable() { this->delegate_->begin_transaction(); }
void disable() { this->delegate_->end_transaction(); }
void write_array(const uint8_t *data, size_t length) { this->delegate_->write_array(data, length); }
template<size_t N> void write_array(const std::array<uint8_t, N> &data) { this->write_array(data.data(), N); }
void write_array(const std::vector<uint8_t> &data) { this->write_array(data.data(), data.size()); }
template<size_t N> void transfer_array(std::array<uint8_t, N> &data) { this->transfer_array(data.data(), N); }
```
