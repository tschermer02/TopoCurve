# pip install rasterio
# pip install numpy
# pip install matplotlib
# pip install scipy

import numpy as np
import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt

from dem_ras_class import Dem_Ras_Class

dem_test = Dem_Ras_Class("C:/Users/tsche/source/repos/TopoCurve/DEM_files/Durango_Clip.tif")

z_detrended, plane = dem_test.detrended()

print(dem_test.z_array)
print(dem_test.dx_dy())
print(dem_test.dimx_dimy())
print(dem_test.detrended)




dem_test.plot_func(dem_test.mirror_array())



'''
fig, ax = plt.subplots(1, figsize = (12,12))
show(Zm, cmap='Greys_r', ax=ax)
plt.axis("off")
plt.show()
'''

<<<<<<< HEAD
=======

rtc = np.rot90(z_detrended,2)
ts = np.flipud(z_detrended) 
ltc = np.rot90(z_detrended,2)
ls = np.fliplr(z_detrended)
cen = z_detrended
rs = np.fliplr(z_detrended)
rbc = np.rot90(z_detrended,2)
bs = np.flipud(z_detrended)
lbc = np.rot90(z_detrended,2)

# rtc, ts, ltc, ls, cen, rs, rbc, bs , lbc
top = np.concatenate((rtc, ts, ltc), axis = 1)
mid = np.concatenate((ls, cen, rs), axis = 1)
bot = np.concatenate((rbc, bs, lbc), axis = 1)

Zm = np.concatenate((top, mid, bot), axis = 0)

#print(top)
print(z_detrended)
#print(Zm)

'''
fig, ax = plt.subplots(1, figsize=(12, 12))
show(Zm, cmap='Greys_r', ax=ax)
plt.axis("off")
plt.show()
'''
>>>>>>> 4d8839dd42eb8d3fb94eaedff5cb290d88ef784d
