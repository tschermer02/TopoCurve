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
from cmcrameri import cm as cmc
fig, axes = plt.subplots(5, 3, figsize=(10, 11))

axf = axes.flatten()
cmap = cmc.lajolla # Or 'plasma', 'jet', etc.
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

cmap = ["brown","purple","navy","black","teal","cyan"]
fig, axes = plt.subplots(2, 3, figsize=(10, 6))

axf = axes.flatten()



km_range=np.arange(0,44,1)
ylim=[-0.03, 0.07]


# Forty Acre Rock
q1_x, q3_x = np.nanpercentile(D["Forty Acre Rock"]["Avg"], [25, 75])
q1_y, q3_y = np.nanpercentile(D["Forty Acre Rock"]["KM_Array"][:,km_range], [25, 75])
min_x, max_x = np.nanmin(D["Forty Acre Rock"]["Avg"]), np.max(D["Forty Acre Rock"]["Avg"])
min_y, max_y = np.nanmin(D["Forty Acre Rock"]["KM_Array"][:,km_range]), np.max(D["Forty Acre Rock"]["KM_Array"][:,km_range])
med_x, med_y = np.nanmedian(D["Forty Acre Rock"]["Avg"]), np.nanmedian(D["Forty Acre Rock"]["KM_Array"][:,km_range])
axf[0].scatter(D["Forty Acre Rock"]["Avg"],np.nanmedian(D["Forty Acre Rock"]["KM_Array"][:,km_range],axis=1),
               c=cmap[0],edgecolors='k', linewidths=1,s=50,marker='D')

axf[0].set_xlim(0,150)
axf[0].set_ylim(ylim[0],ylim[1])
axf[0].set_xlabel('Slab thickness (cm)')
axf[0].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[0].set_title("Piedmont SC")
axf[0].text(-0.3,0.99,"A",transform=axf[0].transAxes,fontsize=14)

# Rocky Face
axf[1].scatter(D["Rocky Face"]["Avg"],np.nanmedian(D["Rocky Face"]["KM_Array"][:,km_range],axis=1),
               c=cmap[1],edgecolors='k', linewidths=1,s=50,marker='^')
axf[1].set_xlim(0,150)
axf[1].set_ylim(ylim[0],ylim[1])
axf[1].set_xlabel('Slab thickness (cm)')
axf[1].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[1].set_title("Foothills NC")
axf[1].text(-0.3,0.99,"B",transform=axf[1].transAxes,fontsize=14)

# Stone Mtn
axf[2].scatter(D["Stone Mountain"]["Avg"],np.nanmedian(D["Stone Mountain"]["KM_Array"][:,km_range],axis=1),
               c=cmap[2],edgecolors='k', linewidths=1,s=50,marker='s')
axf[2].set_xlim(0,150)
axf[2].set_ylim(ylim[0],ylim[1])
axf[2].set_xlabel('Slab thickness (cm)')
axf[2].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[2].set_title("Escarpment NC")
axf[2].text(-0.3,0.99,"C",transform=axf[2].transAxes,fontsize=14)

# Twaine Harte Plots
axf[3].scatter(D["Twaine Harte West"]["Avg"],np.nanmedian(D["Twaine Harte West"]["KM_Array"][:,km_range],axis=1),
               c=cmap[3],edgecolors='k', linewidths=1,s=50    )
axf[3].scatter(D["Twaine Harte Rock"]["Avg"],np.nanmedian(D["Twaine Harte Rock"]["KM_Array"][:,km_range],axis=1),
               c=cmap[3],edgecolors='k', linewidths=1,s=50)
# axf[3].plot([17.2,17.2],[-0.005,0.02])
axf[3].set_xlim(0,150)
axf[3].set_ylim(ylim[0],ylim[1])
axf[3].set_xlabel('Slab thickness (cm)')
axf[3].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[3].set_title("Foothills CA")
axf[3].text(-0.3,0.99,"D",transform=axf[3].transAxes,fontsize=14)

# Yosemite Unglaciated
axf[4].scatter(D["Half Dome"]["Avg"],np.nanmedian(D["Half Dome"]["KM_Array"][:,km_range],axis=1),
               c=cmap[4],edgecolors='k', linewidths=1,s=50)
axf[4].scatter(D["North Dome"]["Avg"],np.nanmedian(D["North Dome"]["KM_Array"][:,km_range],axis=1),
               c=cmap[4],edgecolors='k', linewidths=1,s=50)
axf[4].scatter(D["Sentinal"]["Avg"],np.nanmedian(D["Sentinal"]["KM_Array"][:,km_range],axis=1),
               c=cmap[4],edgecolors='k', linewidths=1,s=50)
axf[4].set_xlim(0,150)
axf[4].set_ylim(ylim[0],ylim[1])
axf[4].set_xlabel('Slab thickness (cm)')
axf[4].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[4].set_title("Yosemite (unglaciated)")
axf[4].text(-0.3,0.99,"E",transform=axf[4].transAxes,fontsize=14)

