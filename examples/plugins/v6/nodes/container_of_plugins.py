import csv
import math
from dataclasses import dataclass
from pathlib import Path

import examples.plugins.v6.nodes.Mover as Mover
import examples.plugins.v6.nodes.Smoother as Smoother
import examples.plugins.v6.nodes.Generator as Generator
from examples.plugins.v6 import Plugin

PLUGIN_NAME=Path(__file__).name.split('.')[0]

@dataclass
class Input:
    speed: float = 0

@dataclass
class Output:
    speed: float = 0
    height: float = 0

class Container_of_plugins(Plugin):
    def __init__(self, *args, **kwargs):
        super().__init__(input=Input(), output=Output(), *args, **kwargs)
        self.input = Input()
        self.output = Output()
        self.smoother = Smoother.Smoother(parent=None)
        self.mover = Mover.Mover(parent=None)
        self.generator = Generator.Generator(parent=None)

    def run(self):
        self.smoother.input.value = self.input.speed

        self.smoother.execute_node()
        self.generator.execute_node()

        self.mover.input.speed = self.smoother.output.value
        self.mover.input.height = self.generator.output.value
        self.mover.execute_node()

        self.output.speed = self.mover.output.speed
        self.output.height = self.mover.output.height

def test():
    testdata = [{'clock_tick': 0.0, 'input.start_value': 0.0, 'output.value': 0.0, 'log': '', 'Generator.py': ''}, {'clock_tick': 1.0, 'input.start_value': 1.0, 'output.value': 0.9999833334166665, 'log': '', 'Generator.py': ''}, {'clock_tick': 2.0, 'input.start_value': 2.0, 'output.value': 1.999866669333308, 'log': '', 'Generator.py': ''}, {'clock_tick': 3.0, 'input.start_value': 3.0, 'output.value': 2.999550020249566, 'log': '', 'Generator.py': ''}, {'clock_tick': 4.0, 'input.start_value': 4.0, 'output.value': 3.998933418663416, 'log': '', 'Generator.py': ''}, {'clock_tick': 5.0, 'input.start_value': 5.0, 'output.value': 4.997916927067833, 'log': '', 'Generator.py': ''}, {'clock_tick': 6.0, 'input.start_value': 6.0, 'output.value': 5.996400647944459, 'log': '', 'Generator.py': ''}, {'clock_tick': 7.0, 'input.start_value': 7.0, 'output.value': 6.994284733753277, 'log': '', 'Generator.py': ''}, {'clock_tick': 8.0, 'input.start_value': 8.0, 'output.value': 7.991469396917269, 'log': '', 'Generator.py': ''}, {'clock_tick': 9.0, 'input.start_value': 9.0, 'output.value': 8.987854919801103, 'log': '', 'Generator.py': ''}, {'clock_tick': 10.0, 'input.start_value': 10.0, 'output.value': 9.983341664682815, 'log': '', 'Generator.py': ''}, {'clock_tick': 11.0, 'input.start_value': 11.0, 'output.value': 10.977830083717482, 'log': '', 'Generator.py': ''}, {'clock_tick': 12.0, 'input.start_value': 12.0, 'output.value': 11.971220728891936, 'log': '', 'Generator.py': ''}, {'clock_tick': 13.0, 'input.start_value': 13.0, 'output.value': 12.963414261969486, 'log': '', 'Generator.py': ''}, {'clock_tick': 14.0, 'input.start_value': 14.0, 'output.value': 13.954311464423649, 'log': '', 'Generator.py': ''}, {'clock_tick': 15.0, 'input.start_value': 15.0, 'output.value': 14.943813247359921, 'log': '', 'Generator.py': ''}]
    s = Container_of_plugins(parent=None)
    CSV_FILE = Path('../csv_testdata/container_of_plugins.csv')
    testdata = list(csv.DictReader(open(CSV_FILE), quoting = csv.QUOTE_NONNUMERIC))
    s.csv.run_test_from_file(verif_dict=testdata)

if __name__ == "__main__":
    test()

