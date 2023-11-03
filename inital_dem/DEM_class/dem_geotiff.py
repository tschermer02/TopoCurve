#pip install numpy
#pip install geotiff
#pip install Pillow
# pip install scipy

from geotiff import GeoTiff
from dem_geotiff_class import Dem_Class
from PIL import Image
import numpy as np

tiff_file = "C:/Users/tsche/source/repos/TopoCurve/DEM_files/Durango_Clip.tif"

# Initializing DEM class
geoTiff = GeoTiff(tiff_file)
array = geoTiff.read()
dimx,dimy = geoTiff.tif_shape

dem = Dem_Class(array, dimx, dimy)

detrended, plane = dem.detrend()

# Plotting detrended DEM
dem.plot(detrended, "greyscale_dem_detrend.png")

# Mirroring DEM on all sides
dem.plot(dem.mirror_dem(), "greyscale_dem_mirror.png")

# Padding array
# https://www.geeksforgeeks.org/numpy-pad-function-in-python/
