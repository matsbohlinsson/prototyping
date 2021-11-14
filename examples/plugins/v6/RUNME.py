import math
from pathlib import Path

from examples.plugins.v6.nodes.Smoother import Smoother
from examples.plugins.v6.nodes.Generator import Generator
from examples.plugins.v6.nodes.container_of_plugins import Container_of_plugins
from examples.plugins.v6.nodes.container_of_container import Container_of_container

'''
TODO
logs in plugin to each csv file column
logs all logs in one file
automatsik generering av testdata.
exception i loops


'''
if __name__ == "__main__":
    print("Running tests:")
    if 0:
        c = Container_of_container(parent=None, csv_out=Path('../v6/csv_out/Container_of_container.csv'))
        for i in range(10):
            c.execute()
        exit(0)

    Container_of_container(parent=None).csv.run_test_from_file(Path(
        'csv_testdata/container_of_container.csv'))

    Smoother(parent=None).csv.run_test_from_file(Path('csv_testdata/Smoother.csv'))
    Generator(parent=None, expression=lambda loop_index: math.sin(loop_index / 100) * 100).csv.run_test_from_file(Path(
        'csv_testdata/GeneratorSin.csv'))
    Container_of_plugins(parent=None).csv.run_test_from_file(Path(
        'csv_testdata/container_of_plugins.csv'))

    print("END")
