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
    

#%%  CStter of Curvature vs thickness for location groupings


fig, axes = plt.subplots(2, 3, figsize=(10, 6))

axf = axes.flatten()
cmap = cm.lajolla # Or 'plasma', 'jet', etc.

# Twaine Harte Plots
axf[3].scatter(D["Twaine Harte West"]["Avg"],np.nanmean(D["Twaine Harte West"]["KM_Array"],axis=1))
axf[3].scatter(D["Twaine Harte Rock"]["Avg"],np.nanmean(D["Twaine Harte Rock"]["KM_Array"],axis=1))
axf[3].plot([17.2,17.2],[-0.005,0.02])
axf[3].set_xlim(0,150)
axf[3].set_ylim(-0.01,0.02)
axf[3].set_xlabel('Slab thickness (cm)')
axf[3].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[3].set_title("Foothills CA")

# Stone Mtn
axf[2].scatter(D["Stone Mountain"]["Avg"],np.nanmean(D["Stone Mountain"]["KM_Array"],axis=1))
axf[2].set_xlim(0,150)
axf[2].set_ylim(-0.01,0.022)
axf[2].set_xlabel('Slab thickness (cm)')
axf[2].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[2].set_title("Escarpment NC")

# Rocky Face
axf[1].scatter(D["Rocky Face"]["Avg"],np.nanmean(D["Rocky Face"]["KM_Array"],axis=1))
axf[1].set_xlim(0,150)
axf[1].set_ylim(-0.01,0.022)
axf[1].set_xlabel('Slab thickness (cm)')
axf[1].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[1].set_title("Foothills NC")

# Forty Acre Rock
axf[0].scatter(D["Forty Acre Rock"]["Avg"],np.nanmean(D["Forty Acre Rock"]["KM_Array"],axis=1))
axf[0].set_xlim(0,150)
axf[0].set_ylim(-0.01,0.022)
axf[0].set_xlabel('Slab thickness (cm)')
axf[0].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[0].set_title("Piedmont SC")


# Yosemite Unglaciated
axf[5].scatter(D["Half Dome"]["Avg"],np.nanmean(D["Half Dome"]["KM_Array"],axis=1))
axf[5].scatter(D["North Dome"]["Avg"],np.nanmean(D["North Dome"]["KM_Array"],axis=1))
axf[5].scatter(D["Sentinal"]["Avg"],np.nanmean(D["Sentinal"]["KM_Array"],axis=1))
axf[5].set_xlim(0,150)
axf[5].set_ylim(-0.01,0.022)
axf[5].set_xlabel('Slab thickness (cm)')
axf[5].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[5].set_title("Yosemite (unglaciated)")

# Yosemite glaciated
axf[4].scatter(D["Lembert"]["Avg"],np.nanmean(D["Lembert"]["KM_Array"],axis=1))
axf[4].scatter(D["Lower Olmsted"]["Avg"],np.nanmean(D["Lower Olmsted"]["KM_Array"],axis=1))
axf[4].scatter(D["Upper Olmsted"]["Avg"],np.nanmean(D["Upper Olmsted"]["KM_Array"],axis=1))
axf[4].scatter(D["Puppy"]["Avg"],np.nanmean(D["Puppy"]["KM_Array"],axis=1))
axf[4].scatter(D["Pothole"]["Avg"],np.nanmean(D["Pothole"]["KM_Array"],axis=1))
axf[4].scatter(D["Turtleback"]["Avg"],np.nanmean (D["Turtleback"]["KM_Array"],axis=1))
axf[4].set_xlim(0,150)
axf[4].set_ylim(-0.01,0.022)
axf[4].set_xlabel('Slab thickness (cm)')
axf[4].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[4].set_title("Yosemite (glaciated)")

plt.tight_layout()
plt.show()


#%% KDE plots of curvature
# import seaborn as sns
import pandas as pd
from scipy.stats import gaussian_kde
fig, axes = plt.subplots(2, 3, figsize=(10, 5))
axf = axes.flatten()

