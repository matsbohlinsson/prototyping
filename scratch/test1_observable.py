from typing import NewType


class ObservableProperty:

    def __set_name__(self, owner: type, name: str) -> None:
        def add_observer(obj, observer):
            if not hasattr(obj, self.observers_name):
                setattr(obj, self.observers_name, [])
            getattr(obj, self.observers_name).append(observer)

        self.private_name = f'_{name}'
        self.observers_name = f'_{name}_observers'
        setattr(owner, f'add_{name}_observer', add_observer)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        setattr(obj, self.private_name, value)
        for observer in getattr(obj, self.observers_name, []):
            observer(value)


Meters = NewType('Meters', float)
Kelvin = NewType('Kelvin', float)


class Axis:

    def __init__(self):
        self._position = 0.0
        self._temperature = 273.0

    position = ObservableProperty()
    temperature = ObservableProperty()


a = Axis()
print(a.position)  # Initial values from the constructor
print(a.temperature)
a.add_position_observer(lambda newval: print(f'New position for a: {newval}'))
a.add_temperature_observer(lambda newval: print(f'New temperature for a: {newval}'))
a.position = 5.0
a.temperature = 2.3
a.position = 5.1
a.temperature = 2.4


