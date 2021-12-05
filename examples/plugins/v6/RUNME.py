import logging
import math
from pathlib import Path

import examples.plugins.v6.nodes.Smoother
import examples.plugins.v6.nodes.Generator

'''
TODO
terminera utifrån o sig själv. 
Cascade terminering.
egen data som sparas mellan sessioner.
logs in plugin to each csv file column
logs all logs in one file
automatsik generering av testdata.
exception i loops
chip enable, nix
sammanfattning antal passed/fail

generera noder från json fil, gömma icke användna in/ut signaler
generera execution order utifrån connect


'''
def old():
    logging.basicConfig(filename='logs/logger.log', level=logging.INFO,
                        format='%(asctime)s,%(msecs)d %(levelname)-5s P:%(name)s  %(message)s [%(funcName)s() %(filename)s:%(lineno)d]',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        force=True)

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

    s=Smoother(parent=None)
    print(s.in_speed)
    s.in_speed = 12

if __name__ == "__main__":
    examples.plugins.v6.nodes.Smoother.test()
    examples.plugins.v6.nodes.Generator.test()