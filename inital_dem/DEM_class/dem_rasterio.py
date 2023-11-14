# pip install rasterio
# pip install numpy
# pip install matplotlib
# pip install scipy
# pip install photutils
# pip install tifffile

import numpy as np
import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt

from dem_ras_class import Dem_Ras_Class

tiff_file= "../../repos/TopoCurve/DEM_files/Purgatory.tif"

dem_test = Dem_Ras_Class(tiff_file)

z_detrended, plane = dem_test.detrend()
'''
print(dem_test.z_array)
print(dem_test.dx_dy())
print(dem_test.dimx_dimy())
print(dem_test.detrended)



mirrored = dem_test.mirror_array()
tukey_win = dem_test.tukey_window(mirrored)
#dem_test.plot_func(tukey_win)
pad_array = dem_test.padding_array(tukey_win)
#dem_test.plot_func(pad_array)


# dem_test.plot_func(dem_test.mirror_array())
'''


dem_test.plot_func(dem_test.padding_array())



