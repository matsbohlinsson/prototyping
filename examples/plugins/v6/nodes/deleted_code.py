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

class InDeltaMax(Interface_in):
    def __init__(self, in_delta_max=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.in_delta_max = in_delta_max

    @property
    def in_speed(self):
        return self._in_speed

    @in_speed.setter
    def in_speed(self, speed):
        self._in_speed = speed

class InHeight(Interface_in):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._in_height = 0

    @property
    def in_height(self):
        return self._in_height

    @in_height.setter
    def in_height(self, height):
        self._in_height = height

class InCourse(Interface_in):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course = None

class InWindowSize(Interface_in):
    def __init__(self, in_window_size:int=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._in_window_size = in_window_size

    @property
    def in_window_size(self):
        return self._in_window_size

    @in_window_size.setter
    def in_window_size(self, new):
        old = self._in_window_size
        self._in_window_size = new
        self._value_changed(old, new)

    def onchange_in_window_size(self, callback):
        self._observers.append(callback)


class OutCourse(Interface_in):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course = None


class OutHeight(Interface_in):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.out_height = None
    @property
    def out_height(self, *args, **kwargs):
        return self._out_height

    @out_height.setter
    def out_height(self, height, *args, **kwargs):
        self._out_height = height


class OutLatLon(Interface_in):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.out_lat = None
        self.out_lon = None


class InLatLon(Interface_in):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.in_lat = None
        self.in_lon = None

