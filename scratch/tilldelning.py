class Event:

    def __init__(self, callback):
        self.callback = callback

    def __get__(self, instance, owner):
        print("get", instance, owner)
        return 5 * (instance.fahrenheit - 32) / 9

    def __set__(self, instance, value):
        print("set", instance, value)
        self.callback(value)
        instance.fahrenheit = 32 + 9 * value / 5

    def reg_callback(self, callback):
        self.callback = callback


class Temperature:

    celsius = Event(lambda x: print(f"Din Mamma {x}"))


    def __init__(self, initial_f):
        self.fahrenheit = initial_f




print("Din Mamma")
Temperature.celsius.
'''t.celsius = 13
t.celsius = 14
t.celsius
tt=Temperature(12)
tt.celsius = 17

print(t.celsius)
'''