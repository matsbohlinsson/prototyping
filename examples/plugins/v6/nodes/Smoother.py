import logging
from dataclasses import dataclass, field
from pathlib import Path
from examples.plugins import GeneralPlugin
from statistics import mean

PLUGIN_NAME=__file__.split('.')[0]

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


if __name__ == "__main__":
    in_data = Input()
    out_data = Output()
    s = GeneralPlugin(input=Input(window_size=10, delta_max=3), output=Output(), run_function=run, run_post_function=run_post, plugin_name=PLUGIN_NAME, parent=None)
    s.csv.run_test_from_file(Path('../csv_testdata/Smoother.csv'))
