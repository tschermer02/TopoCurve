#pip install numpy
#pip install geotiff
#pip install Pillow

from geotiff import GeoTiff
from PIL import Image
import numpy as np
from scipy import signal

tiff_file = "C:/Users/tsche/source/repos/TopoCurve/DEM_files/Durango_Clip.tif"

bounding_box = [(50.0, -10.8), (50.3, -10.9)]
geoTiff = GeoTiff(tiff_file)
array = geoTiff.read()


zarray = np.array(array)

dx = abs(zarray[(0,0)]-zarray[(0,1)])
dy = abs(zarray[(0,0)]-zarray[(1,0)])

print(zarray)

print(dx)
print(dy)


dimx,dimy = geoTiff.tif_shape

print(dimx)
print(dimy)

Z_detrended = signal.detrend(zarray)

plane = zarray-Z_detrended

print(Z_detrended)
print(plane)