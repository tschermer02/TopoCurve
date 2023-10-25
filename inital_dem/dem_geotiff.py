#pip install numpy
#pip install geotiff
#pip install Pillow

from geotiff import GeoTiff
from PIL import Image
import numpy as np
from scipy import signal

from dem_class import Dem_Class

tiff_file = "C:/Users/tsche/source/repos/TopoCurve/DEM_files/Durango_Clip.tif"

bounding_box = [(50.0, -10.8), (50.3, -10.9)]
geoTiff = GeoTiff(tiff_file)
array = geoTiff.read()
dimx,dimy = geoTiff.tif_shape

dem1 = Dem_Class(array, dimx, dimy)

print(dem1.z_array)
print(dem1.dx_dy())
print(dem1.detrend())