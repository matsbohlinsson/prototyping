class Interface_in():
    pass


class Interface_out():
    pass


class Ispeed(Interface_in):
    pass


class InSpeed(Ispeed):
    def __init__(self):
        self.in_speed = None


class OutSpeed(Ispeed):
    def __init__(self):
        self.out_speed = None


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

