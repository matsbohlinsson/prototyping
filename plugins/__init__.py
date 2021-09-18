from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, Any


class Plugin(ABC):
    def __init__(self, plugin_name:str=None , *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_name = self.__class__ if plugin_name is None else plugin_name
        self.connections = []


    def connect(self, out: Callable[[Any], Any], inp: Callable[[Any], Any], inp_obj:Plugin):
        out_obj = self
        print(out, out_obj, inp, inp_obj)
        print(f"Transfer:{out_obj.plugin_name}.{out.__name__} -> {inp_obj.plugin_name}.{inp.__name__}")
        # Add debug info in lambda. Name it plugin_name.out_value .....
        self.connections.append(lambda: inp(inp_obj, out(out_obj)))

    def main_execution(self):
        self.main_loop()
        for connection in self.connections:
            connection()

    @abstractmethod
    def main_loop(self):
        pass