# Yosemite glaciated
axf[5].scatter(D["Lembert"]["Avg"],np.nanmedian(D["Lembert"]["KM_Array"][:,km_range],axis=1),
               c=cmap[5],edgecolors='k', linewidths=1,s=50)
axf[5].scatter(D["Lower Olmsted"]["Avg"],np.nanmedian(D["Lower Olmsted"]["KM_Array"][:,km_range],axis=1),
               c=cmap[5],edgecolors='k', linewidths=1,s=50)
axf[5].scatter(D["Upper Olmsted"]["Avg"],np.nanmedian(D["Upper Olmsted"]["KM_Array"][:,km_range],axis=1),
               c=cmap[5],edgecolors='k', linewidths=1,s=50)
axf[5].scatter(D["Puppy"]["Avg"],np.nanmedian(D["Puppy"]["KM_Array"][:,km_range],axis=1),
               c=cmap[5],edgecolors='k', linewidths=1,s=50)
axf[5].scatter(D["Pothole"]["Avg"],np.nanmedian(D["Pothole"]["KM_Array"][:,km_range],axis=1),
               c=cmap[5],edgecolors='k', linewidths=1,s=50)
axf[5].scatter(D["Turtleback"]["Avg"],np.nanmedian (D["Turtleback"]["KM_Array"][:,km_range],axis=1),
               c=cmap[5],edgecolors='k', linewidths=1,s=50)
axf[5].set_xlim(0,150)
axf[5].set_ylim(ylim[0],ylim[1])
axf[5].set_xlabel('Slab thickness (cm)')
axf[5].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[5].set_title("Yosemite (glaciated)")
axf[5].text(-0.3,0.99,"F",transform=axf[5].transAxes,fontsize=14)

plt.tight_layout()
plt.show()


#%% KDE plots of curvature
# import seaborn as sns
import pandas as pd
from scipy.stats import gaussian_kde
fig, axes = plt.subplots(2, 3, figsize=(10, 5))
axf = axes.flatten()

x_grid = np.linspace(-5e-2, 5e-2, 200)

f_range1=np.arange(0,14)
f_range2=np.arange(15,34)
f_range3=np.arange(35,54)
f_range4=np.arange(55,74)
f_range5=np.arange(75,94)


# Forty Acre Rock
kmfa=D["Forty Acre Rock"]["KM_Array"]
fa1=pd.DataFrame({"KMFA1": kmfa[:,f_range1].flatten()})
fa1 = fa1["KMFA1"].dropna()
kde_fa1 = gaussian_kde(fa1)
KDEFA1 = kde_fa1(x_grid)

fa2=pd.DataFrame({"KMFA2": kmfa[:,f_range2].flatten()})
fa2 = fa2["KMFA2"].dropna()
kde_fa2 = gaussian_kde(fa2)
KDEFA2 = kde_fa2(x_grid)

fa3=pd.DataFrame({"KMFA3": kmfa[:,f_range3].flatten()})
fa3 = fa3["KMFA3"].dropna()
kde_fa3 = gaussian_kde(fa3)
KDEFA3 = kde_fa3(x_grid)

fa4=pd.DataFrame({"KMFA4": kmfa[:,f_range4].flatten()})
fa4 = fa4["KMFA4"].dropna()
kde_fa4 = gaussian_kde(fa4)
KDEFA4 = kde_fa4(x_grid)

fa5=pd.DataFrame({"KMFA5": kmfa[:,f_range5].flatten()})
fa5 = fa5["KMFA5"].dropna()
kde_fa5 = gaussian_kde(fa5)
KDEFA5 = kde_fa5(x_grid)

# Rocky Face
kmrf=D["Rocky Face"]["KM_Array"]
rf1=pd.DataFrame({"KMRF1": kmrf[:,f_range1].flatten()})
rf1 = rf1["KMRF1"].dropna()
kde_rf1 = gaussian_kde(rf1)
KDERF1 = kde_rf1(x_grid)

rf2=pd.DataFrame({"KMRF2": kmrf[:,f_range2].flatten()})
rf2 = rf2["KMRF2"].dropna()
kde_rf2 = gaussian_kde(rf2)
KDERF2 = kde_rf2(x_grid)

rf3=pd.DataFrame({"KMRF3": kmrf[:,f_range3].flatten()})
rf3 = rf3["KMRF3"].dropna()
kde_rf3 = gaussian_kde(rf3)
KDERF3 = kde_rf3(x_grid)

rf4=pd.DataFrame({"KMRF4": kmrf[:,f_range4].flatten()})
rf4 = rf4["KMRF4"].dropna()
kde_rf4 = gaussian_kde(rf4)
KDERF4 = kde_rf4(x_grid)

rf5=pd.DataFrame({"KMrf5": kmrf[:,f_range5].flatten()})
rf5 = rf5["KMrf5"].dropna()
kde_rf5 = gaussian_kde(rf5)
KDErf5 = kde_rf5(x_grid)

# Stone Mountain
kmsm=D["Stone Mountain"]["KM_Array"]
sm1=pd.DataFrame({"kmsm1": kmsm[:,f_range1].flatten()})
sm1 = sm1["kmsm1"].dropna()
kde_sm1 = gaussian_kde(sm1)
KDEsm1 = kde_sm1(x_grid)

