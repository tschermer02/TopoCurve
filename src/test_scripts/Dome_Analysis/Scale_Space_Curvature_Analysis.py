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
import sys
from pathlib import Path

# ---------------- Import datasets ---------------------
tiff_file = "/Users/ntklema/Library/CloudStorage/OneDrive-FortLewisCollege/Research_Projects/Dome Exfoliation/Dome_Exfoliation_2/DEMs/Stone_Mtn.tif"

# Instantiate TopoCurve object
dem = TopoCurve(tiff_file=tiff_file)

# Instantiate SpectralFiltering object
spectral_filter = SpectralFiltering(tiff_file)

# Apply FFT filtering with a lowpass filter
filter=[150,200] # Low pass filter cutoffs
dx, dy, filtered_elevation = spectral_filter.FFT(filter, 'lowpass', 0)

# Compute curvature attributes
K = dem.CurveCalc(filtered_elevation, dx, dy, 0)





