import math

from examples.plugins.old.v2.Smoother import Smoother
from examples.plugins.v2.Generator import Generator
import matplotlib.pyplot as plt


def test_smoother():
    test_speed_list = [1, 2, 7, 4, 3, 200, 198, 201, 200, 100, 101, 102, 80, 104, 106, 107, 107, 107, 107, 107, 107,
                       107, 107, 107, 107, 107, 107]

    def simulate_first_loop(d):
        d.init_history_window()

    def simulate_loop(d, index):
        d.main_loop(index)

    def connect(transfer_connections, out, out_obj, inp, inp_obj):
        print(out, out_obj, inp, inp_obj)
        transfer_connections.append(lambda  x: inp(inp_obj, out(out_obj)))

    def better_connect(a,b):
        print("Better", a,b)

    smoother = Smoother(window_size=20, speed_change_limit=20)
    generator = Generator(lambda loop_index2: math.sin(loop_index2/100)*100)


    transfer_connections = []
    connect(transfer_connections, Generator.out_value.fget, generator, Smoother.in_speed.fset, smoother)
    better_connect( generator.__class__.out_value.fget, smoother.__str__())
    #connect(generator, 'out_value', smoother, 'in_speed')
    execution_order = [generator.main_loop, transfer_connections[0], smoother.main_loop]

    connections = []

    x=[]
    y=[]
    z=[]

    simulate_first_loop(smoother)
    for loop_index in range(0, 2000):
        for current_execution in execution_order:
            current_execution(loop_index)
        print(loop_index, smoother.in_speed, smoother.out_speed)
        x.append(loop_index)
        y.append(smoother.in_speed)
        z.append(smoother.out_speed)
    plt.plot(x, y, z)
    plt.show()


test_smoother()



