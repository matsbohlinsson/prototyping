from __future__ import annotations

import copy
import csv
import pprint
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Any


class Runtime():
    def __init__(self):
        pass

    def sleep(self):
        pass

    def sleep_until_next_execution(self):
        pass

    def wait(self, lambda_expression):
        while not lambda_expression():
            self.sleep_until_next_execution()


class Dji():
    def __init__(self, runtime):
        self.runtime=runtime
        pass

    def takeoff(self):
        #print("Taking off")
        #self.java.takeoff()
        self.runtime.wait(lambda: self.is_flying())

    def is_flying(self):
        return True

class Api:
    def __init__(self):
        self.runtime = Runtime()
        self.dji = Dji(self.runtime)


class Plugin(ABC):
    _execution_list: list[Plugin]
    _all_plugins: list[Plugin] = []
    api: Api

    class Csv:
        def __init__(self, plugin:Plugin, in_file: Path, out_file: Path):
            self.out_file = None
            self.in_file = None
            self.in_vars = [attr for attr in dir(plugin) if attr.startswith('in_')]
            self.out_vars = [attr for attr in dir(plugin) if attr.startswith('out_')]
            self.plugin = plugin
            if in_file:
                self.in_file = in_file
                self.in_dict: {} = list(csv.DictReader(open(in_file)))
            if out_file:
                self.out_file = out_file
                column_names = ['loop_counter']+self.in_vars+self.out_vars+[self.plugin.plugin_name]
                self.out_writer = csv.DictWriter(open(self.out_file, 'w', ), fieldnames=column_names, quoting = csv.QUOTE_NONNUMERIC)
                self.out_writer.writeheader()


        def str_to_nbr(self, string):
            try:    return float(string)
            except:  return string

        def fetch_input_from_in_file(self, row_nbr: int):
            if self.in_file:
                self._fetch_input_from_dict(self.in_dict[row_nbr])

        def _fetch_input_from_dict(self, row: {}):
            in_name: str
            for in_name, value  in row.items():
                if in_name.startswith('in_'):
                    self.plugin.__getattribute__(in_name) # Fails if attribut doesn't exists
                    self.plugin.__setattr__(in_name, self.str_to_nbr(value))

        def _compare_output_with_dict(self, row: {}):
            out_name: str
            diff = {}
            for out_name, expected  in row.items():
                if out_name.startswith('out_'):
                    real = self.plugin.__getattribute__(out_name) # Fails if attribut doesn't exists
                    if expected != real:
                        diff.update({out_name: {'real':real, 'expected':expected}})
            return diff

        def save_output_to_file(self, loop_counter: int):
            if self.out_file:
                d = {}
                d.update({'loop_counter': loop_counter})
                for out_var in self.in_vars + self.out_vars:
                    d.update({out_var: self.plugin.__getattribute__(out_var)})
                self.out_writer.writerow(d)

        def run_test_from_file(self, verif_file: Path = None) -> []:
            print(f"{self.plugin.plugin_name} running test with data from:{verif_file}", end=' -> ')
            all_diff=[]
            verif_dict: {} = list(csv.DictReader(open(verif_file), quoting = csv.QUOTE_NONNUMERIC))
            for loop_nbr, verif_data in enumerate(verif_dict):
                #print(f"Testing: {self.plugin.plugin_name}: {verif_data}")
                self._fetch_input_from_dict(verif_data)
                self.plugin.main_execution(loop_nbr)
                diff = self._compare_output_with_dict(verif_data)
                if diff:
                    all_diff.append(diff)
                    print("Diff:", diff)
            if all_diff or len(verif_dict)<10:
                print(f'FAILED:{len(all_diff)} rows')
            else:
                print(f"SUCCESS {len(verif_dict)} rows")
            return all_diff


    def __init__(self, plugin_name:str=None, csv_in: Path=None, csv_out: Path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_name = self.__class__.__name__ if plugin_name is None else plugin_name
        self.connections = []
        self.debug = {}
        self._execution_list = []
        self.api = Api()
        self.csv = Plugin.Csv(self, csv_in, csv_out)

    def add_plugin(self, plugin: Plugin):
        self._execution_list.append(plugin)
        Plugin._all_plugins.append(plugin)

    def run_all(self, loop_counter: int):
        debug = {}
        for plugin in self._execution_list:
            d = plugin.main_execution(loop_counter)
            debug.update(d)
        return debug


    def _connect(self, inp_obj: Plugin, out: Callable[[Any], Any], inp: Callable[[Any], Any]):
        def debug_info(connection_name:str, value):
            self.debug.update({connection_name: value})

        def transfer(out, out_obj, inp, inp_obj):
            inp(inp_obj, out(out_obj))
            debug_info(f'{out_obj.plugin_name}.{out.__name__}', out(out_obj))
            debug_info(f'{inp_obj.plugin_name}.{inp.__name__}', out(out_obj))

        out_obj = self
        #print(out, out_obj, inp, inp_obj)
        self.connections.append(lambda out=out, out_obj=out_obj, inp=inp, inp_obj=inp_obj: transfer(out, out_obj, inp, inp_obj))



    def connect(self, inp_obj: Plugin, out , inp):
        self._connect(inp_obj, out.fget, inp.fset)


    def main_execution(self, loop_counter: int) -> {}:
        self.debug = {}
        self.csv.fetch_input_from_in_file(loop_counter)
        self.main_loop(loop_counter)
        self.csv.save_output_to_file(loop_counter)
        for connection in self.connections:
            connection()
        return self.debug

    @abstractmethod
    def main_loop(self, loop_counter: int):
        pass

