from examples.plugins.v5 import OutSpeed, InSpeed
from plugins import Plugin
from plugins.scheduler import on_scheduler_fast_loop, on_restarted, restart_on_exception, on_exception, on_first_loop


@restart_on_exception
class Smoother(Plugin, InSpeed, OutSpeed):
    window_size: int
    speed_change_limit: int
    speed_history: list

    def __init__(self, window_size: int = 4, speed_change_limit: int = 10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_size, self.speed_change_limit = window_size, speed_change_limit
        self.out_speed=0
        self.in_speed=0
        self.init_history_window()

    @on_scheduler_fast_loop
    def main_loop(self):
        speed_avg = self.calcsmoothing_speed(self.speed_history, self.in_speed, self.speed_change_limit)
        self.out_speed=speed_avg

    @classmethod
    def calcsmoothing_speed(cls, speed_history, speed_current, speed_change_limit):
        window = speed_history
        window.append(speed_current)
        window.pop(0)
        speed_avg = sum(window) / len(window)
        speed_avg = speed_avg if abs(speed_current - speed_avg) < speed_change_limit else speed_current
        return speed_avg

    def init_history_window(self):
        speed = self.in_speed if self.in_speed is not None else 0
        self.speed_history = [speed] * self.window_size
        self.out_speed=self.in_speed


    @on_exception
    def exception(self, loop_index: int, current_try_index: int, exception):
        pass

    def __del__(self):
        pass






