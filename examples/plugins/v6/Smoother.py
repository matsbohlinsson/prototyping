from examples.plugins.v6 import OutSpeed, InSpeed, InWindowSize
from plugins import Plugin
from plugins.scheduler import on_scheduler_fast_loop, on_restarted, restart_on_exception, on_exception, on_first_loop


@restart_on_exception
class Smoother(Plugin, InSpeed, InWindowSize, OutSpeed):
    window_size: int
    speed_change_limit: int
    speed_history: list

    def __init__(self, speed_change_limit: int = 10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed_change_limit = speed_change_limit
        self.out_speed=0
        self.in_speed=0
        self.init_history_window()

    @on_scheduler_fast_loop
    def main_loop(self, loop_counter:int):
        speed_avg = self.calcsmoothing_speed(self.speed_history, self.in_speed, self.speed_change_limit, self.in_window_size)
        self.out_speed=speed_avg

    @classmethod
    def calcsmoothing_speed(cls, speed_history, speed_current, speed_change_limit, windows_size):
        window = speed_history
        window.append(speed_current)
        if len(window)>windows_size:
            window.pop(0)
        speed_avg = sum(window) / len(window)
        speed_avg = speed_avg if abs(speed_current - speed_avg) < speed_change_limit else speed_current
        return speed_avg

    def init_history_window(self):
        speed = self.in_speed if self.in_speed is not None else 0
        self.speed_history = [speed] * self.in_window_size
        self.out_speed=self.in_speed


    @on_exception
    def exception(self, loop_index: int, current_try_index: int, exception):
        pass

    def __del__(self):
        pass