x_grid = np.linspace(-5e-2, 5e-2, 200)

# Forty Acre Rock
kmfa=D["Forty Acre Rock"]["KM_Array"]
fa1=pd.DataFrame({"KMFA1": kmfa[:,0:19].flatten()})
fa1 = fa1["KMFA1"].dropna()
kde_fa1 = gaussian_kde(fa1)
KDEFA1 = kde_fa1(x_grid)

fa2=pd.DataFrame({"KMFA2": kmfa[:,20:44].flatten()})
fa2 = fa2["KMFA2"].dropna()
kde_fa2 = gaussian_kde(fa2)
KDEFA2 = kde_fa2(x_grid)

fa3=pd.DataFrame({"KMFA3": kmfa[:,45:69].flatten()})
fa3 = fa3["KMFA3"].dropna()
kde_fa3 = gaussian_kde(fa3)
KDEFA3 = kde_fa3(x_grid)

fa4=pd.DataFrame({"KMFA4": kmfa[:,70:94].flatten()})
fa4 = fa4["KMFA4"].dropna()
kde_fa4 = gaussian_kde(fa4)
KDEFA4 = kde_fa4(x_grid)

fa5=pd.DataFrame({"KMFA5": kmfa[:,95:200].flatten()})
fa5 = fa5["KMFA5"].dropna()
kde_fa5 = gaussian_kde(fa5)
KDEFA5 = kde_fa5(x_grid)

# Rocky Face
kmrf=D["Rocky Face"]["KM_Array"]
rf1=pd.DataFrame({"KMRF1": kmrf[:,0:19].flatten()})
rf1 = rf1["KMRF1"].dropna()
kde_rf1 = gaussian_kde(rf1)
KDERF1 = kde_rf1(x_grid)

rf2=pd.DataFrame({"KMRF2": kmrf[:,20:44].flatten()})
rf2 = rf2["KMRF2"].dropna()
kde_rf2 = gaussian_kde(rf2)
KDERF2 = kde_rf2(x_grid)

rf3=pd.DataFrame({"KMRF3": kmrf[:,45:69].flatten()})
rf3 = rf3["KMRF3"].dropna()
kde_rf3 = gaussian_kde(rf3)
KDERF3 = kde_rf3(x_grid)

rf4=pd.DataFrame({"KMRF4": kmrf[:,70:94].flatten()})
rf4 = rf4["KMRF4"].dropna()
kde_rf4 = gaussian_kde(rf4)
KDERF4 = kde_rf4(x_grid)

rf5=pd.DataFrame({"KMrf5": kmrf[:,95:200].flatten()})
rf5 = rf5["KMrf5"].dropna()
kde_rf5 = gaussian_kde(rf5)
KDErf5 = kde_rf5(x_grid)

# Stone Mountain
kmsm=D["Stone Mountain"]["KM_Array"]
sm1=pd.DataFrame({"kmsm1": kmsm[:,0:19].flatten()})
sm1 = sm1["kmsm1"].dropna()
kde_sm1 = gaussian_kde(sm1)
KDEsm1 = kde_sm1(x_grid)

sm2=pd.DataFrame({"kmsm2": kmsm[:,20:44].flatten()})
sm2 = sm2["kmsm2"].dropna()
kde_sm2 = gaussian_kde(sm2)
KDEsm2 = kde_sm2(x_grid)

sm3=pd.DataFrame({"kmsm3": kmsm[:,45:69].flatten()})
sm3 = sm3["kmsm3"].dropna()
kde_sm3 = gaussian_kde(sm3)
KDEsm3 = kde_sm3(x_grid)

sm4=pd.DataFrame({"kmsm4": kmsm[:,70:94].flatten()})
sm4 = sm4["kmsm4"].dropna()
kde_sm4 = gaussian_kde(sm4)
KDEsm4 = kde_sm4(x_grid)

sm5=pd.DataFrame({"KMsm5": kmsm[:,95:200].flatten()})
sm5 = sm5["KMsm5"].dropna()
kde_sm5 = gaussian_kde(sm5)
KDEsm5 = kde_sm5(x_grid)

