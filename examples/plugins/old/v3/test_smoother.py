import math
from random import random
from typing import Optional, Callable, Any

from examples.plugins.v3 import InSpeed, OutSpeed, OutValue
from examples.plugins.v3.Smoother import Smoother
from examples.plugins.v3.Generator import Generator
import matplotlib.pyplot as plt

from plugins import Plugin


def test_smoother():
    def simulate_first_loop(d):
        d.init_history_window()

    def make_transfer_function(out: Callable[[Any], Any], out_obj:Plugin, inp: Callable[[Any], Any], inp_obj:Plugin):

        print(out, out_obj, inp, inp_obj)
        print(f"QQTransfer:{out_obj.plugin_name}.{out.__name__} -> {inp_obj.plugin_name}.{inp.__name__}")
        # Add debug info in lambda. Name it plugin_name.out_value .....
        return lambda  x,y: inp(inp_obj, out(out_obj))

    generator = Generator(plugin_name='SpeedGenerator', function=lambda loop_index,_: math.sin(loop_index / 100) * 100)
    smoother = Smoother(plugin_name='SpeedSmoother', window_size=20, speed_change_limit=20)
    generator_out_value = make_transfer_function(Generator.out_value.fget, generator, Smoother.in_speed.fset, smoother)


    #Execution order
    execution_order = []
    add = execution_order.append
    add(generator.main_loop)
    add(generator_out_value) # Can be many for each plugin.
    add(smoother.main_loop)


    x=[]
    y=[]
    z=[]

    simulate_first_loop(smoother)
    for loop_index in range(0, 2000):
        for execution in execution_order:
            execution(loop_index, loop_index)
        print(loop_index, smoother.in_speed, smoother.out_speed)
        x.append(loop_index)
        y.append(smoother.in_speed)
        z.append(smoother.out_speed)
    plt.plot(x, y, z)
    plt.show()


test_smoother()

def foo():
    pass

foo.__name__


