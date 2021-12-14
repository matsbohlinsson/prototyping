from dataclasses import dataclass
from typing import NewType, List


class ObservableProperty:
    pass

class InputBase():
    def __init__(self):
        pass

    def add_observer(self, var, callback):
        print("QQ", var, callback)

    def ok_1(self, foo: List[str] = ...) -> None: ...

    def add_value1_observer(self, callback: callable) -> None: ...
