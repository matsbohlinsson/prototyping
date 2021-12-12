import csv
import math
from dataclasses import dataclass
from pathlib import Path

from examples.plugins.v6 import Plugin
from examples.plugins.v6.nodes.container_of_plugins import Container_of_plugins

PLUGIN_NAME=Path(__file__).name.split('.')[0]

@dataclass
class Input:
    speed: float = 0

@dataclass
class Output:
    speed: float = 0
    height: float = 0


class Container_of_2container(Plugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input = Input()
        self.output = Output()
        self.container_of_plugins1 = Container_of_plugins(parent=self)
        self.container_of_plugins2 = Container_of_plugins(parent=self)

    def run(self):
        #In
        self.container_of_plugins1.input.speed = self.input.speed

        self.container_of_plugins1.execute_node()
        self.container_of_plugins2.input.speed = self.container_of_plugins1.output.speed
        self.container_of_plugins2.execute_node()

        #Out
        self.output.speed = self.container_of_plugins2.output.speed
        self.output.height = self.container_of_plugins2.output.height

def test():
    testdata = [{'clock_tick': 0.0, 'input.speed': 0.0, 'output.speed': 0.0, 'output.height': 0.0, 'output.log': '', 'log': '', 'Container_of_2container': ''}, {'clock_tick': 1.0, 'input.speed': 1.0, 'output.speed': 2.25, 'output.height': 1.999966666833333, 'output.log': '', 'log': '', 'Container_of_2container': ''}, {'clock_tick': 2.0, 'input.speed': 2.0, 'output.speed': 4.5, 'output.height': 3.999733338666616, 'output.log': '', 'log': '', 'Container_of_2container': ''}, {'clock_tick': 3.0, 'input.speed': 3.0, 'output.speed': 10.5, 'output.height': 5.999100040499132, 'output.log': '', 'log': '', 'Container_of_2container': ''}, {'clock_tick': 4.0, 'input.speed': 4.0, 'output.speed': 18.0, 'output.height': 7.997866837326832, 'output.log': '', 'log': '', 'Container_of_2container': ''}, {'clock_tick': 5.0, 'input.speed': 5.0, 'output.speed': 27.0, 'output.height': 9.995833854135666, 'output.log': '', 'log': '', 'Container_of_2container': ''}, {'clock_tick': 6.0, 'input.speed': 6.0, 'output.speed': 36.0, 'output.height': 11.992801295888919, 'output.log': '', 'log': '', 'Container_of_2container': ''}, {'clock_tick': 7.0, 'input.speed': 7.0, 'output.speed': 45.0, 'output.height': 13.988569467506554, 'output.log': '', 'log': '', 'Container_of_2container': ''}, {'clock_tick': 8.0, 'input.speed': 8.0, 'output.speed': 54.0, 'output.height': 15.982938793834538, 'output.log': '', 'log': '', 'Container_of_2container': ''}, {'clock_tick': 9.0, 'input.speed': 9.0, 'output.speed': 63.0, 'output.height': 17.975709839602207, 'output.log': '', 'log': '', 'Container_of_2container': ''}, {'clock_tick': 10.0, 'input.speed': 10.0, 'output.speed': 72.0, 'output.height': 19.96668332936563, 'output.log': '', 'log': '', 'Container_of_2container': ''}, {'clock_tick': 11.0, 'input.speed': 11.0, 'output.speed': 81.0, 'output.height': 21.955660167434964, 'output.log': '', 'log': '', 'Container_of_2container': ''}, {'clock_tick': 12.0, 'input.speed': 12.0, 'output.speed': 90.0, 'output.height': 23.942441457783872, 'output.log': '', 'log': '', 'Container_of_2container': ''}, {'clock_tick': 13.0, 'input.speed': 13.0, 'output.speed': 99.0, 'output.height': 25.926828523938973, 'output.log': '', 'log': '', 'Container_of_2container': ''}, {'clock_tick': 14.0, 'input.speed': 14.0, 'output.speed': 108.0, 'output.height': 27.908622928847297, 'output.log': '', 'log': '', 'Container_of_2container': ''}, {'clock_tick': 15.0, 'input.speed': 15.0, 'output.speed': 117.0, 'output.height': 29.887626494719843, 'output.log': '', 'log': '', 'Container_of_2container': ''}]
    s = Container_of_2container(parent=None)
    #CSV_FILE = Path('../csv_testdata/container_of_2container.csv')
    #testdata = list(csv.DictReader(open(CSV_FILE), quoting = csv.QUOTE_NONNUMERIC))
    #print(testdata)
    s.csv.run_test_from_file(verif_dict=testdata)

if __name__ == "__main__":
    test()
