from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, Any


class Plugin(ABC):
    def __init__(self, plugin_name:str=None , *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_name = self.__class__ if plugin_name is None else plugin_name
        self.connections = []
        self.debug = {}


    def _connect(self, inp_obj: Plugin, out: Callable[[Any], Any], inp: Callable[[Any], Any]):
        def debug_info(connection_name:str, value):
            self.debug.update({connection_name: value})

        def transfer():
            inp(inp_obj, out(out_obj))
            debug_info(f'{out_obj.plugin_name}.{out.__name__}', out(out_obj))
            debug_info(f'{inp_obj.plugin_name}.{inp.__name__}', out(out_obj))

        out_obj = self
        print(out, out_obj, inp, inp_obj)
        # Add debug info in lambda. Name it plugin_name.out_value .....
        self.connections.append(transfer)

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

