import math
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from examples.plugins import GeneralPlugin, Plugin

PLUGIN_NAME=Path(__file__).name.split('.')[0]
CSV_FILE=Path('../csv_testdata/Smoother.csv')

@dataclass
class Input:
    start_value: float = 0
    function: Callable[[float], float] = None

@dataclass
class Output:
    value: float = 0

def run(input: Input, output: Output, log: logging.Logger):
    output.value = input.function(input.start_value)

def run_post(input: Input, output: Output, log: logging.Logger):
    input.start_value = input.start_value+1

class Generator(Plugin):
    def __init__(self, *args, **kwargs):
        super().__init__(input=Input(), output=Output(), *args, **kwargs)
        self.run_function=run
        self.run_post_function=run_post
        self.input = Input()
        self.output = Output()
        self.input.function = lambda x: math.sin(x / 100)*100

    def run(self):
        self.run_function(self.input, self.output, self.log)

    def run_post(self):
        if self.run_post_function:
            self.run_post_function(self.input, self.output, self.log)




def test():
    testdata = [{'clock_tick': 0.0, 'input.start_value': 0.0, 'output.value': 0.0, 'log': '', 'Generator.py': ''}, {'clock_tick': 1.0, 'input.start_value': 1.0, 'output.value': 0.9999833334166665, 'log': '', 'Generator.py': ''}, {'clock_tick': 2.0, 'input.start_value': 2.0, 'output.value': 1.999866669333308, 'log': '', 'Generator.py': ''}, {'clock_tick': 3.0, 'input.start_value': 3.0, 'output.value': 2.999550020249566, 'log': '', 'Generator.py': ''}, {'clock_tick': 4.0, 'input.start_value': 4.0, 'output.value': 3.998933418663416, 'log': '', 'Generator.py': ''}, {'clock_tick': 5.0, 'input.start_value': 5.0, 'output.value': 4.997916927067833, 'log': '', 'Generator.py': ''}, {'clock_tick': 6.0, 'input.start_value': 6.0, 'output.value': 5.996400647944459, 'log': '', 'Generator.py': ''}, {'clock_tick': 7.0, 'input.start_value': 7.0, 'output.value': 6.994284733753277, 'log': '', 'Generator.py': ''}, {'clock_tick': 8.0, 'input.start_value': 8.0, 'output.value': 7.991469396917269, 'log': '', 'Generator.py': ''}, {'clock_tick': 9.0, 'input.start_value': 9.0, 'output.value': 8.987854919801103, 'log': '', 'Generator.py': ''}, {'clock_tick': 10.0, 'input.start_value': 10.0, 'output.value': 9.983341664682815, 'log': '', 'Generator.py': ''}, {'clock_tick': 11.0, 'input.start_value': 11.0, 'output.value': 10.977830083717482, 'log': '', 'Generator.py': ''}, {'clock_tick': 12.0, 'input.start_value': 12.0, 'output.value': 11.971220728891936, 'log': '', 'Generator.py': ''}, {'clock_tick': 13.0, 'input.start_value': 13.0, 'output.value': 12.963414261969486, 'log': '', 'Generator.py': ''}, {'clock_tick': 14.0, 'input.start_value': 14.0, 'output.value': 13.954311464423649, 'log': '', 'Generator.py': ''}, {'clock_tick': 15.0, 'input.start_value': 15.0, 'output.value': 14.943813247359921, 'log': '', 'Generator.py': ''}]
    s = Generator(parent=None)
    #s = GeneralPlugin(input=Input(function=lambda x: math.sin(x / 100)*100), output=Output(), run_function=run, run_post_function=run_post, plugin_name=PLUGIN_NAME, parent=None)
    #verif_dict: {} = list(csv.DictReader(open(verif_file), quoting = csv.QUOTE_NONNUMERIC))
    s.csv.run_test_from_file(verif_dict=testdata)

if __name__ == "__main__":
    test()