sm2=pd.DataFrame({"kmsm2": kmsm[:,f_range2].flatten()})
sm2 = sm2["kmsm2"].dropna()
kde_sm2 = gaussian_kde(sm2)
KDEsm2 = kde_sm2(x_grid)

sm3=pd.DataFrame({"kmsm3": kmsm[:,f_range3].flatten()})
sm3 = sm3["kmsm3"].dropna()
kde_sm3 = gaussian_kde(sm3)
KDEsm3 = kde_sm3(x_grid)

sm4=pd.DataFrame({"kmsm4": kmsm[:,f_range4].flatten()})
sm4 = sm4["kmsm4"].dropna()
kde_sm4 = gaussian_kde(sm4)
KDEsm4 = kde_sm4(x_grid)

sm5=pd.DataFrame({"KMsm5": kmsm[:,f_range5].flatten()})
sm5 = sm5["KMsm5"].dropna()
kde_sm5 = gaussian_kde(sm5)
KDEsm5 = kde_sm5(x_grid)

# Twaine Harte
kmth=np.vstack((D["Twaine Harte West"]["KM_Array"],D["Twaine Harte Rock"]["KM_Array"]))
th1=pd.DataFrame({"kmth1": kmth[:,f_range1].flatten()})
th1 = th1["kmth1"].dropna()
kde_th1 = gaussian_kde(th1)
KDEth1 = kde_th1(x_grid)

th2=pd.DataFrame({"kmth2": kmth[:,f_range2].flatten()})
th2 = th2["kmth2"].dropna()
kde_th2 = gaussian_kde(th2)
KDEth2 = kde_th2(x_grid)

th3=pd.DataFrame({"kmth3": kmth[:,f_range3].flatten()})
th3 = th3["kmth3"].dropna()
kde_th3 = gaussian_kde(th3)
KDEth3 = kde_th3(x_grid)

th4=pd.DataFrame({"kmth4": kmth[:,f_range4].flatten()})
th4 = th4["kmth4"].dropna()
kde_th4 = gaussian_kde(th4)
KDEth4 = kde_th4(x_grid)

th5=pd.DataFrame({"KMth5": kmth[:,f_range5].flatten()})
th5 = th5["KMth5"].dropna()
kde_th5 = gaussian_kde(th5)
KDEth5 = kde_th5(x_grid)

# Yosemite (unglaciated)
kmyu=np.vstack((D["Half Dome"]["KM_Array"],D["North Dome"]["KM_Array"],D["Sentinal"]["KM_Array"]))
yu1=pd.DataFrame({"kmyu1": kmyu[:,f_range1].flatten()})
yu1 = yu1["kmyu1"].dropna()
kde_yu1 = gaussian_kde(yu1)
KDEyu1 = kde_yu1(x_grid)

yu2=pd.DataFrame({"kmyu2": kmyu[:,f_range2].flatten()})
yu2 = yu2["kmyu2"].dropna()
kde_yu2 = gaussian_kde(yu2)
KDEyu2 = kde_yu2(x_grid)

yu3=pd.DataFrame({"kmyu3": kmyu[:,f_range3].flatten()})
yu3 = yu3["kmyu3"].dropna()
kde_yu3 = gaussian_kde(yu3)
KDEyu3 = kde_yu3(x_grid)

yu4=pd.DataFrame({"kmyu4": kmyu[:,f_range4].flatten()})
yu4 = yu4["kmyu4"].dropna()
kde_yu4 = gaussian_kde(yu4)
KDEyu4 = kde_yu4(x_grid)

yu5=pd.DataFrame({"KMyu5": kmyu[:,f_range5].flatten()})
yu5 = yu5["KMyu5"].dropna()
kde_yu5 = gaussian_kde(yu5)
KDEyu5 = kde_yu5(x_grid)

# Yosemite (glaciated)

kmyg=np.vstack((D["Lembert"]["KM_Array"],D["Lower Olmsted"]["KM_Array"],D["Upper Olmsted"]["KM_Array"],D["Pothole"]["KM_Array"],
                D["Puppy"]["KM_Array"],D["Turtleback"]["KM_Array"]))
yg1=pd.DataFrame({"kmyg1": kmyg[:,f_range1].flatten()})
yg1 = yg1["kmyg1"].dropna()
kde_yg1 = gaussian_kde(yg1)
KDEyg1 = kde_yg1(x_grid)

yg2=pd.DataFrame({"kmyg2": kmyg[:,f_range2].flatten()})
yg2 = yg2["kmyg2"].dropna()
kde_yg2 = gaussian_kde(yg2)
KDEyg2 = kde_yg2(x_grid)

yg3=pd.DataFrame({"kmyg3": kmyg[:,f_range3].flatten()})
yg3 = yg3["kmyg3"].dropna()
kde_yg3 = gaussian_kde(yg3)
KDEyg3 = kde_yg3(x_grid)

yg4=pd.DataFrame({"kmyg4": kmyg[:,f_range4].flatten()})
yg4 = yg4["kmyg4"].dropna()
kde_yg4 = gaussian_kde(yg4)
KDEyg4 = kde_yg4(x_grid)

