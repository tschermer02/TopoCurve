import rasterio as rio
from scipy import signal

class Dem_Ras_Class():
    def __init__(self, dem_path):
        dem = rio.open(dem_path)
        self.z_array = dem.read().astype('float64')


    def dimx_dimy(self):
        dim_x =  self.z_array.shape[1]
        dim_y =  self.z_array.shape[2]
        return dim_x, dim_y


    def dx_dy(self):
        dx = abs(self.z_array[0][0][0] -self.z_array[0][0][1])
        dy = abs(self.z_array[0][0][0] -self.z_array[0][1][0])
        return dx,dy


    def detrend(self):
        Z_detrended = signal.detrend(self.z_array)
        plane = self.z_array-Z_detrended
        return Z_detrended, plane