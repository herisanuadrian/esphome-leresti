# ESPHome component: `captive_portal`

Source: `esphome/components/captive_portal/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `captive_portal.h`

**class `CaptivePortal` — public interface:**
```cpp
CaptivePortal(web_server_base::WebServerBase *base);
void setup() override;
void dump_config() override;
void loop() override { #if defined(USE_ESP32) if (this->dns_server_ != nullptr) { this->dns_server_->process_next_request(); } #elif defined(USE_ARDUINO) if (this->dns_server_ != nullptr) { this->dns_server_->processNextRequest(); } #endif }
float get_setup_priority() const override;
void start();
bool is_active() const { return this->active_; }
void end() { this->active_ = false; this->disable_loop(); this->base_->deinit(); if (this->dns_server_ != nullptr) { this->dns_server_->stop(); this->dns_server_ = nullptr; } }
bool canHandle(AsyncWebServerRequest *request) const override { return this->active_ && request->method() == HTTP_GET; }
void handle_config(AsyncWebServerRequest *request);
void handle_wifisave(AsyncWebServerRequest *request);
void handleRequest(AsyncWebServerRequest *req) override;
```

## `dns_server_esp32_idf.h`

**class `DNSServer` — public interface:**
```cpp
void start(const network::IPAddress &ip);
void stop();
void process_next_request();
```
