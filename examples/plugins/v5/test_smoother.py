import math
from random import random
from typing import Optional, Callable, Any

from examples.plugins.v5 import InSpeed, OutSpeed, OutValue
from examples.plugins.v5.Smoother import Smoother
from examples.plugins.v5.Generator import Generator
import matplotlib.pyplot as plt

from plugins import Plugin


class PluginContainer():

    def __init__(self):
        self._execution_list = []

    def add_executer(self, plugin):
        self._execution_list.append(plugin)

    #            print(loop_index, smoother.in_speed, smoother.out_speed)

    def execute(self):
        for plugin in self._execution_list:
            plugin.main_execution()



def test_smoother():
    def simulate_first_loop(d):
        d.init_history_window()


    generator = Generator(plugin_name='SpeedGenerator', function=lambda loop_index: math.sin(loop_index / 100) * 100)
    smoother = Smoother(plugin_name='SpeedSmoother', window_size=20, speed_change_limit=20)
    generator.connect(Generator.out_value.fget, Smoother.in_speed.fset, smoother)

    p = PluginContainer()
    p.add_executer(generator.main_execution)
    p.add_executer(smoother.main_execution)

    p.execute()
    p.execute()
    p.execute()



test_smoother()