# Twaine Harte
kmth=np.vstack((D["Twaine Harte West"]["KM_Array"],D["Twaine Harte Rock"]["KM_Array"]))
th1=pd.DataFrame({"kmth1": kmth[:,0:19].flatten()})
th1 = th1["kmth1"].dropna()
kde_th1 = gaussian_kde(th1)
KDEth1 = kde_th1(x_grid)

th2=pd.DataFrame({"kmth2": kmth[:,20:44].flatten()})
th2 = th2["kmth2"].dropna()
kde_th2 = gaussian_kde(th2)
KDEth2 = kde_th2(x_grid)

th3=pd.DataFrame({"kmth3": kmth[:,45:69].flatten()})
th3 = th3["kmth3"].dropna()
kde_th3 = gaussian_kde(th3)
KDEth3 = kde_th3(x_grid)

th4=pd.DataFrame({"kmth4": kmth[:,70:94].flatten()})
th4 = th4["kmth4"].dropna()
kde_th4 = gaussian_kde(th4)
KDEth4 = kde_th4(x_grid)

th5=pd.DataFrame({"KMth5": kmth[:,95:200].flatten()})
th5 = th5["KMth5"].dropna()
kde_th5 = gaussian_kde(th5)
KDEth5 = kde_th5(x_grid)

# Yosemite (unglaciated)
kmyu=np.vstack((D["Half Dome"]["KM_Array"],D["North Dome"]["KM_Array"],D["Sentinal"]["KM_Array"]))
yu1=pd.DataFrame({"kmyu1": kmyu[:,0:19].flatten()})
yu1 = yu1["kmyu1"].dropna()
kde_yu1 = gaussian_kde(yu1)
KDEyu1 = kde_yu1(x_grid)

yu2=pd.DataFrame({"kmyu2": kmyu[:,20:44].flatten()})
yu2 = yu2["kmyu2"].dropna()
kde_yu2 = gaussian_kde(yu2)
KDEyu2 = kde_yu2(x_grid)

yu3=pd.DataFrame({"kmyu3": kmyu[:,45:69].flatten()})
yu3 = yu3["kmyu3"].dropna()
kde_yu3 = gaussian_kde(yu3)
KDEyu3 = kde_yu3(x_grid)

yu4=pd.DataFrame({"kmyu4": kmyu[:,70:94].flatten()})
yu4 = yu4["kmyu4"].dropna()
kde_yu4 = gaussian_kde(yu4)
KDEyu4 = kde_yu4(x_grid)

yu5=pd.DataFrame({"KMyu5": kmyu[:,95:200].flatten()})
yu5 = yu5["KMyu5"].dropna()
kde_yu5 = gaussian_kde(yu5)
KDEyu5 = kde_yu5(x_grid)

# Yosemite (glaciated)

kmyg=np.vstack((D["Lembert"]["KM_Array"],D["Lower Olmsted"]["KM_Array"],D["Upper Olmsted"]["KM_Array"],D["Pothole"]["KM_Array"],
                D["Puppy"]["KM_Array"],D["Turtleback"]["KM_Array"]))
yg1=pd.DataFrame({"kmyg1": kmyg[:,0:19].flatten()})
yg1 = yg1["kmyg1"].dropna()
kde_yg1 = gaussian_kde(yg1)
KDEyg1 = kde_yg1(x_grid)

yg2=pd.DataFrame({"kmyg2": kmyg[:,20:44].flatten()})
yg2 = yg2["kmyg2"].dropna()
kde_yg2 = gaussian_kde(yg2)
KDEyg2 = kde_yg2(x_grid)

yg3=pd.DataFrame({"kmyg3": kmyg[:,45:69].flatten()})
yg3 = yg3["kmyg3"].dropna()
kde_yg3 = gaussian_kde(yg3)
KDEyg3 = kde_yg3(x_grid)

yg4=pd.DataFrame({"kmyg4": kmyg[:,70:94].flatten()})
yg4 = yg4["kmyg4"].dropna()
kde_yg4 = gaussian_kde(yg4)
KDEyg4 = kde_yg4(x_grid)

