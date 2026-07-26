# ESPHome component: `sntp`

Source: `esphome/components/sntp/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `sntp_component.h`

**class `SNTPComponent` — public interface:**
```cpp
SNTPComponent(const std::array<const char *, SNTP_SERVER_COUNT> &servers) : servers_(servers) {}
void setup() override;
void dump_config() override;
float get_setup_priority() const override { return setup_priority::BEFORE_CONNECTION; }
void update() override;
void loop() override;
void time_synced();
```
