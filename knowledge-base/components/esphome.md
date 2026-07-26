# ESPHome component: `esphome`

Source: `esphome/components/esphome/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `ota/ota_esphome.h`

**Enums:**
```cpp
enum class OTAState : uint8_t {
    IDLE,
    MAGIC_READ,    
    MAGIC_ACK,     
    FEATURE_READ,  
    FEATURE_ACK,   
#ifdef USE_OTA_PASSWORD
    AUTH_SEND,  
    AUTH_READ,  
#endif          
    DATA,       
  };
```

**class `ESPHomeOTAComponent` — public interface:**
```cpp
enum class OTAState : uint8_t { IDLE, MAGIC_READ, MAGIC_ACK, FEATURE_READ, FEATURE_ACK, #ifdef USE_OTA_PASSWORD AUTH_SEND, AUTH_READ, #endif DATA, }
#ifdef USE_OTA_PASSWORD void set_auth_password(const std::string &password) { password_ = password; }
#else template<bool B = false> void set_auth_password(const std::string &) { static_assert(B, "set_auth_password() requires the OTA auth path to be compiled. " "Add 'password: \"\"' (empty string) to your 'ota: - platform: esphome' " "config to enable runtime password rotation."); }
#endif void set_port(uint16_t port);
void setup() override;
void dump_config() override;
float get_setup_priority() const override;
void loop() override;
uint16_t get_port() const;
```
