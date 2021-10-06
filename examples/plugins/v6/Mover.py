import numbers
from typing import Callable

from plugins import Plugin
from examples.plugins.v6 import OutValue
from plugins.scheduler import on_scheduler_fast_loop
from examples.plugins.v6 import InSpeed, InHeight

class Mover(Plugin, InSpeed, InHeight):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @on_scheduler_fast_loop
    def main_loop(self):
        print(f'Got in_speed:{self.in_speed}')
        print(f'Got in_height:{self.in_height}')
