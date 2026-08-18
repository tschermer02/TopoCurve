#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nate Klema - 6/23/26

Curvature analysis of exfoliation domes in NC, SC, and CA 

Inputs: 
    DEM raster
    Polygon shapefile with region of interest (clip of dome)
    Shapefile with sample points
"""

# Import packages
from topocurve import TopoCurve,SpectralFiltering
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import time
import matplotlib.animation as animation


#%% ---------------- Import datasets ---------------------
tiff_file = "/Users/ntklema/Library/CloudStorage/OneDrive-FortLewisCollege/Research_Projects/Dome Exfoliation/Yosemite/Clipped_Rasters/Pothole.tif"

shapefile="/Users/ntklema/Library/CloudStorage/OneDrive-FortLewisCollege/Research_Projects/Dome Exfoliation/Yosemite/Shapefiles/Pothole.shp"
s_points = gpd.read_file(shapefile)
x = np.array(s_points.geometry.x)

# Instantiate TopoCurve object
dem = TopoCurve(tiff_file=tiff_file)

# Instantiate SpectralFiltering object
spectral_filter = SpectralFiltering(tiff_file)


#%% Build filter 
ns=200
df=1
KM = np.full((len(x),ns), np.nan)
F=np.array([1,6])
f=np.full(ns,np.nan)

start_time = time.perf_counter()  # Record start time
for i in range(ns):
    dx, dy, filtered_elevation = spectral_filter.FFT(F, 'lowpass', 0)
    K = dem.CurveCalc(filtered_elevation, dx, dy, 0)
    Att,X,Y=dem.TopoCurve_Sample(shapefile,K[6],shapefile_attributes=["Sheet Thic"])
    
    KM[:,i]=Att["KM"]
    f[i]=F[1]
    F=F+df
    it_time = time.perf_counter()    # Record end time
    elapsed = it_time - start_time
    print(f"Iteration: {i+1} of {ns}")
    print(f"Elapsed time: {elapsed:0.0f} seconds\n")

Att['f']=f
Att['KM_Array']=KM
#%%
# for i in range(len(x)):
#     plt.plot(f,((KM[i,:])),color='k',linewidth=0.5)
    
plt.plot(f,(np.median((KM),axis=0)),color='r')
plt.show()
#%%
plt.scatter(Att['Sheet Thic'],np.median(KM,axis=1))

#%%

x_a=Att['Sheet Thic']
y_a=KM
fig, ax = plt.subplots()
scat = ax.scatter(x_a,y_a[:, 0])
plt.axhline(0,color='k',linewidth=0.5)
ax.set_xlim(0,100)
ax.set_ylim(-0.05,0.05)

def update(frame):
    scat.set_offsets(np.c_[x_a, y_a[:, frame]])
    return scat,

ani = animation.FuncAnimation(fig, update, frames=ns, interval=1, blit=True)

# Save as gif (no extra install needed)
# ani.save('scatter.gif', writer='pillow', fps=1)

# Or save as mp4 (requires: brew install ffmpeg)
ani.save('/Users/ntklema/Library/CloudStorage/OneDrive-FortLewisCollege/Research_Projects/Dome Exfoliation/Dome_Exfoliation_2/Animations/Pothole_0to200.mp4', writer='ffmpeg', fps=6)

plt.show()

#%% Save dictionary

import pickle

with open('/Users/ntklema/Library/CloudStorage/OneDrive-FortLewisCollege/Research_Projects/Dome Exfoliation/Dome_Exfoliation_2/Python_Dictionaries/Pothole.pkl', 'wb') as r:
    pickle.dump(Att, r)


