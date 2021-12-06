import logging
import math
from pathlib import Path

import examples.plugins.v6.nodes.Smoother
import examples.plugins.v6.nodes.Generator
import examples.plugins.v6.nodes.Mover
import examples.plugins.v6.nodes.container_of_plugins
'''
TODO
Lägg till de andra plugins till RUNME
rensa i init, tag bort all död kod.

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

if __name__ == "__main__":
    examples.plugins.v6.nodes.Smoother.test()
    examples.plugins.v6.nodes.Generator.test()
    examples.plugins.v6.nodes.Mover.test()
    examples.plugins.v6.nodes.container_of_plugins.test()

