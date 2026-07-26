# ESPHome component: `wifi`

Source: `esphome/components/wifi/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `automation.h`

**class `WiFiConnectedCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return global_wifi_component->is_connected(); }
```

**class `WiFiEnabledCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return !global_wifi_component->is_disabled(); }
```

**class `WiFiAPActiveCondition` — public interface:**
```cpp
bool check(const Ts &...x) override { return global_wifi_component->is_ap_active(); }
```

**class `WiFiEnableAction` — public interface:**
```cpp
void play(const Ts &...x) override { global_wifi_component->enable(); }
```

**class `WiFiDisableAction` — public interface:**
```cpp
void play(const Ts &...x) override { global_wifi_component->disable(); }
```

**class `WiFiConfigureAction` — public interface:**
```cpp
TEMPLATABLE_VALUE(std::string, ssid) TEMPLATABLE_VALUE(std::string, password) TEMPLATABLE_VALUE(bool, save) TEMPLATABLE_VALUE(uint32_t, connection_timeout) void play(const Ts &...x) override { auto ssid = this->ssid_.value(x...); auto password = this->password_.value(x...); if (this->connecting_) return; char ssid_buf[SSID_BUFFER_SIZE]; if (strcmp(global_wifi_component->wifi_ssid_to(ssid_buf), ssid.c_str()) == 0) { this->connect_trigger_.trigger(); return; } this->new_sta_.set_ssid(ssid); this->new_sta_.set_password(password); this->old_sta_ = global_wifi_component->get_sta(); global_wifi_component->disable(); this->connecting_ = true; if (this->save_.value(x...)) { global_wifi_component->save_wifi_sta(new_sta_.get_ssid(), new_sta_.get_password()); } else { global_wifi_component->set_sta(new_sta_); } global_wifi_component->enable(); this->set_timeout("wifi-connect-timeout", this->connection_timeout_.value(x...), [this, x...]() { global_wifi_component->disable(); global_wifi_component->save_wifi_sta(old_sta_.get_ssid(), old_sta_.get_password()); global_wifi_component->enable(); this->set_timeout("wifi-fallback-timeout", this->connection_timeout_.value(x...), [this]() { this->connecting_ = false; this->error_trigger_.trigger(); }); }); }
Trigger<> *get_connect_trigger() { return &this->connect_trigger_; }
Trigger<> *get_error_trigger() { return &this->error_trigger_; }
void loop() override { if (!this->connecting_) return; if (global_wifi_component->is_connected()) { this->cancel_timeout("wifi-connect-timeout"); this->cancel_timeout("wifi-fallback-timeout"); this->connecting_ = false; char ssid_buf[SSID_BUFFER_SIZE]; if (strcmp(global_wifi_component->wifi_ssid_to(ssid_buf), this->new_sta_.get_ssid().c_str()) == 0) { this->connect_trigger_.trigger(); } else { this->error_trigger_.trigger(); } } }
```

## `wifi_component.h`

**Enums:**
```cpp
enum WiFiComponentState : uint8_t {
  WIFI_COMPONENT_STATE_OFF = 0,
  WIFI_COMPONENT_STATE_DISABLED,
  WIFI_COMPONENT_STATE_COOLDOWN,
  WIFI_COMPONENT_STATE_STA_SCANNING,
  WIFI_COMPONENT_STATE_STA_CONNECTING,
  WIFI_COMPONENT_STATE_STA_CONNECTED,
  WIFI_COMPONENT_STATE_AP,
};
enum class WiFiSTAConnectStatus : int {
  IDLE,
  CONNECTING,
  CONNECTED,
  ERROR_NETWORK_NOT_FOUND,
  ERROR_CONNECT_FAILED,
};
enum class WiFiRetryPhase : uint8_t {
  INITIAL_CONNECT,
#ifdef USE_WIFI_FAST_CONNECT
  FAST_CONNECT_CYCLING_APS,
#endif
  EXPLICIT_HIDDEN,
  SCAN_CONNECTING,
  RETRY_HIDDEN,
  RESTARTING_ADAPTER,
};
enum class RoamingState : uint8_t {
  IDLE,
  SCANNING,
  CONNECTING,
  RECONNECTING,
};
enum class RetryHiddenMode : uint8_t {
  SCAN_BASED,
  BLIND_RETRY,
};
enum WiFiPowerSaveMode : uint8_t {
  WIFI_POWER_SAVE_NONE = 0,
  WIFI_POWER_SAVE_LIGHT,
  WIFI_POWER_SAVE_HIGH,
};
enum WifiMinAuthMode : uint8_t {
  WIFI_MIN_AUTH_MODE_WPA = 0,
  WIFI_MIN_AUTH_MODE_WPA2,
  WIFI_MIN_AUTH_MODE_WPA3,
};
enum WiFi8266PhyMode : uint8_t {
  WIFI_8266_PHY_MODE_AUTO = 0,
  WIFI_8266_PHY_MODE_11B = 1,
  WIFI_8266_PHY_MODE_11G = 2,
  WIFI_8266_PHY_MODE_11N = 3,
};
```

**class `CompactString` — public interface:**
```cpp
static constexpr uint8_t MAX_LENGTH = 127;
static constexpr uint8_t INLINE_CAPACITY = 18;
CompactString() : length_(0), is_heap_(0) { this->storage_[0] = '\0'; }
CompactString(const char *str, size_t len);
CompactString(const CompactString &other);
CompactString(CompactString &&other) noexcept;
CompactString &operator=(const CompactString &other);
CompactString &operator=(CompactString &&other) noexcept;
~CompactString();
const char *data() const { return this->is_heap_ ? this->get_heap_ptr_() : this->storage_; }
const char *c_str() const { return this->data(); }
size_t size() const { return this->length_; }
bool empty() const { return this->length_ == 0; }
StringRef ref() const { return StringRef(this->data(), this->size()); }
bool operator==(const CompactString &other) const;
bool operator!=(const CompactString &other) const { return !(*this == other); }
bool operator==(const StringRef &other) const;
bool operator!=(const StringRef &other) const { return !(*this == other); }
bool operator==(const char *other) const { return *this == StringRef(other); }
bool operator!=(const char *other) const { return !(*this == other); }
```

**class `WiFiAP` — public interface:**
```cpp
void set_ssid(const std::string &ssid);
void set_ssid(const char *ssid);
void set_ssid(StringRef ssid) { this->ssid_ = CompactString(ssid.c_str(), ssid.size()); }
void set_bssid(const bssid_t &bssid);
void clear_bssid();
void set_password(const std::string &password);
void set_password(const char *password);
void set_password(StringRef password) { this->password_ = CompactString(password.c_str(), password.size()); }
#ifdef USE_WIFI_WPA2_EAP void set_eap(optional<EAPAuth> eap_auth);
#endif void set_channel(uint8_t channel);
void clear_channel();
void set_priority(int8_t priority) { priority_ = priority; }
#ifdef USE_WIFI_MANUAL_IP void set_manual_ip(optional<ManualIP> manual_ip);
#endif void set_hidden(bool hidden);
StringRef get_ssid() const { return this->ssid_.ref(); }
StringRef get_password() const { return this->password_.ref(); }
const bssid_t &get_bssid() const;
bool has_bssid() const;
#ifdef USE_WIFI_WPA2_EAP const optional<EAPAuth> &get_eap() const;
#endif uint8_t get_channel() const { return this->channel_; }
bool has_channel() const { return this->channel_ != 0; }
int8_t get_priority() const { return priority_; }
#ifdef USE_WIFI_MANUAL_IP const optional<ManualIP> &get_manual_ip() const;
#endif bool get_hidden() const;
```

**class `WiFiScanResult` — public interface:**
```cpp
WiFiScanResult(const bssid_t &bssid, const char *ssid, size_t ssid_len, uint8_t channel, int8_t rssi, bool with_auth, bool is_hidden);
bool matches(const WiFiAP &config) const;
bool get_matches() const;
void set_matches(bool matches);
const bssid_t &get_bssid() const;
StringRef get_ssid() const { return this->ssid_.ref(); }
uint8_t get_channel() const;
int8_t get_rssi() const;
bool get_with_auth() const;
bool get_is_hidden() const;
int8_t get_priority() const { return priority_; }
void set_priority(int8_t priority) { priority_ = priority; }
bool operator==(const WiFiScanResult &rhs) const;
```

**class `WiFiIPStateListener` — public interface:**
```cpp
virtual void on_ip_state(const network::IPAddresses &ips, const network::IPAddress &dns1, const network::IPAddress &dns2) = 0;
```

**class `WiFiScanResultsListener` — public interface:**
```cpp
virtual void on_wifi_scan_results(const wifi_scan_vector_t<WiFiScanResult> &results) = 0;
```

**class `WiFiConnectStateListener` — public interface:**
```cpp
virtual void on_wifi_connect_state(StringRef ssid, std::span<const uint8_t, 6> bssid) = 0;
```

**class `WiFiPowerSaveListener` — public interface:**
```cpp
virtual void on_wifi_power_save(WiFiPowerSaveMode mode) = 0;
```

**class `WiFiComponent` — public interface:**
```cpp
WiFiComponent();
void set_sta(const WiFiAP &ap);
WiFiAP get_sta() const;
void init_sta(size_t count);
void add_sta(const WiFiAP &ap);
void clear_sta();
#ifdef USE_WIFI_AP void set_ap(const WiFiAP &ap);
WiFiAP get_ap() { return this->ap_; }
void set_ap_timeout(uint32_t ap_timeout) { ap_timeout_ = ap_timeout; }
#endif void enable();
void disable();
bool is_disabled();
void start_scanning();
void check_scanning_finished();
void start_connecting(const WiFiAP &ap);
void start_connecting(const WiFiAP &ap, bool ) { this->start_connecting(ap); }
void check_connecting_finished(uint32_t now);
void retry_connect();
void set_reboot_timeout(uint32_t reboot_timeout);
bool is_connected() const { return this->connected_; }
void set_power_save_mode(WiFiPowerSaveMode power_save);
void set_min_auth_mode(WifiMinAuthMode min_auth_mode) { min_auth_mode_ = min_auth_mode; }
void set_output_power(float output_power) { output_power_ = output_power; }
#if defined(USE_ESP32) && defined(SOC_WIFI_SUPPORT_5G) void set_band_mode(wifi_band_mode_t band_mode) { this->band_mode_ = band_mode; }
#endif #ifdef USE_WIFI_PHY_MODE void set_phy_mode(WiFi8266PhyMode phy_mode) { this->phy_mode_ = phy_mode; }
#endif void set_passive_scan(bool passive);
void save_wifi_sta(const std::string &ssid, const std::string &password);
void save_wifi_sta(const char *ssid, const char *password);
void save_wifi_sta(StringRef ssid, StringRef password) { this->save_wifi_sta(ssid.c_str(), password.c_str()); }
void setup() override;
void start();
void dump_config() override;
void restart_adapter();
float get_setup_priority() const override;
void loop() override;
bool has_sta() const { return !this->sta_.empty(); }
bool has_ap() const { return this->has_ap_; }
bool is_ap_active() const { return this->ap_started_; }
#ifdef USE_WIFI_11KV_SUPPORT void set_btm(bool btm);
void set_rrm(bool rrm);
#endif network::IPAddress get_dns_address(int num);
network::IPAddresses get_ip_addresses();
const char *get_use_address() const { return this->use_address_; }
void set_use_address(const char *use_address) { this->use_address_ = use_address; }
const wifi_scan_vector_t<WiFiScanResult> &get_scan_result() const { return scan_result_; }
network::IPAddress wifi_soft_ap_ip();
bool has_sta_priority(const bssid_t &bssid) { for (auto &it : this->sta_priorities_) { if (it.bssid == bssid) return true; } return false; }
int8_t get_sta_priority(const bssid_t bssid) { for (auto &it : this->sta_priorities_) { if (it.bssid == bssid) return it.priority; } return 0; }
void set_sta_priority(bssid_t bssid, int8_t priority);
network::IPAddresses wifi_sta_ip_addresses();
ESPDEPRECATED("Use wifi_ssid_to() instead. Removed in 2026.9.0", "2026.3.0") std::string wifi_ssid();
const char *wifi_ssid_to(std::span<char, SSID_BUFFER_SIZE> buffer);
bssid_t wifi_bssid();
int8_t wifi_rssi();
void set_enable_on_boot(bool enable_on_boot) { this->enable_on_boot_ = enable_on_boot; }
void set_keep_scan_results(bool keep_scan_results) { this->keep_scan_results_ = keep_scan_results; }
void set_post_connect_roaming(bool enabled) { this->post_connect_roaming_ = enabled; }
#ifdef USE_WIFI_CONNECT_TRIGGER Trigger<> *get_connect_trigger() { return &this->connect_trigger_; }
#endif #ifdef USE_WIFI_DISCONNECT_TRIGGER Trigger<> *get_disconnect_trigger() { return &this->disconnect_trigger_; }
#endif int32_t get_wifi_channel();
#ifdef USE_WIFI_IP_STATE_LISTENERS void add_ip_state_listener(WiFiIPStateListener *listener) { this->ip_state_listeners_.push_back(listener); }
#endif #ifdef USE_WIFI_SCAN_RESULTS_LISTENERS void add_scan_results_listener(WiFiScanResultsListener *listener) { this->scan_results_listeners_.push_back(listener); }
#endif #ifdef USE_WIFI_CONNECT_STATE_LISTENERS void add_connect_state_listener(WiFiConnectStateListener *listener) { this->connect_state_listeners_.push_back(listener); }
#endif #ifdef USE_WIFI_POWER_SAVE_LISTENERS void add_power_save_listener(WiFiPowerSaveListener *listener) { this->power_save_listeners_.push_back(listener); }
#endif #ifdef USE_WIFI_RUNTIME_POWER_SAVE bool request_high_performance();
bool release_high_performance();
#endif #if defined(USE_ESP32) && defined(USE_WIFI_RUNTIME_ROAMING_SUPPRESSION) void request_roaming_suppression() { uint8_t current = this->roaming_suppression_count_.load(std::memory_order_relaxed); while (current < std::numeric_limits<uint8_t>::max() && !this->roaming_suppression_count_.compare_exchange_weak(current, current + 1, std::memory_order_relaxed)) { } }
void release_roaming_suppression() { uint8_t current = this->roaming_suppression_count_.load(std::memory_order_relaxed); while (current > 0 && !this->roaming_suppression_count_.compare_exchange_weak(current, current - 1, std::memory_order_relaxed)) { } }
#endif protected: #ifdef USE_WIFI_AP void setup_ap_config_();
#endif void print_connect_params_();
WiFiAP build_params_for_current_phase_();
WiFiRetryPhase determine_next_phase_();
bool transition_to_phase_(WiFiRetryPhase new_phase);
bool needs_scan_results_() const;
bool went_through_explicit_hidden_phase_() const;
int8_t find_first_non_hidden_index_() const;
bool ssid_was_seen_in_scan_(const CompactString &ssid) const;
bool needs_full_scan_results_() const;
bool matches_configured_network_(const char *ssid, const uint8_t *bssid) const;
void log_discarded_scan_result_(const char *ssid, const uint8_t *bssid, int8_t rssi, uint8_t channel);
int8_t find_next_hidden_sta_(int8_t start_index);
void log_and_adjust_priority_for_failed_connect_();
void clear_all_bssid_priorities_();
void clear_priorities_if_all_min_();
void advance_to_next_target_or_increment_retry_();
void start_initial_connection_();
const WiFiAP *get_selected_sta_() const { if (this->selected_sta_index_ >= 0 && static_cast<size_t>(this->selected_sta_index_) < this->sta_.size()) { return &this->sta_[this->selected_sta_index_]; } return nullptr; }
void reset_selected_ap_to_first_if_invalid_() { if (this->selected_sta_index_ < 0 || static_cast<size_t>(this->selected_sta_index_) >= this->sta_.size()) { this->selected_sta_index_ = this->sta_.empty() ? -1 : 0; } }
bool all_networks_hidden_() const { if (this->sta_.empty()) return false; for (const auto &ap : this->sta_) { if (!ap.get_hidden()) return false; } return true; }
void connect_soon_();
bool wifi_loop_();
#ifdef USE_ESP8266 void process_pending_callbacks_();
#endif bool wifi_mode_(optional<bool> sta, optional<bool> ap);
bool wifi_sta_pre_setup_();
bool wifi_apply_output_power_(float output_power);
bool wifi_apply_power_save_();
#if defined(USE_ESP32) && defined(SOC_WIFI_SUPPORT_5G) bool wifi_apply_band_mode_();
#endif #ifdef USE_WIFI_PHY_MODE bool wifi_apply_phy_mode_();
#endif bool wifi_sta_ip_config_(const optional<ManualIP> &manual_ip);
bool wifi_apply_hostname_();
bool wifi_sta_connect_(const WiFiAP &ap);
void wifi_pre_setup_();
#ifdef USE_ESP32 void wifi_lazy_init_();
#endif WiFiSTAConnectStatus wifi_sta_connect_status_() const;
bool is_connected_() const { return this->state_ == WIFI_COMPONENT_STATE_STA_CONNECTED && this->wifi_sta_connect_status_() == WiFiSTAConnectStatus::CONNECTED && !this->error_from_callback_; }
void update_connected_state_() { this->connected_ = this->is_connected_(); }
bool wifi_scan_start_(bool passive);
#ifdef USE_WIFI_AP bool wifi_ap_ip_config_(const optional<ManualIP> &manual_ip);
bool wifi_start_ap_(const WiFiAP &ap);
#endif bool wifi_disconnect_();
network::IPAddress wifi_subnet_mask_();
network::IPAddress wifi_gateway_ip_();
network::IPAddress wifi_dns_ip_(int num);
bool is_captive_portal_active_();
bool is_esp32_improv_active_();
#ifdef USE_WIFI_FAST_CONNECT bool load_fast_connect_settings_(WiFiAP &params);
void save_fast_connect_settings_();
#endif void check_roaming_(uint32_t now);
void process_roaming_scan_();
void clear_roaming_state_();
bool roaming_suppressed_() const { #if defined(USE_ESP32) && defined(USE_WIFI_RUNTIME_ROAMING_SUPPRESSION) return this->roaming_suppression_count_.load(std::memory_order_relaxed) != 0; #else return false; #endif }
void release_scan_results_();
#ifdef USE_WIFI_CONNECT_STATE_LISTENERS void notify_connect_state_listeners_();
void notify_disconnect_state_listeners_();
#endif #ifdef USE_WIFI_IP_STATE_LISTENERS void notify_ip_state_listeners_();
#endif #ifdef USE_WIFI_SCAN_RESULTS_LISTENERS void notify_scan_results_listeners_();
#endif #ifdef USE_ESP8266 static void wifi_event_callback(System_Event_t *event);
void wifi_scan_done_callback_(void *arg, STATUS status);
static void s_wifi_scan_done_callback(void *arg, STATUS status);
#endif #ifdef USE_ESP32 void wifi_process_event_(IDFWiFiEvent *data);
#endif #ifdef USE_RP2 static int s_wifi_scan_result(void *env, const cyw43_ev_scan_result_t *result);
void wifi_scan_result(void *env, const cyw43_ev_scan_result_t *result);
#endif #ifdef USE_LIBRETINY void wifi_event_callback_(arduino_event_id_t event, arduino_event_info_t info);
void wifi_process_event_(LTWiFiEvent *event);
void wifi_scan_done_callback_();
#endif FixedVector<WiFiAP> sta_;
std::vector<WiFiSTAPriority> sta_priorities_;
wifi_scan_vector_t<WiFiScanResult> scan_result_;
#ifdef USE_WIFI_AP WiFiAP ap_;
#endif #ifdef USE_WIFI_IP_STATE_LISTENERS StaticVector<WiFiIPStateListener *, ESPHOME_WIFI_IP_STATE_LISTENERS> ip_state_listeners_;
#endif #ifdef USE_WIFI_SCAN_RESULTS_LISTENERS StaticVector<WiFiScanResultsListener *, ESPHOME_WIFI_SCAN_RESULTS_LISTENERS> scan_results_listeners_;
#endif #ifdef USE_WIFI_CONNECT_STATE_LISTENERS StaticVector<WiFiConnectStateListener *, ESPHOME_WIFI_CONNECT_STATE_LISTENERS> connect_state_listeners_;
#endif #ifdef USE_WIFI_POWER_SAVE_LISTENERS StaticVector<WiFiPowerSaveListener *, ESPHOME_WIFI_POWER_SAVE_LISTENERS> power_save_listeners_;
#endif ESPPreferenceObject pref_;
#ifdef USE_WIFI_FAST_CONNECT ESPPreferenceObject fast_connect_pref_;
#endif #ifdef USE_WIFI_CONNECT_TRIGGER Trigger<> connect_trigger_;
#endif #ifdef USE_WIFI_DISCONNECT_TRIGGER Trigger<> disconnect_trigger_;
#endif #if defined(USE_ESP32) && defined(USE_WIFI_RUNTIME_POWER_SAVE) SemaphoreHandle_t high_performance_semaphore_{nullptr}
#endif static constexpr uint8_t FIRST_5GHZ_CHANNEL = 36;
static constexpr uint32_t ROAMING_CHECK_INTERVAL = 5 * 60 * 1000;
static constexpr int8_t ROAMING_MIN_IMPROVEMENT = 10;
static constexpr int8_t ROAMING_GOOD_RSSI = -49;
static constexpr uint8_t ROAMING_MAX_ATTEMPTS = 3;
static constexpr uint32_t ROAMING_SCAN_GRACE_PERIOD = 30 * 1000;
float output_power_{NAN}
uint32_t action_started_;
uint32_t last_connected_{0}
uint32_t reboot_timeout_{}
uint32_t roaming_last_check_{0}
uint32_t roaming_scan_end_{0}
#ifdef USE_WIFI_AP uint32_t ap_timeout_{}
#endif WiFiComponentState state_{WIFI_COMPONENT_STATE_OFF}
WiFiPowerSaveMode power_save_{WIFI_POWER_SAVE_NONE}
#if defined(USE_ESP32) && defined(SOC_WIFI_SUPPORT_5G) wifi_band_mode_t band_mode_{WIFI_BAND_MODE_AUTO}
#endif #ifdef USE_WIFI_PHY_MODE WiFi8266PhyMode phy_mode_{WIFI_8266_PHY_MODE_AUTO}
#endif WifiMinAuthMode min_auth_mode_{WIFI_MIN_AUTH_MODE_WPA2}
WiFiRetryPhase retry_phase_{WiFiRetryPhase::INITIAL_CONNECT}
uint8_t num_retried_{0}
int8_t selected_sta_index_{-1}
uint8_t roaming_attempts_{0}
#if defined(USE_ESP32) && defined(USE_WIFI_RUNTIME_ROAMING_SUPPRESSION) std::atomic<uint8_t> roaming_suppression_count_{0}
#endif #if USE_NETWORK_IPV6 uint8_t num_ipv6_addresses_{0}
#endif bool error_from_callback_{false}
#if defined(USE_ESP8266) || defined(USE_LIBRETINY) uint8_t sta_state_{0}
#endif RetryHiddenMode retry_hidden_mode_{RetryHiddenMode::BLIND_RETRY}
RoamingState roaming_state_{RoamingState::IDLE}
bssid_t roaming_target_bssid_{}
#if defined(USE_ESP32) && defined(USE_WIFI_RUNTIME_POWER_SAVE) WiFiPowerSaveMode configured_power_save_{WIFI_POWER_SAVE_NONE}
#endif struct { #ifdef USE_WIFI_CONNECT_STATE_LISTENERS bool connect_state : 1; #ifdef USE_ESP8266 bool disconnect : 1; #endif #endif #if defined(USE_ESP8266) && defined(USE_WIFI_IP_STATE_LISTENERS) bool got_ip : 1; #endif #if defined(USE_ESP8266) && defined(USE_WIFI_SCAN_RESULTS_LISTENERS) bool scan_complete : 1; #endif }
pending_{}
bool has_ap_{false}
#if defined(USE_WIFI_CONNECT_TRIGGER) || defined(USE_WIFI_DISCONNECT_TRIGGER) bool handled_connected_state_{false}
#endif bool scan_done_{false}
bool ap_setup_{false}
bool ap_started_{false}
bool passive_scan_{false}
bool has_saved_wifi_settings_{false}
#ifdef USE_WIFI_11KV_SUPPORT bool btm_{false}
bool rrm_{false}
#endif bool enable_on_boot_{true}
#ifdef USE_ESP32 bool wifi_initialized_{false}
#endif bool got_ipv4_address_{false}
bool keep_scan_results_{false}
bool has_completed_scan_after_captive_portal_start_{ false}
bool skip_cooldown_next_cycle_{false}
bool connected_{false}
bool post_connect_roaming_{true}
#if defined(USE_ESP32) && defined(USE_WIFI_RUNTIME_POWER_SAVE) bool is_high_performance_mode_{false}
#endif #ifdef USE_ESP32 LockFreeQueue<IDFWiFiEvent, 17> event_queue_;
#endif #ifdef USE_LIBRETINY static constexpr uint8_t LT_EVENT_QUEUE_SIZE = 16;
#ifdef ESPHOME_THREAD_MULTI_ATOMICS LockFreeQueue<LTWiFiEvent, LT_EVENT_QUEUE_SIZE + 1> event_queue_;
#else FreeRTOSQueue<LTWiFiEvent, LT_EVENT_QUEUE_SIZE> event_queue_;
#endif #endif private: const char *use_address_{nullptr}
```
