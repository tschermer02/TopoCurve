#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 15:17:12 2026

@author: ntklema
"""
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import pickle


Domes=["Forty_Acre_Rock","Twaine_Harte_West","Twaine_Harte","Stone_Mtn","Rocky_Face","Half_Dome","Lembert_Small","North_Dome","Olmsted_Lower","Olmsted_Upper","Pothole",
       "Puppy","Sentinal","Turtleback"]

D={}
Th=[]
km=[]
th_med=[]

for d in Domes:
   with open('/Users/ntklema/Library/CloudStorage/OneDrive-FortLewisCollege/Research_Projects/Dome Exfoliation/Dome_Exfoliation_2/Python_Dictionaries/'+''+d+''+'.pkl', 'rb') as r:
       D[d] = pickle.load(r)
       if "Sheet Thic" in D[d]:
               D[d]["Avg"] = D[d].pop("Sheet Thic")
       Avg=D[d]["Avg"]   
       Avg=Avg.tolist()
       
       KM=D[d]["KM"]
       KM=KM.tolist()
       
       print(d)
       print(np.nanmedian(D[d]["Avg"]))
       
       km=km+KM
       Th=Th+Avg

  
plt.scatter(Th,km)

#%% Plot thermal stresses

E=60e9
alpha_T=8e-6
v=0.25

sd=0.2

tau=E*alpha_T/(1-v)*np.exp(-np.array(Th)/100/sd)
