from interface import InSpeed, OutSpeed, InCourse, OutCourse, OutLatLon, InLatLon


class DroneRunner(InSpeed, InCourse):
   def __init__(self):
       super().__init__()


class Smoother(InLatLon, OutLatLon):
    def __init__(self):
        super().__init__()

    def loop(self):
        self.out_lat = self.in_lat
        self.out_lon = self.in_lon


d = DroneRunner()
print(isinstance(d, OutSpeed))
print(d.__getattribute__('in_speed'))

