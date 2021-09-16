class Interface_in():
    pass


class Interface_out():
    pass


class Ispeed(Interface_in):
    pass


class P:
    def __init__(self, value):
        super().__init__()  # forwards all unused arguments
        self._value = value

    def set(self, value):
        self._value = value

    def get(self):
        return self._value


class OutSpeed():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.out_speed = P(0)


class InSpeed():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.in_speed = P(0)




class InCourse(Interface_in):
    def __init__(self):
        self.course = None


class OutCourse(Interface_in):
    def __init__(self):
        self.course = None



class OutLatLon(Interface_in):
    def __init__(self):
        self.out_lat = None
        self.out_lon = None

class InLatLon(Interface_in):
    def __init__(self):
        self.in_lat = None
        self.in_lon = None