yg5=pd.DataFrame({"KMyg5": kmyg[:,95:200].flatten()})
yg5 = yg5["KMyg5"].dropna()
kde_yg5 = gaussian_kde(yg5)
KDEyg5 = kde_yg5(x_grid)


cmap = ["brown","purple","navy","black","teal","cyan"]
lw=2
a=0

axf[0].fill_between(x_grid,KDEFA1,color=cmap[0],alpha=a,label="Piedmont SC")
axf[0].plot(x_grid,KDEFA1,color=cmap[0],linewidth=lw)

axf[0].fill_between(x_grid,KDERF1,color=cmap[1],alpha=a,label="Foothills NC")
axf[0].plot(x_grid,KDERF1,color=cmap[1],linewidth=lw)

axf[0].fill_between(x_grid,KDEsm1,color=cmap[2],alpha=a,label="Escarpment NC")
axf[0].plot(x_grid,KDEsm1,color=cmap[2],linewidth=lw)

axf[0].fill_between(x_grid,KDEth1,color=cmap[3],alpha=a,label="Foothills CA")
axf[0].plot(x_grid,KDEth1,color=cmap[3],linewidth=lw)


axf[0].fill_between(x_grid,KDEyu1,color=cmap[4],alpha=a,label="Yosemite (unglaciated)")
axf[0].plot(x_grid,KDEyu1,color=cmap[4],linewidth=lw)

axf[0].fill_between(x_grid,KDEyg1,color=cmap[5],alpha=a,label="Yosemite (glaciated)")
axf[0].plot(x_grid,KDEyg1,color=cmap[5],linewidth=lw)
axf[0].set_xlim(np.min(x_grid),np.max(x_grid))
# axf[0].set_ylim(0,40)
axf[0].set_xlabel(r"$K_M$ $(m^{-1})$")
axf[0].set_ylabel(r"Density ($m$)")
axf[0].set_title(r"$0$ m $<$ $\lambda$ $\leq$ $25$ m ")

# axf[0].legend()


axf[1].fill_between(x_grid,KDEFA2,color=cmap[0],alpha=a,label="Piedmont SC")
axf[1].plot(x_grid,KDEFA2,color=cmap[0],linewidth=lw)

axf[1].fill_between(x_grid,KDERF2,color=cmap[1],alpha=a,label="Foothills NC")
axf[1].plot(x_grid,KDERF2,color=cmap[1],linewidth=lw)

axf[1].fill_between(x_grid,KDEsm2,color=cmap[2],alpha=a,label="Escarpment NC")
axf[1].plot(x_grid,KDEsm2,color=cmap[2],linewidth=lw)

axf[1].fill_between(x_grid,KDEth2,color=cmap[3],alpha=a,label="Foothills CA")
axf[1].plot(x_grid,KDEth2,color=cmap[3],linewidth=lw)


axf[1].fill_between(x_grid,KDEyu2,color=cmap[4],alpha=a,label="Yosemite (unglaciated)")
axf[1].plot(x_grid,KDEyu2,color=cmap[4],linewidth=lw)

axf[1].fill_between(x_grid,KDEyg2,color=cmap[5],alpha=a,label="Yosemite (glaciated)")
axf[1].plot(x_grid,KDEyg2,color=cmap[5],linewidth=lw)
axf[1].set_xlim(np.min(x_grid),np.max(x_grid))
axf[1].set_xlabel(r"$K_M$ $(m^{-1})$")
axf[1].set_ylabel(r"Density ($m$)")
axf[1].set_title(r"$25$ m $<$ $\lambda$ $\leq$ $50$ m ")
# axf[1].set_ylim(1,100)


axf[2].fill_between(x_grid,KDEFA3,color=cmap[0],alpha=a,label="Piedmont SC")
axf[2].plot(x_grid,KDEFA2,color=cmap[0],linewidth=lw)

