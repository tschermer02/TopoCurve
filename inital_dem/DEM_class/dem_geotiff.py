#pip install numpy
#pip install geotiff
#pip install Pillow
#pip install scipy
#pip install photutils

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
dimx_f,dimy_f, mirror = dem.mirror_dem()
dem.plot(mirror, "greyscale_dem_mirror.png")

# Padding array
dem.plot(dem.padding(), "greyscale_dem_padding.png")

#Tukey Window
dem.plot(dem.tukeyWindow(), "tukeyWind.png")

