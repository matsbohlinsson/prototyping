import math
from random import random

from examples.Plugins.v1.Smoother import Smoother
from examples.Plugins.v1.Generator import Generator
import matplotlib.pyplot as plt


def test_smoother():
    test_speed_list = [1, 2, 7, 4, 3, 200, 198, 201, 200, 100, 101, 102, 80, 104, 106, 107, 107, 107, 107, 107, 107,
                       107, 107, 107, 107, 107, 107]

    def simulate_first_loop(d):
        d.init_history_window()

    def simulate_loop(d, index):
        d.main_loop(index)

    smoother = Smoother(window_size=20, speed_change_limit=20)
    generator = Generator(lambda loop_index2: math.sin(loop_index2/100)*100)

    transfer_connections = lambda x: smoother.in_speed.set(generator.out_value + random()*5)


    execution_order = [generator.main_loop, transfer_connections, smoother.main_loop]

    connections = []

    x=[]
    y=[]
    z=[]

    simulate_first_loop(smoother)
    for loop_index in range(0, 2000):
        for current_execution in execution_order:
            current_execution(loop_index)
        print(loop_index, smoother.in_speed.get(), smoother.out_speed.get())
        x.append(loop_index)
        y.append(smoother.in_speed.get())
        z.append(smoother.out_speed.get())
    plt.plot(x, y, z)
    plt.show()


test_smoother()