axf[2].fill_between(x_grid,KDERF3,color=cmap[1],alpha=a,label="Foothills NC")
axf[2].plot(x_grid,KDERF3,color=cmap[1],linewidth=lw)

axf[2].fill_between(x_grid,KDEsm3,color=cmap[2],alpha=a,label="Escarpment NC")
axf[2].plot(x_grid,KDEsm3,color=cmap[2],linewidth=lw)

axf[2].fill_between(x_grid,KDEth3,color=cmap[3],alpha=a,label="Foothills CA")
axf[2].plot(x_grid,KDEth3,color=cmap[3],linewidth=lw)


axf[2].fill_between(x_grid,KDEyu3,color=cmap[4],alpha=a,label="Yosemite (unglaciated)")
axf[2].plot(x_grid,KDEyu3,color=cmap[4],linewidth=lw)

axf[2].fill_between(x_grid,KDEyg3,color=cmap[5],alpha=a,label="Yosemite (glaciated)")
axf[2].plot(x_grid,KDEyg3,color=cmap[5],linewidth=lw)
axf[2].set_xlim(np.min(x_grid),np.max(x_grid))
axf[2].set_xlabel(r"$K_M$ $(m^{-1})$")
axf[2].set_ylabel(r"Density ($m$)")
axf[2].set_title(r"$50$ m $<$ $\lambda$ $\leq$ $75$ m ")

axf[3].fill_between(x_grid,KDEFA4,color=cmap[0],alpha=a,label="Piedmont SC")
axf[3].plot(x_grid,KDEFA2,color=cmap[0],linewidth=lw)

axf[3].fill_between(x_grid,KDERF4,color=cmap[1],alpha=a,label="Foothills NC")
axf[3].plot(x_grid,KDERF4,color=cmap[1],linewidth=lw)

axf[3].fill_between(x_grid,KDEsm4,color=cmap[2],alpha=a,label="Escarpment NC")
axf[3].plot(x_grid,KDEsm4,color=cmap[2],linewidth=lw)

axf[3].fill_between(x_grid,KDEth4,color=cmap[3],alpha=a,label="Foothills CA")
axf[3].plot(x_grid,KDEth4,color=cmap[3],linewidth=lw)


axf[3].fill_between(x_grid,KDEyu4,color=cmap[4],alpha=a,label="Yosemite (unglaciated)")
axf[3].plot(x_grid,KDEyu4,color=cmap[4],linewidth=lw)

axf[3].fill_between(x_grid,KDEyg4,color=cmap[5],alpha=a,label="Yosemite (glaciated)")
axf[3].plot(x_grid,KDEyg4,color=cmap[5],linewidth=lw)
axf[3].set_xlim(np.min(x_grid),np.max(x_grid))
axf[3].set_xlabel(r"$K_M$ $(m^{-1})$")
axf[3].set_ylabel(r"Density ($m$)")
axf[3].set_title(r"$75$ m $<$ $\lambda$ $\leq$ $100$ m ")

axf[4].fill_between(x_grid,KDEFA5,color=cmap[0],alpha=a)
axf[4].plot(x_grid,KDEFA2,color=cmap[0],linewidth=lw,label="Piedmont SC")

axf[4].fill_between(x_grid,KDErf5,color=cmap[1],alpha=a)
axf[4].plot(x_grid,KDErf5,color=cmap[1],linewidth=lw,label="Foothills NC")

axf[4].fill_between(x_grid,KDEsm5,color=cmap[2],alpha=a)
axf[4].plot(x_grid,KDEsm5,color=cmap[2],linewidth=lw,label="Escarpment NC")

axf[4].fill_between(x_grid,KDEth5,color=cmap[3],alpha=a)
axf[4].plot(x_grid,KDEth5,color=cmap[3],linewidth=lw,label="Foothills CA")

axf[4].fill_between(x_grid,KDEyu5,color=cmap[4],alpha=a)
axf[4].plot(x_grid,KDEyu5,color=cmap[4],linewidth=lw,label="Yosemite (unglaciated)")

