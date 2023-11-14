import rasterio as rio
from scipy import signal
import numpy as np
from rasterio.plot import show
import matplotlib.pyplot as plt
import math
from scipy.fft import fft, fftshift
from photutils.psf import TukeyWindow
from tifffile import TiffFile

class Dem_Ras_Class():
    def __init__(self, dem_path):
        
        tif=TiffFile(dem_path);
        
        
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
        
        
        # Pull out array of elevation values and store it as array within the dem class
        dem = rio.open(dem_path)
        self.z_array = dem.read(1).astype('float64')
        
        # Pull out dimensions of DEM grid
        self.dimx=dem.width
        self.dimy=dem.height
        
        # Assign grid spacing and check to ensure grid spacing is uniform in x and y directions
        dx=tif.geotiff_metadata["ModelPixelScale"]
        
        if abs(dx[1]-dx[0]) <1e-3:
            self.dx_dy=dx[0]
        else:
            raise Exception("WARNING: Grid spacing is not uniform in x and y directions!")
      

    def detrended(self):
        self.detrend = signal.detrend(self.z_array)
        plane = self.z_array-self.detrend
        return self.detrend, plane
    
    def plot_func(self, input):
        fig, ax = plt.subplots(1, figsize = (12,12))
        show(input, cmap='Greys_r', ax=ax)
        plt.axis("off")
        plt.show()

    def mirror_array(self):
        top = np.concatenate((np.rot90(self.detrend,2), np.flipud(self.detrend), np.rot90(self.detrend,2)), axis = 1)
        mid = np.concatenate((np.fliplr(self.detrend), self.detrend, np.fliplr(self.detrend)), axis =1)
        bot = np.concatenate((np.rot90(self.detrend,2), np.flipud(self.detrend), np.rot90(self.detrend,2)), axis =1)

        Zm = np.concatenate((top, mid, bot), axis=0)
        return Zm


    def padding_array(self, input):
        x_dim =  len(input)
        y_dim =  len(input[0])
        
        if(x_dim > y_dim):
            N = x_dim
            a = int(math.log2(N))
            if 2**a == N:
                self.power_of2 = N
            self.power_of2 = 2**(a + 1)
        
        if(x_dim < y_dim):
            N = y_dim
            a = int(math.log2(N))
            if 2**a == N:
                self.power_of2 = N
            self.power_of2 = 2**(a + 1)

        self.pad_x_max = math.ceil((self.power_of2 - x_dim)/2)
        self.pad_x_min = math.floor((self.power_of2 - x_dim)/2)
        self.pad_y_max = math.ceil((self.power_of2 - y_dim)/2)
        self.pad_y_min = math.floor((self.power_of2 - y_dim)/2)

        self.array = np.pad(input,((self.pad_x_max, self.pad_x_min), (self.pad_y_max, self.pad_y_min)), 'constant', constant_values= (0,0))
        return self.array
        

    def tukey_window(self, input):
        length = len(input)
        width = len(input[0])
        taper = TukeyWindow(alpha=0.5)
        data = taper((length, width))
        output = data * input
        self.dim_x =  self.z_array.shape[0]
        self.dim_y =  self.z_array.shape[1]
        
        # this commented code will cut out the origanal size after the tukey window is applied..
        #output[(self.pad_x_max + self.dim_x): -(self.pad_x_max + self.dim_x),(self.pad_y_max + self.dim_y): -(self.pad_y_max + self.dim_y)]

        return output
    
    def fftf_2d(self, input):
        # https://docs.scipy.org/doc/scipy/tutorial/fft.html#and-n-d-discrete-fourier-transforms
