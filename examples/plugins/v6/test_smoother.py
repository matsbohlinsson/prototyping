import math

from examples.plugins.v6.Mover import Mover
from examples.plugins.v6.Smoother import Smoother
from examples.plugins.v6.Generator import Generator
import matplotlib.pyplot as plt

from plugins import Plugin


class MainPlugin(Plugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create nodes
        generator_speed = Generator(plugin_name='SpeedGenerator', expression=lambda loop_index: math.sin(loop_index / 100) * 100)
        generator_height = Generator(plugin_name='HeightGenerator', expression=lambda loop_index: math.cos(loop_index / 100) * 100)
        smoother = Smoother(plugin_name='SpeedSmoother', window_size=20, speed_change_limit=20)
        mover = Mover(plugin_name='Mover')

        # Connect nodes
        generator_speed.connect(smoother, Generator.out_value, Smoother.in_speed)
        generator_height.connect(mover,   Generator.out_value, Mover.in_height)
        smoother.connect(mover,           Smoother.out_speed,  Mover.in_speed)
        # Schedule execution
        self.add_plugin(generator_speed)
        self.add_plugin(smoother)
        self.add_plugin(generator_height)
        self.add_plugin(mover)

    def main_loop(self):
        d = self.run_all()
        return d


def my_main():
    debug = []
    main = MainPlugin(plugin_name='main')
    for i in range(0,111):
        d = main.main_loop()
        debug.append(d)
    print(debug)

    for plugin in Plugin._all_plugins:
        try:
            print(plugin.plugin_name, plugin.in_speed)
        except:
            pass

my_main()