axf[4].fill_between(x_grid,KDEyg5,color=cmap[5],alpha=a)
axf[4].plot(x_grid,KDEyg5,color=cmap[5],linewidth=lw,label="Yosemite (glaciated)")
axf[4].set_xlim(-0.02,0.02)
axf[4].set_xlabel(r"$K_M$ $(m^{-1})$")
axf[4].set_ylabel(r"Density ($m$)")
axf[4].set_title(r"$100$ m $<$ $\lambda$ $\leq$ $200$ m ")

h, l = axf[4].get_legend_handles_labels()
axf[5].axis('off')
axf[5].legend(h,l,loc='center')
plt.tight_layout()
plt.show()


#%% Plot of curavture vs wavlength by climate groupiing
from matplotlib import cm
fig, axes = plt.subplots(2, 3, figsize=(10, 6))

axf = axes.flatten()
cmap = cm.viridis # Or 'plasma', 'jet', etc.
norm = mcolors.Normalize(vmin=0.5, vmax=2.0)

xlim=[6,100]
ylim=[-0.15,0.15]


# Forty Acre Rock
f=D["Forty Acre Rock"]["f"]
km=np.vstack((D["Forty Acre Rock"]["KM_Array"]))
thk=D["Forty Acre Rock"]["Avg"]
indices = np.argwhere(np.isnan(thk))
km[indices,:]=np.nan

axf[0].fill_between(f, np.nanmin(km,axis=0),
                 np.nanmax(km,axis=0), color="k", alpha=0.1, label="Shaded Region")

for i in range(len(thk)):
    if not np.isnan(thk[i]):
        axf[0].plot(f,km[i,:],color=cmap(norm(np.log10(thk[i]))),linewidth=0.8)
        
# axf[0].plot(f,np.nanmedian(km,axis=0),color='k',linewidth=1)

axf[0].set_xlabel('Low-pass filter cutoff (m)')
axf[0].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[0].set_title("Piedmont SC")
axf[0].set_xlim(xlim[0],xlim[1])
axf[0].set_ylim(ylim[0],ylim[1])
# axf[i].set_ylim(-0.1,0.1)

# Rocky Face
f=D["Rocky Face"]["f"]
km=np.vstack((D["Rocky Face"]["KM_Array"]))
thk=D["Rocky Face"]["Avg"]
indices = np.argwhere(np.isnan(thk))
km[indices,:]=np.nan

axf[1].fill_between(f, np.nanmin(km,axis=0),
                np.nanmax(km,axis=0), color="k", alpha=0.1, label="Shaded Region")

for i in range(len(thk)):
    if not np.isnan(thk[i]):
        axf[1].plot(f,km[i,:],color=cmap(norm(np.log10(thk[i]))),linewidth=0.8)

# axf[1].plot(f,np.nanmedian(km,axis=0),color='k',linewidth=1)

axf[1].set_xlabel('Low-pass filter cutoff (m)')
axf[1].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[1].set_title("Foothills NC")
axf[1].set_xlim(xlim[0],xlim[1])
axf[1].set_ylim(ylim[0],ylim[1])

# Stone Mountain
f=D["Stone Mountain"]["f"]
km=np.vstack((D["Stone Mountain"]["KM_Array"]))
thk=D["Stone Mountain"]["Avg"]
indices = np.argwhere(np.isnan(thk))
km[indices,:]=np.nan

axf[2].fill_between(f, np.nanmin(km,axis=0),
                 np.nanmax(km,axis=0), color="k", alpha=0.1, label="Shaded Region")
for i in range(len(thk)):
    if not np.isnan(thk[i]):
        axf[2].plot(f,km[i,:],color=cmap(norm(np.log10(thk[i]))),linewidth=0.8)

# axf[2].plot(f,np.nanmedian(km,axis=0),color='k',linewidth=1)

axf[2].set_xlabel('Low-pass filter cutoff (m)')
axf[2].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[2].set_title("Escarpment NC")
axf[2].set_xlim(xlim[0],xlim[1])
axf[2].set_ylim(ylim[0],ylim[1])

