import numbers
from typing import Callable

from plugins import Plugin
from examples.plugins.v5 import OutValue
from plugins.scheduler import on_scheduler_fast_loop
from examples.plugins.v5 import InSpeed

class Mover(Plugin, InSpeed):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @on_scheduler_fast_loop
    def main_loop(self):
        print(f'Got:{self.in_speed}')
