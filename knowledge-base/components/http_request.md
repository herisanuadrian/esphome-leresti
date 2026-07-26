# ESPHome component: `http_request`

Source: `esphome/components/http_request/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `http_request.h`

**Enums:**
```cpp
enum HttpStatus {
  HTTP_STATUS_OK = 200,
  HTTP_STATUS_NO_CONTENT = 204,
  HTTP_STATUS_RESET_CONTENT = 205,
  HTTP_STATUS_PARTIAL_CONTENT = 206,
  HTTP_STATUS_MULTIPLE_CHOICES = 300,
  HTTP_STATUS_MOVED_PERMANENTLY = 301,
  HTTP_STATUS_FOUND = 302,
  HTTP_STATUS_SEE_OTHER = 303,
  HTTP_STATUS_NOT_MODIFIED = 304,
  HTTP_STATUS_TEMPORARY_REDIRECT = 307,
  HTTP_STATUS_PERMANENT_REDIRECT = 308,
  HTTP_STATUS_BAD_REQUEST = 400,
  HTTP_STATUS_UNAUTHORIZED = 401,
  HTTP_STATUS_FORBIDDEN = 403,
  HTTP_STATUS_NOT_FOUND = 404,
  HTTP_STATUS_METHOD_NOT_ALLOWED = 405,
  HTTP_STATUS_NOT_ACCEPTABLE = 406,
  HTTP_STATUS_LENGTH_REQUIRED = 411,
  HTTP_STATUS_INTERNAL_ERROR = 500
};
enum class HttpReadStatus : uint8_t {
  OK,       
  ERROR,    
  TIMEOUT,  
};
enum class HttpReadLoopResult : uint8_t {
  DATA,      
  COMPLETE,  
  RETRY,     
  ERROR,     
  TIMEOUT,   
};
```

**class `HttpContainer` — public interface:**
```cpp
virtual ~HttpContainer() = default;
size_t content_length{0}
int status_code{-1}
uint32_t duration_ms{0}
virtual int read(uint8_t *buf, size_t max_len) = 0;
virtual void end() = 0;
void set_secure(bool secure) { this->secure_ = secure; }
void set_chunked(bool chunked) { this->is_chunked_ = chunked; }
size_t get_bytes_read() const { return this->bytes_read_; }
virtual bool is_read_complete() const { if ((this->status_code >= 100 && this->status_code < 200) || this->status_code == HTTP_STATUS_NO_CONTENT || this->status_code == HTTP_STATUS_RESET_CONTENT || this->status_code == HTTP_STATUS_NOT_MODIFIED) { return true; } return !this->is_chunked_ && this->bytes_read_ >= this->content_length; }
std::string get_response_header(const std::string &header_name);
```

**class `HttpRequestResponseTrigger` — public interface:**
```cpp
void process(const std::shared_ptr<HttpContainer> &container, std::string &response_body) { this->trigger(container, response_body); }
```

**class `HttpRequestComponent` — public interface:**
```cpp
void dump_config() override;
float get_setup_priority() const override { return setup_priority::AFTER_WIFI; }
void set_useragent(const char *useragent) { this->useragent_ = useragent; }
void set_timeout(uint32_t timeout) { this->timeout_ = timeout; }
uint32_t get_timeout() const { return this->timeout_; }
void set_watchdog_timeout(uint32_t watchdog_timeout) { this->watchdog_timeout_ = watchdog_timeout; }
uint32_t get_watchdog_timeout() const { return this->watchdog_timeout_; }
void set_follow_redirects(bool follow_redirects) { this->follow_redirects_ = follow_redirects; }
void set_redirect_limit(uint16_t limit) { this->redirect_limit_ = limit; }
std::shared_ptr<HttpContainer> get(const std::string &url) { return this->start(url, "GET", "", std::vector<Header>{}); }
std::shared_ptr<HttpContainer> get(const std::string &url, const std::vector<Header> &request_headers) { return this->start(url, "GET", "", request_headers); }
std::shared_ptr<HttpContainer> get(const std::string &url, const std::vector<Header> &request_headers, const std::vector<std::string> &lower_case_collect_headers) { return this->start(url, "GET", "", request_headers, lower_case_collect_headers); }
std::shared_ptr<HttpContainer> post(const std::string &url, const std::string &body) { return this->start(url, "POST", body, std::vector<Header>{}); }
std::shared_ptr<HttpContainer> post(const std::string &url, const std::string &body, const std::vector<Header> &request_headers) { return this->start(url, "POST", body, request_headers); }
std::shared_ptr<HttpContainer> post(const std::string &url, const std::string &body, const std::vector<Header> &request_headers, const std::vector<std::string> &lower_case_collect_headers) { return this->start(url, "POST", body, request_headers, lower_case_collect_headers); }
ESPDEPRECATED("Pass request_headers as std::vector<Header> instead of std::list. Removed in 2027.1.0.", "2026.7.0") std::shared_ptr<HttpContainer> get(const std::string &url, const std::list<Header> &request_headers) { return this->get(url, std::vector<Header>(request_headers.begin(), request_headers.end())); }
ESPDEPRECATED("Pass request_headers as std::vector<Header> instead of std::list. Removed in 2027.1.0.", "2026.7.0") std::shared_ptr<HttpContainer> get(const std::string &url, const std::list<Header> &request_headers, const std::vector<std::string> &collect_headers) { return this->get(url, std::vector<Header>(request_headers.begin(), request_headers.end()), collect_headers); }
ESPDEPRECATED("Pass request_headers as std::vector<Header> instead of std::list. Removed in 2027.1.0.", "2026.7.0") std::shared_ptr<HttpContainer> post(const std::string &url, const std::string &body, const std::list<Header> &request_headers) { return this->post(url, body, std::vector<Header>(request_headers.begin(), request_headers.end())); }
ESPDEPRECATED("Pass request_headers as std::vector<Header> instead of std::list. Removed in 2027.1.0.", "2026.7.0") std::shared_ptr<HttpContainer> post(const std::string &url, const std::string &body, const std::list<Header> &request_headers, const std::vector<std::string> &collect_headers) { return this->post(url, body, std::vector<Header>(request_headers.begin(), request_headers.end()), collect_headers); }
std::shared_ptr<HttpContainer> start(const std::string &url, const std::string &method, const std::string &body, const std::vector<Header> &request_headers) { return this->perform(url, method, body, request_headers, {}); }
ESPDEPRECATED("Pass request_headers as std::vector<Header> instead of std::list. Removed in 2027.1.0.", "2026.7.0") std::shared_ptr<HttpContainer> start(const std::string &url, const std::string &method, const std::string &body, const std::list<Header> &request_headers) { return this->start(url, method, body, std::vector<Header>(request_headers.begin(), request_headers.end())); }
ESPDEPRECATED("Pass collect_headers as std::vector<std::string> instead of std::set. Removed in 2027.1.0.", "2026.7.0") std::shared_ptr<HttpContainer> start(const std::string &url, const std::string &method, const std::string &body, const std::vector<Header> &request_headers, const std::set<std::string> &collect_headers) { std::vector<std::string> lower; lower.reserve(collect_headers.size()); for (const auto &h : collect_headers) { lower.push_back(str_lower_case(h)); } return this->perform(url, method, body, request_headers, lower); }
ESPDEPRECATED("Pass request_headers as std::vector<Header> instead of std::list, and collect_headers as " "std::vector<std::string> instead of std::set. Removed in 2027.1.0.", "2026.7.0") std::shared_ptr<HttpContainer> start(const std::string &url, const std::string &method, const std::string &body, const std::list<Header> &request_headers, const std::set<std::string> &collect_headers) { std::vector<std::string> lower; lower.reserve(collect_headers.size()); for (const auto &h : collect_headers) { lower.push_back(str_lower_case(h)); } return this->perform(url, method, body, std::vector<Header>(request_headers.begin(), request_headers.end()), lower); }
ESPDEPRECATED("Pass request_headers as std::vector<Header> instead of std::list. Removed in 2027.1.0.", "2026.7.0") std::shared_ptr<HttpContainer> start(const std::string &url, const std::string &method, const std::string &body, const std::list<Header> &request_headers, const std::vector<std::string> &lower_case_collect_headers) { return this->perform(url, method, body, std::vector<Header>(request_headers.begin(), request_headers.end()), lower_case_collect_headers); }
std::shared_ptr<HttpContainer> start(const std::string &url, const std::string &method, const std::string &body, const std::vector<Header> &request_headers, const std::vector<std::string> &lower_case_collect_headers) { return this->perform(url, method, body, request_headers, lower_case_collect_headers); }
```

**class `HttpRequestSendAction` — public interface:**
```cpp
HttpRequestSendAction(HttpRequestComponent *parent) : parent_(parent) {}
TEMPLATABLE_VALUE(std::string, url) TEMPLATABLE_VALUE(const char *, method) TEMPLATABLE_VALUE(std::string, body) #ifdef USE_HTTP_REQUEST_RESPONSE TEMPLATABLE_VALUE(bool, capture_response) #endif void init_request_headers(size_t count) { this->request_headers_.init(count); }
void add_request_header(const char *key, TemplatableFn<const char *, Ts...> value) { this->request_headers_.push_back({key, value}); }
void add_collect_header(const char *value) { this->lower_case_collect_headers_.emplace_back(value); }
void init_json(size_t count) { this->json_.init(count); }
void add_json(const char *key, TemplatableValue<std::string, Ts...> value) { this->json_.push_back({key, value}); }
void set_json(std::function<void(Ts..., JsonObject)> json_func) { this->json_func_ = json_func; }
#ifdef USE_HTTP_REQUEST_RESPONSE Trigger<std::shared_ptr<HttpContainer>, std::string &, Ts...> *get_success_trigger_with_response() { return &this->success_trigger_with_response_; }
#endif Trigger<std::shared_ptr<HttpContainer>, Ts...> *get_success_trigger() { return &this->success_trigger_; }
Trigger<Ts...> *get_error_trigger() { return &this->error_trigger_; }
void set_max_response_buffer_size(size_t max_response_buffer_size) { this->max_response_buffer_size_ = max_response_buffer_size; }
void play(const Ts &...x) override { std::string body; if (this->body_.has_value()) { body = this->body_.value(x...); } if (!this->json_.empty()) { body = json::build_json([this, x...](JsonObject root) mutable { this->encode_json_(x..., root); }); } if (this->json_func_ != nullptr) { body = json::build_json([this, x...](JsonObject root) mutable { this->json_func_(x..., root); }); } std::vector<Header> request_headers; request_headers.reserve(this->request_headers_.size()); for (const auto &[key, val] : this->request_headers_) { request_headers.push_back({key, val.value(x...)}); } auto container = this->parent_->start(this->url_.value(x...), this->method_.value(x...), body, request_headers, this->lower_case_collect_headers_); auto captured_args = std::make_tuple(x...); if (container == nullptr) { std::apply([this](Ts... captured_args_inner) { this->error_trigger_.trigger(captured_args_inner...); }, captured_args); return; } #ifdef USE_HTTP_REQUEST_RESPONSE if (this->capture_response_.value(x...)) { size_t max_length = this->max_response_buffer_size_; std::string response_body; RAMAllocator<uint8_t> allocator; uint8_t *buf = allocator.allocate(max_length); if (buf != nullptr) { size_t read_index = 0; uint32_t last_data_time = millis(); const uint32_t read_timeout = this->parent_->get_timeout(); while (container->get_bytes_read() < max_length) { int read_or_error = container->read(buf + read_index, std::min<size_t>(max_length - read_index, 512)); App.feed_wdt(); yield(); auto result = http_read_loop_result(read_or_error, last_data_time, read_timeout, container->is_read_complete()); if (result == HttpReadLoopResult::RETRY) continue; if (result != HttpReadLoopResult::DATA) break; read_index += read_or_error; } response_body.reserve(read_index); response_body.assign((char *) buf, read_index); allocator.deallocate(buf, max_length); } std::apply( [this, &container, &response_body](Ts... captured_args_inner) { this->success_trigger_with_response_.trigger(container, response_body, captured_args_inner...); }, captured_args); } else #endif { std::apply([this, &container]( Ts... captured_args_inner) { this->success_trigger_.trigger(container, captured_args_inner...); }, captured_args); } container->end(); }
```

## `http_request_arduino.h`

**Enums:**
```cpp
enum class ChunkedState : uint8_t {
  CHUNK_HEADER,      
  CHUNK_HEADER_EXT,  
  CHUNK_DATA,        
  CHUNK_DATA_TRAIL,  
  CHUNK_TRAILER,     
  COMPLETE,          
};
```

**class `HttpContainerArduino` — public interface:**
```cpp
int read(uint8_t *buf, size_t max_len) override;
void end() override;
```

**class `HttpRequestArduino` — public interface:**
```cpp
#ifdef USE_ESP8266 void set_tls_buffer_size_rx(uint16_t size) { this->tls_buffer_size_rx_ = size; }
void set_tls_buffer_size_tx(uint16_t size) { this->tls_buffer_size_tx_ = size; }
#endif protected: std::shared_ptr<HttpContainer> perform(const std::string &url, const std::string &method, const std::string &body, const std::vector<Header> &request_headers, const std::vector<std::string> &lower_case_collect_headers) override;
#ifdef USE_ESP8266 uint16_t tls_buffer_size_rx_{512}
uint16_t tls_buffer_size_tx_{512}
```

## `http_request_host.h`

**class `HttpContainerHost` — public interface:**
```cpp
int read(uint8_t *buf, size_t max_len) override;
void end() override;
```

**class `HttpRequestHost` — public interface:**
```cpp
std::shared_ptr<HttpContainer> perform(const std::string &url, const std::string &method, const std::string &body, const std::vector<Header> &request_headers, const std::vector<std::string> &lower_case_collect_headers) override;
void set_ca_path(const char *ca_path) { this->ca_path_ = ca_path; }
```

## `http_request_idf.h`

**class `HttpContainerIDF` — public interface:**
```cpp
HttpContainerIDF(esp_http_client_handle_t client) : client_(client) {}
int read(uint8_t *buf, size_t max_len) override;
void end() override;
bool is_read_complete() const override;
void feed_wdt();
```

**class `HttpRequestIDF` — public interface:**
```cpp
void dump_config() override;
void set_buffer_size_rx(uint16_t buffer_size_rx) { this->buffer_size_rx_ = buffer_size_rx; }
void set_buffer_size_tx(uint16_t buffer_size_tx) { this->buffer_size_tx_ = buffer_size_tx; }
void set_verify_ssl(bool verify_ssl) { this->verify_ssl_ = verify_ssl; }
void set_ca_certificate(const char *ca_certificate) { this->ca_certificate_ = ca_certificate; }
```

## `httplib.h`

**Enums:**
```cpp
enum StatusCode {
  Continue_100 = 100,
  SwitchingProtocol_101 = 101,
  Processing_102 = 102,
  EarlyHints_103 = 103,
  OK_200 = 200,
  Created_201 = 201,
  Accepted_202 = 202,
  NonAuthoritativeInformation_203 = 203,
  NoContent_204 = 204,
  ResetContent_205 = 205,
  PartialContent_206 = 206,
  MultiStatus_207 = 207,
  AlreadyReported_208 = 208,
  IMUsed_226 = 226,
  MultipleChoices_300 = 300,
  MovedPermanently_301 = 301,
  Found_302 = 302,
  SeeOther_303 = 303,
  NotModified_304 = 304,
  UseProxy_305 = 305,
  unused_306 = 306,
  TemporaryRedirect_307 = 307,
  PermanentRedirect_308 = 308,
  BadRequest_400 = 400,
  Unauthorized_401 = 401,
  PaymentRequired_402 = 402,
  Forbidden_403 = 403,
  NotFound_404 = 404,
  MethodNotAllowed_405 = 405,
  NotAcceptable_406 = 406,
  ProxyAuthenticationRequired_407 = 407,
  RequestTimeout_408 = 408,
  Conflict_409 = 409,
  Gone_410 = 410,
  LengthRequired_411 = 411,
  PreconditionFailed_412 = 412,
  PayloadTooLarge_413 = 413,
  UriTooLong_414 = 414,
  UnsupportedMediaType_415 = 415,
  RangeNotSatisfiable_416 = 416,
  ExpectationFailed_417 = 417,
  ImATeapot_418 = 418,
  MisdirectedRequest_421 = 421,
  UnprocessableContent_422 = 422,
  Locked_423 = 423,
  FailedDependency_424 = 424,
  TooEarly_425 = 425,
  UpgradeRequired_426 = 426,
  PreconditionRequired_428 = 428,
  TooManyRequests_429 = 429,
  RequestHeaderFieldsTooLarge_431 = 431,
  UnavailableForLegalReasons_451 = 451,
  InternalServerError_500 = 500,
  NotImplemented_501 = 501,
  BadGateway_502 = 502,
  ServiceUnavailable_503 = 503,
  GatewayTimeout_504 = 504,
  HttpVersionNotSupported_505 = 505,
  VariantAlsoNegotiates_506 = 506,
  InsufficientStorage_507 = 507,
  LoopDetected_508 = 508,
  NotExtended_510 = 510,
  NetworkAuthenticationRequired_511 = 511,
};
enum class HandlerResponse {
    Handled,
    Unhandled,
  };
enum class Error {
  Success = 0,
  Unknown,
  Connection,
  BindIPAddress,
  Read,
  Write,
  ExceedRedirectCount,
  Canceled,
  SSLConnection,
  SSLLoadingCerts,
  SSLServerVerification,
  SSLServerHostnameVerification,
  UnsupportedMultipartBoundaryChars,
  Compression,
  ConnectionTimeout,
  ProxyConnection,
  SSLPeerCouldBeClosed_,
};
enum class EncodingType { None = 0, Gzip, Brotli };
```

**Constants:**
```cpp
inline constexpr unsigned int operator""_t(const char *s, size_t l) { return str2tag_core(s, l, 0);
```

**class `DataSink` — public interface:**
```cpp
DataSink() : os(&sb_), sb_(*this) {}
DataSink(const DataSink &) = delete;
DataSink &operator=(const DataSink &) = delete;
DataSink(DataSink &&) = delete;
DataSink &operator=(DataSink &&) = delete;
std::function<bool(const char *data, size_t data_len)> write;
std::function<bool()> is_writable;
std::function<void()> done;
std::function<void(const Headers &trailer)> done_with_trailer;
std::ostream os;
```

**class `data_sink_streambuf` — public interface:**
```cpp
explicit data_sink_streambuf(DataSink &sink) : sink_(sink) {}
```

**class `ContentReader` — public interface:**
```cpp
using Reader = std::function<bool(ContentReceiver receiver)>;
using MultipartReader = std::function<bool(MultipartContentHeader header, ContentReceiver receiver)>;
ContentReader(Reader reader, MultipartReader multipart_reader) : reader_(std::move(reader)), multipart_reader_(std::move(multipart_reader)) {}
bool operator()(MultipartContentHeader header, ContentReceiver receiver) const { return multipart_reader_(std::move(header), std::move(receiver)); }
bool operator()(ContentReceiver receiver) const { return reader_(std::move(receiver)); }
Reader reader_;
MultipartReader multipart_reader_;
```

**class `Stream` — public interface:**
```cpp
virtual ~Stream() = default;
virtual bool is_readable() const = 0;
virtual bool is_writable() const = 0;
virtual ssize_t read(char *ptr, size_t size) = 0;
virtual ssize_t write(const char *ptr, size_t size) = 0;
virtual void get_remote_ip_and_port(std::string &ip, int &port) const = 0;
virtual void get_local_ip_and_port(std::string &ip, int &port) const = 0;
virtual socket_t socket() const = 0;
ssize_t write(const char *ptr);
ssize_t write(const std::string &s);
```

**class `TaskQueue` — public interface:**
```cpp
TaskQueue() = default;
virtual ~TaskQueue() = default;
virtual bool enqueue(std::function<void()> fn) = 0;
virtual void shutdown() = 0;
virtual void on_idle() {}
```

**class `ThreadPool` — public interface:**
```cpp
explicit ThreadPool(size_t n, size_t mqr = 0) : shutdown_(false), max_queued_requests_(mqr) { while (n) { threads_.emplace_back(worker(*this)); n--; } }
ThreadPool(const ThreadPool &) = delete;
~ThreadPool() override = default;
bool enqueue(std::function<void()> fn) override { { std::unique_lock<std::mutex> lock(mutex_); if (max_queued_requests_ > 0 && jobs_.size() >= max_queued_requests_) { return false; } jobs_.push_back(std::move(fn)); } cond_.notify_one(); return true; }
void shutdown() override { { std::unique_lock<std::mutex> lock(mutex_); shutdown_ = true; } cond_.notify_all(); for (auto &t : threads_) { t.join(); } }
```

**class `MatcherBase` — public interface:**
```cpp
virtual ~MatcherBase() = default;
virtual bool match(Request &request) const = 0;
```

**class `PathParamsMatcher` — public interface:**
```cpp
PathParamsMatcher(const std::string &pattern);
bool match(Request &request) const override;
```

**class `RegexMatcher` — public interface:**
```cpp
RegexMatcher(const std::string &pattern) : regex_(pattern) {}
bool match(Request &request) const override;
```

**class `Server` — public interface:**
```cpp
using Handler = std::function<void(const Request &, Response &)>;
using ExceptionHandler = std::function<void(const Request &, Response &, std::exception_ptr ep)>;
enum class HandlerResponse { Handled, Unhandled, }
using HandlerWithResponse = std::function<HandlerResponse(const Request &, Response &)>;
using HandlerWithContentReader = std::function<void(const Request &, Response &, const ContentReader &content_reader)>;
using Expect100ContinueHandler = std::function<int(const Request &, Response &)>;
Server();
virtual ~Server();
virtual bool is_valid() const;
Server &Get(const std::string &pattern, Handler handler);
Server &Post(const std::string &pattern, Handler handler);
Server &Post(const std::string &pattern, HandlerWithContentReader handler);
Server &Put(const std::string &pattern, Handler handler);
Server &Put(const std::string &pattern, HandlerWithContentReader handler);
Server &Patch(const std::string &pattern, Handler handler);
Server &Patch(const std::string &pattern, HandlerWithContentReader handler);
Server &Delete(const std::string &pattern, Handler handler);
Server &Delete(const std::string &pattern, HandlerWithContentReader handler);
Server &Options(const std::string &pattern, Handler handler);
bool set_base_dir(const std::string &dir, const std::string &mount_point = std::string());
bool set_mount_point(const std::string &mount_point, const std::string &dir, Headers headers = Headers());
bool remove_mount_point(const std::string &mount_point);
Server &set_file_extension_and_mimetype_mapping(const std::string &ext, const std::string &mime);
Server &set_default_file_mimetype(const std::string &mime);
Server &set_file_request_handler(Handler handler);
template<class ErrorHandlerFunc> Server &set_error_handler(ErrorHandlerFunc &&handler) { return set_error_handler_core(std::forward<ErrorHandlerFunc>(handler), std::is_convertible<ErrorHandlerFunc, HandlerWithResponse>{}); }
Server &set_exception_handler(ExceptionHandler handler);
Server &set_pre_routing_handler(HandlerWithResponse handler);
Server &set_post_routing_handler(Handler handler);
Server &set_expect_100_continue_handler(Expect100ContinueHandler handler);
Server &set_logger(Logger logger);
Server &set_address_family(int family);
Server &set_tcp_nodelay(bool on);
Server &set_ipv6_v6only(bool on);
Server &set_socket_options(SocketOptions socket_options);
Server &set_default_headers(Headers headers);
Server &set_header_writer(std::function<ssize_t(Stream &, Headers &)> const &writer);
Server &set_keep_alive_max_count(size_t count);
Server &set_keep_alive_timeout(time_t sec);
Server &set_read_timeout(time_t sec, time_t usec = 0);
template<class Rep, class Period> Server &set_read_timeout(const std::chrono::duration<Rep, Period> &duration);
Server &set_write_timeout(time_t sec, time_t usec = 0);
template<class Rep, class Period> Server &set_write_timeout(const std::chrono::duration<Rep, Period> &duration);
Server &set_idle_interval(time_t sec, time_t usec = 0);
template<class Rep, class Period> Server &set_idle_interval(const std::chrono::duration<Rep, Period> &duration);
Server &set_payload_max_length(size_t length);
bool bind_to_port(const std::string &host, int port, int socket_flags = 0);
int bind_to_any_port(const std::string &host, int socket_flags = 0);
bool listen_after_bind();
bool listen(const std::string &host, int port, int socket_flags = 0);
bool is_running() const;
void wait_until_ready() const;
void stop();
void decommission();
std::function<TaskQueue *(void)> new_task_queue;
```

**class `Result` — public interface:**
```cpp
Result() = default;
Result(std::unique_ptr<Response> &&res, Error err, Headers &&request_headers = Headers{}
) : res_(std::move(res)), err_(err), request_headers_(std::move(request_headers)) {}
operator bool() const { return res_ != nullptr; }
bool operator==(std::nullptr_t) const { return res_ == nullptr; }
bool operator!=(std::nullptr_t) const { return res_ != nullptr; }
const Response &value() const { return *res_; }
Response &value() { return *res_; }
const Response &operator*() const { return *res_; }
Response &operator*() { return *res_; }
const Response *operator->() const { return res_.get(); }
Response *operator->() { return res_.get(); }
Error error() const { return err_; }
bool has_request_header(const std::string &key) const;
std::string get_request_header_value(const std::string &key, const char *def = "", size_t id = 0) const;
uint64_t get_request_header_value_u64(const std::string &key, uint64_t def = 0, size_t id = 0) const;
size_t get_request_header_value_count(const std::string &key) const;
```

**class `ClientImpl` — public interface:**
```cpp
explicit ClientImpl(const std::string &host);
explicit ClientImpl(const std::string &host, int port);
explicit ClientImpl(const std::string &host, int port, const std::string &client_cert_path, const std::string &client_key_path);
virtual ~ClientImpl();
virtual bool is_valid() const;
Result Get(const std::string &path);
Result Get(const std::string &path, const Headers &headers);
Result Get(const std::string &path, Progress progress);
Result Get(const std::string &path, const Headers &headers, Progress progress);
Result Get(const std::string &path, ContentReceiver content_receiver);
Result Get(const std::string &path, const Headers &headers, ContentReceiver content_receiver);
Result Get(const std::string &path, ContentReceiver content_receiver, Progress progress);
Result Get(const std::string &path, const Headers &headers, ContentReceiver content_receiver, Progress progress);
Result Get(const std::string &path, ResponseHandler response_handler, ContentReceiver content_receiver);
Result Get(const std::string &path, const Headers &headers, ResponseHandler response_handler, ContentReceiver content_receiver);
Result Get(const std::string &path, ResponseHandler response_handler, ContentReceiver content_receiver, Progress progress);
Result Get(const std::string &path, const Headers &headers, ResponseHandler response_handler, ContentReceiver content_receiver, Progress progress);
Result Get(const std::string &path, const Params &params, const Headers &headers, Progress progress = nullptr);
Result Get(const std::string &path, const Params &params, const Headers &headers, ContentReceiver content_receiver, Progress progress = nullptr);
Result Get(const std::string &path, const Params &params, const Headers &headers, ResponseHandler response_handler, ContentReceiver content_receiver, Progress progress = nullptr);
Result Head(const std::string &path);
Result Head(const std::string &path, const Headers &headers);
Result Post(const std::string &path);
Result Post(const std::string &path, const Headers &headers);
Result Post(const std::string &path, const char *body, size_t content_length, const std::string &content_type);
Result Post(const std::string &path, const Headers &headers, const char *body, size_t content_length, const std::string &content_type);
Result Post(const std::string &path, const Headers &headers, const char *body, size_t content_length, const std::string &content_type, Progress progress);
Result Post(const std::string &path, const std::string &body, const std::string &content_type);
Result Post(const std::string &path, const std::string &body, const std::string &content_type, Progress progress);
Result Post(const std::string &path, const Headers &headers, const std::string &body, const std::string &content_type);
Result Post(const std::string &path, const Headers &headers, const std::string &body, const std::string &content_type, Progress progress);
Result Post(const std::string &path, size_t content_length, ContentProvider content_provider, const std::string &content_type);
Result Post(const std::string &path, ContentProviderWithoutLength content_provider, const std::string &content_type);
Result Post(const std::string &path, const Headers &headers, size_t content_length, ContentProvider content_provider, const std::string &content_type);
Result Post(const std::string &path, const Headers &headers, ContentProviderWithoutLength content_provider, const std::string &content_type);
Result Post(const std::string &path, const Params &params);
Result Post(const std::string &path, const Headers &headers, const Params &params);
Result Post(const std::string &path, const Headers &headers, const Params &params, Progress progress);
Result Post(const std::string &path, const MultipartFormDataItems &items);
Result Post(const std::string &path, const Headers &headers, const MultipartFormDataItems &items);
Result Post(const std::string &path, const Headers &headers, const MultipartFormDataItems &items, const std::string &boundary);
Result Post(const std::string &path, const Headers &headers, const MultipartFormDataItems &items, const MultipartFormDataProviderItems &provider_items);
Result Put(const std::string &path);
Result Put(const std::string &path, const char *body, size_t content_length, const std::string &content_type);
Result Put(const std::string &path, const Headers &headers, const char *body, size_t content_length, const std::string &content_type);
Result Put(const std::string &path, const Headers &headers, const char *body, size_t content_length, const std::string &content_type, Progress progress);
Result Put(const std::string &path, const std::string &body, const std::string &content_type);
Result Put(const std::string &path, const std::string &body, const std::string &content_type, Progress progress);
Result Put(const std::string &path, const Headers &headers, const std::string &body, const std::string &content_type);
Result Put(const std::string &path, const Headers &headers, const std::string &body, const std::string &content_type, Progress progress);
Result Put(const std::string &path, size_t content_length, ContentProvider content_provider, const std::string &content_type);
Result Put(const std::string &path, ContentProviderWithoutLength content_provider, const std::string &content_type);
Result Put(const std::string &path, const Headers &headers, size_t content_length, ContentProvider content_provider, const std::string &content_type);
Result Put(const std::string &path, const Headers &headers, ContentProviderWithoutLength content_provider, const std::string &content_type);
Result Put(const std::string &path, const Params &params);
Result Put(const std::string &path, const Headers &headers, const Params &params);
Result Put(const std::string &path, const Headers &headers, const Params &params, Progress progress);
Result Put(const std::string &path, const MultipartFormDataItems &items);
Result Put(const std::string &path, const Headers &headers, const MultipartFormDataItems &items);
Result Put(const std::string &path, const Headers &headers, const MultipartFormDataItems &items, const std::string &boundary);
Result Put(const std::string &path, const Headers &headers, const MultipartFormDataItems &items, const MultipartFormDataProviderItems &provider_items);
Result Patch(const std::string &path);
Result Patch(const std::string &path, const char *body, size_t content_length, const std::string &content_type);
Result Patch(const std::string &path, const char *body, size_t content_length, const std::string &content_type, Progress progress);
Result Patch(const std::string &path, const Headers &headers, const char *body, size_t content_length, const std::string &content_type);
Result Patch(const std::string &path, const Headers &headers, const char *body, size_t content_length, const std::string &content_type, Progress progress);
Result Patch(const std::string &path, const std::string &body, const std::string &content_type);
Result Patch(const std::string &path, const std::string &body, const std::string &content_type, Progress progress);
Result Patch(const std::string &path, const Headers &headers, const std::string &body, const std::string &content_type);
Result Patch(const std::string &path, const Headers &headers, const std::string &body, const std::string &content_type, Progress progress);
Result Patch(const std::string &path, size_t content_length, ContentProvider content_provider, const std::string &content_type);
Result Patch(const std::string &path, ContentProviderWithoutLength content_provider, const std::string &content_type);
Result Patch(const std::string &path, const Headers &headers, size_t content_length, ContentProvider content_provider, const std::string &content_type);
Result Patch(const std::string &path, const Headers &headers, ContentProviderWithoutLength content_provider, const std::string &content_type);
Result Delete(const std::string &path);
Result Delete(const std::string &path, const Headers &headers);
Result Delete(const std::string &path, const char *body, size_t content_length, const std::string &content_type);
Result Delete(const std::string &path, const char *body, size_t content_length, const std::string &content_type, Progress progress);
Result Delete(const std::string &path, const Headers &headers, const char *body, size_t content_length, const std::string &content_type);
Result Delete(const std::string &path, const Headers &headers, const char *body, size_t content_length, const std::string &content_type, Progress progress);
Result Delete(const std::string &path, const std::string &body, const std::string &content_type);
Result Delete(const std::string &path, const std::string &body, const std::string &content_type, Progress progress);
Result Delete(const std::string &path, const Headers &headers, const std::string &body, const std::string &content_type);
Result Delete(const std::string &path, const Headers &headers, const std::string &body, const std::string &content_type, Progress progress);
Result Options(const std::string &path);
Result Options(const std::string &path, const Headers &headers);
bool send(Request &req, Response &res, Error &error);
Result send(const Request &req);
void stop();
std::string host() const;
int port() const;
size_t is_socket_open() const;
socket_t socket() const;
void set_hostname_addr_map(std::map<std::string, std::string> addr_map);
void set_default_headers(Headers headers);
void set_header_writer(std::function<ssize_t(Stream &, Headers &)> const &writer);
void set_address_family(int family);
void set_tcp_nodelay(bool on);
void set_ipv6_v6only(bool on);
void set_socket_options(SocketOptions socket_options);
void set_connection_timeout(time_t sec, time_t usec = 0);
template<class Rep, class Period> void set_connection_timeout(const std::chrono::duration<Rep, Period> &duration);
void set_read_timeout(time_t sec, time_t usec = 0);
template<class Rep, class Period> void set_read_timeout(const std::chrono::duration<Rep, Period> &duration);
void set_write_timeout(time_t sec, time_t usec = 0);
template<class Rep, class Period> void set_write_timeout(const std::chrono::duration<Rep, Period> &duration);
void set_basic_auth(const std::string &username, const std::string &password);
void set_bearer_token_auth(const std::string &token);
#ifdef CPPHTTPLIB_OPENSSL_SUPPORT void set_digest_auth(const std::string &username, const std::string &password);
#endif void set_keep_alive(bool on);
void set_follow_location(bool on);
void set_url_encode(bool on);
void set_compress(bool on);
void set_decompress(bool on);
void set_interface(const std::string &intf);
void set_proxy(const std::string &host, int port);
void set_proxy_basic_auth(const std::string &username, const std::string &password);
void set_proxy_bearer_token_auth(const std::string &token);
#ifdef CPPHTTPLIB_OPENSSL_SUPPORT void set_proxy_digest_auth(const std::string &username, const std::string &password);
#endif #ifdef CPPHTTPLIB_OPENSSL_SUPPORT void set_ca_cert_path(const std::string &ca_cert_file_path, const std::string &ca_cert_dir_path = std::string());
void set_ca_cert_store(X509_STORE *ca_cert_store);
X509_STORE *create_ca_cert_store(const char *ca_cert, std::size_t size) const;
#endif #ifdef CPPHTTPLIB_OPENSSL_SUPPORT void enable_server_certificate_verification(bool enabled);
void enable_server_hostname_verification(bool enabled);
void set_server_certificate_verifier(std::function<bool(SSL *ssl)> verifier);
#endif void set_logger(Logger logger);
```

**class `Client` — public interface:**
```cpp
explicit Client(const std::string &scheme_host_port);
explicit Client(const std::string &scheme_host_port, const std::string &client_cert_path, const std::string &client_key_path);
explicit Client(const std::string &host, int port);
explicit Client(const std::string &host, int port, const std::string &client_cert_path, const std::string &client_key_path);
Client(Client &&) = default;
Client &operator=(Client &&) = default;
~Client();
bool is_valid() const;
Result Get(const std::string &path);
Result Get(const std::string &path, const Headers &headers);
Result Get(const std::string &path, Progress progress);
Result Get(const std::string &path, const Headers &headers, Progress progress);
Result Get(const std::string &path, ContentReceiver content_receiver);
Result Get(const std::string &path, const Headers &headers, ContentReceiver content_receiver);
Result Get(const std::string &path, ContentReceiver content_receiver, Progress progress);
Result Get(const std::string &path, const Headers &headers, ContentReceiver content_receiver, Progress progress);
Result Get(const std::string &path, ResponseHandler response_handler, ContentReceiver content_receiver);
Result Get(const std::string &path, const Headers &headers, ResponseHandler response_handler, ContentReceiver content_receiver);
Result Get(const std::string &path, const Headers &headers, ResponseHandler response_handler, ContentReceiver content_receiver, Progress progress);
Result Get(const std::string &path, ResponseHandler response_handler, ContentReceiver content_receiver, Progress progress);
Result Get(const std::string &path, const Params &params, const Headers &headers, Progress progress = nullptr);
Result Get(const std::string &path, const Params &params, const Headers &headers, ContentReceiver content_receiver, Progress progress = nullptr);
Result Get(const std::string &path, const Params &params, const Headers &headers, ResponseHandler response_handler, ContentReceiver content_receiver, Progress progress = nullptr);
Result Head(const std::string &path);
Result Head(const std::string &path, const Headers &headers);
Result Post(const std::string &path);
Result Post(const std::string &path, const Headers &headers);
Result Post(const std::string &path, const char *body, size_t content_length, const std::string &content_type);
Result Post(const std::string &path, const Headers &headers, const char *body, size_t content_length, const std::string &content_type);
Result Post(const std::string &path, const Headers &headers, const char *body, size_t content_length, const std::string &content_type, Progress progress);
Result Post(const std::string &path, const std::string &body, const std::string &content_type);
Result Post(const std::string &path, const std::string &body, const std::string &content_type, Progress progress);
Result Post(const std::string &path, const Headers &headers, const std::string &body, const std::string &content_type);
Result Post(const std::string &path, const Headers &headers, const std::string &body, const std::string &content_type, Progress progress);
Result Post(const std::string &path, size_t content_length, ContentProvider content_provider, const std::string &content_type);
Result Post(const std::string &path, ContentProviderWithoutLength content_provider, const std::string &content_type);
Result Post(const std::string &path, const Headers &headers, size_t content_length, ContentProvider content_provider, const std::string &content_type);
Result Post(const std::string &path, const Headers &headers, ContentProviderWithoutLength content_provider, const std::string &content_type);
Result Post(const std::string &path, const Params &params);
Result Post(const std::string &path, const Headers &headers, const Params &params);
Result Post(const std::string &path, const Headers &headers, const Params &params, Progress progress);
Result Post(const std::string &path, const MultipartFormDataItems &items);
Result Post(const std::string &path, const Headers &headers, const MultipartFormDataItems &items);
Result Post(const std::string &path, const Headers &headers, const MultipartFormDataItems &items, const std::string &boundary);
Result Post(const std::string &path, const Headers &headers, const MultipartFormDataItems &items, const MultipartFormDataProviderItems &provider_items);
Result Put(const std::string &path);
Result Put(const std::string &path, const char *body, size_t content_length, const std::string &content_type);
Result Put(const std::string &path, const Headers &headers, const char *body, size_t content_length, const std::string &content_type);
Result Put(const std::string &path, const Headers &headers, const char *body, size_t content_length, const std::string &content_type, Progress progress);
Result Put(const std::string &path, const std::string &body, const std::string &content_type);
Result Put(const std::string &path, const std::string &body, const std::string &content_type, Progress progress);
Result Put(const std::string &path, const Headers &headers, const std::string &body, const std::string &content_type);
Result Put(const std::string &path, const Headers &headers, const std::string &body, const std::string &content_type, Progress progress);
Result Put(const std::string &path, size_t content_length, ContentProvider content_provider, const std::string &content_type);
Result Put(const std::string &path, ContentProviderWithoutLength content_provider, const std::string &content_type);
Result Put(const std::string &path, const Headers &headers, size_t content_length, ContentProvider content_provider, const std::string &content_type);
Result Put(const std::string &path, const Headers &headers, ContentProviderWithoutLength content_provider, const std::string &content_type);
Result Put(const std::string &path, const Params &params);
Result Put(const std::string &path, const Headers &headers, const Params &params);
Result Put(const std::string &path, const Headers &headers, const Params &params, Progress progress);
Result Put(const std::string &path, const MultipartFormDataItems &items);
Result Put(const std::string &path, const Headers &headers, const MultipartFormDataItems &items);
Result Put(const std::string &path, const Headers &headers, const MultipartFormDataItems &items, const std::string &boundary);
Result Put(const std::string &path, const Headers &headers, const MultipartFormDataItems &items, const MultipartFormDataProviderItems &provider_items);
Result Patch(const std::string &path);
Result Patch(const std::string &path, const char *body, size_t content_length, const std::string &content_type);
Result Patch(const std::string &path, const char *body, size_t content_length, const std::string &content_type, Progress progress);
Result Patch(const std::string &path, const Headers &headers, const char *body, size_t content_length, const std::string &content_type);
Result Patch(const std::string &path, const Headers &headers, const char *body, size_t content_length, const std::string &content_type, Progress progress);
Result Patch(const std::string &path, const std::string &body, const std::string &content_type);
Result Patch(const std::string &path, const std::string &body, const std::string &content_type, Progress progress);
Result Patch(const std::string &path, const Headers &headers, const std::string &body, const std::string &content_type);
Result Patch(const std::string &path, const Headers &headers, const std::string &body, const std::string &content_type, Progress progress);
Result Patch(const std::string &path, size_t content_length, ContentProvider content_provider, const std::string &content_type);
Result Patch(const std::string &path, ContentProviderWithoutLength content_provider, const std::string &content_type);
Result Patch(const std::string &path, const Headers &headers, size_t content_length, ContentProvider content_provider, const std::string &content_type);
Result Patch(const std::string &path, const Headers &headers, ContentProviderWithoutLength content_provider, const std::string &content_type);
Result Delete(const std::string &path);
Result Delete(const std::string &path, const Headers &headers);
Result Delete(const std::string &path, const char *body, size_t content_length, const std::string &content_type);
Result Delete(const std::string &path, const char *body, size_t content_length, const std::string &content_type, Progress progress);
Result Delete(const std::string &path, const Headers &headers, const char *body, size_t content_length, const std::string &content_type);
Result Delete(const std::string &path, const Headers &headers, const char *body, size_t content_length, const std::string &content_type, Progress progress);
Result Delete(const std::string &path, const std::string &body, const std::string &content_type);
Result Delete(const std::string &path, const std::string &body, const std::string &content_type, Progress progress);
Result Delete(const std::string &path, const Headers &headers, const std::string &body, const std::string &content_type);
Result Delete(const std::string &path, const Headers &headers, const std::string &body, const std::string &content_type, Progress progress);
Result Options(const std::string &path);
Result Options(const std::string &path, const Headers &headers);
bool send(Request &req, Response &res, Error &error);
Result send(const Request &req);
void stop();
std::string host() const;
int port() const;
size_t is_socket_open() const;
socket_t socket() const;
void set_hostname_addr_map(std::map<std::string, std::string> addr_map);
void set_default_headers(Headers headers);
void set_header_writer(std::function<ssize_t(Stream &, Headers &)> const &writer);
void set_address_family(int family);
void set_tcp_nodelay(bool on);
void set_socket_options(SocketOptions socket_options);
void set_connection_timeout(time_t sec, time_t usec = 0);
template<class Rep, class Period> void set_connection_timeout(const std::chrono::duration<Rep, Period> &duration);
void set_read_timeout(time_t sec, time_t usec = 0);
template<class Rep, class Period> void set_read_timeout(const std::chrono::duration<Rep, Period> &duration);
void set_write_timeout(time_t sec, time_t usec = 0);
template<class Rep, class Period> void set_write_timeout(const std::chrono::duration<Rep, Period> &duration);
void set_basic_auth(const std::string &username, const std::string &password);
void set_bearer_token_auth(const std::string &token);
#ifdef CPPHTTPLIB_OPENSSL_SUPPORT void set_digest_auth(const std::string &username, const std::string &password);
#endif void set_keep_alive(bool on);
void set_follow_location(bool on);
void set_url_encode(bool on);
void set_compress(bool on);
void set_decompress(bool on);
void set_interface(const std::string &intf);
void set_proxy(const std::string &host, int port);
void set_proxy_basic_auth(const std::string &username, const std::string &password);
void set_proxy_bearer_token_auth(const std::string &token);
#ifdef CPPHTTPLIB_OPENSSL_SUPPORT void set_proxy_digest_auth(const std::string &username, const std::string &password);
#endif #ifdef CPPHTTPLIB_OPENSSL_SUPPORT void enable_server_certificate_verification(bool enabled);
void enable_server_hostname_verification(bool enabled);
void set_server_certificate_verifier(std::function<bool(SSL *ssl)> verifier);
#endif void set_logger(Logger logger);
#ifdef CPPHTTPLIB_OPENSSL_SUPPORT void set_ca_cert_path(const std::string &ca_cert_file_path, const std::string &ca_cert_dir_path = std::string());
void set_ca_cert_store(X509_STORE *ca_cert_store);
void load_ca_cert_store(const char *ca_cert, std::size_t size);
long get_openssl_verify_result() const;
SSL_CTX *ssl_context() const;
#endif private: std::unique_ptr<ClientImpl> cli_;
#ifdef CPPHTTPLIB_OPENSSL_SUPPORT bool is_ssl_ = false;
```

**class `SSLServer` — public interface:**
```cpp
SSLServer(const char *cert_path, const char *private_key_path, const char *client_ca_cert_file_path = nullptr, const char *client_ca_cert_dir_path = nullptr, const char *private_key_password = nullptr);
SSLServer(X509 *cert, EVP_PKEY *private_key, X509_STORE *client_ca_cert_store = nullptr);
SSLServer(const std::function<bool(SSL_CTX &ssl_ctx)> &setup_ssl_ctx_callback);
~SSLServer() override;
bool is_valid() const override;
SSL_CTX *ssl_context() const;
void update_certs(X509 *cert, EVP_PKEY *private_key, X509_STORE *client_ca_cert_store = nullptr);
```

**class `SSLClient` — public interface:**
```cpp
explicit SSLClient(const std::string &host);
explicit SSLClient(const std::string &host, int port);
explicit SSLClient(const std::string &host, int port, const std::string &client_cert_path, const std::string &client_key_path, const std::string &private_key_password = std::string());
explicit SSLClient(const std::string &host, int port, X509 *client_cert, EVP_PKEY *client_key, const std::string &private_key_password = std::string());
~SSLClient() override;
bool is_valid() const override;
void set_ca_cert_store(X509_STORE *ca_cert_store);
void load_ca_cert_store(const char *ca_cert, std::size_t size);
long get_openssl_verify_result() const;
SSL_CTX *ssl_context() const;
```

**class `BufferStream` — public interface:**
```cpp
BufferStream() = default;
~BufferStream() override = default;
bool is_readable() const override;
bool is_writable() const override;
ssize_t read(char *ptr, size_t size) override;
ssize_t write(const char *ptr, size_t size) override;
void get_remote_ip_and_port(std::string &ip, int &port) const override;
void get_local_ip_and_port(std::string &ip, int &port) const override;
socket_t socket() const override;
const std::string &get_buffer() const;
```

**class `compressor` — public interface:**
```cpp
virtual ~compressor() = default;
typedef std::function<bool(const char *data, size_t data_len)> Callback;
virtual bool compress(const char *data, size_t data_length, bool last, Callback callback) = 0;
```

**class `decompressor` — public interface:**
```cpp
virtual ~decompressor() = default;
virtual bool is_valid() const = 0;
typedef std::function<bool(const char *data, size_t data_len)> Callback;
virtual bool decompress(const char *data, size_t data_length, Callback callback) = 0;
```

**class `nocompressor` — public interface:**
```cpp
~nocompressor() override = default;
bool compress(const char *data, size_t data_length, bool , Callback callback) override;
```

**class `gzip_compressor` — public interface:**
```cpp
gzip_compressor();
~gzip_compressor() override;
bool compress(const char *data, size_t data_length, bool last, Callback callback) override;
```

**class `gzip_decompressor` — public interface:**
```cpp
gzip_decompressor();
~gzip_decompressor() override;
bool is_valid() const override;
bool decompress(const char *data, size_t data_length, Callback callback) override;
```

**class `brotli_compressor` — public interface:**
```cpp
brotli_compressor();
~brotli_compressor();
bool compress(const char *data, size_t data_length, bool last, Callback callback) override;
```

**class `brotli_decompressor` — public interface:**
```cpp
brotli_decompressor();
~brotli_decompressor();
bool is_valid() const override;
bool decompress(const char *data, size_t data_length, Callback callback) override;
```

**class `stream_line_reader` — public interface:**
```cpp
stream_line_reader(Stream &strm, char *fixed_buffer, size_t fixed_buffer_size);
const char *ptr() const;
size_t size() const;
bool end_with_crlf() const;
bool getline();
```

**class `mmap` — public interface:**
```cpp
mmap(const char *path);
~mmap();
bool open(const char *path);
void close();
bool is_open() const;
size_t size() const;
const char *data() const;
```

**class `SocketStream` — public interface:**
```cpp
SocketStream(socket_t sock, time_t read_timeout_sec, time_t read_timeout_usec, time_t write_timeout_sec, time_t write_timeout_usec);
~SocketStream() override;
bool is_readable() const override;
bool is_writable() const override;
ssize_t read(char *ptr, size_t size) override;
ssize_t write(const char *ptr, size_t size) override;
void get_remote_ip_and_port(std::string &ip, int &port) const override;
void get_local_ip_and_port(std::string &ip, int &port) const override;
socket_t socket() const override;
```

**class `SSLSocketStream` — public interface:**
```cpp
SSLSocketStream(socket_t sock, SSL *ssl, time_t read_timeout_sec, time_t read_timeout_usec, time_t write_timeout_sec, time_t write_timeout_usec);
~SSLSocketStream() override;
bool is_readable() const override;
bool is_writable() const override;
ssize_t read(char *ptr, size_t size) override;
ssize_t write(const char *ptr, size_t size) override;
void get_remote_ip_and_port(std::string &ip, int &port) const override;
void get_local_ip_and_port(std::string &ip, int &port) const override;
socket_t socket() const override;
```

**class `MultipartFormDataParser` — public interface:**
```cpp
MultipartFormDataParser() = default;
void set_boundary(std::string &&boundary) { boundary_ = boundary; dash_boundary_crlf_ = dash_ + boundary_ + crlf_; crlf_dash_boundary_ = crlf_ + dash_ + boundary_; }
bool is_valid() const { return is_valid_; }
bool parse(const char *buf, size_t n, const ContentReceiver &content_callback, const MultipartContentHeader &header_callback) { buf_append(buf, n); while (buf_size() > 0) { switch (state_) { case 0: { buf_erase(buf_find(dash_boundary_crlf_)); if (dash_boundary_crlf_.size() > buf_size()) { return true; } if (!buf_start_with(dash_boundary_crlf_)) { return false; } buf_erase(dash_boundary_crlf_.size()); state_ = 1; break; } case 1: { clear_file_info(); state_ = 2; break; } case 2: { auto pos = buf_find(crlf_); if (pos > CPPHTTPLIB_HEADER_MAX_LENGTH) { return false; } while (pos < buf_size()) { if (pos == 0) { if (!header_callback(file_)) { is_valid_ = false; return false; } buf_erase(crlf_.size()); state_ = 3; break; } const auto header = buf_head(pos); if (!parse_header(header.data(), header.data() + header.size(), [&](const std::string &, const std::string &) {})) { is_valid_ = false; return false; } static const std::string header_content_type = "Content-Type:"; if (start_with_case_ignore(header, header_content_type)) { file_.content_type = trim_copy(header.substr(header_content_type.size())); } else { static const std::regex re_content_disposition(R"~(^Content-Disposition:\s*form-data;\s*(.*)$)~", std::regex_constants::icase); std::smatch m; if (std::regex_match(header, m, re_content_disposition)) { Params params; parse_disposition_params(m[1], params); auto it = params.find("name"); if (it != params.end()) { file_.name = it->second; } else { is_valid_ = false; return false; } it = params.find("filename"); if (it != params.end()) { file_.filename = it->second; } it = params.find("filename*"); if (it != params.end()) { static const std::regex re_rfc5987_encoding(R"~(^UTF-8''(.+?)$)~", std::regex_constants::icase); std::smatch m2; if (std::regex_match(it->second, m2, re_rfc5987_encoding)) { file_.filename = decode_url(m2[1], false); } else { is_valid_ = false; return false; } } } } buf_erase(pos + crlf_.size()); pos = buf_find(crlf_); } if (state_ != 3) { return true; } break; } case 3: { if (crlf_dash_boundary_.size() > buf_size()) { return true; } auto pos = buf_find(crlf_dash_boundary_); if (pos < buf_size()) { if (!content_callback(buf_data(), pos)) { is_valid_ = false; return false; } buf_erase(pos + crlf_dash_boundary_.size()); state_ = 4; } else { auto len = buf_size() - crlf_dash_boundary_.size(); if (len > 0) { if (!content_callback(buf_data(), len)) { is_valid_ = false; return false; } buf_erase(len); } return true; } break; } case 4: { if (crlf_.size() > buf_size()) { return true; } if (buf_start_with(crlf_)) { buf_erase(crlf_.size()); state_ = 1; } else { if (dash_.size() > buf_size()) { return true; } if (buf_start_with(dash_)) { buf_erase(dash_.size()); is_valid_ = true; buf_erase(buf_size()); } else { return true; } } break; } } } return true; }
```

**class `WSInit` — public interface:**
```cpp
WSInit() { WSADATA wsaData; if (WSAStartup(0x0002, &wsaData) == 0) is_valid_ = true; }
~WSInit() { if (is_valid_) WSACleanup(); }
bool is_valid_ = false;
```

**class `ContentProviderAdapter` — public interface:**
```cpp
explicit ContentProviderAdapter(ContentProviderWithoutLength &&content_provider) : content_provider_(content_provider) {}
bool operator()(size_t offset, size_t, DataSink &sink) { return content_provider_(offset, sink); }
```

**class `SSLInit` — public interface:**
```cpp
SSLInit() { OPENSSL_init_ssl(OPENSSL_INIT_LOAD_SSL_STRINGS | OPENSSL_INIT_LOAD_CRYPTO_STRINGS, NULL); }
```

## `ota/automation.h`

**class `OtaHttpRequestComponentFlashAction` — public interface:**
```cpp
OtaHttpRequestComponentFlashAction(OtaHttpRequestComponent *parent) : parent_(parent) {}
TEMPLATABLE_VALUE(std::string, md5_url) TEMPLATABLE_VALUE(std::string, md5) TEMPLATABLE_VALUE(std::string, password) TEMPLATABLE_VALUE(std::string, url) TEMPLATABLE_VALUE(std::string, username) void play(const Ts &...x) override { if (this->md5_url_.has_value()) { this->parent_->set_md5_url(this->md5_url_.value(x...)); } if (this->md5_.has_value()) { this->parent_->set_md5(this->md5_.value(x...)); } if (this->password_.has_value()) { this->parent_->set_password(this->password_.value(x...)); } if (this->username_.has_value()) { this->parent_->set_username(this->username_.value(x...)); } this->parent_->set_url(this->url_.value(x...)); this->parent_->flash(); }
```

## `ota/ota_http_request.h`

**Enums:**
```cpp
enum OtaHttpRequestError : uint8_t {
  OTA_MD5_INVALID = 0x10,
  OTA_BAD_URL = 0x11,
  OTA_CONNECTION_ERROR = 0x12,
};
```

**class `OtaHttpRequestComponent` — public interface:**
```cpp
void dump_config() override;
float get_setup_priority() const override { return setup_priority::AFTER_WIFI; }
void set_md5_url(const std::string &md5_url);
void set_md5(const std::string &md5) { this->md5_expected_ = md5; }
void set_password(const std::string &password);
void set_url(const std::string &url);
void set_username(const std::string &username);
std::string md5_computed() { return this->md5_computed_; }
std::string md5_expected() { return this->md5_expected_; }
void flash();
```

## `update/http_request_update.h`

**class `HttpRequestUpdate` — public interface:**
```cpp
void setup() override;
void update() override;
void perform(bool force) override;
void check() override { this->update(); }
void set_source_url(const std::string &source_url) { this->source_url_ = source_url; }
void set_request_parent(HttpRequestComponent *request_parent) { this->request_parent_ = request_parent; }
void set_ota_parent(OtaHttpRequestComponent *ota_parent) { this->ota_parent_ = ota_parent; }
float get_setup_priority() const override { return setup_priority::AFTER_WIFI; }
void on_ota_state(ota::OTAState state, float progress, uint8_t error) override;
```
