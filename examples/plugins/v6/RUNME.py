import csv
import math
from pathlib import Path

from examples.plugins.v6.Mover import Mover
from examples.plugins.v6.Smoother import Smoother
from examples.plugins.v6.Generator import Generator
from examples.plugins.v6 import OutSpeed, OutHeight
import matplotlib.pyplot as plt

from plugins import Plugin


class MainPlugin(Plugin, OutSpeed, OutHeight):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create nodes
        generator_speed = Generator(plugin_name='SpeedGenerator', expression=lambda loop_index: math.sin(loop_index / 100) * 100, csv_out='./2st_out.csv')
        generator_height = Generator(plugin_name='HeightGenerator', expression=lambda loop_index: math.cos(loop_index / 100) * 100, csv_out='./3st_out.csv' )
        self.mover = Mover(plugin_name='Mover', csv_out='./4st_out.csv')

        # Connect nodes
        self.smoother = Smoother(plugin_name='SpeedSmoother', in_window_size=20, speed_change_limit=20, csv_out='./1st_out.csv')
        generator_speed.connect(self.smoother, Generator.out_value, Smoother.in_speed)
        generator_height.connect(self.mover,   Generator.out_value, Mover.in_height)
        self.smoother.connect(self.mover, Smoother.out_speed, Mover.in_speed)
        # Schedule execution
        self.add_plugin(generator_speed)
        self.add_plugin(self.smoother)
        self.add_plugin(generator_height)
        self.add_plugin(self.mover)

    def main_loop(self, loop_counter: int):
        d = self.run_all(loop_counter)
        self.out_height = self.mover.in_height
        self.out_speed = self.mover.in_speed
        return d




def my_main():
    debug = []
    main = MainPlugin(plugin_name='main', csv_out=Path('csv/main.csv'))
    for i in range(0,111):
        d = main.main_execution(i)
        debug.append(d)
    main = None
    '''
    for plugin in Plugin._all_plugins:
        try:
            print(plugin.plugin_name, plugin.in_speed) #in_speed doesnt exist in all objects.
        except:
            pass
    '''

#my_main()

print("Running tests:")
Smoother(csv_out=Path('./csv/Smoother_out.csv')).csv.run_test_from_file(Path('./csv/Smoother.csv'))
Generator(expression=lambda loop_index: math.sin(loop_index / 100) * 100).csv.run_test_from_file(Path('./csv/GeneratorSin.csv'))
MainPlugin().csv.run_test_from_file(Path('./csv/MainPlugin.csv'))


