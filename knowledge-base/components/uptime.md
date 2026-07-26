# ESPHome component: `uptime`

Source: `esphome/components/uptime/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `sensor/uptime_seconds_sensor.h`

**class `UptimeSecondsSensor` — public interface:**
```cpp
void update() override;
void dump_config() override;
float get_setup_priority() const override;
```

## `sensor/uptime_timestamp_sensor.h`

**class `UptimeTimestampSensor` — public interface:**
```cpp
void setup() override;
void dump_config() override;
float get_setup_priority() const override;
void set_time(time::RealTimeClock *time) { this->time_ = time; }
```

## `text_sensor/uptime_text_sensor.h`

**class `UptimeTextSensor` — public interface:**
```cpp
UptimeTextSensor(const char *days_text, const char *hours_text, const char *minutes_text, const char *seconds_text, const char *separator, bool expand) : days_text_(days_text), hours_text_(hours_text), minutes_text_(minutes_text), seconds_text_(seconds_text), separator_(separator), expand_(expand) {}
void update() override;
void dump_config() override;
void setup() override;
float get_setup_priority() const override;
void set_days(const char *days_text) { this->days_text_ = days_text; }
void set_hours(const char *hours_text) { this->hours_text_ = hours_text; }
void set_minutes(const char *minutes_text) { this->minutes_text_ = minutes_text; }
void set_seconds(const char *seconds_text) { this->seconds_text_ = seconds_text; }
```
