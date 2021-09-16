class S:
    def __init__(self):
        super().__init__()  # forwards all unused arguments




class A(S):
    def __init__(self):
        def __init__(self, *args, **kwargs):
            self._speed = 10

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed

class B:
    def __init__(self):
        super().__init__()  # forwards all unused arguments
        self._speed = 20

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed


class CC:
    def __init__(self):
        super().__init__()  # forwards all unused arguments
        self._out_value = 0

    @property
    def out_value(self):
        return self._out_value

    @out_value.setter
    def out_value(self, value):
        self._out_value = value


a=A()
b=B()


A_get = A.speed
B_set = B.speed.fset




print(b.speed)
B_set(b, A_get(a))
print(b.speed)

def connect(out, out_obj, inp, inp_obj):
    print(out, out_obj, inp, inp_obj)
    out(out_obj, inp(inp_obj))

connect(B.speed.fset, b, A.speed.fget, a)




