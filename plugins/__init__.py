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
        print("Taking off")
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
                self.out_writer = csv.DictWriter(open(self.out_file, 'w'), fieldnames=self.in_vars+self.out_vars)
                self.out_writer.writeheader()


        def str_to_nbr(self, string):
            try:    return float(string)
            except:  return string

        def fetch_input_from_in_file(self, row_nbr: int):
            if self.in_file:
                in_name: str
                for in_name, value  in self.in_dict[row_nbr].items():
                    if in_name.startswith('in_'):
                        self.plugin.__getattribute__(in_name) # Fails if attribut doesn't exists
                        self.plugin.__setattr__(in_name, self.str_to_nbr(value))

        def save_output_to_file(self):
            if self.out_file:
                d = {}
                for out_var in self.in_vars + self.out_vars:
                    print({out_var: self.plugin.__getattribute__(out_var)})
                    d.update({out_var: self.plugin.__getattribute__(out_var)})
                self.out_writer.writerow(d)
                print("YY", d)





        def test_with_csv_create_template(self, plugin: Plugin = None, file: Path = None):
            in_vars = [attr for attr in dir(plugin) if attr.startswith('in_')]
            out_vars = [attr for attr in dir(plugin) if attr.startswith('out_')]
            with open(file.absolute(), 'w') as f:
                writer = csv.DictWriter(f, fieldnames=in_vars + out_vars)
                writer.writeheader()
            print("QQ", in_vars, out_vars)

        def run_test_from_file(self, file: Path = None):
            with open(file.absolute(), 'r') as f:
                reader = csv.DictReader(f)
                print(reader.fieldnames)
                in_fields = [x for x in reader.fieldnames if x.startswith('in_')]
                out_fields = [x for x in reader.fieldnames if x.startswith('out_')]
                print("IN", in_fields)
                print("OUT", out_fields)
                for row in reader:
                    print(row)

    def __init__(self, plugin_name:str=None, csv_in: Path=None, csv_out: Path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_name = self.__class__ if plugin_name is None else plugin_name
        self.connections = []
        self.debug = {}
        self._execution_list = []
        self.api = Api()
        self.csv = Plugin.Csv(self, csv_in, csv_out)

    def add_plugin(self, plugin: Plugin):
        self._execution_list.append(plugin)
        Plugin._all_plugins.append(plugin)

    def run_all(self):
        debug = {}
        for plugin in self._execution_list:
            d = plugin.main_execution()
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
        print(out, out_obj, inp, inp_obj)
        self.connections.append(lambda out=out, out_obj=out_obj, inp=inp, inp_obj=inp_obj: transfer(out, out_obj, inp, inp_obj))



    def connect(self, inp_obj: Plugin, out , inp):
        self._connect(inp_obj, out.fget, inp.fset)


    def main_execution(self) -> {}:
        self.debug = {}
        self.csv.fetch_input_from_in_file(row_nbr=1)
        self.main_loop()
        self.csv.save_output_to_file()
        for connection in self.connections:
            connection()
        return self.debug

    @abstractmethod
    def main_loop(self):
        pass

