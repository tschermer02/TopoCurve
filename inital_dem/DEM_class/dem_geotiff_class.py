import numpy as np
from scipy import signal
from PIL import Image
import math
from photutils.psf import TukeyWindow



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
        pad_x_max = math.ceil((powerOfTwo -self.dimx_f)/2)
        pad_x_min = math.floor((powerOfTwo -self.dimx_f)/2)
        pad_y_max =math.ceil((powerOfTwo -self.dimy_f)/2)
        pad_y_min = math.floor((powerOfTwo -self.dimy_f)/2)

        #pads array
        self.padded_array =np.pad(self.mirrored_array, ((pad_x_max, pad_x_min), (pad_y_max, pad_y_min)), 'constant', constant_values=(0, 0))
        return self.padded_array
    
    def tukeyWindow(self):
        taper = TukeyWindow(alpha=1)
        data = taper((len(self.padded_array), len(self.padded_array)))
        newArray =np.multiply(data, self.padded_array)
    
        return newArray

    

  
