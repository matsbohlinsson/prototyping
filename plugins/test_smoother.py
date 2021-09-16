from timeit import timeit

from plugins.interface import InSpeed, OutSpeed
from plugins.Smoother import Smoother
from plugins.Generator import Generator


def test_smoother():
    test_speed_list = [1, 2, 7, 4, 3, 200, 198, 201, 200, 100, 101, 102, 80, 104, 106, 107, 107, 107, 107, 107, 107,
                       107, 107, 107, 107, 107, 107]

    def simulate_first_loop(d):
        d.init_history_window()

    def simulate_loop(d, index):
        d.main_loop(index)

    smoother = Smoother()
    generator = Generator(lambda loop_index2: loop_index2 % 1000)

    transfer_connections = lambda x: smoother.in_speed.set(generator.out_speed.get())

    execution_order = [generator.main_loop, transfer_connections, smoother.main_loop]

    connections = []


    simulate_first_loop(smoother)
    for loop_index in range(0, 20):
        for current_execution in execution_order:
            current_execution(loop_index)
        print(smoother.in_speed.get(), smoother.out_speed.get())


print(timeit(test_smoother, number=10))
