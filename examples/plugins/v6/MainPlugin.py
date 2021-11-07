import csv
import math
from pathlib import Path

from examples.plugins.v6.Mover import Mover
from examples.plugins.v6.Smoother import Smoother
from examples.plugins.v6.Generator import Generator
from examples.plugins.v6 import OutSpeed, OutHeight

from plugins import Plugin


class MainPlugin(Plugin, OutSpeed, OutHeight):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create nodes
        self.generator_speed = Generator(plugin_name='SpeedGenerator', expression=lambda loop_index: math.sin(loop_index / 100) * 100, csv_out='./2st_out.csv')
        self.generator_height = Generator(plugin_name='HeightGenerator', expression=lambda loop_index: math.cos(loop_index / 100) * 100, csv_out='./3st_out.csv' )
        self.mover = Mover(plugin_name='Mover', csv_out='./4st_out.csv')

        # Connect nodes
        self.smoother = Smoother(plugin_name='SpeedSmoother', in_window_size=20, speed_change_limit=20, csv_out='./1st_out.csv')
        self.generator_speed.connect(self.smoother, Generator.out_value, Smoother.in_speed)
        self.generator_height.connect(self.mover,   Generator.out_value, Mover.in_height)
        self.smoother.connect(self.mover, Smoother.out_speed, Mover.in_speed)
        # Schedule execution
        self.add_plugin(self.generator_speed)
        self.add_plugin(self.smoother)
        self.add_plugin(self.generator_height)
        self.add_plugin(self.mover)

    def main_loop(self, loop_counter: int):
        d = self.run_all(loop_counter)
        self.out_height = self.mover.in_height
        self.out_speed = self.mover.in_speed
        return d

