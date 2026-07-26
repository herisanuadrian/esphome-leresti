# ESPHome component: `rtttl`

Source: `esphome/components/rtttl/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `rtttl.h`

**Enums:**
```cpp
enum class State : uint8_t {
  STOPPED = 0,
  INIT,
  STARTING,
  RUNNING,
  STOPPING,
};
```

**Constants:**
```cpp
inline constexpr uint8_t DEFAULT_NOTE_DENOMINATOR = 4;
```

**class `Rtttl` — public interface:**
```cpp
#ifdef USE_OUTPUT void set_output(output::FloatOutput *output) { this->output_ = output; }
#endif #ifdef USE_SPEAKER void set_speaker(speaker::Speaker *speaker) { this->speaker_ = speaker; }
#endif void dump_config() override;
void loop() override;
void play(std::string rtttl);
void stop();
float get_gain() { return this->gain_; }
void set_gain(float gain) { this->gain_ = clamp(gain, 0.0f, 1.0f); }
bool is_playing() { return this->state_ != State::STOPPED; }
#ifdef USE_RTTTL_FINISHED_PLAYBACK_CALLBACK template<typename F> void add_on_finished_playback_callback(F &&callback) { this->on_finished_playback_callback_.add(std::forward<F>(callback)); }
#endif protected: inline uint16_t get_integer_() { uint16_t ret = 0; while (isdigit(this->rtttl_[this->position_])) { ret = (ret * 10) + (this->rtttl_[this->position_++] - '0'); } return ret; }
void finish_();
void set_state_(State state);
std::string rtttl_;
size_t position_{0}
uint8_t default_note_denominator_{DEFAULT_NOTE_DENOMINATOR}
uint8_t default_octave_{DEFAULT_OCTAVE}
uint16_t note_duration_{0}
uint16_t wholenote_duration_;
uint32_t last_note_start_time_;
uint32_t output_freq_{0}
float gain_{0.6f}
State state_{State::STOPPED}
#ifdef USE_OUTPUT output::FloatOutput *output_{nullptr}
#endif #ifdef USE_SPEAKER speaker::Speaker *speaker_{nullptr}
uint32_t samples_per_wave_{0}
uint32_t samples_sent_{0}
uint32_t samples_count_{0}
uint32_t samples_gap_{0}
#endif #ifdef USE_RTTTL_FINISHED_PLAYBACK_CALLBACK CallbackManager<void()> on_finished_playback_callback_;
```

**class `PlayAction` — public interface:**
```cpp
PlayAction(Rtttl *rtttl) : rtttl_(rtttl) {}
TEMPLATABLE_VALUE(std::string, value) void play(const Ts &...x) override { this->rtttl_->play(this->value_.value(x...)); }
```

**class `StopAction` — public interface:**
```cpp
void play(const Ts &...x) override { this->parent_->stop(); }
```

**class `IsPlayingCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return this->parent_->is_playing(); }
```
