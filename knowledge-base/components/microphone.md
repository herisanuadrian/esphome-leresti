# ESPHome component: `microphone`

Source: `esphome/components/microphone/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `DataTrigger` — public interface:**
```cpp
explicit DataTrigger(Microphone *mic) { mic->add_data_callback([this](const std::vector<uint8_t> &data) { this->trigger(data); }); }
```

**class `IsCapturingCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return this->parent_->is_running(); }
```

**class `IsMutedCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return this->parent_->get_mute_state(); }
```

## `microphone.h`

**Enums:**
```cpp
enum State : uint8_t {
  STATE_STOPPED = 0,
  STATE_STARTING,
  STATE_RUNNING,
  STATE_STOPPING,
};
```

**class `Microphone` — public interface:**
```cpp
virtual void start() = 0;
virtual void stop() = 0;
template<typename F> void add_data_callback(F &&data_callback) { this->data_callbacks_.add([this, data_callback](const std::vector<uint8_t> &data) { if (this->mute_state_) { data_callback(std::vector<uint8_t>(data.size(), 0)); } else { data_callback(data); } }); }
bool is_running() const { return this->state_ == STATE_RUNNING; }
bool is_stopped() const { return this->state_ == STATE_STOPPED; }
void set_mute_state(bool is_muted) { this->mute_state_ = is_muted; }
bool get_mute_state() { return this->mute_state_; }
audio::AudioStreamInfo get_audio_stream_info() { return this->audio_stream_info_; }
```

## `microphone_source.h`

**class `MicrophoneSource` — public interface:**
```cpp
MicrophoneSource(Microphone *mic, uint8_t bits_per_sample, int32_t gain_factor, bool passive) : mic_(mic), bits_per_sample_(bits_per_sample), gain_factor_(gain_factor), passive_(passive) {}
void add_channel(uint8_t channel) { this->channels_.set(channel); }
template<typename F> void add_data_callback(F &&data_callback) { this->mic_->add_data_callback([this, data_callback](const std::vector<uint8_t> &data) { if (this->enabled_ || this->passive_) { if (this->processed_samples_.use_count() == 0) { this->processed_samples_ = std::make_shared<std::vector<uint8_t>>(); } std::shared_ptr<std::vector<uint8_t>> output_samples = this->processed_samples_; this->process_audio_(data, *output_samples); data_callback(*output_samples); } }); }
void set_gain_factor(int32_t gain_factor) { this->gain_factor_ = clamp<int32_t>(gain_factor, 1, MAX_GAIN_FACTOR); }
int32_t get_gain_factor() { return this->gain_factor_; }
audio::AudioStreamInfo get_audio_stream_info();
void start();
void stop();
bool is_passive() const { return this->passive_; }
bool is_running() const { return (this->mic_->is_running() && (this->enabled_ || this->passive_)); }
bool is_stopped() const { return !this->is_running(); }
```
