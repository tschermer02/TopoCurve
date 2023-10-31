import numpy as np
from scipy import signal
from PIL import Image

class Dem_Class():
    def __init__(self, array, dimx, dimy):
        z_array = array
        self.z_array = z_array
        self.dimx= dimx
        self.dimy = dimy

    def dx_dy(self):
        dx = abs(self.z_array[(0,0)]-self.z_array[(0,1)])
        dy = abs(self.z_array[(0,0)]-self.z_array[(1,0)])
        return dx,dy

    def detrend(self):
        self.Z_detrended = signal.detrend(self.z_array)
        plane = self.z_array-self.Z_detrended
        return self.Z_detrended, plane
    
    def plot(self, input, filename):
        img_array = 255*((input - np.amin(input))/(np.amax(input)- np.amin(input)))
        Image.fromarray(img_array).convert("RGB").save(filename)
    
    def mirror_dem(self):
        f_array = []
        top = np.concatenate((np.rot90(self.Z_detrended,2),np.flipud(self.Z_detrended),np.rot90(self.Z_detrended,2)), axis=1)
        middle = np.concatenate((np.fliplr(self.Z_detrended),self.Z_detrended,np.fliplr(self.Z_detrended)), axis=1)
        bottom = np.concatenate((np.rot90(self.Z_detrended,2),np.flipud(self.Z_detrended),np.rot90(self.Z_detrended,2)), axis=1)
        f_array = np.concatenate((top, middle, bottom), axis=0)
        return f_array