yg5=pd.DataFrame({"KMyg5": kmyg[:,f_range5].flatten()})
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
axf[0].set_title(r"$0$ m $<$ $\lambda$ $\leq$ $20$ m ")
axf[0].text(-0.2,0.99,"A",transform=axf[0].transAxes,fontsize=14)

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
axf[1].set_title(r"$20$ m $<$ $\lambda$ $\leq$ $40$ m ")
axf[1].text(-0.2,0.99,"B",transform=axf[1].transAxes,fontsize=14)
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
axf[2].set_title(r"$40$ m $<$ $\lambda$ $\leq$ $60$ m ")
axf[2].text(-0.2,0.99,"C",transform=axf[2].transAxes,fontsize=14)

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
axf[3].set_title(r"$60$ m $<$ $\lambda$ $\leq$ $80$ m ")
axf[3].text(-0.2,0.99,"D",transform=axf[3].transAxes,fontsize=14)

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
axf[4].set_xlim(np.min(x_grid),np.max(x_grid))
axf[4].set_xlabel(r"$K_M$ $(m^{-1})$")
axf[4].set_ylabel(r"Density ($m$)")
axf[4].set_title(r"$80$ m $<$ $\lambda$ $\leq$ $100$ m ")
axf[4].text(-0.2,0.99,"E",transform=axf[4].transAxes,fontsize=14)

h, l = axf[4].get_legend_handles_labels()
axf[5].axis('off')
axf[5].legend(h,l,loc='center',fontsize=14,frameon=False)
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
                 np.nanmax(km,axis=0), color="k", alpha=0, label="Shaded Region")

for i in range(len(thk)):
    if not np.isnan(thk[i]):
        axf[0].plot(f,km[i,:],color=cmap(norm(np.log10(thk[i]))),linewidth=0.8)
        
# axf[0].plot(f,np.nanmedian(km,axis=0),color='k',linewidth=1)

axf[0].set_xlabel('Low-pass filter cutoff (m)')
axf[0].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[0].set_title("Piedmont SC")
axf[0].set_xlim(xlim[0],xlim[1])
axf[0].set_ylim(ylim[0],ylim[1])
axf[0].text(-0.32,0.99,"A",transform=axf[0].transAxes,fontsize=14)
# axf[i].set_ylim(-0.1,0.1)

# Rocky Face
f=D["Rocky Face"]["f"]
km=np.vstack((D["Rocky Face"]["KM_Array"]))
thk=D["Rocky Face"]["Avg"]
indices = np.argwhere(np.isnan(thk))
km[indices,:]=np.nan

axf[1].fill_between(f, np.nanmin(km,axis=0),
                np.nanmax(km,axis=0), color="k", alpha=0, label="Shaded Region")

for i in range(len(thk)):
    if not np.isnan(thk[i]):
        axf[1].plot(f,km[i,:],color=cmap(norm(np.log10(thk[i]))),linewidth=0.8)

# axf[1].plot(f,np.nanmedian(km,axis=0),color='k',linewidth=1)

axf[1].set_xlabel('Low-pass filter cutoff (m)')
axf[1].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[1].set_title("Foothills NC")
axf[1].set_xlim(xlim[0],xlim[1])
axf[1].set_ylim(ylim[0],ylim[1])
axf[1].text(-0.32,0.99,"B",transform=axf[1].transAxes,fontsize=14)

# Stone Mountain
f=D["Stone Mountain"]["f"]
km=np.vstack((D["Stone Mountain"]["KM_Array"]))
thk=D["Stone Mountain"]["Avg"]
indices = np.argwhere(np.isnan(thk))
km[indices,:]=np.nan

axf[2].fill_between(f, np.nanmin(km,axis=0),
                 np.nanmax(km,axis=0), color="k", alpha=0, label="Shaded Region")
for i in range(len(thk)):
    if not np.isnan(thk[i]):
        axf[2].plot(f,km[i,:],color=cmap(norm(np.log10(thk[i]))),linewidth=0.8)

# axf[2].plot(f,np.nanmedian(km,axis=0),color='k',linewidth=1)

axf[2].set_xlabel('Low-pass filter cutoff (m)')
axf[2].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[2].set_title("Escarpment NC")
axf[2].set_xlim(xlim[0],xlim[1])
axf[2].set_ylim(ylim[0],ylim[1])
axf[2].text(-0.32,0.99,"C",transform=axf[2].transAxes,fontsize=14)

# Twaine Harte
f=D["Twaine Harte West"]["f"]
km=np.vstack((D["Twaine Harte West"]["KM_Array"],D["Twaine Harte Rock"]["KM_Array"]))
thk=np.concatenate((D["Twaine Harte West"]["Avg"],D["Twaine Harte Rock"]["Avg"]))
indices = np.argwhere(np.isnan(thk))
km[indices,:]=np.nan

axf[3].fill_between(f, np.nanmin(km,axis=0),
                 np.nanmax(km,axis=0), color="k", alpha=0, label="Shaded Region")
