import numbers
from typing import Callable

from examples.plugins.v6 import OutValue, Plugin
from scratch2.scheduler import on_scheduler_fast_loop
from examples.plugins.v6 import InSpeed, InHeight, OutSpeed


class Mover(Plugin, InSpeed, InHeight, OutSpeed):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_location = 123
        self.connect(self, Mover.out_speed, Mover.in_speed)

    @on_scheduler_fast_loop
    def main_loop(self):
        self.api.dji.takeoff()
