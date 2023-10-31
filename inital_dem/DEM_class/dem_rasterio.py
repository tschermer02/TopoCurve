# pip install rasterio
# pip install numpy
# pip install matplotlib
# pip install scipy



import numpy as np
import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt
from scipy import signal

from dem_ras_class import Dem_Ras_Class

dem_test = Dem_Ras_Class("C:/Users/Joeln/source/repos/TopoCurve/DEM_files/Durango_Clip.tif")

z_detrended, plane = dem_test.detrend()

'''
print(dem_test.z_array)
print(dem_test.dx_dy())
print(dem_test.dimx_dimy())
print(dem_test.detrend())


fig, ax = plt.subplots(1, figsize=(12, 12))
show(z_detrended, cmap='Greys_r', ax=ax)
show(z_detrended, contour=True,  linewidths=0.7)
plt.axis("off")
plt.show()
'''


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
top = np.concatenate((rtc, ts, ltc), axis = None)
mid = np.concatenate((ls, cen, rs), axis = None)
bot = np.concatenate((rbc, bs, lbc), axis = None)

Zm = np.vstack((top, mid, bot), axis = 0)
# Zm.extend(ts); Zm.extend(ltc); Zm.extend(ls); Zm.extend(cen); Zm.extend(rs); Zm.extend(rbc); Zm.extend(bs); Zm.extend(lbc);

print(z_detrended.size)
print(Zm.size)

fig, ax = plt.subplots(1, figsize=(12, 12))
show(Zm, cmap='Greys_r', ax=ax)
plt.axis("off")
plt.show()