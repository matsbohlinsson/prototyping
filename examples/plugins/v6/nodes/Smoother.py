import csv
import logging
from dataclasses import dataclass, field
from pathlib import Path
from examples.plugins import GeneralPlugin, Plugin
from statistics import mean
PLUGIN_NAME=Path(__file__).name.split('.')[0]
CSV_FILE=Path('../csv_testdata/Smoother.csv')

@dataclass
class Input:
    value: float = 0
    delta_max: float = 4
    window_size: int = 3
    value_history: [float] = field(default_factory=list)


@dataclass
class Output:
    value: float = 0
    value_history:  [float] = field(default_factory=list)


def run(input: Input, output: Output, log: logging.Logger):
    output.value_history = input.value_history.copy()
    output.value_history.append(input.value)
    output.value_history = output.value_history[-int(input.window_size):]
    speed_avg = mean(output.value_history)
    output.value = speed_avg if abs(input.value - speed_avg) < input.delta_max else input.value

def run_post(input: Input, output: Output, log: logging.Logger):
    input.value_history = output.value_history.copy()

#Smoother = lambda parent:GeneralPlugin(input=Input(window_size=10, delta_max=3), output=Output(), run_function=run, run_post_function=run_post, plugin_name=PLUGIN_NAME, parent=parent)

class Smoother(Plugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.run_function=run
        self.run_post_function=run_post
        self.input = Input()
        self.output = Output()

    def run(self):
        self.run_function(self.input, self.output, self.log)

    def run_post(self):
        if self.run_post_function:
            self.run_post_function(self.input, self.output, self.log)



def test():
    testdata=[{'clock_tick': 0.0, 'input.value': 0.0, 'input.delta_max': 3.0, 'input.window_size': 3.0, 'input.value_history': '[]', 'output.value': 0.0, 'output.value_history': '[0.0]', 'log': '', 'qqq': ''}, {'clock_tick': 1.0, 'input.value': 0.9999833334166665, 'input.delta_max': 3.0, 'input.window_size': 3.0, 'input.value_history': '[0.0]', 'output.value': 0.4999916667083332, 'output.value_history': '[0.0, 0.9999833334166665]', 'log': '', 'qqq': ''}, {'clock_tick': 2.0, 'input.value': 1.999866669333308, 'input.delta_max': 3.0, 'input.window_size': 3.0, 'input.value_history': '[0.0, 0.9999833334166665]', 'output.value': 0.9999500009166582, 'output.value_history': '[0.0, 0.9999833334166665, 1.999866669333308]', 'log': '', 'qqq': ''}, {'clock_tick': 3.0, 'input.value': 2.999550020249566, 'input.delta_max': 3.0, 'input.window_size': 3.0, 'input.value_history': '[0.0, 0.9999833334166665, 1.999866669333308]', 'output.value': 1.9998000076665137, 'output.value_history': '[0.9999833334166665, 1.999866669333308, 2.999550020249566]', 'log': '', 'qqq': ''}, {'clock_tick': 4.0, 'input.value': 3.998933418663416, 'input.delta_max': 3.0, 'input.window_size': 3.0, 'input.value_history': '[0.9999833334166665, 1.999866669333308, 2.999550020249566]', 'output.value': 2.999450036082097, 'output.value_history': '[1.999866669333308, 2.999550020249566, 3.998933418663416]', 'log': '', 'qqq': ''}, {'clock_tick': 5.0, 'input.value': 4.997916927067833, 'input.delta_max': 3.0, 'input.window_size': 3.0, 'input.value_history': '[1.999866669333308, 2.999550020249566, 3.998933418663416]', 'output.value': 3.998800121993605, 'output.value_history': '[2.999550020249566, 3.998933418663416, 4.997916927067833]', 'log': '', 'qqq': ''}, {'clock_tick': 6.0, 'input.value': 5.996400647944459, 'input.delta_max': 3.0, 'input.window_size': 3.0, 'input.value_history': '[2.999550020249566, 3.998933418663416, 4.997916927067833]', 'output.value': 4.9977503312252365, 'output.value_history': '[3.998933418663416, 4.997916927067833, 5.996400647944459]', 'log': '', 'qqq': ''}, {'clock_tick': 7.0, 'input.value': 6.994284733753277, 'input.delta_max': 3.0, 'input.window_size': 3.0, 'input.value_history': '[3.998933418663416, 4.997916927067833, 5.996400647944459]', 'output.value': 5.9962007695885235, 'output.value_history': '[4.997916927067833, 5.996400647944459, 6.994284733753277]', 'log': '', 'qqq': ''}, {'clock_tick': 8.0, 'input.value': 7.991469396917269, 'input.delta_max': 3.0, 'input.window_size': 3.0, 'input.value_history': '[4.997916927067833, 5.996400647944459, 6.994284733753277]', 'output.value': 6.994051592871669, 'output.value_history': '[5.996400647944459, 6.994284733753277, 7.991469396917269]', 'log': '', 'qqq': ''}, {'clock_tick': 9.0, 'input.value': 8.987854919801103, 'input.delta_max': 3.0, 'input.window_size': 3.0, 'input.value_history': '[5.996400647944459, 6.994284733753277, 7.991469396917269]', 'output.value': 7.991203016823883, 'output.value_history': '[6.994284733753277, 7.991469396917269, 8.987854919801103]', 'log': '', 'qqq': ''}, {'clock_tick': 10.0, 'input.value': 9.983341664682815, 'input.delta_max': 3.0, 'input.window_size': 3.0, 'input.value_history': '[6.994284733753277, 7.991469396917269, 8.987854919801103]', 'output.value': 8.987555327133729, 'output.value_history': '[7.991469396917269, 8.987854919801103, 9.983341664682815]', 'log': '', 'qqq': ''}, {'clock_tick': 11.0, 'input.value': 10.977830083717482, 'input.delta_max': 3.0, 'input.window_size': 3.0, 'input.value_history': '[7.991469396917269, 8.987854919801103, 9.983341664682815]', 'output.value': 9.983008889400466, 'output.value_history': '[8.987854919801103, 9.983341664682815, 10.977830083717482]', 'log': '', 'qqq': ''}, {'clock_tick': 12.0, 'input.value': 11.971220728891936, 'input.delta_max': 3.0, 'input.window_size': 3.0, 'input.value_history': '[8.987854919801103, 9.983341664682815, 10.977830083717482]', 'output.value': 10.97746415909741, 'output.value_history': '[9.983341664682815, 10.977830083717482, 11.971220728891936]', 'log': '', 'qqq': ''}, {'clock_tick': 13.0, 'input.value': 12.963414261969486, 'input.delta_max': 3.0, 'input.window_size': 3.0, 'input.value_history': '[9.983341664682815, 10.977830083717482, 11.971220728891936]', 'output.value': 11.970821691526302, 'output.value_history': '[10.977830083717482, 11.971220728891936, 12.963414261969486]', 'log': '', 'qqq': ''}]
    s = Smoother(parent=None)
    s.csv.run_test_from_file(verif_dict=testdata)

if __name__ == "__main__":
    test()