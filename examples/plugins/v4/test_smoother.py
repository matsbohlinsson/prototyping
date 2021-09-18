import math
from random import random
from typing import Optional, Callable, Any

from examples.plugins.v4 import InSpeed, OutSpeed, OutValue
from examples.plugins.v4.Smoother import Smoother
from examples.plugins.v4.Generator import Generator
import matplotlib.pyplot as plt

from plugins import Plugin


class PluginExecutersType():

    def __init__(self):
        self._execution_list = []

    def add_executer(self, plugin, transfer_list):
        self._execution_list.append([plugin, transfer_list])

    #            print(loop_index, smoother.in_speed, smoother.out_speed)

    def execute(self):
        for plugin,transfers in self._execution_list:
            print(f'QQ:{plugin}, {transfers}')
            plugin.main_loop()
            for transfer in transfers:
                transfer()



def test_smoother():
    def simulate_first_loop(d):
        d.init_history_window()

    def make_transfer_function(out: Callable[[Any], Any], out_obj:Plugin, inp: Callable[[Any], Any], inp_obj:Plugin):
        print(out, out_obj, inp, inp_obj)
        print(f"Transfer:{out_obj.plugin_name}.{out.__name__} -> {inp_obj.plugin_name}.{inp.__name__}")
        # Add debug info in lambda. Name it plugin_name.out_value .....
        return lambda: inp(inp_obj, out(out_obj))

    generator = Generator(plugin_name='SpeedGenerator', function=lambda loop_index: math.sin(loop_index / 100) * 100)
    smoother = Smoother(plugin_name='SpeedSmoother', window_size=20, speed_change_limit=20)
    generator_out_value = make_transfer_function(Generator.out_value.fget, generator, Smoother.in_speed.fset, smoother)


    #Execution order
    exec = PluginExecutersType()
    exec.add_executer(generator,
                      [generator_out_value]
                      )
    exec.add_executer(smoother, [])

    #Run
    exec.execute()

test_smoother()

def foo():
    pass




