# pip install rasterio
# pip install numpy
# pip install matplotlib
# pip install scipy
# 

import numpy as np
import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt
from scipy import signal

dem = rio.open("C:/Users/Joeln/source/repos/TopoCurve/DEM_files/Durango_Clip.tif")
# dem_array = dem.read(1).astype('float64')

dem_array = dem.read()
print(dem_array)

dx = abs(dem_array[0][0][0] -dem_array[0][0][1])
print(dx)

dy = abs(dem_array[0][0][0] -dem_array[0][1][0])
print(dy)

dim_x = dem_array.shape[1]
dim_y = dem_array.shape[2]

print(dim_x)
print(dim_y)

dem_array_detrend = signal.detrend(dem_array)
print(dem_array_detrend)