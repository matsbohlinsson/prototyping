from abc import ABC


class Plugin(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
