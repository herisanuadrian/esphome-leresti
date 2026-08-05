# ESPHome component: `micro_wake_word`

Source: `esphome/components/micro_wake_word/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `StartAction` — public interface:**
```cpp
void play(const Ts &...x) override { this->parent_->start(); }
```

**class `StopAction` — public interface:**
```cpp
void play(const Ts &...x) override { this->parent_->stop(); }
```

**class `IsRunningCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return this->parent_->is_running(); }
```

**class `EnableModelAction` — public interface:**
```cpp
explicit EnableModelAction(WakeWordModel *wake_word_model) : wake_word_model_(wake_word_model) {}
void play(const Ts &...x) override { this->wake_word_model_->enable(); }
```

**class `DisableModelAction` — public interface:**
```cpp
explicit DisableModelAction(WakeWordModel *wake_word_model) : wake_word_model_(wake_word_model) {}
void play(const Ts &...x) override { this->wake_word_model_->disable(); }
```

**class `ModelIsEnabledCondition` — public interface:**
```cpp
explicit ModelIsEnabledCondition(WakeWordModel *wake_word_model) : wake_word_model_(wake_word_model) {}
bool check(const Ts &...x) override { return this->wake_word_model_->is_enabled(); }
```

## `micro_wake_word.h`

**Enums:**
```cpp
enum State {
  STARTING,
  DETECTING_WAKE_WORD,
  STOPPING,
  STOPPED,
};
```

**class `MicroWakeWord` — public interface:**
```cpp
void setup() override;
void loop() override;
float get_setup_priority() const override;
void dump_config() override;
#ifdef USE_OTA_STATE_LISTENER void on_ota_global_state(ota::OTAState state, float progress, uint8_t error, ota::OTAComponent *comp) override;
#endif void start();
void stop();
bool is_running() const { return this->state_ != State::STOPPED; }
void set_features_step_size(uint8_t step_size) { this->features_step_size_ = step_size; }
void set_microphone_source(microphone::MicrophoneSource *microphone_source) { this->microphone_source_ = microphone_source; }
void set_stop_after_detection(bool stop_after_detection) { this->stop_after_detection_ = stop_after_detection; }
void set_task_stack_in_psram(bool task_stack_in_psram) { this->task_stack_in_psram_ = task_stack_in_psram; }
Trigger<std::string> *get_wake_word_detected_trigger() { return &this->wake_word_detected_trigger_; }
void add_wake_word_model(WakeWordModel *model);
#ifdef USE_MICRO_WAKE_WORD_VAD void add_vad_model(const uint8_t *model_start, uint8_t probability_cutoff, size_t sliding_window_size, size_t tensor_arena_size);
bool get_vad_state() { return this->vad_state_; }
#endif std::vector<WakeWordModel *> get_wake_words();
```

## `streaming_model.h`

**class `StreamingModel` — public interface:**
```cpp
virtual void log_model_config() = 0;
virtual DetectionEvent determine_detected() = 0;
bool perform_streaming_inference(const int8_t features[PREPROCESSOR_FEATURE_SIZE]);
void reset_probabilities();
void unload_model();
virtual void enable() { this->enabled_ = true; }
virtual void disable() { this->enabled_ = false; }
bool is_enabled() const { return this->enabled_; }
bool get_unprocessed_probability_status() const { return this->unprocessed_probability_status_; }
uint8_t get_default_probability_cutoff() const { return this->default_probability_cutoff_; }
uint8_t get_probability_cutoff() const { return this->probability_cutoff_; }
void set_probability_cutoff(uint8_t probability_cutoff) { this->probability_cutoff_ = probability_cutoff; }
```

**class `WakeWordModel` — public interface:**
```cpp
WakeWordModel(const std::string &id, const uint8_t *model_start, uint8_t default_probability_cutoff, size_t sliding_window_average_size, const std::string &wake_word, size_t tensor_arena_size, bool default_enabled, bool internal_only);
void log_model_config() override;
DetectionEvent determine_detected() override;
const std::string &get_id() const { return this->id_; }
const std::string &get_wake_word() const { return this->wake_word_; }
void add_trained_language(const std::string &language) { this->trained_languages_.push_back(language); }
const std::vector<std::string> &get_trained_languages() const { return this->trained_languages_; }
void enable() override;
void disable() override;
bool get_internal_only() { return this->internal_only_; }
```

**class `VADModel` — public interface:**
```cpp
VADModel(const uint8_t *model_start, uint8_t default_probability_cutoff, size_t sliding_window_size, size_t tensor_arena_size);
void log_model_config() override;
DetectionEvent determine_detected() override;
```
