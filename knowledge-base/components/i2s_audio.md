# ESPHome component: `i2s_audio`

Source: `esphome/components/i2s_audio/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `i2s_audio.h`

**class `I2SAudioBase` — public interface:**
```cpp
void set_i2s_role(i2s_role_t role) { this->i2s_role_ = role; }
void set_slot_mode(i2s_slot_mode_t slot_mode) { this->slot_mode_ = slot_mode; }
void set_std_slot_mask(i2s_std_slot_mask_t std_slot_mask) { this->std_slot_mask_ = std_slot_mask; }
void set_slot_bit_width(i2s_slot_bit_width_t slot_bit_width) { this->slot_bit_width_ = slot_bit_width; }
void set_sample_rate(uint32_t sample_rate) { this->sample_rate_ = sample_rate; }
void set_use_apll(uint32_t use_apll) { this->use_apll_ = use_apll; }
void set_mclk_multiple(i2s_mclk_multiple_t mclk_multiple) { this->mclk_multiple_ = mclk_multiple; }
```

**class `I2SAudioComponent` — public interface:**
```cpp
i2s_std_gpio_config_t get_pin_config() const { return {.mclk = (gpio_num_t) this->mclk_pin_, .bclk = (gpio_num_t) this->bclk_pin_, .ws = (gpio_num_t) this->lrclk_pin_, .dout = I2S_GPIO_UNUSED, .din = I2S_GPIO_UNUSED, .invert_flags = { .mclk_inv = false, .bclk_inv = false, .ws_inv = false, }}; }
void set_mclk_pin(int pin) { this->mclk_pin_ = pin; }
void set_bclk_pin(int pin) { this->bclk_pin_ = pin; }
void set_lrclk_pin(int pin) { this->lrclk_pin_ = pin; }
void set_port(int port) { this->port_ = port; }
#if ESP_IDF_VERSION >= ESP_IDF_VERSION_VAL(6, 0, 0) int get_port() const { return this->port_; }
#else i2s_port_t get_port() const { return static_cast<i2s_port_t>(this->port_); }
#endif void lock() { this->lock_.lock(); }
bool try_lock() { return this->lock_.try_lock(); }
void unlock() { this->lock_.unlock(); }
```

## `microphone/i2s_audio_microphone.h`

**class `I2SAudioMicrophone` — public interface:**
```cpp
void setup() override;
void dump_config() override;
void start() override;
void stop() override;
void loop() override;
void set_correct_dc_offset(bool correct_dc_offset) { this->correct_dc_offset_ = correct_dc_offset; }
void set_din_pin(int8_t pin) { this->din_pin_ = (gpio_num_t) pin; }
void set_pdm(bool pdm) { this->pdm_ = pdm; }
```

## `speaker/i2s_audio_spdif.h`

**class `I2SAudioSpeakerSPDIF` — public interface:**
```cpp
void setup() override;
void dump_config() override;
size_t play(const uint8_t *data, size_t length, TickType_t ticks_to_wait) override;
```

## `speaker/i2s_audio_speaker.h`

**Enums:**
```cpp
enum SpeakerEventGroupBits : uint32_t {
  COMMAND_START = (1 << 0),            
  COMMAND_STOP = (1 << 1),             
  COMMAND_STOP_GRACEFULLY = (1 << 2),  
  TASK_STARTING = (1 << 10),
  TASK_RUNNING = (1 << 11),
  TASK_STOPPING = (1 << 12),
  TASK_STOPPED = (1 << 13),
  ERR_ESP_NO_MEM = (1 << 19),
  ERR_DROPPED_EVENT = (1 << 20),    
  ERR_PARTIAL_WRITE = (1 << 21),    
  ERR_LOCKSTEP_DESYNC = (1 << 22),  
  ALL_BITS = 0x00FFFFFF,  
};
```

**class `I2SAudioSpeakerBase` — public interface:**
```cpp
float get_setup_priority() const override { return esphome::setup_priority::PROCESSOR; }
void setup() override;
void dump_config() override;
void loop() override;
void set_buffer_duration(uint32_t buffer_duration_ms) { this->buffer_duration_ms_ = buffer_duration_ms; }
void set_timeout(uint32_t ms) { this->timeout_ = ms; }
void set_dout_pin(uint8_t pin) { this->dout_pin_ = (gpio_num_t) pin; }
i2s_chan_handle_t get_tx_handle() const { return this->tx_handle_; }
void start() override;
void stop() override;
void finish() override;
void set_pause_state(bool pause_state) override { this->pause_state_ = pause_state; }
bool get_pause_state() const override { return this->pause_state_; }
size_t play(const uint8_t *data, size_t length, TickType_t ticks_to_wait) override;
size_t play(const uint8_t *data, size_t length) override { return play(data, length, 0); }
bool has_buffered_data() const override;
void set_volume(float volume) override;
void set_mute_state(bool mute_state) override;
```

## `speaker/i2s_audio_speaker_standard.h`

**Enums:**
```cpp
enum class I2SCommFmt : uint8_t {
  STANDARD,  
  PCM,       
  MSB,       
};
```

**class `I2SAudioSpeaker` — public interface:**
```cpp
void dump_config() override;
void set_i2s_comm_fmt(I2SCommFmt fmt) { this->i2s_comm_fmt_ = fmt; }
```

## `speaker/spdif_encoder.h`

**class `SPDIFEncoder` — public interface:**
```cpp
bool setup();
void set_write_callback(SPDIFBlockCallback callback, void *user_ctx) { this->write_callback_ = callback; this->write_callback_ctx_ = user_ctx; }
void set_preload_callback(SPDIFBlockCallback callback, void *user_ctx) { this->preload_callback_ = callback; this->preload_callback_ctx_ = user_ctx; }
void set_preload_mode(bool preload) { this->preload_mode_ = preload; }
bool is_preload_mode() const { return this->preload_mode_; }
void set_bytes_per_sample(uint8_t bytes_per_sample);
uint8_t get_bytes_per_sample() const { return this->bytes_per_sample_; }
esp_err_t write(const uint8_t *src, size_t size, TickType_t ticks_to_wait, uint32_t *blocks_sent = nullptr, size_t *bytes_consumed = nullptr);
esp_err_t flush_with_silence(TickType_t ticks_to_wait);
void reset();
void set_sample_rate(uint32_t sample_rate);
uint32_t get_sample_rate() const { return this->sample_rate_; }
```
