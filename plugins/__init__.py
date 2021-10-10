from __future__ import annotations

import copy
from abc import ABC, abstractmethod
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

    def __init__(self, plugin_name:str=None , *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_name = self.__class__ if plugin_name is None else plugin_name
        self.connections = []
        self.debug = {}
        self._execution_list = []
        self.api = Api()

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
        self.main_loop()
        for connection in self.connections:
            connection()
        return self.debug

    @abstractmethod
    def main_loop(self):
        pass

