import numpy as np
from scipy import signal

class Dem_Class():
    def __init__(self, z_array, dimx, dimy):
        self.z_array = z_array
        self.dimx= dimx
        self.dimy = dimy

    def dx_dy(self):
        dx = abs(self.z_array[(0,0)]-self.z_array[(0,1)])
        dy = abs(self.z_array[(0,0)]-self.z_array[(1,0)])
        return dx,dy

    def detrend(self):
        Z_detrended = signal.detrend(self.z_array)
        plane = self.z_array-Z_detrended
        return Z_detrended, plane
