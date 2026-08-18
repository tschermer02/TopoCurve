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

for d in Domes:
   with open('/Users/ntklema/Library/CloudStorage/OneDrive-FortLewisCollege/Research_Projects/Dome Exfoliation/Dome_Exfoliation_2/Python_Dictionaries/'+''+d+''+'.pkl', 'rb') as r:
       D[d] = pickle.load(r)
       if "Sheet Thic" in D[d]:
               D[d]["Avg"] = D[d].pop("Sheet Thic")
       plt.scatter((D[d]['Avg']),D[d]['KM'])
plt.show()
    
# plt.plot(D['f'],D['KM_Array'][5,:])