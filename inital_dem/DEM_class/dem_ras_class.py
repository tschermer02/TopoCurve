import rasterio as rio
from scipy import signal
import numpy as np
from rasterio.plot import show
import matplotlib.pyplot as plt
import math
from scipy.fft import fft, fftshift
from photutils.psf import TukeyWindow

class Dem_Ras_Class():
    def __init__(self, dem_path):
        dem = rio.open(dem_path)
        self.z_array = dem.read(1).astype('float64')


    def dimx_dimy(self):
        dim_x =  self.z_array.shape[0]
        dim_y =  self.z_array.shape[1]
        return dim_x, dim_y


    def dx_dy(self):
        dx = abs(self.z_array[0][0] -self.z_array[0][1])
        dy = abs(self.z_array[0][0] -self.z_array[1][0])
        return dx,dy


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
        dim_x =  len(input)
        dim_y =  len(input[0])
        
        if(dim_x > dim_y):
            N = dim_x
            a = int(math.log2(N))
            if 2**a == N:
                self.power_of2 = N
            self.power_of2 = 2**(a + 1)
        
        if(dim_x < dim_y):
            N = dim_y
            a = int(math.log2(N))
            if 2**a == N:
                self.power_of2 = N
            self.power_of2 = 2**(a + 1)

        pad_x_max = math.ceil((self.power_of2 - dim_x)/2)
        pad_x_min = math.floor((self.power_of2 - dim_x)/2)
        pad_y_max = math.ceil((self.power_of2 - dim_y)/2)
        pad_y_min = math.floor((self.power_of2 - dim_y)/2)

        self.array = np.pad(input,((pad_x_max, pad_x_min), (pad_y_max, pad_y_min)), 'constant', constant_values= (0,0))
        return self.array
        

    def tukey_window(self, input):
        length = len(input)
        taper = TukeyWindow(alpha=0.5)
        data = taper((length, length))
        return data * input


        
        




