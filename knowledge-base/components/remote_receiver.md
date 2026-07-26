# ESPHome component: `remote_receiver`

Source: `esphome/components/remote_receiver/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `remote_receiver.h`

**class `RemoteReceiverComponent` — public interface:**
```cpp
RemoteReceiverComponent(InternalGPIOPin *pin) : RemoteReceiverBase(pin) {}
void setup() override;
void dump_config() override;
void loop() override;
#if defined(USE_ESP32) && SOC_RMT_SUPPORTED void set_filter_symbols(uint32_t filter_symbols) { this->filter_symbols_ = filter_symbols; }
void set_receive_symbols(uint32_t receive_symbols) { this->receive_symbols_ = receive_symbols; }
void set_with_dma(bool with_dma) { this->with_dma_ = with_dma; }
void set_carrier_duty_percent(uint8_t carrier_duty_percent) { this->carrier_duty_percent_ = carrier_duty_percent; }
void set_carrier_frequency(uint32_t carrier_frequency) { this->carrier_frequency_ = carrier_frequency; }
#endif void set_buffer_size(uint32_t buffer_size) { this->buffer_size_ = buffer_size; }
void set_filter_us(uint32_t filter_us) { this->filter_us_ = filter_us; }
void set_idle_us(uint32_t idle_us) { this->idle_us_ = idle_us; }
```
