class A:
    def __init__(self):
        super().__init__()  # forwards all unused arguments
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


a=A()
b=B()


A_get = A.speed.fget
B_set = B.speed.fset




print(b.speed)
B_set(b, A_get(a))
print(b.speed)

def connect(out, out_obj, inp, inp_obj):
    print(out, out_obj, inp, inp_obj)
    out(out_obj, inp(inp_obj))

connect(B.speed.fset, b, A.speed.fget, a)




