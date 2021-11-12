import csv
import math
from pathlib import Path

from examples.plugins.v6.Mover import Mover
from examples.plugins.v6.Smoother import Smoother
from examples.plugins.v6.Generator import Generator
from examples.plugins.v6 import OutSpeed, OutHeight, InSpeed, Plugin


class MainPlugin(Plugin, InSpeed, OutSpeed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create nodes
        #self.generator_speed = Generator(plugin_name='SpeedGenerator', expression=lambda loop_index: math.sin(loop_index / 100) * 100, csv_out='./2st_out.csv')
        self.generator_height = Generator(plugin_name='HeightGenerator', expression=lambda loop_index: math.cos(loop_index / 100) * 100, csv_out='./3st_out.csv' )
        self.mover = Mover(plugin_name='Mover', csv_out='./4st_out.csv')

        # Connect nodes
        self.smoother = Smoother(plugin_name='SpeedSmoother', in_window_size=20, speed_change_limit=20, csv_out='./1st_out.csv')
        #self.generator_speed.connect(self.smoother, Smoother.in_speed, Generator.out_value)
        self.generator_height.connect(self.mover, Mover.in_height, Generator.out_value)
        self.smoother.connect(self.mover, Mover.in_speed, Smoother.out_speed)  #self.mover.in_speed = self.smoother.out_speed
        
        self.mover.connect(self, MainPlugin.out_speed, Mover.out_speed)  #self.out_speed = self.mover.in_speed

        #remove testdata
        #self.generator_speed.connect(self, MainPlugin.in_speed, Generator.out_value)


        # Schedule execution
        #self.add_plugin(self.generator_speed)
        self.add_plugin(self.smoother)
        self.add_plugin(self.generator_height)
        self.add_plugin(self.mover)

    def connect_external_inputs(self):
        self.smoother.in_speed = self.in_speed

    def main_loop(self, loop_counter: int):
        pass
