class Interface_in():
    pass


class Interface_out():
    pass


class Ispeed(Interface_in):
    pass


class P:
    def __init__(self, value):
        super().__init__()
        self._value = value

    def set(self, value):
        self._value = value

    def get(self):
        return self._value


class OutValue(Interface_out):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._out_value = 0

    @property
    def out_value(self):
        return self._out_value

    @out_value.setter
    def out_value(self, value):
        self._out_value = value


class OutSpeed(Interface_out):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._out_speed = 0

    @property
    def out_speed(self):
        return self._out_speed

    @out_speed.setter
    def out_speed(self, speed):
        self._out_speed = speed


class InSpeed(Interface_in):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._in_speed = 0

    @property
    def in_speed(self):
        return self._in_speed

    @in_speed.setter
    def in_speed(self, speed):
        self._in_speed = speed


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

