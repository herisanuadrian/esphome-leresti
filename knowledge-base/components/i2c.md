# ESPHome component: `i2c`

Source: `esphome/components/i2c/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `i2c.h`

**class `I2CRegister` — public interface:**
```cpp
I2CRegister &operator=(uint8_t value);
I2CRegister &operator&=(uint8_t value);
I2CRegister &operator|=(uint8_t value);
explicit operator uint8_t() const { return get(); }
uint8_t get() const;
```

**class `I2CRegister16` — public interface:**
```cpp
I2CRegister16 &operator=(uint8_t value);
I2CRegister16 &operator&=(uint8_t value);
I2CRegister16 &operator|=(uint8_t value);
explicit operator uint8_t() const { return get(); }
uint8_t get() const;
```

**class `I2CDevice` — public interface:**
```cpp
I2CDevice() = default;
void set_i2c_address(uint8_t address) { address_ = address; }
uint8_t get_i2c_address() const { return this->address_; }
void set_i2c_bus(I2CBus *bus) { bus_ = bus; }
I2CRegister reg(uint8_t a_register) { return {this, a_register}; }
I2CRegister16 reg16(uint16_t a_register) { return {this, a_register}; }
ErrorCode read(uint8_t *data, size_t len) const { return bus_->write_readv(this->address_, nullptr, 0, data, len); }
ErrorCode read_register(uint8_t a_register, uint8_t *data, size_t len);
ErrorCode read_register16(uint16_t a_register, uint8_t *data, size_t len);
ErrorCode write(const uint8_t *data, size_t len) const { return bus_->write_readv(this->address_, data, len, nullptr, 0); }
ErrorCode write_read(const uint8_t *write_data, size_t write_len, uint8_t *read_data, size_t read_len) const { return bus_->write_readv(this->address_, write_data, write_len, read_data, read_len); }
ErrorCode write_register(uint8_t a_register, const uint8_t *data, size_t len) const;
ErrorCode write_register16(uint16_t a_register, const uint8_t *data, size_t len) const;
bool read_bytes(uint8_t a_register, uint8_t *data, uint8_t len) { return read_register(a_register, data, len) == ERROR_OK; }
bool read_bytes_raw(uint8_t *data, uint8_t len) const { return read(data, len) == ERROR_OK; }
template<size_t N> optional<std::array<uint8_t, N>> read_bytes(uint8_t a_register) { std::array<uint8_t, N> res; if (!this->read_bytes(a_register, res.data(), N)) { return {}; } return res; }
template<size_t N> optional<std::array<uint8_t, N>> read_bytes_raw() { std::array<uint8_t, N> res; if (!this->read_bytes_raw(res.data(), N)) { return {}; } return res; }
bool read_bytes_16(uint8_t a_register, uint16_t *data, uint8_t len);
bool read_byte(uint8_t a_register, uint8_t *data) { return read_register(a_register, data, 1) == ERROR_OK; }
optional<uint8_t> read_byte(uint8_t a_register) { uint8_t data; if (!this->read_byte(a_register, &data)) return {}; return data; }
bool read_byte_16(uint8_t a_register, uint16_t *data) { return read_bytes_16(a_register, data, 1); }
bool write_bytes(uint8_t a_register, const uint8_t *data, uint8_t len) const { return write_register(a_register, data, len) == ERROR_OK; }
bool write_bytes(uint8_t a_register, const std::vector<uint8_t> &data) const { return write_bytes(a_register, data.data(), data.size()); }
template<size_t N> bool write_bytes(uint8_t a_register, const std::array<uint8_t, N> &data) { return write_bytes(a_register, data.data(), data.size()); }
bool write_bytes_16(uint8_t a_register, const uint16_t *data, uint8_t len) const;
bool write_byte(uint8_t a_register, uint8_t data) const { return write_bytes(a_register, &data, 1); }
bool write_byte_16(uint8_t a_register, uint16_t data) const { return write_bytes_16(a_register, &data, 1); }
```

## `i2c_bus.h`

**Enums:**
```cpp
enum ErrorCode {
  NO_ERROR = 0,                
  ERROR_OK = 0,                
  ERROR_INVALID_ARGUMENT = 1,  
  ERROR_NOT_ACKNOWLEDGED = 2,  
  ERROR_TIMEOUT = 3,           
  ERROR_NOT_INITIALIZED = 4,   
  ERROR_TOO_LARGE = 5,         
  ERROR_UNKNOWN = 6,           
  ERROR_CRC = 7,               
};
```

**class `I2CBus` — public interface:**
```cpp
virtual ~I2CBus() = default;
virtual ErrorCode write_readv(uint8_t address, const uint8_t *write_buffer, size_t write_count, uint8_t *read_buffer, size_t read_count) = 0;
ErrorCode read(uint8_t address, uint8_t *buffer, size_t len) { return this->write_readv(address, nullptr, 0, buffer, len); }
ErrorCode write(uint8_t address, const uint8_t *buffer, size_t len, bool stop = true) { return this->write_readv(address, buffer, len, nullptr, 0); }
```

**class `InternalI2CBus` — public interface:**
```cpp
virtual int get_port() const = 0;
```

## `i2c_bus_arduino.h`

**Enums:**
```cpp
enum RecoveryCode {
  RECOVERY_FAILED_SCL_LOW,
  RECOVERY_FAILED_SDA_LOW,
  RECOVERY_COMPLETED,
};
```

**class `ArduinoI2CBus` — public interface:**
```cpp
void setup() override;
void dump_config() override;
ErrorCode write_readv(uint8_t address, const uint8_t *write_buffer, size_t write_count, uint8_t *read_buffer, size_t read_count) override;
float get_setup_priority() const override { return setup_priority::BUS; }
void set_scan(bool scan) { scan_ = scan; }
void set_sda_pin(uint8_t sda_pin) { sda_pin_ = sda_pin; }
void set_scl_pin(uint8_t scl_pin) { scl_pin_ = scl_pin; }
void set_frequency(uint32_t frequency) { frequency_ = frequency; }
void set_timeout(uint32_t timeout) { timeout_ = timeout; }
int get_port() const override { return 0; }
```

## `i2c_bus_esp_idf.h`

**Enums:**
```cpp
enum RecoveryCode {
  RECOVERY_FAILED_SCL_LOW,
  RECOVERY_FAILED_SDA_LOW,
  RECOVERY_COMPLETED,
};
```

**class `IDFI2CBus` — public interface:**
```cpp
void setup() override;
void dump_config() override;
ErrorCode write_readv(uint8_t address, const uint8_t *write_buffer, size_t write_count, uint8_t *read_buffer, size_t read_count) override;
float get_setup_priority() const override { return setup_priority::BUS; }
void set_scan(bool scan) { this->scan_ = scan; }
void set_sda_pin(uint8_t sda_pin) { this->sda_pin_ = sda_pin; }
void set_sda_pullup_enabled(bool sda_pullup_enabled) { this->sda_pullup_enabled_ = sda_pullup_enabled; }
void set_scl_pin(uint8_t scl_pin) { this->scl_pin_ = scl_pin; }
void set_scl_pullup_enabled(bool scl_pullup_enabled) { this->scl_pullup_enabled_ = scl_pullup_enabled; }
void set_frequency(uint32_t frequency) { this->frequency_ = frequency; }
void set_timeout(uint32_t timeout) { this->timeout_ = timeout; }
#if SOC_LP_I2C_SUPPORTED void set_lp_mode(bool lp_mode) { this->lp_mode_ = lp_mode; }
#endif int get_port() const override { return this->port_; }
```

## `i2c_bus_host.h`

**class `HostI2CBus` — public interface:**
```cpp
~HostI2CBus() override;
void setup() override;
void dump_config() override;
float get_setup_priority() const override { return setup_priority::BUS; }
ErrorCode write_readv(uint8_t address, const uint8_t *write_buffer, size_t write_count, uint8_t *read_buffer, size_t read_count) override;
void set_device(const std::string &device) { this->device_ = device; }
void set_scan(bool scan) { this->scan_ = scan; }
void set_frequency(uint32_t frequency) { this->frequency_ = frequency; }
const std::string &get_device() const { return this->device_; }
```

## `i2c_bus_zephyr.h`

**class `ZephyrI2CBus` — public interface:**
```cpp
explicit ZephyrI2CBus(const device *i2c_dev) : i2c_dev_(i2c_dev) {}
void setup() override;
void dump_config() override;
ErrorCode write_readv(uint8_t address, const uint8_t *write_buffer, size_t write_count, uint8_t *read_buffer, size_t read_count) override;
float get_setup_priority() const override { return setup_priority::BUS; }
void set_scan(bool scan) { scan_ = scan; }
void set_sda_pin(uint8_t sda_pin) { this->sda_pin_ = sda_pin; }
void set_scl_pin(uint8_t scl_pin) { this->scl_pin_ = scl_pin; }
void set_frequency(uint32_t frequency);
int get_port() const override { return 0; }
```
