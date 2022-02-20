
import numpy as np
from scipy.interpolate import interpn
def value_func_3d(x, y, z):
    return 2 * x + 3 * y - z
x = np.linspace(0, 4, 5)
y = np.linspace(0, 5, 6)
z = np.linspace(0, 6, 7)
points = (x, y, z)
values = value_func_3d(*np.meshgrid(*points, indexing='ij'))
print(points)

#numpy multidimensional interpolation
#https://scipy.github.io/devdocs/tutorial/interpolate.html
