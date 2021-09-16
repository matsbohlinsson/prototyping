class P:
    def __init__(self, value):
        self._value = value

    def set(self, value):
        self._value = value

    def get(self):
        return self._value


class OutSpeed:
    def __init__(self):
        super().__init__()  # forwards all unused arguments
        print("OutSpeed")
        self.out_speed = P(0)


class InSpeed:
    def __init__(self):
        super().__init__()  # forwards all unused arguments
        print("InSpeed")
        self.in_speed = P(0)


class Smoother(InSpeed, OutSpeed):

    def __init__(self):
        super().__init__()  # forwards all unused arguments
        self.foo = 'foo'


s = Smoother()
print(s.out_speed.get())
