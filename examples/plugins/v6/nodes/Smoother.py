import time

from examples.plugins.v6 import OutSpeed, InSpeed, InWindowSize, InDeltaMax, Plugin
from scratch2.scheduler import on_scheduler_fast_loop, on_restarted, restart_on_exception, on_exception, on_first_loop


@restart_on_exception
class Smoother(Plugin, InSpeed, InDeltaMax, InWindowSize, OutSpeed):
    speed_change_limit: int
    speed_history: list

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        speed = self.in_speed if self.in_speed is not None else 0
        self.speed_history = [speed] * self.in_window_size
        self.onchange_in_window_size(self.window_size_change)

    def  window_size_change(self, x):
        if len(self.speed_history)>self.in_window_size:
            self.speed_history.pop(0)

    def main_loop(self):
        self.speed_history.append(self.in_speed)
        if len(self.speed_history)>self.in_window_size:
            self.speed_history.pop(0)
        speed_avg = sum(self.speed_history) / len(self.speed_history)
        self.out_speed = speed_avg if abs(self.in_speed - speed_avg) < self.in_delta_max else self.in_speed
        if self.out_speed>2: self.log.info(f"FAST:{self.out_speed}")
        self.log.info(f"Last line")