for i in range(len(thk)):
    if not np.isnan(thk[i]):
        axf[3].plot(f,km[i,:],color=cmap(norm(np.log10(thk[i]))),linewidth=0.8)

# axf[3].plot(f,np.nanmedian(km,axis=0),color='k',linewidth=1)
axf[3].set_xlabel('Low-pass filter cutoff (m)')
axf[3].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[3].set_title("Foothills CA")
axf[3].set_xlim(xlim[0],xlim[1])
axf[3].set_ylim(ylim[0],ylim[1])
axf[3].text(-0.32,0.99,"D",transform=axf[3].transAxes,fontsize=14)

# Yosemite UNglaciated
f=D["Half Dome"]["f"]
km=np.vstack((D["Half Dome"]["KM_Array"],D["North Dome"]["KM_Array"],D["Sentinal"]["KM_Array"]))
thk=np.concatenate((D["Half Dome"]["Avg"],D["North Dome"]["Avg"],D["Sentinal"]["Avg"]))
indices = np.argwhere(np.isnan(thk))
km[indices,:]=np.nan

axf[4].fill_between(f, np.nanmin(km,axis=0),
                 np.nanmax(km,axis=0), color="k", alpha=0, label="Shaded Region")
for i in range(len(thk)):
    if not np.isnan(thk[i]):
        axf[4].plot(f,km[i,:],color=cmap(norm(np.log10(thk[i]))),linewidth=0.8)

# axf[4].plot(f,np.nanmedian(km,axis=0),color='k',linewidth=1)
axf[4].set_xlabel('Low-pass filter cutoff (m)')
axf[4].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[4].set_title("Yosemite (unglaciated)")
axf[4].set_xlim(xlim[0],xlim[1])
axf[4].set_ylim(ylim[0],ylim[1])
axf[4].text(-0.32,0.99,"E",transform=axf[4].transAxes,fontsize=14)

# Yosemite glaciated
f=D["Half Dome"]["f"]
km=np.vstack((D["Lembert"]["KM_Array"],D["Lower Olmsted"]["KM_Array"],D["Upper Olmsted"]["KM_Array"],
              D["Pothole"]["KM_Array"],D["Puppy"]["KM_Array"],D["Turtleback"]["KM_Array"]))

thk=np.concatenate((D["Lembert"]["Avg"],D["Lower Olmsted"]["Avg"],D["Upper Olmsted"]["Avg"],
              D["Pothole"]["Avg"],D["Puppy"]["Avg"],D["Turtleback"]["Avg"]))
indices = np.argwhere(np.isnan(thk))
km[indices,:]=np.nan

axf[5].fill_between(f, np.nanmin(km,axis=0),
                 np.nanmax(km,axis=0), color="k", alpha=0, label="Shaded Region")
for i in range(len(thk)):
    if not np.isnan(thk[i]):
        axf[5].plot(f,km[i,:],color=cmap(norm(np.log10(thk[i]))),linewidth=0.8)

# axf[5].plot(f,np.nanmedian(km,axis=0),color='k',linewidth=1)
axf[5].set_xlabel('Low-pass filter cutoff (m)')
axf[5].set_ylabel(r'$K_M$ ($m^{-1}$)')
axf[5].set_title("Yosemite (glaciated)")
axf[5].set_xlim(xlim[0],xlim[1])
axf[5].set_ylim(ylim[0],ylim[1])
axf[5].text(-0.32,0.99,"F",transform=axf[5].transAxes,fontsize=14)

plt.tight_layout()
plt.show()



#%% KDE of slab thicknesses
x_grid = np.linspace(0, 120, 200)

# Forty Acre Rock
thkfa=D["Forty Acre Rock"]["Avg"]
fa=pd.DataFrame({"thfa": thkfa})
fa = fa["thfa"].dropna()
kde_fa = gaussian_kde(fa)
KDEfa = kde_fa(x_grid)

# Rocky Face
thkrf=D["Rocky Face"]["Avg"]
rf=pd.DataFrame({"thrf": thkrf})
rf = rf["thrf"].dropna()
kde_rf = gaussian_kde(rf)
KDErf = kde_rf(x_grid)

# Stone Mountain
thksm=D["Stone Mountain"]["Avg"]
sm=pd.DataFrame({"thsm": thksm})
sm = sm["thsm"].dropna()
kde_sm = gaussian_kde(sm)
KDEsm = kde_sm(x_grid)

# Twaine Harte
thkth=np.concatenate((D["Twaine Harte West"]["Avg"],D["Twaine Harte Rock"]["Avg"]))
th=pd.DataFrame({"thth": thkth})
th = th["thth"].dropna()
kde_th = gaussian_kde(th)
KDEth = kde_th(x_grid)

# Yosemite unglaciated
thkyu=np.concatenate((D["Half Dome"]["Avg"],D["North Dome"]["Avg"],D["Sentinal"]["Avg"]))
yu=pd.DataFrame({"thyu": thkyu})
yu = yu["thyu"].dropna()
kde_yu = gaussian_kde(yu)
KDEyu = kde_yu(x_grid)

