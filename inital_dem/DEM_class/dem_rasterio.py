# pip install rasterio
# pip install numpy
# pip install matplotlib
# pip install scipy

import numpy as np
import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt

from dem_ras_class import Dem_Ras_Class

dem_test = Dem_Ras_Class("C:/Users/Joeln/source/repos/TopoCurve/DEM_files/Durango_Clip.tif")

z_detrended, plane = dem_test.detrended()

print(dem_test.z_array)
print(dem_test.dx_dy())
print(dem_test.dimx_dimy())
print(dem_test.detrended)




dem_test.plot_func(dem_test.mirror_array())




