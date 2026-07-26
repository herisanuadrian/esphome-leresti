# ESPHome component: `speaker`

Source: `esphome/components/speaker/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `PlayAction` — public interface:**
```cpp
void set_data_template(std::vector<uint8_t> (*func)(Ts...)) { this->data_.func = func; this->len_ = -1; }
void set_data_static(const uint8_t *data, size_t len) { this->data_.data = data; this->len_ = len; }
void play(const Ts &...x) override { if (this->len_ >= 0) { this->parent_->play(this->data_.data, static_cast<size_t>(this->len_)); } else { auto val = this->data_.func(x...); this->parent_->play(val); } }
```

**class `MuteOnAction` — public interface:**
```cpp
explicit MuteOnAction(Speaker *speaker) : speaker_(speaker) {}
void play(const Ts &...x) override { this->speaker_->set_mute_state(true); }
```

**class `MuteOffAction` — public interface:**
```cpp
explicit MuteOffAction(Speaker *speaker) : speaker_(speaker) {}
void play(const Ts &...x) override { this->speaker_->set_mute_state(false); }
```

**class `StopAction` — public interface:**
```cpp
void play(const Ts &...x) override { this->parent_->stop(); }
```

**class `FinishAction` — public interface:**
```cpp
void play(const Ts &...x) override { this->parent_->finish(); }
```

**class `IsPlayingCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return this->parent_->is_running(); }
```

**class `IsStoppedCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return this->parent_->is_stopped(); }
```

## `media_player/audio_pipeline.h`

**Enums:**
```cpp
enum class AudioPipelineType : uint8_t {
  MEDIA,
  ANNOUNCEMENT,
};
enum class AudioPipelineState : uint8_t {
  STARTING_FILE,
  STARTING_URL,
  PLAYING,
  STOPPING,
  STOPPED,
  PAUSED,
  ERROR_READING,
  ERROR_DECODING,
};
enum class InfoErrorSource : uint8_t {
  READER = 0,
  DECODER,
};
enum class DecodingError : uint8_t {
  FAILED_HEADER = 0,
  INCOMPATIBLE_BITS_PER_SAMPLE,
  INCOMPATIBLE_CHANNELS,
};
```

**class `AudioPipeline` — public interface:**
```cpp
AudioPipeline(speaker::Speaker *speaker, size_t buffer_size, bool task_stack_in_psram, std::string base_name, UBaseType_t priority);
void start_url(const std::string &uri);
void start_file(audio::AudioFile *audio_file);
esp_err_t stop();
AudioPipelineState process_state();
void suspend_tasks();
void resume_tasks();
uint32_t get_playback_ms() { return this->playback_ms_; }
void set_pause_state(bool pause_state);
```

## `media_player/automation.h`

## `media_player/speaker_media_player.h`

**class `SpeakerMediaPlayer` — public interface:**
```cpp
float get_setup_priority() const override { return esphome::setup_priority::PROCESSOR; }
void setup() override;
void loop() override;
#ifdef USE_OTA_STATE_LISTENER void on_ota_global_state(ota::OTAState state, float progress, uint8_t error, ota::OTAComponent *comp) override;
#endif media_player::MediaPlayerTraits get_traits() override;
bool is_muted() const override { return this->is_muted_; }
void set_buffer_size(size_t buffer_size) { this->buffer_size_ = buffer_size; }
void set_task_stack_in_psram(bool task_stack_in_psram) { this->task_stack_in_psram_ = task_stack_in_psram; }
void set_volume_increment(float volume_increment) { this->volume_increment_ = volume_increment; }
void set_volume_initial(float volume_initial) { this->volume_initial_ = volume_initial; }
void set_volume_max(float volume_max) { this->volume_max_ = volume_max; }
void set_volume_min(float volume_min) { this->volume_min_ = volume_min; }
void set_announcement_speaker(Speaker *announcement_speaker) { this->announcement_speaker_ = announcement_speaker; }
void set_announcement_format(const media_player::MediaPlayerSupportedFormat &announcement_format) { this->announcement_format_ = announcement_format; }
void set_media_speaker(Speaker *media_speaker) { this->media_speaker_ = media_speaker; }
void set_media_format(const media_player::MediaPlayerSupportedFormat &media_format) { this->media_format_ = media_format; }
Trigger<> *get_mute_trigger() { return &this->mute_trigger_; }
Trigger<> *get_unmute_trigger() { return &this->unmute_trigger_; }
Trigger<float> *get_volume_trigger() { return &this->volume_trigger_; }
void play_file(audio::AudioFile *media_file, bool announcement, bool enqueue);
void set_playlist_delay_ms(AudioPipelineType pipeline_type, uint32_t delay_ms);
```

## `speaker.h`

**Enums:**
```cpp
enum State : uint8_t {
  STATE_STOPPED = 0,
  STATE_STARTING,
  STATE_RUNNING,
  STATE_STOPPING,
};
```

**class `Speaker` — public interface:**
```cpp
#ifdef USE_ESP32 virtual size_t play(const uint8_t *data, size_t length, TickType_t ticks_to_wait) { return this->play(data, length); }
#endif virtual size_t play(const uint8_t *data, size_t length) = 0;
size_t play(const std::vector<uint8_t> &data) { return this->play(data.data(), data.size()); }
virtual void start() = 0;
virtual void stop() = 0;
virtual void finish() { this->stop(); }
virtual void set_pause_state(bool pause_state) {}
virtual bool get_pause_state() const { return false; }
virtual bool has_buffered_data() const = 0;
bool is_running() const { return this->state_ == STATE_RUNNING; }
bool is_stopped() const { return this->state_ == STATE_STOPPED; }
virtual void set_volume(float volume) { this->volume_ = volume; #ifdef USE_AUDIO_DAC if (this->audio_dac_ != nullptr) { this->audio_dac_->set_volume(volume); } #endif }
virtual float get_volume() { return this->volume_; }
virtual void set_mute_state(bool mute_state) { this->mute_state_ = mute_state; #ifdef USE_AUDIO_DAC if (this->audio_dac_) { if (mute_state) { this->audio_dac_->set_mute_on(); } else { this->audio_dac_->set_mute_off(); } } #endif }
virtual bool get_mute_state() { return this->mute_state_; }
#ifdef USE_AUDIO_DAC void set_audio_dac(audio_dac::AudioDac *audio_dac) { this->audio_dac_ = audio_dac; }
#endif void set_audio_stream_info(const audio::AudioStreamInfo &audio_stream_info) { this->audio_stream_info_ = audio_stream_info; }
audio::AudioStreamInfo &get_audio_stream_info() { return this->audio_stream_info_; }
template<typename F> void add_audio_output_callback(F &&callback) { this->audio_output_callback_.add(std::forward<F>(callback)); }
```
