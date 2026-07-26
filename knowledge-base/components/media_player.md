# ESPHome component: `media_player`

Source: `esphome/components/media_player/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `MediaPlayerCommandAction` — public interface:**
```cpp
TEMPLATABLE_VALUE(bool, announcement);
void play(const Ts &...x) override { this->parent_->make_call().set_command(Command).set_announcement(this->announcement_.value(x...)).perform(); }
```

**class `IsIdleCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return this->parent_->state == MediaPlayerState::MEDIA_PLAYER_STATE_IDLE; }
```

**class `IsPlayingCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return this->parent_->state == MediaPlayerState::MEDIA_PLAYER_STATE_PLAYING; }
```

**class `IsPausedCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return this->parent_->state == MediaPlayerState::MEDIA_PLAYER_STATE_PAUSED; }
```

**class `IsAnnouncingCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return this->parent_->state == MediaPlayerState::MEDIA_PLAYER_STATE_ANNOUNCING; }
```

**class `IsOnCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return this->parent_->state == MediaPlayerState::MEDIA_PLAYER_STATE_ON; }
```

**class `IsOffCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return this->parent_->state == MediaPlayerState::MEDIA_PLAYER_STATE_OFF; }
```

**class `IsMutedCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return this->parent_->is_muted(); }
```

## `media_player.h`

**Enums:**
```cpp
enum MediaPlayerEntityFeature : uint32_t {
  PAUSE = 1 << 0,
  SEEK = 1 << 1,
  VOLUME_SET = 1 << 2,
  VOLUME_MUTE = 1 << 3,
  PREVIOUS_TRACK = 1 << 4,
  NEXT_TRACK = 1 << 5,
  TURN_ON = 1 << 7,
  TURN_OFF = 1 << 8,
  PLAY_MEDIA = 1 << 9,
  VOLUME_STEP = 1 << 10,
  SELECT_SOURCE = 1 << 11,
  STOP = 1 << 12,
  CLEAR_PLAYLIST = 1 << 13,
  PLAY = 1 << 14,
  SHUFFLE_SET = 1 << 15,
  SELECT_SOUND_MODE = 1 << 16,
  BROWSE_MEDIA = 1 << 17,
  REPEAT_SET = 1 << 18,
  GROUPING = 1 << 19,
  MEDIA_ANNOUNCE = 1 << 20,
  MEDIA_ENQUEUE = 1 << 21,
  SEARCH_MEDIA = 1 << 22,
};
enum MediaPlayerState : uint8_t {
  MEDIA_PLAYER_STATE_NONE = 0,
  MEDIA_PLAYER_STATE_IDLE = 1,
  MEDIA_PLAYER_STATE_PLAYING = 2,
  MEDIA_PLAYER_STATE_PAUSED = 3,
  MEDIA_PLAYER_STATE_ANNOUNCING = 4,
  MEDIA_PLAYER_STATE_OFF = 5,
  MEDIA_PLAYER_STATE_ON = 6,
};
enum MediaPlayerCommand : uint8_t {
  MEDIA_PLAYER_COMMAND_PLAY = 0,
  MEDIA_PLAYER_COMMAND_PAUSE = 1,
  MEDIA_PLAYER_COMMAND_STOP = 2,
  MEDIA_PLAYER_COMMAND_MUTE = 3,
  MEDIA_PLAYER_COMMAND_UNMUTE = 4,
  MEDIA_PLAYER_COMMAND_TOGGLE = 5,
  MEDIA_PLAYER_COMMAND_VOLUME_UP = 6,
  MEDIA_PLAYER_COMMAND_VOLUME_DOWN = 7,
  MEDIA_PLAYER_COMMAND_ENQUEUE = 8,
  MEDIA_PLAYER_COMMAND_REPEAT_ONE = 9,
  MEDIA_PLAYER_COMMAND_REPEAT_OFF = 10,
  MEDIA_PLAYER_COMMAND_CLEAR_PLAYLIST = 11,
  MEDIA_PLAYER_COMMAND_TURN_ON = 12,
  MEDIA_PLAYER_COMMAND_TURN_OFF = 13,
  MEDIA_PLAYER_COMMAND_NEXT = 14,
  MEDIA_PLAYER_COMMAND_PREVIOUS = 15,
  MEDIA_PLAYER_COMMAND_REPEAT_ALL = 16,
  MEDIA_PLAYER_COMMAND_SHUFFLE = 17,
  MEDIA_PLAYER_COMMAND_UNSHUFFLE = 18,
  MEDIA_PLAYER_COMMAND_GROUP_JOIN = 19,
};
enum class MediaPlayerFormatPurpose : uint8_t {
  PURPOSE_DEFAULT = 0,
  PURPOSE_ANNOUNCEMENT = 1,
};
```

**class `MediaPlayerTraits` — public interface:**
```cpp
MediaPlayerTraits() = default;
uint32_t get_feature_flags() const { return this->feature_flags_; }
void add_feature_flags(uint32_t feature_flags) { this->feature_flags_ |= feature_flags; }
void clear_feature_flags(uint32_t feature_flags) { this->feature_flags_ &= ~feature_flags; }
bool has_feature_flags(uint32_t feature_flags) const { return (this->feature_flags_ & feature_flags) == feature_flags; }
std::vector<MediaPlayerSupportedFormat> &get_supported_formats() { return this->supported_formats_; }
void set_supports_pause(bool supports_pause);
bool get_supports_pause() const { return this->has_feature_flags(MediaPlayerEntityFeature::PAUSE); }
void set_supports_turn_off_on(bool supports_turn_off_on);
bool get_supports_turn_off_on() const { return this->has_feature_flags(MediaPlayerEntityFeature::TURN_ON | MediaPlayerEntityFeature::TURN_OFF); }
```

**class `MediaPlayerCall` — public interface:**
```cpp
MediaPlayerCall(MediaPlayer *parent) : parent_(parent) {}
MediaPlayerCall &set_command(MediaPlayerCommand command);
MediaPlayerCall &set_command(optional<MediaPlayerCommand> command);
MediaPlayerCall &set_command(const char *command);
MediaPlayerCall &set_command(const std::string &command) { return this->set_command(command.c_str()); }
MediaPlayerCall &set_media_url(const std::string &url);
MediaPlayerCall &set_volume(float volume);
MediaPlayerCall &set_announcement(bool announce);
void perform();
const optional<MediaPlayerCommand> &get_command() const { return this->command_; }
const optional<std::string> &get_media_url() const { return this->media_url_; }
const optional<float> &get_volume() const { return this->volume_; }
const optional<bool> &get_announcement() const { return this->announcement_; }
```

**class `MediaPlayer` — public interface:**
```cpp
MediaPlayerState state{MEDIA_PLAYER_STATE_NONE}
float volume{1.0f}
MediaPlayerCall make_call() { return MediaPlayerCall(this); }
void publish_state();
template<typename F> void add_on_state_callback(F &&callback) { this->state_callback_.add(std::forward<F>(callback)); }
virtual bool is_muted() const { return false; }
virtual MediaPlayerTraits get_traits() = 0;
```
