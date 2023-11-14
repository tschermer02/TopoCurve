import numpy as np
from scipy import signal
from PIL import Image
import math
from photutils.psf import TukeyWindow
from scipy.fft import fft2, ifft2
from tifffile import TiffFile
from geotiff import GeoTiff

class Dem_Class():
    def __init__(self, tiff_file):
        tif=TiffFile(tiff_file)
        
        
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
        self.dx=tif.geotiff_metadata["ModelPixelScale"]
        
        if abs(self.dx[1]-self.dx[0]) <1e-3:
            self.dx_dy=self.dx[0]
        else:
            raise Exception("WARNING: Grid spacing is not uniform in x and y directions!")
        
            

    def detrend(self):
        Z_detrended = signal.detrend(self.z_array)
        plane = self.z_array-Z_detrended
        return Z_detrended, plane
    
    def plot(self, input, filename):
        img_array = 255*((input - np.amin(input))/(np.amax(input)- np.amin(input)))
        Image.fromarray(img_array).convert("RGB").save(filename)
    
    def mirror_dem(self):
        detrend, plane = self.detrend()
        mirrored_array = []
        top = np.concatenate((np.rot90(detrend,2),np.flipud(detrend),np.rot90(detrend,2)), axis=1)
        middle = np.concatenate((np.fliplr(detrend),detrend,np.fliplr(detrend)), axis=1)
        bottom = np.concatenate((np.rot90(detrend,2),np.flipud(detrend),np.rot90(detrend,2)), axis=1)
        mirrored_array  = np.concatenate((top, middle, bottom), axis=0)
        self.dimx_ma=len(mirrored_array)
        self.dimy_ma=len(mirrored_array[0])
        return mirrored_array
    
    def tukeyWindow(self, alphaIn):
        mirrored_array = self.mirror_dem()
        taper = TukeyWindow(alpha=alphaIn)
        data = taper((len(mirrored_array), len(mirrored_array[0])))
        tukey_array =np.multiply(data, mirrored_array)
    
        return tukey_array

    def padding(self, alphaIn):
        # Finds next power of two
        tukey_array = self.tukeyWindow(alphaIn)
        if self.dimx_ma>self.dimy_ma:
            a = int(math.log2(self.dimx_ma))
            if 2**a == self.dimx_ma:
                self.powerOfTwo= self.dimx_ma
            self.powerOfTwo= 2**(a+1)
        else:
            a = int(math.log2(self.dimy_ma))
            if 2**a == self.dimy_ma:
                self.powerOfTwo= self.dimy_ma
        self.powerOfTwo= 2**(a+1)

        # Finds difference in dimention of final array and power of two
        pad_x_max = math.ceil((self.powerOfTwo -self.dimx_ma)/2)
        pad_x_min = math.floor((self.powerOfTwo -self.dimx_ma)/2)
        pad_y_max =math.ceil((self.powerOfTwo -self.dimy_ma)/2)
        pad_y_min = math.floor((self.powerOfTwo -self.dimy_ma)/2)

        #pads array
        padded_window_array =np.pad(tukey_array, ((pad_x_max, pad_x_min), (pad_y_max, pad_y_min)), 'constant', constant_values=(0, 0))
        return padded_window_array

    def FFT(self, filter, filterType, alphaIn):
        padded_window_array= self.padding(alphaIn)
        #Doing fft on the windowed and padded array
        fft_array = fft2(padded_window_array)


        dkx = 1/(self.dx*self.powerOfTwo)
        dky = 1/(self.dx*self.powerOfTwo)
       
        xc = self.powerOfTwo/2+1; yc = self.powerOfTwo/2+1 #matrix indices of zero wavenumber
        [cols, rows] = np.meshgrid(self.powerOfTwo,self.powerOfTwo) #matrices of column and row indices
        km = math.sqrt(np.square(dky*(rows-yc)) + np.square(dkx*(cols-xc))) #matrix of radial wavenumbers

        match filterType:
            case 'lowpass':
                kfilt=np.divide(np.ones_like(filter),filter)
                sigma=abs(kfilt(1)-kfilt(0))/3
                F=math.exp(-np.square(km-kfilt(0))/(2*sigma^2))
                F[km<kfilt(1)]=1

            case 'highpass':
                kfilt=np.divide(np.ones_like(filter),filter)
                sigma=abs(kfilt(1)-kfilt(0))/3
                F=math.exp(-np.square(km-kfilt(1))/(2*sigma^2))
                F[km>=kfilt(1)]=1

        ZMWF = np.real(ifft2(np.multiply(fft_array,F)))
       

        return ZMWF

    

  
