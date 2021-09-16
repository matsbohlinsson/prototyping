from typing import Callable

from plugins import Plugin
from plugins.interface import OutSpeed
from plugins.scheduler import on_scheduler_fast_loop


class Generator(Plugin, OutSpeed):

    def __init__(self, function: Callable[[int], None],  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.function = function

    @on_scheduler_fast_loop
    def main_loop(self, loop_index: int):
        self.out_speed.set(self.function(loop_index))