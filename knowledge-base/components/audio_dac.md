# ESPHome component: `audio_dac`

Source: `esphome/components/audio_dac/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `audio_dac.h`

**class `AudioDac` — public interface:**
```cpp
virtual bool set_mute_off() = 0;
virtual bool set_mute_on() = 0;
virtual bool set_volume(float volume) = 0;
virtual bool is_muted() = 0;
virtual float volume() = 0;
```

## `automation.h`

**class `MuteOffAction` — public interface:**
```cpp
explicit MuteOffAction(AudioDac *audio_dac) : audio_dac_(audio_dac) {}
void play(const Ts &...x) override { this->audio_dac_->set_mute_off(); }
```

**class `MuteOnAction` — public interface:**
```cpp
explicit MuteOnAction(AudioDac *audio_dac) : audio_dac_(audio_dac) {}
void play(const Ts &...x) override { this->audio_dac_->set_mute_on(); }
```

**class `SetVolumeAction` — public interface:**
```cpp
explicit SetVolumeAction(AudioDac *audio_dac) : audio_dac_(audio_dac) {}
TEMPLATABLE_VALUE(float, volume) void play(const Ts &...x) override { this->audio_dac_->set_volume(this->volume_.value(x...)); }
```
