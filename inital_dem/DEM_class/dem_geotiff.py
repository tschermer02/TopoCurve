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

#Python program to find
#smallest power of 2
#greater than or equal to n
import math

# Function to find the smallest power of 2
# greater than or equal to n
def nearestPowerOf2(N):
	# Calculate log2 of N
	a = int(math.log2(N))

	# If 2^a is equal to N, return N
	if 2**a == N:
		return N
	
	# Return 2^(a + 1)
	return 2**(a + 1)

# Main function
if __name__ == "__main__":
	# Input number
	n = 5
	# Call the nearestPowerOf2 function
	print(nearestPowerOf2(n))

# https://www.geeksforgeeks.org/numpy-pad-function-in-python/
