from abc import ABC


class Plugin(ABC):
    def __init__(self, plugin_name:str=None , *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_name = self.__class__ if plugin_name is None else plugin_name
