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
'''
print(dem_test.z_array)
print(dem_test.dx_dy())
print(dem_test.dimx_dimy())
print(dem_test.detrend())
'''

fig, ax = plt.subplots(1, figsize=(12, 12))
show(dem_test.detrend, cmap='Greys_r', ax=ax)
show(dem_test.detrend, contour=False,  linewidths=0.7)
plt.axis("off")
plt.show()