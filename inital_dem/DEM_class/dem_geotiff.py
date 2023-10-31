#pip install numpy
#pip install geotiff
#pip install Pillow
# pip install scipy

from geotiff import GeoTiff
from dem_geotiff_class import Dem_Class
from PIL import Image
import numpy as np

tiff_file = "C:/Users/tsche/source/repos/TopoCurve/DEM_files/Durango_Clip.tif"

#initializing DEM class
geoTiff = GeoTiff(tiff_file)
array = geoTiff.read()
dimx,dimy = geoTiff.tif_shape

dem = Dem_Class(array, dimx, dimy)

detrended, plane = dem.detrend()

#Plotting detrended DEM
img_array = 255*((detrended - np.amin(detrended))/(np.amax(detrended)- np.amin(detrended)))
Image.fromarray(img_array).convert("RGB").save("greyscale_dem_detrend.png")

#Mirroring DEM on all sides
f_array = []
top = np.concatenate((np.rot90(detrended,2),np.flipud(detrended),np.rot90(detrended,2)), axis=1)
middle = np.concatenate((np.fliplr(detrended),detrended,np.fliplr(detrended)), axis=1)
bottom = np.concatenate((np.rot90(detrended,2),np.flipud(detrended),np.rot90(detrended,2)), axis=1)

f_array = np.concatenate((top, middle, bottom), axis=0)

img_array_Zm = 255*((f_array - np.amin(f_array))/(np.amax(f_array)- np.amin(f_array)))
Image.fromarray(img_array_Zm).convert("RGB").save("greyscale_dem_detrend_Zm.png")

print(detrended)

