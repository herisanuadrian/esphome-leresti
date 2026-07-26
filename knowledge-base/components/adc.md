# ESPHome component: `adc`

Source: `esphome/components/adc/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `adc_sensor.h`

**Enums:**
```cpp
enum class SamplingMode : uint8_t {
  AVG = 0,
  MIN = 1,
  MAX = 2,
};
```

**class `Aggregator` — public interface:**
```cpp
Aggregator(SamplingMode mode);
void add_sample(T value);
T aggregate();
```

**class `ADCSensor` — public interface:**
```cpp
void update() override;
void setup() override;
void dump_config() override;
#ifdef USE_ZEPHYR void set_adc_channel(const adc_dt_spec *channel) { this->channel_ = channel; }
#endif void set_pin(InternalGPIOPin *pin) { this->pin_ = pin; }
void set_output_raw(bool output_raw) { this->output_raw_ = output_raw; }
void set_sample_count(uint8_t sample_count);
void set_sampling_mode(SamplingMode sampling_mode);
float sample() override;
#ifdef USE_ESP32 void set_attenuation(adc_atten_t attenuation) { this->attenuation_ = attenuation; }
void set_channel(adc_unit_t unit, adc_channel_t channel) { this->adc_unit_ = unit; this->channel_ = channel; }
void set_autorange(bool autorange) { this->autorange_ = autorange; }
#endif #ifdef USE_RP2 void set_is_temperature() { this->is_temperature_ = true; }
#endif protected: uint8_t sample_count_{1}
bool output_raw_{false}
InternalGPIOPin *pin_;
SamplingMode sampling_mode_{SamplingMode::AVG}
#ifdef USE_ESP32 float sample_autorange_();
float sample_fixed_attenuation_();
bool autorange_{false}
adc_oneshot_unit_handle_t adc_handle_{nullptr}
adc_cali_handle_t calibration_handle_{nullptr}
adc_atten_t attenuation_{ADC_ATTEN_DB_0}
adc_channel_t channel_{}
adc_unit_t adc_unit_{}
struct SetupFlags { uint8_t init_complete : 1; uint8_t config_complete : 1; uint8_t handle_init_complete : 1; uint8_t calibration_complete : 1; uint8_t reserved : 4; }
setup_flags_{}
static adc_oneshot_unit_handle_t shared_adc_handles[2];
#endif #ifdef USE_RP2 bool is_temperature_{false}
#endif #ifdef USE_ZEPHYR const struct adc_dt_spec *channel_ = nullptr;
```
