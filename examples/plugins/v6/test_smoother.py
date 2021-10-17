import csv
import math
from pathlib import Path

from examples.plugins.v6.Mover import Mover
from examples.plugins.v6.Smoother import Smoother
from examples.plugins.v6.Generator import Generator
import matplotlib.pyplot as plt

from plugins import Plugin


class MainPlugin(Plugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create nodes
        generator_speed = Generator(plugin_name='SpeedGenerator', expression=lambda loop_index: math.sin(loop_index / 100) * 100, csv_out='./2st_out.csv')
        generator_height = Generator(plugin_name='HeightGenerator', expression=lambda loop_index: math.cos(loop_index / 100) * 100, csv_out='./3st_out.csv' )
        mover = Mover(plugin_name='Mover', csv_out='./4st_out.csv')

        # Connect nodes
        self.smoother = Smoother(plugin_name='SpeedSmoother', window_size=20, speed_change_limit=20, csv_out='./1st_out.csv')
        generator_speed.connect(self.smoother, Generator.out_value, Smoother.in_speed)
        generator_height.connect(mover,   Generator.out_value, Mover.in_height)
        self.smoother.connect(mover, Smoother.out_speed, Mover.in_speed)
        # Schedule execution
        self.add_plugin(generator_speed)
        self.add_plugin(self.smoother)
        self.add_plugin(generator_height)
        self.add_plugin(mover)

    def main_loop(self, loop_counter: int):
        d = self.run_all(loop_counter)
        return d


    def test(self):
        #self.test_with_csv_create_template(self.smoother, Path('./test.csv'))
        self.smoother.csv.run_test_from_file(Path('./test.csv'))


def my_main():
    debug = []
    main = MainPlugin(plugin_name='main')
    for i in range(0,111):
        d = main.main_loop(i)
        debug.append(d)
    print(debug)

    for plugin in Plugin._all_plugins:
        try:
            print(plugin.plugin_name, plugin.in_speed) #in_speed doesnt exist in all objects.
        except:
            pass

    #CSV
    main.test()

my_main()

p = Smoother(csv_in=Path('./test.csv'), csv_out=Path('./test_out.csv'))
p.main_execution()
p.main_execution()
p.main_execution()
#p.csv.fetch_input_from_in_file(0)
#p.csv.save_output_to_file()