# Twaine Harte
f=D["Twaine Harte West"]["f"]
km=np.vstack((D["Twaine Harte West"]["KM_Array"],D["Twaine Harte Rock"]["KM_Array"]))
thk=np.concatenate((D["Twaine Harte West"]["Avg"],D["Twaine Harte Rock"]["Avg"]))
indices = np.argwhere(np.isnan(thk))
km[indices,:]=np.nan

axf[3].fill_between(f, np.nanmin(km,axis=0),
                 np.nanmax(km,axis=0), color="k", alpha=0.1, label="Shaded Region")
for i in range(len(thk)):
    if not np.isnan(thk[i]):
        axf[3].plot(f,km[i,:],color=cmap(norm(np.log10(thk[i]))),linewidth=0.8)

# axf[3].plot(f,np.nanmedian(km,axis=0),color='k',linewidth=1)
axf[3].set_xlabel('Low-pass filter cutoff (m)')
axf[3].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[3].set_title("Foothills CA")
axf[3].set_xlim(xlim[0],xlim[1])
axf[3].set_ylim(ylim[0],ylim[1])

# Yosemite UNglaciated
f=D["Half Dome"]["f"]
km=np.vstack((D["Half Dome"]["KM_Array"],D["North Dome"]["KM_Array"],D["Sentinal"]["KM_Array"]))
thk=np.concatenate((D["Half Dome"]["Avg"],D["North Dome"]["Avg"],D["Sentinal"]["Avg"]))
indices = np.argwhere(np.isnan(thk))
km[indices,:]=np.nan

axf[4].fill_between(f, np.nanmin(km,axis=0),
                 np.nanmax(km,axis=0), color="k", alpha=0.1, label="Shaded Region")
for i in range(len(thk)):
    if not np.isnan(thk[i]):
        axf[4].plot(f,km[i,:],color=cmap(norm(np.log10(thk[i]))),linewidth=0.8)

# axf[4].plot(f,np.nanmedian(km,axis=0),color='k',linewidth=1)
axf[4].set_xlabel('Low-pass filter cutoff (m)')
axf[4].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[4].set_title("Yosemite (unglaciated)")
axf[4].set_xlim(xlim[0],xlim[1])
axf[4].set_ylim(ylim[0],ylim[1])

# Yosemite glaciated
f=D["Half Dome"]["f"]
km=np.vstack((D["Lembert"]["KM_Array"],D["Lower Olmsted"]["KM_Array"],D["Upper Olmsted"]["KM_Array"],
              D["Pothole"]["KM_Array"],D["Puppy"]["KM_Array"],D["Turtleback"]["KM_Array"]))

thk=np.concatenate((D["Lembert"]["Avg"],D["Lower Olmsted"]["Avg"],D["Upper Olmsted"]["Avg"],
              D["Pothole"]["Avg"],D["Puppy"]["Avg"],D["Turtleback"]["Avg"]))
indices = np.argwhere(np.isnan(thk))
km[indices,:]=np.nan

axf[5].fill_between(f, np.nanmin(km,axis=0),
                 np.nanmax(km,axis=0), color="k", alpha=0.1, label="Shaded Region")
for i in range(len(thk)):
    if not np.isnan(thk[i]):
        axf[5].plot(f,km[i,:],color=cmap(norm(np.log10(thk[i]))),linewidth=0.8)

# axf[5].plot(f,np.nanmedian(km,axis=0),color='k',linewidth=1)
axf[5].set_xlabel('Low-pass filter cutoff (m)')
axf[5].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[5].set_title("Yosemite (glaciated)")
axf[5].set_xlim(xlim[0],xlim[1])
axf[5].set_ylim(ylim[0],ylim[1])

plt.tight_layout()
plt.show()



#%%
# fig, axes = plt.subplots(5, 3, figsize=(10, 11))

# axf = axes.flatten()
# for i in range(14):
data=D[dome_name[3]]
axf[i]=plt.hist(data["KM_Array"].flatten(), bins=50, edgecolor='black', color='skyblue')



