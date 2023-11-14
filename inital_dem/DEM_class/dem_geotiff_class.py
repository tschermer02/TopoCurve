import numpy as np
from scipy import signal
from PIL import Image
import math
from photutils.psf import TukeyWindow
from scipy.fft import fft2
from tifffile import TiffFile
from geotiff import GeoTiff

class Dem_Class():
    def __init__(self, tiff_file):
        tif=TiffFile(tiff_file);
        
        
        # Ensure input file is of the right type and contains georeferencing information
        if not tif.is_geotiff:
            raise Exception("Not a geotiff file")
            
        if not tif.geotiff_metadata:
            raise Exception("Metadata missing")
            
        
        # Store projection information               
        self.metadata={'GeogAngularUnitsGeoKey': tif.geotiff_metadata["GeogAngularUnitsGeoKey"],
                       'GeogCitationGeoKey': tif.geotiff_metadata["GeogCitationGeoKey"],
                       'GTCitationGeoKey': tif.geotiff_metadata["GTCitationGeoKey"],
                       'GTModelTypeGeoKey': tif.geotiff_metadata["GTModelTypeGeoKey"],
                       'GTRasterTypeGeoKey': tif.geotiff_metadata["GTRasterTypeGeoKey"],
                       'KeyDirectoryVersion': tif.geotiff_metadata["KeyDirectoryVersion"],
                       'KeyRevision': tif.geotiff_metadata["KeyRevision"],
                       'KeyRevisionMinor': tif.geotiff_metadata["KeyRevisionMinor"],
                       'ModelPixelScale': tif.geotiff_metadata["ModelPixelScale"],
                       'ModelTiepoint': tif.geotiff_metadata["ModelTiepoint"],
                       'ProjectedCSTypeGeoKey': tif.geotiff_metadata["ProjectedCSTypeGeoKey"],
                       'ProjLinearUnitsGeoKey': tif.geotiff_metadata["ProjLinearUnitsGeoKey"],}
        
        crs= tif.geotiff_metadata["ProjectedCSTypeGeoKey"].value
        
        # Pull out array of elevation values and store it as array within the dem class
        gtiff=GeoTiff(tiff_file, crs_code=crs)
        self.z_array = gtiff.read()
        
        # Pull out dimensions of DEM grid
        self.dimx,self.dimy=gtiff.tif_shape
        
        # Assign grid spacing and check to ensure grid spacing is uniform in x and y directions
        dx=tif.geotiff_metadata["ModelPixelScale"]
        
        if abs(dx[1]-dx[0]) <1e-3:
            self.dx_dy=dx[0]
        else:
            raise Exception("WARNING: Grid spacing is not uniform in x and y directions!")
            

    def detrend(self):
        self.Z_detrended = signal.detrend(self.z_array)
        plane = self.z_array-self.Z_detrended
        return self.Z_detrended, plane
    
    def plot(self, input, filename):
        img_array = 255*((input - np.amin(input))/(np.amax(input)- np.amin(input)))
        Image.fromarray(img_array).convert("RGB").save(filename)
    
    def mirror_dem(self):
        self.mirrored_array = []
        top = np.concatenate((np.rot90(self.Z_detrended,2),np.flipud(self.Z_detrended),np.rot90(self.Z_detrended,2)), axis=1)
        middle = np.concatenate((np.fliplr(self.Z_detrended),self.Z_detrended,np.fliplr(self.Z_detrended)), axis=1)
        bottom = np.concatenate((np.rot90(self.Z_detrended,2),np.flipud(self.Z_detrended),np.rot90(self.Z_detrended,2)), axis=1)
        self.mirrored_array  = np.concatenate((top, middle, bottom), axis=0)
        self.dimx_f=len(self.mirrored_array)
        self.dimy_f=len(self.mirrored_array[0])
        return self.dimx_f,self.dimy_f,self.mirrored_array
    
    def padding(self):
        # Finds next power of two
        if self.dimx_f>self.dimy_f:
            a = int(math.log2(self.dimx_f))
            if 2**a == self.dimx_f:
                powerOfTwo= self.dimx_f
            powerOfTwo= 2**(a+1)
        else:
            a = int(math.log2(self.dimy_f))
            if 2**a == self.dimy_f:
                powerOfTwo= self.dimy_f
        powerOfTwo= 2**(a+1)

        # Finds difference in dimention of final array and power of two
        self.pad_x_max = math.ceil((powerOfTwo -self.dimx_f)/2)
        self.pad_x_min = math.floor((powerOfTwo -self.dimx_f)/2)
        self.pad_y_max =math.ceil((powerOfTwo -self.dimy_f)/2)
        self.pad_y_min = math.floor((powerOfTwo -self.dimy_f)/2)

        #pads array
        self.padded_array =np.pad(self.tukey_array, ((self.pad_x_max, self.pad_x_min), (self.pad_y_max, self.pad_y_min)), 'constant', constant_values=(0, 0))
        return self.padded_array
    
    def tukeyWindow(self, alphaIn):
        taper = TukeyWindow(alpha=alphaIn)
        data = taper((len(self.mirrored_array), len(self.mirrored_array[0])))
        self.tukey_array =np.multiply(data, self.mirrored_array)
    
        return self.tukey_array

    def FFT(self):
       fft_array = fft2(self.tukey_array)
       return fft_array

    

  
