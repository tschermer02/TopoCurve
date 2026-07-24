#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 14:32:24 2026

@author: ntklema
"""
import geopandas as gpd

def TopoCurve_Sample(tiff_file,shapefile,Attributes=None):
    s_points = gpd.read_file(shapefile)
    x = s_points.geometry.x
    y = s_points.geometry.y
    
    # Instantiate TopoCurve object
    dem = TopoCurve(tiff_file=tiff_file)

    # Instantiate SpectralFiltering object
    spectral_filter = SpectralFiltering(tiff_file)
    
    for i in x:
        print(i)
    
    
    
    return x,y
    