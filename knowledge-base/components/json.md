# ESPHome component: `json`

Source: `esphome/components/json/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `json_util.h`

**class `SerializationBuffer` — public interface:**
```cpp
static constexpr size_t BUFFER_SIZE = STACK_SIZE;
explicit SerializationBuffer(size_t size) : size_(size) { if (size + 1 <= STACK_SIZE) { buffer_ = stack_buffer_; } else { heap_buffer_ = new char[size + 1]; buffer_ = heap_buffer_; } buffer_[0] = '\0'; }
~SerializationBuffer() { delete[] heap_buffer_; }
SerializationBuffer(SerializationBuffer &&other) noexcept : heap_buffer_(other.heap_buffer_), size_(other.size_) { if (other.buffer_ == other.stack_buffer_) { std::memcpy(stack_buffer_, other.stack_buffer_, size_ + 1); buffer_ = stack_buffer_; } else { buffer_ = heap_buffer_; other.heap_buffer_ = nullptr; } other.stack_buffer_[0] = '\0'; other.buffer_ = other.stack_buffer_; other.size_ = 0; }
SerializationBuffer &operator=(SerializationBuffer &&other) noexcept { if (this != &other) { delete[] heap_buffer_; heap_buffer_ = other.heap_buffer_; size_ = other.size_; if (other.buffer_ == other.stack_buffer_) { std::memcpy(stack_buffer_, other.stack_buffer_, size_ + 1); buffer_ = stack_buffer_; } else { buffer_ = heap_buffer_; other.heap_buffer_ = nullptr; } other.stack_buffer_[0] = '\0'; other.buffer_ = other.stack_buffer_; other.size_ = 0; } return *this; }
SerializationBuffer(const SerializationBuffer &) = delete;
SerializationBuffer &operator=(const SerializationBuffer &) = delete;
const char *c_str() const { return buffer_; }
const char *data() const { return buffer_; }
size_t size() const { return size_; }
operator std::string() const { return std::string(buffer_, size_); }
```

**class `JsonBuilder` — public interface:**
```cpp
JsonObject root() { if (!root_created_) { root_ = doc_.to<JsonObject>(); root_created_ = true; } return root_; }
SerializationBuffer<> serialize();
```
