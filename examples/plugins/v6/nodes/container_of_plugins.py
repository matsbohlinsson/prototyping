import math

from examples.plugins.v6.nodes.Mover import Mover
from examples.plugins.v6.nodes.Smoother import Smoother
from examples.plugins.v6.nodes.Generator import Generator
from examples.plugins.v6 import OutSpeed, InSpeed, Plugin


class Container_of_plugins(Plugin, InSpeed, OutSpeed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create nodes
        #self.generator_speed = Generator(plugin_name='SpeedGenerator', expression=lambda loop_index: math.sin(loop_index / 100) * 100, csv_out='./2st_out.csv_testdata')
        self.generator_height = Generator(parent=self, plugin_name='HeightGenerator', expression=lambda loop_index: math.cos(loop_index / 100) * 100 )
        self.mover = Mover(parent=self,  plugin_name='Mover')

        # Connect nodes
        self.smoother = Smoother(parent=self, plugin_name='SpeedSmoother', in_window_size=20, speed_change_limit=20)
        #self.generator_speed.connect(self.smoother, Smoother.in_speed, Generator.out_value)
        self.generator_height.connect(self.mover, Mover.in_height, Generator.out_value)
        self.smoother.connect(self.mover, Mover.in_speed, Smoother.out_speed)  #self.mover.in_speed = self.smoother.out_speed
        
        self.mover.connect(self, Container_of_plugins.out_speed, Mover.out_speed)  #self.out_speed = self.mover.in_speed

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