# ESPHome component: `voice_assistant`

Source: `esphome/components/voice_assistant/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `voice_assistant.h`

**Enums:**
```cpp
enum VoiceAssistantFeature : uint32_t {
  FEATURE_VOICE_ASSISTANT = 1 << 0,
  FEATURE_SPEAKER = 1 << 1,
  FEATURE_API_AUDIO = 1 << 2,
  FEATURE_TIMERS = 1 << 3,
  FEATURE_ANNOUNCE = 1 << 4,
  FEATURE_START_CONVERSATION = 1 << 5,
  FEATURE_MULTI_CHANNEL_AUDIO = 1 << 6,
};
enum class State {
  IDLE,
  START_MICROPHONE,
  STARTING_MICROPHONE,
  WAIT_FOR_VAD,
  WAITING_FOR_VAD,
  START_PIPELINE,
  STARTING_PIPELINE,
  STREAMING_MICROPHONE,
  STOP_MICROPHONE,
  STOPPING_MICROPHONE,
  AWAITING_RESPONSE,
  STREAMING_RESPONSE,
  RESPONSE_FINISHED,
};
enum AudioMode : uint8_t {
  AUDIO_MODE_UDP,
  AUDIO_MODE_API,
};
enum class MediaPlayerResponseState {
  IDLE,
  URL_SENT,
  PLAYING,
  FINISHED,
};
```

**class `VoiceAssistant` — public interface:**
```cpp
VoiceAssistant();
void loop() override;
void setup() override;
float get_setup_priority() const override;
void start_streaming();
void start_streaming(struct sockaddr_storage *addr, uint16_t port);
void failed_to_start();
void set_microphone_source(microphone::MicrophoneSource *mic_source) { this->mic_source_ = mic_source; }
void set_microphone_source2(microphone::MicrophoneSource *mic_source2) { this->mic_source2_ = mic_source2; }
#ifdef USE_MICRO_WAKE_WORD void set_micro_wake_word(micro_wake_word::MicroWakeWord *mww) { this->micro_wake_word_ = mww; }
#endif #ifdef USE_SPEAKER void set_speaker(speaker::Speaker *speaker) { this->speaker_ = speaker; this->local_output_ = true; }
#endif #ifdef USE_MEDIA_PLAYER void set_media_player(media_player::MediaPlayer *media_player) { this->media_player_ = media_player; this->local_output_ = true; }
#endif uint32_t get_legacy_version() const { #ifdef USE_SPEAKER if (this->speaker_ != nullptr) { return LEGACY_SPEAKER_SUPPORT; } #endif return LEGACY_INITIAL_VERSION; }
uint32_t get_feature_flags() const { uint32_t flags = 0; flags |= VoiceAssistantFeature::FEATURE_VOICE_ASSISTANT; flags |= VoiceAssistantFeature::FEATURE_API_AUDIO; if (this->mic_source2_ != nullptr) { flags |= VoiceAssistantFeature::FEATURE_MULTI_CHANNEL_AUDIO; } #ifdef USE_SPEAKER if (this->speaker_ != nullptr) { flags |= VoiceAssistantFeature::FEATURE_SPEAKER; } #endif if (this->has_timers_) { flags |= VoiceAssistantFeature::FEATURE_TIMERS; } #ifdef USE_MEDIA_PLAYER if (this->media_player_ != nullptr) { flags |= VoiceAssistantFeature::FEATURE_ANNOUNCE; flags |= VoiceAssistantFeature::FEATURE_START_CONVERSATION; } #endif return flags; }
void request_start(bool continuous, bool silence_detection);
void request_stop();
void on_event(const api::VoiceAssistantEventResponse &msg);
void on_audio(const api::VoiceAssistantAudio &msg);
void on_timer_event(const api::VoiceAssistantTimerEventResponse &msg);
void on_announce(const api::VoiceAssistantAnnounceRequest &msg);
void on_set_configuration(const std::vector<std::string> &active_wake_words);
const Configuration &get_configuration();
bool is_running() const { return this->state_ != State::IDLE; }
void set_continuous(bool continuous) { this->continuous_ = continuous; }
bool is_continuous() const { return this->continuous_; }
void set_use_wake_word(bool use_wake_word) { this->use_wake_word_ = use_wake_word; }
void set_noise_suppression_level(uint8_t noise_suppression_level) { this->noise_suppression_level_ = noise_suppression_level; }
void set_auto_gain(uint8_t auto_gain) { this->auto_gain_ = auto_gain; }
void set_volume_multiplier(float volume_multiplier) { this->volume_multiplier_ = volume_multiplier; }
void set_conversation_timeout(uint32_t conversation_timeout) { this->conversation_timeout_ = conversation_timeout; }
void reset_conversation_id();
Trigger<> *get_intent_end_trigger() { return &this->intent_end_trigger_; }
Trigger<> *get_intent_start_trigger() { return &this->intent_start_trigger_; }
Trigger<std::string> *get_intent_progress_trigger() { return &this->intent_progress_trigger_; }
Trigger<> *get_listening_trigger() { return &this->listening_trigger_; }
Trigger<> *get_end_trigger() { return &this->end_trigger_; }
Trigger<> *get_start_trigger() { return &this->start_trigger_; }
Trigger<> *get_stt_vad_end_trigger() { return &this->stt_vad_end_trigger_; }
Trigger<> *get_stt_vad_start_trigger() { return &this->stt_vad_start_trigger_; }
#ifdef USE_SPEAKER Trigger<> *get_tts_stream_start_trigger() { return &this->tts_stream_start_trigger_; }
Trigger<> *get_tts_stream_end_trigger() { return &this->tts_stream_end_trigger_; }
#endif Trigger<> *get_wake_word_detected_trigger() { return &this->wake_word_detected_trigger_; }
Trigger<std::string> *get_stt_end_trigger() { return &this->stt_end_trigger_; }
Trigger<std::string> *get_tts_end_trigger() { return &this->tts_end_trigger_; }
Trigger<std::string> *get_tts_start_trigger() { return &this->tts_start_trigger_; }
Trigger<std::string, std::string> *get_error_trigger() { return &this->error_trigger_; }
Trigger<> *get_idle_trigger() { return &this->idle_trigger_; }
Trigger<> *get_client_connected_trigger() { return &this->client_connected_trigger_; }
Trigger<> *get_client_disconnected_trigger() { return &this->client_disconnected_trigger_; }
void client_subscription(api::APIConnection *client, bool subscribe);
api::APIConnection *get_api_connection() const { return this->api_client_; }
void set_wake_word(const std::string &wake_word) { this->wake_word_ = wake_word; }
Trigger<Timer> *get_timer_started_trigger() { return &this->timer_started_trigger_; }
Trigger<Timer> *get_timer_updated_trigger() { return &this->timer_updated_trigger_; }
Trigger<Timer> *get_timer_cancelled_trigger() { return &this->timer_cancelled_trigger_; }
Trigger<Timer> *get_timer_finished_trigger() { return &this->timer_finished_trigger_; }
Trigger<const std::vector<Timer> &> *get_timer_tick_trigger() { return &this->timer_tick_trigger_; }
void set_has_timers(bool has_timers) { this->has_timers_ = has_timers; }
const std::vector<Timer> &get_timers() const { return this->timers_; }
```

**class `StartAction` — public interface:**
```cpp
void play(const Ts &...x) override { this->parent_->set_wake_word(this->wake_word_.value(x...)); this->parent_->request_start(false, this->silence_detection_); }
void set_silence_detection(bool silence_detection) { this->silence_detection_ = silence_detection; }
```

**class `StartContinuousAction` — public interface:**
```cpp
void play(const Ts &...x) override { this->parent_->request_start(true, true); }
```

**class `StopAction` — public interface:**
```cpp
void play(const Ts &...x) override { this->parent_->request_stop(); }
```

**class `IsRunningCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return this->parent_->is_running() || this->parent_->is_continuous(); }
```

**class `ConnectedCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return this->parent_->get_api_connection() != nullptr; }
```
