# ESPHome component: `homeassistant`

Source: `esphome/components/homeassistant/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `binary_sensor/homeassistant_binary_sensor.h`

**class `HomeassistantBinarySensor` — public interface:**
```cpp
void set_entity_id(const char *entity_id) { this->entity_id_ = entity_id; }
void set_attribute(const char *attribute) { this->attribute_ = attribute; }
void setup() override;
void dump_config() override;
float get_setup_priority() const override;
```

## `number/homeassistant_number.h`

**class `HomeassistantNumber` — public interface:**
```cpp
void set_entity_id(const char *entity_id) { this->entity_id_ = entity_id; }
void setup() override;
void dump_config() override;
float get_setup_priority() const override;
```

## `sensor/homeassistant_sensor.h`

**class `HomeassistantSensor` — public interface:**
```cpp
void set_entity_id(const char *entity_id) { this->entity_id_ = entity_id; }
void set_attribute(const char *attribute) { this->attribute_ = attribute; }
void setup() override;
void dump_config() override;
float get_setup_priority() const override;
```

## `switch/homeassistant_switch.h`

**class `HomeassistantSwitch` — public interface:**
```cpp
void set_entity_id(const char *entity_id) { this->entity_id_ = entity_id; }
void setup() override;
void dump_config() override;
float get_setup_priority() const override;
```

## `text_sensor/homeassistant_text_sensor.h`

**class `HomeassistantTextSensor` — public interface:**
```cpp
void set_entity_id(const char *entity_id) { this->entity_id_ = entity_id; }
void set_attribute(const char *attribute) { this->attribute_ = attribute; }
void setup() override;
void dump_config() override;
float get_setup_priority() const override;
```

## `time/homeassistant_time.h`

**class `HomeassistantTime` — public interface:**
```cpp
void setup() override;
void update() override;
void dump_config() override;
void set_epoch_time(uint32_t epoch) { this->synchronize_epoch_(epoch); }
```
