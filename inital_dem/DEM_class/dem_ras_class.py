import rasterio as rio
from scipy import signal
import numpy as np
from rasterio.plot import show
import matplotlib.pyplot as plt

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
        