# Yosemite glaciated
thkyg=np.concatenate((D["Lembert"]["Avg"],D["Lower Olmsted"]["Avg"],
                      D["Upper Olmsted"]["Avg"],D["Pothole"]["Avg"],
                      D["Puppy"]["Avg"],D["Turtleback"]["Avg"]))
yg=pd.DataFrame({"thyg": thkyg})
yg = yg["thyg"].dropna()
kde_yg = gaussian_kde(yg)
KDEyg = kde_yg(x_grid)

fig, axes = plt.subplots(2, 1,figsize=(6, 6), height_ratios=[1, 2])

axf=axes.flatten()
cmap = ["brown","purple","navy","black","teal","cyan"]
lw=2
sd=[20.2,21.4,20.3,17.2]

axf[0].plot(x_grid,np.exp(-x_grid/sd[0]),c=cmap[0])
axf[0].axvline(x=sd[0], c=cmap[0], linestyle="--",linewidth=3)
axf[0].axvline(x=2*sd[0], c=cmap[0], linestyle="--",linewidth=2)
axf[0].axvline(x=3*sd[0], c=cmap[0], linestyle="--",linewidth=1)

axf[0].plot(x_grid,np.exp(-x_grid/sd[1]),c=cmap[1])
axf[0].axvline(x=sd[1], c=cmap[1], linestyle="-.",linewidth=3)
axf[0].axvline(x=2*sd[1], c=cmap[1], linestyle="-.",linewidth=2)
axf[0].axvline(x=3*sd[1], c=cmap[1], linestyle="-.",linewidth=1)

axf[0].plot(x_grid,np.exp(-x_grid/sd[2]),c=cmap[2])
axf[0].axvline(x=sd[2], c=cmap[2], linestyle=":",linewidth=3)
axf[0].axvline(x=2*sd[2], c=cmap[2], linestyle=":",linewidth=2)
axf[0].axvline(x=3*sd[2], c=cmap[2], linestyle=":",linewidth=1)

axf[0].plot(x_grid,np.exp(-x_grid/sd[3]),c=cmap[3])
axf[0].axvline(x=sd[3], c=cmap[3], linestyle=":",linewidth=3)
axf[0].axvline(x=2*sd[3], c=cmap[3], linestyle=":",linewidth=2)
axf[0].axvline(x=3*sd[3], c=cmap[3], linestyle=":",linewidth=1)

axf[0].set_ylabel(r"$|\Delta T|/|\Delta T_{s}|$")
axf[0].set_xlabel(r"Depth (cm)")
axf[0].set_xlim(0,120)
axf[0].text(-0.13,0.99,"A",transform=axf[0].transAxes,fontsize=14)

axf[1].plot(x_grid,KDEfa,c=cmap[0],linewidth=lw,label="Piedmont SC")
axf[1].plot(x_grid,KDErf,c=cmap[1],linewidth=lw,label="Foothills NC")
axf[1].plot(x_grid,KDEsm,c=cmap[2],linewidth=lw,label="Escarpment NC")
axf[1].plot(x_grid,KDEth,c=cmap[3],linewidth=lw,label="Foothills CA")
axf[1].plot(x_grid,KDEyu,c=cmap[4],linewidth=lw,label="Yosemite (unglaciated)")
axf[1].plot(x_grid,KDEyg,c=cmap[5],linewidth=lw,label="Yosemite (glaciated)")
axf[1].set_ylabel(r"Kernal density (cm$^{-1}$)")
axf[1].set_xlabel(r"Slab thickness measurements (cm)")
axf[1].set_xlim(0,120)
axf[1].legend(loc="upper right")
axf[1].text(-0.13,0.99,"B",transform=axf[1].transAxes,fontsize=14)

