# ESPHome component: `mqtt`

Source: `esphome/components/mqtt/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `custom_mqtt_device.h`

**class `CustomMQTTDevice` — public interface:**
```cpp
template<typename T> void subscribe(const std::string &topic, void (T::*callback)(const std::string &, const std::string &), uint8_t qos = 0);
template<typename T> void subscribe(const std::string &topic, void (T::*callback)(const std::string &), uint8_t qos = 0);
template<typename T> void subscribe(const std::string &topic, void (T::*callback)(), uint8_t qos = 0);
template<typename T> void subscribe_json(const std::string &topic, void (T::*callback)(const std::string &, JsonObject), uint8_t qos = 0);
template<typename T> void subscribe_json(const std::string &topic, void (T::*callback)(JsonObject), uint8_t qos = 0);
bool publish(const std::string &topic, const std::string &payload, uint8_t qos = 0, bool retain = false);
bool publish(const std::string &topic, float value, int8_t number_decimals = 3);
bool publish(const std::string &topic, int value);
bool publish_json(const std::string &topic, const json::json_build_t &f, uint8_t qos, bool retain);
bool publish_json(const std::string &topic, const json::json_build_t &f);
bool is_connected();
```

## `mqtt_alarm_control_panel.h`

**class `MQTTAlarmControlPanelComponent` — public interface:**
```cpp
explicit MQTTAlarmControlPanelComponent(alarm_control_panel::AlarmControlPanel *alarm_control_panel);
void setup() override;
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
bool send_initial_state() override;
bool publish_state();
void dump_config() override;
```

## `mqtt_backend.h`

**Enums:**
```cpp
enum class MQTTClientDisconnectReason : int8_t {
  TCP_DISCONNECTED = 0,
  MQTT_UNACCEPTABLE_PROTOCOL_VERSION = 1,
  MQTT_IDENTIFIER_REJECTED = 2,
  MQTT_SERVER_UNAVAILABLE = 3,
  MQTT_MALFORMED_CREDENTIALS = 4,
  MQTT_NOT_AUTHORIZED = 5,
  ESP8266_NOT_ENOUGH_SPACE = 6,
  TLS_BAD_FINGERPRINT = 7,
  DNS_RESOLVE_ERROR = 8
};
```

**class `MQTTBackend` — public interface:**
```cpp
using on_connect_callback_t = void(bool session_present);
using on_disconnect_callback_t = void(MQTTClientDisconnectReason reason);
using on_subscribe_callback_t = void(uint16_t packet_id, uint8_t qos);
using on_unsubscribe_callback_t = void(uint16_t packet_id);
using on_message_callback_t = void(const char *topic, const char *payload, size_t len, size_t index, size_t total);
using on_publish_user_callback_t = void(uint16_t packet_id);
virtual void set_keep_alive(uint16_t keep_alive) = 0;
virtual void set_client_id(const char *client_id) = 0;
virtual void set_clean_session(bool clean_session) = 0;
virtual void set_credentials(const char *username, const char *password) = 0;
virtual void set_will(const char *topic, uint8_t qos, bool retain, const char *payload) = 0;
virtual void set_server(network::IPAddress ip, uint16_t port) = 0;
virtual void set_server(const char *host, uint16_t port) = 0;
virtual void set_on_connect(std::function<on_connect_callback_t> &&callback) = 0;
virtual void set_on_disconnect(std::function<on_disconnect_callback_t> &&callback) = 0;
virtual void set_on_subscribe(std::function<on_subscribe_callback_t> &&callback) = 0;
virtual void set_on_unsubscribe(std::function<on_unsubscribe_callback_t> &&callback) = 0;
virtual void set_on_message(std::function<on_message_callback_t> &&callback) = 0;
virtual void set_on_publish(std::function<on_publish_user_callback_t> &&callback) = 0;
virtual bool connected() const = 0;
virtual void connect() = 0;
virtual void disconnect() = 0;
virtual bool subscribe(const char *topic, uint8_t qos) = 0;
virtual bool unsubscribe(const char *topic) = 0;
virtual bool publish(const char *topic, const char *payload, size_t length, uint8_t qos, bool retain) = 0;
virtual bool publish(const MQTTMessage &message) { return publish(message.topic.c_str(), message.payload.c_str(), message.payload.length(), message.qos, message.retain); }
virtual void loop() {}
```

## `mqtt_backend_esp32.h`

**Enums:**
```cpp
enum MqttQueueTypeT : uint8_t {
  MQTT_QUEUE_TYPE_NONE = 0,
  MQTT_QUEUE_TYPE_SUBSCRIBE,
  MQTT_QUEUE_TYPE_UNSUBSCRIBE,
  MQTT_QUEUE_TYPE_PUBLISH,
};
```

**class `MQTTBackendESP32` — public interface:**
```cpp
static constexpr size_t MQTT_BUFFER_SIZE = 4096;
static constexpr size_t TASK_STACK_SIZE = 3072;
static constexpr size_t TASK_STACK_SIZE_TLS = 4096;
static constexpr ssize_t TASK_PRIORITY = 5;
static constexpr uint8_t MQTT_QUEUE_LENGTH = 30;
static constexpr uint8_t MQTT_EVENT_QUEUE_LENGTH = 32;
void set_keep_alive(uint16_t keep_alive) final { this->keep_alive_ = keep_alive; }
void set_client_id(const char *client_id) final { this->client_id_ = client_id; }
void set_clean_session(bool clean_session) final { this->clean_session_ = clean_session; }
void set_credentials(const char *username, const char *password) final { if (username) this->username_ = username; if (password) this->password_ = password; }
void set_will(const char *topic, uint8_t qos, bool retain, const char *payload) final { if (topic) this->lwt_topic_ = topic; this->lwt_qos_ = qos; if (payload) this->lwt_message_ = payload; this->lwt_retain_ = retain; }
void set_server(network::IPAddress ip, uint16_t port) final { char ip_buf[network::IP_ADDRESS_BUFFER_SIZE]; this->host_ = ip.str_to(ip_buf); this->port_ = port; }
void set_server(const char *host, uint16_t port) final { this->host_ = host; this->port_ = port; }
void set_on_connect(std::function<on_connect_callback_t> &&callback) final { this->on_connect_.add(std::move(callback)); }
void set_on_disconnect(std::function<on_disconnect_callback_t> &&callback) final { this->on_disconnect_.add(std::move(callback)); }
void set_on_subscribe(std::function<on_subscribe_callback_t> &&callback) final { this->on_subscribe_.add(std::move(callback)); }
void set_on_unsubscribe(std::function<on_unsubscribe_callback_t> &&callback) final { this->on_unsubscribe_.add(std::move(callback)); }
void set_on_message(std::function<on_message_callback_t> &&callback) final { this->on_message_.add(std::move(callback)); }
void set_on_publish(std::function<on_publish_user_callback_t> &&callback) final { this->on_publish_.add(std::move(callback)); }
bool connected() const final { return this->is_connected_; }
void connect() final { if (!is_initalized_) { if (initialize_()) { esp_mqtt_client_start(handler_.get()); } } }
void disconnect() final { if (is_initalized_) esp_mqtt_client_disconnect(handler_.get()); }
bool subscribe(const char *topic, uint8_t qos) final { #if defined(USE_MQTT_IDF_ENQUEUE) return enqueue_(MQTT_QUEUE_TYPE_SUBSCRIBE, topic, qos); #else return esp_mqtt_client_subscribe(handler_.get(), topic, qos) != -1; #endif }
bool unsubscribe(const char *topic) final { #if defined(USE_MQTT_IDF_ENQUEUE) return enqueue_(MQTT_QUEUE_TYPE_UNSUBSCRIBE, topic); #else return esp_mqtt_client_unsubscribe(handler_.get(), topic) != -1; #endif }
bool publish(const char *topic, const char *payload, size_t length, uint8_t qos, bool retain) final { #if defined(USE_MQTT_IDF_ENQUEUE) return enqueue_(MQTT_QUEUE_TYPE_PUBLISH, topic, qos, retain, payload, length); #else return esp_mqtt_client_publish(handler_.get(), topic, payload, length, qos, retain) != -1; #endif }
using MQTTBackend::publish;
void loop() final;
void set_ca_certificate(const std::string &cert) { ca_certificate_ = cert; }
void set_cl_certificate(const std::string &cert) { cl_certificate_ = cert; }
void set_cl_key(const std::string &key) { cl_key_ = key; }
void set_skip_cert_cn_check(bool skip_check) { skip_cert_cn_check_ = skip_check; }
```

## `mqtt_backend_esp8266.h`

**class `MQTTBackendESP8266` — public interface:**
```cpp
void set_keep_alive(uint16_t keep_alive) final { mqtt_client_.setKeepAlive(keep_alive); }
void set_client_id(const char *client_id) final { mqtt_client_.setClientId(client_id); }
void set_clean_session(bool clean_session) final { mqtt_client_.setCleanSession(clean_session); }
void set_credentials(const char *username, const char *password) final { mqtt_client_.setCredentials(username, password); }
void set_will(const char *topic, uint8_t qos, bool retain, const char *payload) final { mqtt_client_.setWill(topic, qos, retain, payload); }
void set_server(network::IPAddress ip, uint16_t port) final { mqtt_client_.setServer(ip, port); }
void set_server(const char *host, uint16_t port) final { mqtt_client_.setServer(host, port); }
void set_on_connect(std::function<on_connect_callback_t> &&callback) final { this->mqtt_client_.onConnect(std::move(callback)); }
void set_on_disconnect(std::function<on_disconnect_callback_t> &&callback) final { auto async_callback = [callback](AsyncMqttClientDisconnectReason reason) { callback(static_cast<MQTTClientDisconnectReason>(reason)); }; this->mqtt_client_.onDisconnect(std::move(async_callback)); }
void set_on_subscribe(std::function<on_subscribe_callback_t> &&callback) final { this->mqtt_client_.onSubscribe(std::move(callback)); }
void set_on_unsubscribe(std::function<on_unsubscribe_callback_t> &&callback) final { this->mqtt_client_.onUnsubscribe(std::move(callback)); }
void set_on_message(std::function<on_message_callback_t> &&callback) final { auto async_callback = [callback](const char *topic, const char *payload, AsyncMqttClientMessageProperties async_properties, size_t len, size_t index, size_t total) { callback(topic, payload, len, index, total); }; mqtt_client_.onMessage(std::move(async_callback)); }
void set_on_publish(std::function<on_publish_user_callback_t> &&callback) final { this->mqtt_client_.onPublish(std::move(callback)); }
bool connected() const final { return mqtt_client_.connected(); }
void connect() final { mqtt_client_.connect(); }
void disconnect() final { mqtt_client_.disconnect(true); }
bool subscribe(const char *topic, uint8_t qos) final { return mqtt_client_.subscribe(topic, qos) != 0; }
bool unsubscribe(const char *topic) final { return mqtt_client_.unsubscribe(topic) != 0; }
bool publish(const char *topic, const char *payload, size_t length, uint8_t qos, bool retain) final { return mqtt_client_.publish(topic, qos, retain, payload, length, false, 0) != 0; }
using MQTTBackend::publish;
```

## `mqtt_backend_libretiny.h`

**class `MQTTBackendLibreTiny` — public interface:**
```cpp
void set_keep_alive(uint16_t keep_alive) final { mqtt_client_.setKeepAlive(keep_alive); }
void set_client_id(const char *client_id) final { mqtt_client_.setClientId(client_id); }
void set_clean_session(bool clean_session) final { mqtt_client_.setCleanSession(clean_session); }
void set_credentials(const char *username, const char *password) final { mqtt_client_.setCredentials(username, password); }
void set_will(const char *topic, uint8_t qos, bool retain, const char *payload) final { mqtt_client_.setWill(topic, qos, retain, payload); }
void set_server(network::IPAddress ip, uint16_t port) final { mqtt_client_.setServer(IPAddress(ip), port); }
void set_server(const char *host, uint16_t port) final { mqtt_client_.setServer(host, port); }
void set_on_connect(std::function<on_connect_callback_t> &&callback) final { this->mqtt_client_.onConnect(std::move(callback)); }
void set_on_disconnect(std::function<on_disconnect_callback_t> &&callback) final { auto async_callback = [callback](AsyncMqttClientDisconnectReason reason) { callback(static_cast<MQTTClientDisconnectReason>(reason)); }; this->mqtt_client_.onDisconnect(std::move(async_callback)); }
void set_on_subscribe(std::function<on_subscribe_callback_t> &&callback) final { this->mqtt_client_.onSubscribe(std::move(callback)); }
void set_on_unsubscribe(std::function<on_unsubscribe_callback_t> &&callback) final { this->mqtt_client_.onUnsubscribe(std::move(callback)); }
void set_on_message(std::function<on_message_callback_t> &&callback) final { auto async_callback = [callback](const char *topic, const char *payload, AsyncMqttClientMessageProperties async_properties, size_t len, size_t index, size_t total) { callback(topic, payload, len, index, total); }; mqtt_client_.onMessage(std::move(async_callback)); }
void set_on_publish(std::function<on_publish_user_callback_t> &&callback) final { this->mqtt_client_.onPublish(std::move(callback)); }
bool connected() const final { return mqtt_client_.connected(); }
void connect() final { mqtt_client_.connect(); }
void disconnect() final { mqtt_client_.disconnect(true); }
bool subscribe(const char *topic, uint8_t qos) final { return mqtt_client_.subscribe(topic, qos) != 0; }
bool unsubscribe(const char *topic) final { return mqtt_client_.unsubscribe(topic) != 0; }
bool publish(const char *topic, const char *payload, size_t length, uint8_t qos, bool retain) final { return mqtt_client_.publish(topic, qos, retain, payload, length, false, 0) != 0; }
using MQTTBackend::publish;
```

## `mqtt_binary_sensor.h`

**class `MQTTBinarySensorComponent` — public interface:**
```cpp
explicit MQTTBinarySensorComponent(binary_sensor::BinarySensor *binary_sensor);
void setup() override;
void dump_config() override;
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
void set_is_status(bool status);
bool send_initial_state() override;
bool publish_state(bool state);
```

## `mqtt_button.h`

**class `MQTTButtonComponent` — public interface:**
```cpp
explicit MQTTButtonComponent(button::Button *button);
void setup() override;
void dump_config() override;
bool send_initial_state() override { return true; }
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
```

## `mqtt_client.h`

**Enums:**
```cpp
enum MQTTDiscoveryUniqueIdGenerator {
  MQTT_LEGACY_UNIQUE_ID_GENERATOR = 0,
  MQTT_MAC_ADDRESS_UNIQUE_ID_GENERATOR,
};
enum MQTTDiscoveryObjectIdGenerator {
  MQTT_NONE_OBJECT_ID_GENERATOR = 0,
  MQTT_DEVICE_NAME_OBJECT_ID_GENERATOR,
};
enum MQTTClientState {
  MQTT_CLIENT_DISABLED = 0,
  MQTT_CLIENT_DISCONNECTED,
  MQTT_CLIENT_RESOLVING_ADDRESS,
  MQTT_CLIENT_CONNECTING,
  MQTT_CLIENT_CONNECTED,
};
```

**class `MQTTClientComponent` — public interface:**
```cpp
MQTTClientComponent();
void set_last_will(MQTTMessage &&message);
void disable_last_will();
void set_birth_message(MQTTMessage &&message);
void disable_birth_message();
void set_shutdown_message(MQTTMessage &&message);
void disable_shutdown_message();
void set_keep_alive(uint16_t keep_alive_s);
void set_discovery_info(std::string &&prefix, MQTTDiscoveryUniqueIdGenerator unique_id_generator, MQTTDiscoveryObjectIdGenerator object_id_generator, bool retain, bool discover_ip, bool clean = false);
const MQTTDiscoveryInfo &get_discovery_info() const;
void disable_discovery();
bool is_discovery_enabled() const;
bool is_discovery_ip_enabled() const;
#ifdef USE_ESP32 void set_ca_certificate(const char *cert) { this->mqtt_backend_.set_ca_certificate(cert); }
void set_cl_certificate(const char *cert) { this->mqtt_backend_.set_cl_certificate(cert); }
void set_cl_key(const char *key) { this->mqtt_backend_.set_cl_key(key); }
void set_skip_cert_cn_check(bool skip_check) { this->mqtt_backend_.set_skip_cert_cn_check(skip_check); }
#endif const Availability &get_availability();
void set_topic_prefix(const std::string &topic_prefix, const std::string &check_topic_prefix);
const std::string &get_topic_prefix() const;
void set_log_message_template(MQTTMessage &&message);
void set_log_level(int level);
void disable_log_message();
bool is_log_message_enabled() const;
void subscribe(const std::string &topic, mqtt_callback_t callback, uint8_t qos = 0);
void subscribe_json(const std::string &topic, const mqtt_json_callback_t &callback, uint8_t qos = 0);
void unsubscribe(const std::string &topic);
bool publish(const MQTTMessage &message);
bool publish(const std::string &topic, const std::string &payload, uint8_t qos = 0, bool retain = false);
bool publish(const std::string &topic, const char *payload, size_t payload_length, uint8_t qos = 0, bool retain = false);
bool publish(const char *topic, const char *payload, size_t payload_length, uint8_t qos = 0, bool retain = false);
bool publish_json(const std::string &topic, const json::json_build_t &f, uint8_t qos = 0, bool retain = false);
bool publish_json(const char *topic, const json::json_build_t &f, uint8_t qos = 0, bool retain = false);
void setup() override;
void dump_config() override;
void loop() override;
float get_setup_priority() const override;
#ifdef USE_LOGGER void on_log(uint8_t level, const char *tag, const char *message, size_t message_len);
#endif void on_message(const std::string &topic, const std::string &payload);
bool can_proceed() override;
void check_connected();
void set_reboot_timeout(uint32_t reboot_timeout);
void register_mqtt_component(MQTTComponent *component);
bool is_connected();
void set_enable_on_boot(bool enable_on_boot) { this->enable_on_boot_ = enable_on_boot; }
void enable();
void disable();
void on_shutdown() override;
void set_broker_address(const std::string &address) { this->credentials_.address = address; }
void set_broker_port(uint16_t port) { this->credentials_.port = port; }
void set_username(const std::string &username) { this->credentials_.username = username; }
void set_password(const std::string &password) { this->credentials_.password = password; }
void set_client_id(const std::string &client_id) { this->credentials_.client_id = client_id; }
void set_clean_session(const bool &clean_session) { this->credentials_.clean_session = clean_session; }
void set_on_connect(mqtt_on_connect_callback_t &&callback);
void set_on_disconnect(mqtt_on_disconnect_callback_t &&callback);
void set_publish_nan_as_none(bool publish_nan_as_none);
bool is_publish_nan_as_none() const;
void set_wait_for_connection(bool wait_for_connection) { this->wait_for_connection_ = wait_for_connection; }
```

**class `MQTTMessageTrigger` — public interface:**
```cpp
explicit MQTTMessageTrigger(std::string topic);
void set_qos(uint8_t qos);
void set_payload(const std::string &payload);
void setup() override;
void dump_config() override;
float get_setup_priority() const override;
```

**class `MQTTJsonMessageTrigger` — public interface:**
```cpp
explicit MQTTJsonMessageTrigger(const std::string &topic, uint8_t qos) { global_mqtt_client->subscribe_json( topic, [this](const std::string &topic, JsonObject root) { this->trigger(root); }, qos); }
```

**class `MQTTConnectTrigger` — public interface:**
```cpp
explicit MQTTConnectTrigger(MQTTClientComponent *client) { client->set_on_connect([this](bool session_present) { this->trigger(session_present); }); }
```

**class `MQTTDisconnectTrigger` — public interface:**
```cpp
explicit MQTTDisconnectTrigger(MQTTClientComponent *client) { client->set_on_disconnect([this](MQTTClientDisconnectReason reason) { this->trigger(reason); }); }
```

**class `MQTTPublishAction` — public interface:**
```cpp
MQTTPublishAction(MQTTClientComponent *parent) : parent_(parent) {}
TEMPLATABLE_VALUE(std::string, topic) TEMPLATABLE_VALUE(std::string, payload) TEMPLATABLE_VALUE(uint8_t, qos) TEMPLATABLE_VALUE(bool, retain) void play(const Ts &...x) override { this->parent_->publish(this->topic_.value(x...), this->payload_.value(x...), this->qos_.value(x...), this->retain_.value(x...)); }
```

**class `MQTTPublishJsonAction` — public interface:**
```cpp
MQTTPublishJsonAction(MQTTClientComponent *parent) : parent_(parent) {}
TEMPLATABLE_VALUE(std::string, topic) TEMPLATABLE_VALUE(uint8_t, qos) TEMPLATABLE_VALUE(bool, retain) void set_payload(std::function<void(Ts..., JsonObject)> payload) { this->payload_ = payload; }
void play(const Ts &...x) override { auto topic = this->topic_.value(x...); auto qos = this->qos_.value(x...); auto retain = this->retain_.value(x...); this->parent_->publish_json( topic, [this, x...](JsonObject root) { this->payload_(x..., root); }, qos, retain); }
```

**class `MQTTConnectedCondition` — public interface:**
```cpp
MQTTConnectedCondition(MQTTClientComponent *parent) : parent_(parent) {}
bool check(const Ts &...x) override { return this->parent_->is_connected(); }
```

**class `MQTTEnableAction` — public interface:**
```cpp
MQTTEnableAction(MQTTClientComponent *parent) : parent_(parent) {}
void play(const Ts &...x) override { this->parent_->enable(); }
```

**class `MQTTDisableAction` — public interface:**
```cpp
MQTTDisableAction(MQTTClientComponent *parent) : parent_(parent) {}
void play(const Ts &...x) override { this->parent_->disable(); }
```

## `mqtt_climate.h`

**class `MQTTClimateComponent` — public interface:**
```cpp
MQTTClimateComponent(climate::Climate *device);
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
bool send_initial_state() override;
const char *component_type() const override;
void setup() override;
MQTT_COMPONENT_CUSTOM_TOPIC(current_temperature, state) MQTT_COMPONENT_CUSTOM_TOPIC(current_humidity, state) MQTT_COMPONENT_CUSTOM_TOPIC(mode, state) MQTT_COMPONENT_CUSTOM_TOPIC(mode, command) MQTT_COMPONENT_CUSTOM_TOPIC(target_temperature, state) MQTT_COMPONENT_CUSTOM_TOPIC(target_temperature, command) MQTT_COMPONENT_CUSTOM_TOPIC(target_temperature_low, state) MQTT_COMPONENT_CUSTOM_TOPIC(target_temperature_low, command) MQTT_COMPONENT_CUSTOM_TOPIC(target_temperature_high, state) MQTT_COMPONENT_CUSTOM_TOPIC(target_temperature_high, command) MQTT_COMPONENT_CUSTOM_TOPIC(target_humidity, state) MQTT_COMPONENT_CUSTOM_TOPIC(target_humidity, command) MQTT_COMPONENT_CUSTOM_TOPIC(away, state) MQTT_COMPONENT_CUSTOM_TOPIC(away, command) MQTT_COMPONENT_CUSTOM_TOPIC(action, state) MQTT_COMPONENT_CUSTOM_TOPIC(fan_mode, state) MQTT_COMPONENT_CUSTOM_TOPIC(fan_mode, command) MQTT_COMPONENT_CUSTOM_TOPIC(swing_mode, state) MQTT_COMPONENT_CUSTOM_TOPIC(swing_mode, command) MQTT_COMPONENT_CUSTOM_TOPIC(preset, state) MQTT_COMPONENT_CUSTOM_TOPIC(preset, command) protected: const EntityBase *get_entity() const override;
bool publish_state_();
climate::Climate *device_;
```

## `mqtt_component.h`

**class `MQTTComponent` — public interface:**
```cpp
explicit MQTTComponent();
void call_setup() override;
virtual void send_discovery(JsonObject root, SendDiscoveryConfig &config) = 0;
virtual bool send_initial_state() = 0;
bool is_internal() const { return this->is_internal_; }
void set_qos(uint8_t qos);
uint8_t get_qos() const;
void set_retain(bool retain);
bool get_retain() const;
void disable_discovery();
bool is_discovery_enabled() const;
void set_subscribe_qos(uint8_t qos);
virtual const char *component_type() const = 0;
template<typename T> void set_custom_state_topic(T &&custom_state_topic) { this->custom_state_topic_ = std::forward<T>(custom_state_topic); }
template<typename T> void set_custom_command_topic(T &&custom_command_topic) { this->custom_command_topic_ = std::forward<T>(custom_command_topic); }
void set_command_retain(bool command_retain);
float get_setup_priority() const override;
void set_availability(std::string topic, std::string payload_available, std::string payload_not_available);
void disable_availability();
void schedule_resend_state();
bool is_resend_pending() const { return this->resend_state_; }
void process_resend();
bool publish(const std::string &topic, const std::string &payload);
bool publish(const std::string &topic, const char *payload, size_t payload_length);
bool publish(const std::string &topic, const char *payload) { return this->publish(topic.c_str(), payload, strlen(payload)); }
bool publish(const char *topic, const char *payload, size_t payload_length);
bool publish(StringRef topic, const char *payload, size_t payload_length) { return this->publish(topic.c_str(), payload, payload_length); }
bool publish(const char *topic, const char *payload);
bool publish(StringRef topic, const char *payload) { return this->publish(topic.c_str(), payload); }
#ifdef USE_ESP8266 bool publish(const std::string &topic, ProgmemStr payload);
bool publish(const char *topic, ProgmemStr payload);
bool publish(StringRef topic, ProgmemStr payload) { return this->publish(topic.c_str(), payload); }
#endif bool publish_json(const std::string &topic, const json::json_build_t &f);
bool publish_json(const char *topic, const json::json_build_t &f);
bool publish_json(StringRef topic, const json::json_build_t &f) { return this->publish_json(topic.c_str(), f); }
void subscribe(const std::string &topic, mqtt_callback_t callback, uint8_t qos = 0);
void subscribe_json(const std::string &topic, const mqtt_json_callback_t &callback, uint8_t qos = 0);
```

## `mqtt_cover.h`

**class `MQTTCoverComponent` — public interface:**
```cpp
explicit MQTTCoverComponent(cover::Cover *cover);
void setup() override;
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
MQTT_COMPONENT_CUSTOM_TOPIC(position, command) MQTT_COMPONENT_CUSTOM_TOPIC(position, state) MQTT_COMPONENT_CUSTOM_TOPIC(tilt, command) MQTT_COMPONENT_CUSTOM_TOPIC(tilt, state) bool send_initial_state() override;
bool publish_state();
void dump_config() override;
#ifdef USE_MQTT_COVER_JSON void set_use_json_format(bool use_json_format) { this->use_json_format_ = use_json_format; }
#endif protected: const char *component_type() const override;
const EntityBase *get_entity() const override;
cover::Cover *cover_;
#ifdef USE_MQTT_COVER_JSON bool use_json_format_{false}
```

## `mqtt_date.h`

**class `MQTTDateComponent` — public interface:**
```cpp
explicit MQTTDateComponent(datetime::DateEntity *date);
void setup() override;
void dump_config() override;
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
bool send_initial_state() override;
bool publish_state(uint16_t year, uint8_t month, uint8_t day);
```

## `mqtt_datetime.h`

**class `MQTTDateTimeComponent` — public interface:**
```cpp
explicit MQTTDateTimeComponent(datetime::DateTimeEntity *datetime);
void setup() override;
void dump_config() override;
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
bool send_initial_state() override;
bool publish_state(uint16_t year, uint8_t month, uint8_t day, uint8_t hour, uint8_t minute, uint8_t second);
```

## `mqtt_event.h`

**class `MQTTEventComponent` — public interface:**
```cpp
explicit MQTTEventComponent(event::Event *event);
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
void setup() override;
void dump_config() override;
bool send_initial_state() override { return true; }
```

## `mqtt_fan.h`

**class `MQTTFanComponent` — public interface:**
```cpp
explicit MQTTFanComponent(fan::Fan *state);
MQTT_COMPONENT_CUSTOM_TOPIC(direction, command) MQTT_COMPONENT_CUSTOM_TOPIC(direction, state) MQTT_COMPONENT_CUSTOM_TOPIC(oscillation, command) MQTT_COMPONENT_CUSTOM_TOPIC(oscillation, state) MQTT_COMPONENT_CUSTOM_TOPIC(speed_level, command) MQTT_COMPONENT_CUSTOM_TOPIC(speed_level, state) MQTT_COMPONENT_CUSTOM_TOPIC(speed, command) MQTT_COMPONENT_CUSTOM_TOPIC(speed, state) void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
void setup() override;
void dump_config() override;
bool send_initial_state() override;
bool publish_state();
const char *component_type() const override;
fan::Fan *get_state() const;
```

## `mqtt_light.h`

**class `MQTTJSONLightComponent` — public interface:**
```cpp
explicit MQTTJSONLightComponent(light::LightState *state);
light::LightState *get_state() const;
void setup() override;
void dump_config() override;
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
bool send_initial_state() override;
void on_light_remote_values_update() override;
```

## `mqtt_lock.h`

**class `MQTTLockComponent` — public interface:**
```cpp
explicit MQTTLockComponent(lock::Lock *a_lock);
void setup() override;
void dump_config() override;
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
bool send_initial_state() override;
bool publish_state();
```

## `mqtt_number.h`

**class `MQTTNumberComponent` — public interface:**
```cpp
explicit MQTTNumberComponent(number::Number *number);
void setup() override;
void dump_config() override;
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
bool send_initial_state() override;
bool publish_state(float value);
```

## `mqtt_select.h`

**class `MQTTSelectComponent` — public interface:**
```cpp
explicit MQTTSelectComponent(select::Select *select);
void setup() override;
void dump_config() override;
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
bool send_initial_state() override;
bool publish_state(const std::string &value);
```

## `mqtt_sensor.h`

**class `MQTTSensorComponent` — public interface:**
```cpp
explicit MQTTSensorComponent(sensor::Sensor *sensor);
void set_expire_after(uint32_t expire_after);
void disable_expire_after();
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
void setup() override;
void dump_config() override;
uint32_t get_expire_after() const;
bool publish_state(float value);
bool send_initial_state() override;
```

## `mqtt_switch.h`

**class `MQTTSwitchComponent` — public interface:**
```cpp
explicit MQTTSwitchComponent(switch_::Switch *a_switch);
void setup() override;
void dump_config() override;
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
bool send_initial_state() override;
bool publish_state(bool state);
```

## `mqtt_text.h`

**class `MQTTTextComponent` — public interface:**
```cpp
explicit MQTTTextComponent(text::Text *text);
void setup() override;
void dump_config() override;
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
bool send_initial_state() override;
bool publish_state(const std::string &value);
```

## `mqtt_text_sensor.h`

**class `MQTTTextSensor` — public interface:**
```cpp
explicit MQTTTextSensor(text_sensor::TextSensor *sensor);
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
void setup() override;
void dump_config() override;
bool publish_state(const std::string &value);
bool send_initial_state() override;
```

## `mqtt_time.h`

**class `MQTTTimeComponent` — public interface:**
```cpp
explicit MQTTTimeComponent(datetime::TimeEntity *time);
void setup() override;
void dump_config() override;
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
bool send_initial_state() override;
bool publish_state(uint8_t hour, uint8_t minute, uint8_t second);
```

## `mqtt_update.h`

**class `MQTTUpdateComponent` — public interface:**
```cpp
explicit MQTTUpdateComponent(update::UpdateEntity *update);
void setup() override;
void dump_config() override;
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
bool send_initial_state() override;
bool publish_state();
```

## `mqtt_valve.h`

**class `MQTTValveComponent` — public interface:**
```cpp
explicit MQTTValveComponent(valve::Valve *valve);
void setup() override;
void send_discovery(JsonObject root, mqtt::SendDiscoveryConfig &config) override;
MQTT_COMPONENT_CUSTOM_TOPIC(position, command) MQTT_COMPONENT_CUSTOM_TOPIC(position, state) bool send_initial_state() override;
bool publish_state();
void dump_config() override;
```
