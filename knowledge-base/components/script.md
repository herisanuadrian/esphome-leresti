# ESPHome component: `script`

Source: `esphome/components/script/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `script.h`

**class `Script` — public interface:**
```cpp
virtual void execute(Ts...) = 0;
virtual bool is_running() { return this->is_action_running(); }
virtual void stop() { this->stop_action(); }
void execute_tuple(const std::tuple<Ts...> &tuple) { this->execute_tuple_(tuple, std::make_index_sequence<sizeof...(Ts)>{}); }
void set_name(const LogString *name) { name_ = name; }
```

**class `SingleScript` — public interface:**
```cpp
void execute(Ts... x) override { if (this->is_action_running()) { this->esp_logw_(__LINE__, ESPHOME_LOG_FORMAT("Script '%s' is already running! (mode: single)"), LOG_STR_ARG(this->name_)); return; } this->run_actions_(x...); }
```

**class `RestartScript` — public interface:**
```cpp
void execute(Ts... x) override { if (this->is_action_running()) { this->esp_logd_(__LINE__, ESPHOME_LOG_FORMAT("Script '%s' restarting (mode: restart)"), LOG_STR_ARG(this->name_)); this->stop_action(); } this->run_actions_(x...); }
```

**class `QueueingScript` — public interface:**
```cpp
void execute(Ts... x) override { if (this->is_action_running() || this->num_queued_ > 0) { if (this->num_queued_ + 1 >= this->max_runs_) { this->esp_logw_(__LINE__, ESPHOME_LOG_FORMAT("Script '%s' max instances (running + queued) reached!"), LOG_STR_ARG(this->name_)); return; } this->lazy_init_queue_(); this->esp_logd_(__LINE__, ESPHOME_LOG_FORMAT("Script '%s' queueing new instance (mode: queued)"), LOG_STR_ARG(this->name_)); const size_t queue_capacity = static_cast<size_t>(this->max_runs_ - 1); size_t write_pos = (this->queue_front_ + this->num_queued_) % queue_capacity; this->var_queue_[write_pos] = std::make_unique<std::tuple<Ts...>>(x...); this->num_queued_++; return; } this->run_actions_(x...); this->loop(); }
void stop() override { this->var_queue_.reset(); this->num_queued_ = 0; this->queue_front_ = 0; Script<Ts...>::stop(); }
void loop() override { if (this->num_queued_ != 0 && !this->is_action_running()) { this->num_queued_--; const size_t queue_capacity = static_cast<size_t>(this->max_runs_ - 1); auto tuple_ptr = std::move(this->var_queue_[this->queue_front_]); this->queue_front_ = (this->queue_front_ + 1) % queue_capacity; this->trigger_tuple_(*tuple_ptr, std::make_index_sequence<sizeof...(Ts)>{}); } }
void set_max_runs(int max_runs) { max_runs_ = max_runs; }
```

**class `ParallelScript` — public interface:**
```cpp
void execute(Ts... x) override { if (this->max_runs_ != 0 && this->automation_parent_->num_running() >= this->max_runs_) { this->esp_logw_(__LINE__, ESPHOME_LOG_FORMAT("Script '%s' maximum number of parallel runs exceeded!"), LOG_STR_ARG(this->name_)); return; } this->run_actions_(x...); }
void set_max_runs(int max_runs) { max_runs_ = max_runs; }
```

**class `ScriptStopAction` — public interface:**
```cpp
ScriptStopAction(C *script) : script_(script) {}
void play(const Ts &...x) override { this->script_->stop(); }
```

**class `IsRunningCondition` — public interface:**
```cpp
explicit IsRunningCondition(C *parent) : parent_(parent) {}
bool check(const Ts &...x) override { return this->parent_->is_running(); }
```

**class `ScriptWaitAction` — public interface:**
```cpp
ScriptWaitAction(C *script) : script_(script) {}
void setup() override { if (this->num_running_ == 0) { this->disable_loop(); } }
void play_complex(const Ts &...x) override { this->num_running_++; if (!this->script_->is_running()) { this->play_next_(x...); return; } this->param_queue_.emplace_back(x...); this->enable_loop(); }
void loop() override { if (this->num_running_ == 0) return; if (this->script_->is_running()) return; if (!this->param_queue_.empty()) { auto &params = this->param_queue_.front(); this->play_next_tuple_(params, std::make_index_sequence<sizeof...(Ts)>{}); this->param_queue_.pop_front(); } else { this->disable_loop(); } }
void play(const Ts &...x) override { }
void stop() override { this->param_queue_.clear(); this->disable_loop(); }
```
