#pip install numpy
#pip install geotiff
#pip install Pillow
# pip install scipy

from geotiff import GeoTiff
from dem_geotiff_class import Dem_Class

tiff_file = "C:/Users/tsche/source/repos/TopoCurve/DEM_files/Durango_Clip.tif"

geoTiff = GeoTiff(tiff_file)
array = geoTiff.read()
dimx,dimy = geoTiff.tif_shape

dem1 = Dem_Class(array, dimx, dimy)

print(dem1.z_array)
print(dem1.dx_dy())
print(dem1.detrend())