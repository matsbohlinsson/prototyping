import math

from examples.plugins.v5.Mover import Mover
from examples.plugins.v5.Smoother import Smoother
from examples.plugins.v5.Generator import Generator
import matplotlib.pyplot as plt

from plugins import Plugin


class PluginContainer():
    _execution_list: list[Plugin]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._execution_list = []

    def add_plugin(self, plugin: Plugin):
        self._execution_list.append(plugin)

    def run_all(self):
        debug = {}
        for plugin in self._execution_list:
            d = plugin.main_execution()
            debug.update(d)
        return debug

def test_smoother():
    def simulate_first_loop(d):
        d.init_history_window()


    generator_speed = Generator(plugin_name='SpeedGenerator', expression=lambda loop_index: math.sin(loop_index / 100) * 100)
    generator_height = Generator(plugin_name='HeightGenerator', expression=lambda loop_index: math.cos(loop_index / 100) * 100)
    smoother = Smoother(plugin_name='SpeedSmoother', window_size=20, speed_change_limit=20)
    mover = Mover(plugin_name='Mover')
    generator_speed.connect(smoother, Generator.out_value.fget, Smoother.in_speed.fset)
    generator_height.connect(mover, Generator.out_value.fget, Mover.in_height.fset)
    smoother.connect(mover, Smoother.out_speed.fget, Mover.in_speed.fset)
    p = PluginContainer()
    p.add_plugin(generator_speed)
    p.add_plugin(smoother)
    p.add_plugin(generator_height)
    p.add_plugin(mover)

    debug_rows = []
    for i in range(0,100):
        d = p.run_all()
        debug_rows.append(d)

    print(debug_rows)

    for row in debug_rows:
        print(f'{row["SpeedSmoother.in_speed"], row["SpeedSmoother.out_speed"]}')

test_smoother()




