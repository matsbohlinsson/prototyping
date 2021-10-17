import csv
import math
from pathlib import Path

from examples.plugins.v6.Smoother import Smoother
from examples.plugins.v6.Generator import Generator
from examples.plugins.v6.MainPlugin import MainPlugin

if __name__ == "__main__":
    print("Running tests:")
    Smoother(csv_out=Path('./csv_out/Smoother_out.csv')).csv.run_test_from_file(Path('./csv/Smoother.csv'))
    Generator(csv_out=Path('./csv_out/Generator_out.csv'), expression=lambda loop_index: math.sin(loop_index / 100) * 100).csv.run_test_from_file(Path('./csv/GeneratorSin.csv'))
    MainPlugin(csv_out=Path('./csv_out/MainPlugin_out.csv')).csv.run_test_from_file(Path('./csv/MainPlugin.csv'))
    print("END")


