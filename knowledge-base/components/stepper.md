# ESPHome component: `stepper`

Source: `esphome/components/stepper/ at ref 2026.7.2`

> Auto-extracted public C++ interface. Not exhaustive — for anything
> not covered here, check the `.py` config schema in the same folder
> or the source file directly before guessing a lambda call.

## `stepper.h`

**class `Stepper` — public interface:**
```cpp
void set_target(int32_t steps) { this->target_position = steps; }
void report_position(int32_t steps) { this->current_position = steps; }
void set_acceleration(float acceleration) { this->acceleration_ = acceleration; }
void set_deceleration(float deceleration) { this->deceleration_ = deceleration; }
void set_max_speed(float max_speed) { this->max_speed_ = max_speed; }
virtual void on_update_speed() {}
bool has_reached_target() { return this->current_position == this->target_position; }
int32_t current_position{0}
int32_t target_position{0}
```

**class `SetTargetAction` — public interface:**
```cpp
explicit SetTargetAction(Stepper *parent) : parent_(parent) {}
TEMPLATABLE_VALUE(int32_t, target) void play(const Ts &...x) override { this->parent_->set_target(this->target_.value(x...)); }
```

**class `ReportPositionAction` — public interface:**
```cpp
explicit ReportPositionAction(Stepper *parent) : parent_(parent) {}
TEMPLATABLE_VALUE(int32_t, position) void play(const Ts &...x) override { this->parent_->report_position(this->position_.value(x...)); }
```

**class `SetSpeedAction` — public interface:**
```cpp
explicit SetSpeedAction(Stepper *parent) : parent_(parent) {}
TEMPLATABLE_VALUE(float, speed);
void play(const Ts &...x) override { float speed = this->speed_.value(x...); this->parent_->set_max_speed(speed); this->parent_->on_update_speed(); }
```

**class `SetAccelerationAction` — public interface:**
```cpp
explicit SetAccelerationAction(Stepper *parent) : parent_(parent) {}
TEMPLATABLE_VALUE(float, acceleration);
void play(const Ts &...x) override { float acceleration = this->acceleration_.value(x...); this->parent_->set_acceleration(acceleration); }
```

**class `SetDecelerationAction` — public interface:**
```cpp
explicit SetDecelerationAction(Stepper *parent) : parent_(parent) {}
TEMPLATABLE_VALUE(float, deceleration);
void play(const Ts &...x) override { float deceleration = this->deceleration_.value(x...); this->parent_->set_deceleration(deceleration); }
```
