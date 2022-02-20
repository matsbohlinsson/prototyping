import time

import numpy as np
import scipy.ndimage
resize_factor=int(4096/32)
orig_size=int(32)
x_base = np.arange(orig_size*orig_size).reshape(orig_size,orig_size)
x = resize_factor*x_base
#x= x/4
print('Original array:')
print(x)


def resample(mapx, resize_factor, order ):
    start = time.time()
    print(f'Resampled by a factor of {resize_factor} with order:{order}:')
    print(scipy.ndimage.zoom(mapx, resize_factor, order=order))
    print(f'Time:{time.time()-start}')
    print()

resample(x,resize_factor,0)
resample(x,resize_factor,1)
resample(x,resize_factor,2)
