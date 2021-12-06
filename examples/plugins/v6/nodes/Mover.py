import csv
import logging
import numbers
from dataclasses import dataclass, field
from pathlib import Path

from examples.plugins import GeneralPlugin
from examples.plugins.v6 import Plugin

PLUGIN_NAME=Path(__file__).name.split('.')[0]
CSV_FILE=Path('../csv_testdata/Mover.csv')

@dataclass
class Input:
    speed: float = 0
    height: float = 0
    course: float = 0

@dataclass
class Output:
    speed: float = 0
    height: float = 0

def run(input: Input, output: Output, log: logging.Logger):
    output.speed = input.speed * 3
    output.height = input.height * 2


def test():
    testdata=[{'clock_tick': 0.0, 'input.speed': 0.0, 'input.height': 0.0, 'input.course': 0.0, 'output.speed': 0.0, 'output.height': 0.0, 'output.log': '', 'log': '', 'Mover': ''}, {'clock_tick': 1.0, 'input.speed': 1.0, 'input.height': 0.9999833334166665, 'input.course': 0.0, 'output.speed': 3.0, 'output.height': 1.999966666833333, 'output.log': '', 'log': '', 'Mover': ''}, {'clock_tick': 2.0, 'input.speed': 2.0, 'input.height': 1.999866669333308, 'input.course': 0.0, 'output.speed': 6.0, 'output.height': 3.999733338666616, 'output.log': '', 'log': '', 'Mover': ''}, {'clock_tick': 3.0, 'input.speed': 3.0, 'input.height': 2.999550020249566, 'input.course': 0.0, 'output.speed': 9.0, 'output.height': 5.999100040499132, 'output.log': '', 'log': '', 'Mover': ''}, {'clock_tick': 4.0, 'input.speed': 4.0, 'input.height': 3.998933418663416, 'input.course': 0.0, 'output.speed': 12.0, 'output.height': 7.997866837326832, 'output.log': '', 'log': '', 'Mover': ''}, {'clock_tick': 5.0, 'input.speed': 5.0, 'input.height': 4.997916927067833, 'input.course': 0.0, 'output.speed': 15.0, 'output.height': 9.995833854135666, 'output.log': '', 'log': '', 'Mover': ''}, {'clock_tick': 6.0, 'input.speed': 6.0, 'input.height': 5.996400647944459, 'input.course': 0.0, 'output.speed': 18.0, 'output.height': 11.992801295888919, 'output.log': '', 'log': '', 'Mover': ''}, {'clock_tick': 7.0, 'input.speed': 7.0, 'input.height': 6.994284733753277, 'input.course': 0.0, 'output.speed': 21.0, 'output.height': 13.988569467506554, 'output.log': '', 'log': '', 'Mover': ''}, {'clock_tick': 8.0, 'input.speed': 8.0, 'input.height': 7.991469396917269, 'input.course': 0.0, 'output.speed': 24.0, 'output.height': 15.982938793834538, 'output.log': '', 'log': '', 'Mover': ''}, {'clock_tick': 9.0, 'input.speed': 9.0, 'input.height': 8.987854919801103, 'input.course': 0.0, 'output.speed': 27.0, 'output.height': 17.975709839602207, 'output.log': '', 'log': '', 'Mover': ''}]
    s = GeneralPlugin(input=Input(), output=Output(), run_function=run, plugin_name=PLUGIN_NAME, parent=None)
    #testdata= list(csv.DictReader(open(CSV_FILE), quoting=csv.QUOTE_NONNUMERIC))
    s.csv.run_test_from_file(verif_dict=testdata)

if __name__ == "__main__":
    test()