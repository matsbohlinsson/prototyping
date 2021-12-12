from dataclasses import dataclass
from typing import NewType


class ObservableProperty:
    QQ=0
    def __set_name__(self, owner: type, name: str) -> None:
        def add_observer(obj, observer):
            if not hasattr(obj, self.observers_name):
                setattr(obj, self.observers_name, [])
            getattr(obj, self.observers_name).append(observer)

        self.private_name = f'_{name}'
        self.observers_name = f'_{name}_observers'
        self.name = name
        setattr(owner, f'add_{name}_observer', add_observer)

    def __get__(self, obj, objtype=None):
        if obj is None or ObservableProperty.QQ==1:
            return self
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        setattr(obj, self.private_name, value)
        for observer in getattr(obj, self.observers_name, []):
            observer(value)

    def q(self):
        return self


class InputBase():
    def __init__(self):
        pass

    def add_observer(self, var, callback):
        print("QQ", var, callback)

@dataclass
class Input(InputBase):
    value: float = ObservableProperty()
    window_size: int = ObservableProperty()

'''    def __init__(self):
        self._value = 0.0
        self._window_size = 273.0
'''



a = Input(value=12, window_size=23)
a.add_value_observer(lambda newval: print(f'New position for a: {newval}'))
a.value = 1
a.add_observer(Input.__annotations__, lambda x:print(f'Change:{x}'))
a.value = 1
a.window_size = 2
#a.value.q
ObservableProperty.QQ = 1
print(a.value.name)



'''print(a.position)  # Initial values from the constructor
print(a.temperature)
a.add_position_observer(lambda newval: print(f'New position for a: {newval}'))
a.add_temperature_observer(lambda newval: print(f'New temperature for a: {newval}'))
a.position = 5.0
a.temperature = 2.3
a.position = 5.1
a.temperature = 2.4
'''

