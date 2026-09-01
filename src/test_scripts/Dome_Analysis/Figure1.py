#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 10:58:56 2026

@author: ntklema
"""
# Import packages
from topocurve import TopoCurve,SpectralFiltering
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import time
import matplotlib.animation as animation
import pickle
from cmcrameri import cm

#%% Import pickles and create dictionary of dome datasets

path="/Users/ntklema/Library/CloudStorage/OneDrive-FortLewisCollege/Research_Projects/Dome Exfoliation/Dome_Exfoliation_2/Python_Dictionaries/"

dome=["Twaine_Harte_West","Twaine_Harte","Stone_Mtn","Rocky_Face","Forty_Acre_Rock","Half_Dome","North_Dome","Sentinal","Lembert_Small",
      "Olmsted_Lower","Olmsted_Upper","Pothole","Puppy","Turtleback"]

dome_name=["Twaine Harte West","Twaine Harte Rock","Stone Mountain","Rocky Face","Forty Acre Rock","Half Dome","North Dome","Sentinal","Lembert",
      "Lower Olmsted","Upper Olmsted","Pothole","Puppy","Turtleback"]

D={}
for i in range(14):
    with open(f"{path}{dome[i]}{".pkl"}", 'rb') as r:
        D[dome_name[i]]=pickle.load(r)
        
    if "Sheet Thic" in D[dome_name[i]]:
        D[dome_name[i]]["Avg"] = D[dome_name[i]].pop("Sheet Thic")
        
# del i,r,path,dome

#%% Dd dictionary attribute from shapefile

index=5
shape_path="/Users/ntklema/Library/CloudStorage/OneDrive-FortLewisCollege/Research_Projects/Dome Exfoliation/Dome_Exfoliation_2/Shapefiles/"

shapefile=f"{shape_path}{dome[index]}{".shp"}"
s_points = gpd.read_file(shapefile)
D[dome_name[index]]["Std"]=s_points["Stdev"].to_numpy()

#%% Make plots of curvature vs low-pass filter cutoff for each dome.

import matplotlib.colors as mcolors

fig, axes = plt.subplots(5, 3, figsize=(10, 11))

axf = axes.flatten()
cmap = cm.lajolla # Or 'plasma', 'jet', etc.
norm = mcolors.Normalize(vmin=0, vmax=50)
for i in range(14):
    
    data=D[dome_name[i]]
    r,c=data["KM_Array"].shape
    for j in range(r):
        axf[i].plot(data["f"],data["KM_Array"][j,:],color=cmap(norm(data["Avg"][j])))
        
        
        
    # axf[i].plot(D[dome_name[i][f]])
    axf[i].set_xlabel('Low-pass filter cutoff (m)')
    axf[i].set_ylabel(r'$K_M$ ($m^{-1}$)')
    axf[i].set_title(dome_name[i])
    axf[i].set_xlim(0,200)
    axf[i].set_ylim(-0.1,0.1)

axf[14].set_visible(False)
# Add an overall main title for the whole figure


plt.tight_layout()
plt.show()
    


#%% Scatter of curvature vs thickness

fig, axes = plt.subplots(5, 3, figsize=(10, 11))

axf = axes.flatten()
cmap = cm.lajolla # Or 'plasma', 'jet', etc.
norm = mcolors.Normalize(vmin=0, vmax=50)
for i in range(14):
    
    data=D[dome_name[i]]
    r,c=data["KM_Array"].shape
    medians=np.nanmedian(data["KM_Array"],axis=1)
        
    axf[i].scatter(data["Avg"],medians)
    axf[i].set_xlabel('Low-pass filter cutoff (m)')
    axf[i].set_ylabel(r'$K_M$ ($m^{-1}$)')
    axf[i].set_title(dome_name[i])
    axf[i].set_xlim(0,150)
    axf[i].set_ylim(-0.02,0.02)

axf[14].set_visible(False)
# Add an overall main title for the whole figure


plt.tight_layout()
plt.show()
    

#%%




fig, axes = plt.subplots(2, 3, figsize=(10, 6))

axf = axes.flatten()
cmap = cm.lajolla # Or 'plasma', 'jet', etc.

# Twaine Harte Plots
axf[0].scatter(D["Twaine Harte West"]["Avg"],np.nanmedian(D["Twaine Harte West"]["KM_Array"],axis=1))
axf[0].scatter(D["Twaine Harte Rock"]["Avg"],np.nanmedian(D["Twaine Harte Rock"]["KM_Array"],axis=1))
axf[0].plot([17.2,17.2],[-0.005,0.02])
axf[0].set_xlim(0,150)
axf[0].set_ylim(-0.005,0.02)
axf[0].set_xlabel('Slab thickness (cm)')
axf[0].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[0].set_title("Foothills CA")

# Stone Mtn
axf[1].scatter(D["Stone Mountain"]["Avg"],np.nanmedian(D["Stone Mountain"]["KM_Array"],axis=1))
axf[1].set_xlim(0,150)
axf[1].set_ylim(-0.005,0.02)
axf[1].set_xlabel('Slab thickness (cm)')
axf[1].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[1].set_title("Escarpment NC")

# Rocky Face
axf[2].scatter(D["Rocky Face"]["Avg"],np.nanmedian(D["Rocky Face"]["KM_Array"],axis=1))
axf[2].set_xlim(0,150)
axf[2].set_ylim(-0.005,0.02)
axf[2].set_xlabel('Slab thickness (cm)')
axf[2].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[2].set_title("Foothills NC")

# Forty Acre Rock
axf[3].scatter(D["Forty Acre Rock"]["Avg"],np.nanmedian(D["Forty Acre Rock"]["KM_Array"],axis=1))
axf[3].set_xlim(0,150)
axf[3].set_ylim(-0.005,0.02)
axf[3].set_xlabel('Slab thickness (cm)')
axf[3].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[3].set_title("Piedmont SC")


# Yosemite Unglaciated
axf[4].scatter(D["Half Dome"]["Avg"],np.nanmedian(D["Half Dome"]["KM_Array"],axis=1))
axf[4].scatter(D["North Dome"]["Avg"],np.nanmedian(D["North Dome"]["KM_Array"],axis=1))
axf[4].scatter(D["Sentinal"]["Avg"],np.nanmedian(D["Sentinal"]["KM_Array"],axis=1))
axf[4].set_xlim(0,150)
axf[4].set_ylim(-0.005,0.02)
axf[4].set_xlabel('Slab thickness (cm)')
axf[4].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[4].set_title("Yosemite (unglaciated)")

# Yosemite glaciated
axf[5].scatter(D["Lembert"]["Avg"],np.nanmedian(D["Lembert"]["KM_Array"],axis=1))
axf[5].scatter(D["Lower Olmsted"]["Avg"],np.nanmedian(D["Lower Olmsted"]["KM_Array"],axis=1))
axf[5].scatter(D["Upper Olmsted"]["Avg"],np.nanmedian(D["Upper Olmsted"]["KM_Array"],axis=1))
axf[5].scatter(D["Puppy"]["Avg"],np.nanmedian(D["Puppy"]["KM_Array"],axis=1))
axf[5].scatter(D["Pothole"]["Avg"],np.nanmedian(D["Pothole"]["KM_Array"],axis=1))
axf[5].scatter(D["Turtleback"]["Avg"],np.nanmedian(D["Turtleback"]["KM_Array"],axis=1))
axf[5].set_xlim(0,150)
axf[5].set_ylim(-0.005,0.02)
axf[5].set_xlabel('Slab thickness (cm)')
axf[5].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[5].set_title("Yosemite (glaciated)")

plt.tight_layout()
plt.show()


#%%
# import seaborn as sns
import pandas as pd
from scipy.stats import gaussian_kde

df=pd.DataFrame({"Avg": D["Pothole"]["Avg"]})

cleaned_data = df["Avg"].dropna()
kde = gaussian_kde(cleaned_data)
x_grid = np.linspace(0, 150, 200)
density = kde(x_grid)
plt.plot(x_grid,density)
plt.plot([20.3,20.3],[0, 0.016])


#%%
sd=0.2
z=np.linspace(0,50,100)
s=sd/z*np.sqrt(1-2*np.exp(-z/sd)*np.cos(z/sd)+np.exp(-2*z/sd))
plt.plot(z,s)




