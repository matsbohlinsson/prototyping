import dataclasses
from interface import InSpeed, OutSpeed, InCourse, OutLatLon, InLatLon
from plugins.scheduler import on_scheduler_fast_loop, on_restarted, restart_on_exception, on_exception, on_first_loop


@restart_on_exception
class Smoother(InSpeed, OutSpeed):
    window_size: int = 4
    speed_change_limit: int = 10
    speed_history = None

    def __init__(self, window_size: int = 4, speed_change_limit: int = 10):
        super().__init__()
        self.window_size, self.speed_change_limit = window_size, speed_change_limit

    @on_scheduler_fast_loop
    def main_loop(self, loop_index: int):
        speed_avg = self.calc_average_speed(self.speed_history, self.in_speed, self.speed_change_limit)
        self.out_speed = speed_avg

    @classmethod
    def calc_average_speed(cls, speed_history, speed_current, speed_change_limit):
        window = speed_history
        window.append(speed_current)
        window.pop(0)
        speed_avg = sum(window) / len(window)
        speed_avg = speed_avg if abs(speed_current - speed_avg) < speed_change_limit else speed_current
        return speed_avg

    @on_restarted
    @on_first_loop
    def init_history_window(self):
        speed = self.in_speed if self.in_speed is not None else 0
        self.speed_history = [speed] * self.window_size
        self.out_speed = self.in_speed

    @on_exception
    def exception(self, loop_index: int, current_try_index: int, exception):
        pass

    def __del__(self):
        pass


d = Smoother()
print(isinstance(d, InSpeed))


def simulate_first_loop(d):
    d.init_history_window()


def simulate_loop(d, index):
    d.main_loop(index)


test_speed_list=[1,2,7,4,3,200,198,201,200,100, 101, 102, 80, 104, 106, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107]

simulate_first_loop(d)
for i in range(0, 20):
    d.in_speed = test_speed_list[i]
    simulate_loop(d, i)
    print(d.in_speed, d.out_speed)