#%% Phi metric from thermal perturbation to periodic 1d topography
"""
plot_phi.py

Computes and plots Phi(y), the complex depth-profile of the first-order
thermoelastic Airy function from Section 11 of the topographic
amplification derivation (periodic surface heating on wavy topography).

    Phi(y) = (lambda*delta/2)(1-i) h0 dT (e^{qy} - e^{ky}) + D1 y e^{ky}

    q  = sqrt(k^2 + i*2/delta^2),         Re(q) > 0
    D1 = lambda*h0*dT*[1 + (delta/2)(1-i)(k - q)]
    lambda = E*alpha_T/(1-nu)
    delta  = sqrt(2*alpha/omega)           (thermal skin depth)

y is elevation (positive up, rock at y<0); depth z = -y is used for
plotting, matching the convention used throughout the document.

Physically meaningful outputs, all peak-over-cycle envelopes evaluated
at the ridge crest (x=0):
    |Phi(y)|                    -- magnitude of the Airy-function profile itself
    sigma_xx envelope = |Phi''(y)|          -- "horizontal" / in-plane stress
    sigma_yy envelope = k^2 |Phi(y)|        -- "vertical" / surface-normal
                                                (sheeting-relevant) stress
Also plots the flat-boundary (no-topography) sigma_xx reference,
sigma_T0 * exp(-z/delta), for comparison (Section 11.2a).

Usage
-----
Edit the PARAMETER_SETS list below (each dict is one curve to plot,
compared against the others), then run:

    python plot_phi.py

Requires: numpy, scipy, matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar


# ----------------------------------------------------------------------
# Core physics: Phi(y) and its peak-depth
# ----------------------------------------------------------------------
def compute_lambda_delta(E, alpha_T, nu, alpha_diff, period_seconds):
    """E [Pa], alpha_T [1/C], nu [-], alpha_diff = thermal diffusivity
    [m^2/s], period_seconds = forcing period (86400 for diurnal,
    ~3.156e7 for annual). Returns (lambda, delta)."""
    lam = E * alpha_T / (1 - nu)
    omega = 2 * np.pi / period_seconds
    delta = np.sqrt(2 * alpha_diff / omega)
    return lam, delta


def Phi(y, lam, delta, h0, dT, k):
    """Exact Phi(y) from Section 11, vectorized over y (array or scalar).
    y is elevation (<=0 into the rock)."""
    y = np.asarray(y, dtype=complex)
    q = np.sqrt(k**2 + 1j * 2 / delta**2)
    # ensure the branch with Re(q) > 0 (required for boundedness as y -> -inf)
    if np.real(q) < 0:
        q = -q
    D1 = lam * h0 * dT * (1 + (delta / 2) * (1 - 1j) * (k - q))
    return (lam * delta / 2) * (1 - 1j) * h0 * dT * (np.exp(q * y) - np.exp(k * y)) \
        + D1 * y * np.exp(k * y)


def Phi_derivatives(y, lam, delta, h0, dT, k):
    """Returns (Phi, Phi', Phi'') at y, all exact closed forms (verified
    against symbolic differentiation of Phi). Needed for the stress
    components:
        sigma_xx^(1) = cos(kx) Re[Phi''(y) e^{i*omega*t}]   (in-plane)
        sigma_xy^(1) = k sin(kx) Re[Phi'(y) e^{i*omega*t}]  (shear)
        sigma_yy^(1) = -k^2 cos(kx) Re[Phi(y) e^{i*omega*t}] (surface-normal)
    """
    y = np.asarray(y, dtype=complex)
    q = np.sqrt(k**2 + 1j * 2 / delta**2)
    if np.real(q) < 0:
        q = -q
    D1 = lam * h0 * dT * (1 + (delta / 2) * (1 - 1j) * (k - q))
    pref = (lam * delta / 2) * (1 - 1j) * h0 * dT

    phi = pref * (np.exp(q * y) - np.exp(k * y)) + D1 * y * np.exp(k * y)
    phi_p = D1 * k * y * np.exp(k * y) + D1 * np.exp(k * y) \
        - pref * (k * np.exp(k * y) - q * np.exp(q * y))
    phi_pp = D1 * k**2 * y * np.exp(k * y) + 2 * D1 * k * np.exp(k * y) \
        - pref * (k**2 * np.exp(k * y) - q**2 * np.exp(q * y))
    return phi, phi_p, phi_pp


def zeroth_order_phasor(y, lam, delta, dT):
    """Complex phasor amplitude C0(y) of the flat-boundary (zeroth-order)
    in-plane thermal stress, tension-positive (Section 11.2a):
    sigma_xx^(0)(y,t) = Re[C0(y) e^{i*omega*t}], C0(y) = -lam*dT*e^{q0*y},
    q0 = (1+i)/delta."""
    q0 = (1 + 1j) / delta
    return -lam * dT * np.exp(q0 * y)


def stress_envelopes(y, lam, delta, h0, dT, k):
    """Peak-over-cycle envelopes of the thermally-driven stress
    components at the ridge crest (x=0). IMPORTANT: sigma_xx combines
    the zeroth-order (flat) and first-order (topographic) contributions
    as a SINGLE complex phasor sum before taking the magnitude --
    |C0(y) + Phi''(y)| -- NOT |C0(y)| + |Phi''(y)|. The two terms are
    generally out of phase (different complex arguments), so their
    magnitudes do not simply add; only the combined phasor's magnitude
    is the physically meaningful peak-over-cycle stress. Taking the two
    magnitudes separately (as an earlier version of this script did)
    overstates the topographic correction's effect on the total peak
    stress.
    Returns (sigma_xx_total_envelope, sigma_xx_correction_only_envelope,
    sigma_yy_envelope), all real, Pa. sigma_yy has no zeroth-order part
    (Section 11.2a: sigma_yy^(0)=0 identically), so no combination is
    needed there."""
    phi, phi_p, phi_pp = Phi_derivatives(y, lam, delta, h0, dT, k)
    C0 = zeroth_order_phasor(y, lam, delta, dT)
    sigma_xx_total = np.abs(C0 + phi_pp)     # correct: combine phasors first
    sigma_xx_correction_only = np.abs(phi_pp)  # topographic term in isolation
    sigma_yy = k**2 * np.abs(phi)            # no zeroth-order term to combine
    return sigma_xx_total, sigma_xx_correction_only, sigma_yy


def find_peak_depth(lam, delta, h0, dT, k, z_max=None):
    """Numerically locate z_peak = argmax_z |Phi(-z)|. Search range
    defaults to a generous multiple of both delta and 1/k, whichever
    is larger, so the search window adapts to the parameter regime."""
    if z_max is None:
        z_max = 10 * max(delta, 1 / k)
    res = minimize_scalar(lambda z: -abs(Phi(-z, lam, delta, h0, dT, k)),
                           bounds=(1e-6, z_max), method='bounded')
    return res.x, abs(Phi(-res.x, lam, delta, h0, dT, k))


# ----------------------------------------------------------------------
# Parameter sets to compare -- EDIT THIS SECTION
# ----------------------------------------------------------------------
# Each entry: label, material/forcing properties, and topography.
# alpha_diff = thermal diffusivity [m^2/s]; period_seconds = forcing
# period (86400 s = diurnal, 3.156e7 s = annual).
PARAMETER_SETS = [
    dict(label="wavelength=10 m",  E=60e9, alpha_T=8e-6, nu=0.25,
         alpha_diff=1.2e-6, period_seconds=86400, dT=10.0, h0=0.2,
         wavelength=10.0),
    dict(label="wavelength=20 m",  E=60e9, alpha_T=8e-6, nu=0.25,
         alpha_diff=1.2e-6, period_seconds=86400, dT=10.0, h0=0.2,
         wavelength=20.0),
    dict(label="wavelength=50 m",  E=60e9, alpha_T=8e-6, nu=0.25,
         alpha_diff=1.2e-6, period_seconds=86400, dT=10.0, h0=0.2,
         wavelength=50.0),
    # Example of varying dT instead of wavelength -- uncomment to use:
    # dict(label="dT=10 C", E=60e9, alpha_T=8e-6, nu=0.25,
    #      alpha_diff=1.2e-6, period_seconds=86400, dT=10.0, h0=0.2,
    #      wavelength=20.0),
]

Z_MAX_PLOT = 3.0   # meters, depth range to plot
N_POINTS = 300


# ----------------------------------------------------------------------
# Plotting
# ----------------------------------------------------------------------
def main():
    zs = np.linspace(0, Z_MAX_PLOT, N_POINTS)

    fig, axes = plt.subplots(2, 1, figsize=(8, 11), sharex=True)
    ax_xx, ax_yy = axes

    print(f"{'label':>18} | {'delta (m)':>10} | {'z_peak (m)':>11} | "
          f"{'z_peak/delta':>13} | {'sigma_yy_peak (MPa)':>20}")
    print("-" * 85)

    for params in PARAMETER_SETS:
        lam, delta = compute_lambda_delta(
            params["E"], params["alpha_T"], params["nu"],
            params["alpha_diff"], params["period_seconds"])
        k = 2 * np.pi / params["wavelength"]
        h0, dT = params["h0"], params["dT"]

        mag = np.abs(Phi(-zs, lam, delta, h0, dT, k))
        sigma_xx_total, sigma_xx_corr_only, sigma_yy = \
            stress_envelopes(-zs, lam, delta, h0, dT, k)

        # zeroth-order (flat, no-topography) sigma_xx reference envelope,
        # for comparison -- Section 11.2a: sigma_T0 * e^{-z/delta}
        sigma_T0 = lam * dT
        sigma_xx_flat = sigma_T0 * np.exp(-zs / delta)


        ax_xx.plot(zs, sigma_xx_total / 1e6, label=params["label"])

        ax_yy.plot(zs, sigma_yy / 1e6, label=params["label"])

        z_peak, _ = find_peak_depth(lam, delta, h0, dT, k)
        sigma_yy_peak = k**2 * np.abs(Phi(-z_peak, lam, delta, h0, dT, k))
        ax_yy.axvline(delta, linestyle="--", alpha=1,linewidth=3)
        ax_yy.axvline(2*delta, linestyle="--", alpha=1,linewidth=2)
        ax_yy.axvline(3*delta, linestyle="--", alpha=1,linewidth=1)
        print(f"{params['label']:>18} | {delta:>10.4f} | {z_peak:>11.4f} | "
              f"{z_peak/delta:>13.3f} | {sigma_yy_peak/1e6:>20.4f}")

    # flat-boundary reference curve (same for all parameter sets that
    # share E, alpha_T, nu, dT, delta -- plotted once using the last set)
    ax_xx.plot(zs, sigma_xx_flat / 1e6, 'k--', alpha=0.6,
               label="Flat boundary")




    ax_xx.set_ylabel(r"$\sigma_{xx}$ envelope (MPa)")
    ax_xx.legend(fontsize=8)

    ax_yy.set_ylabel(r"$\sigma_{yy}$ envelope (MPa)" )
    ax_yy.set_xlabel("Depth (m)")
    ax_yy.legend(fontsize=8)

    for ax in axes:
        ax.grid(alpha=0.3)

    plt.tight_layout()
    out_path = "/mnt/user-data/outputs/phi_plot.png"
    plt.savefig(out_path, dpi=150)
    print(f"\nSaved plot to {out_path}")


if __name__ == "__main__":
    main()