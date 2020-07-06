#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# Zones
# =============================================================================
# HK: Hindu-Kush / Karakoram / Western Himalay
# HM: Central and Est Himalaya
# TB: Tibetan Plateau
def get_zones_IPSL_CM6A_LR():
    # Grid size for LMDZ
    dx=2.5
    dy=1.2676

    lonlim_HK=(70-dx/2, 70-dx/2 + 10+dx)
    latlim_HK=(31.690142-dy/2, 31.690142-dy/2 + 7.6056339+dy)
    
    lonlim_HM=(77.5-dx/2+dx, 77.5-dx/2+dx + 15+2*dx)
    latlim_HM=(26.619719-dy/2, 26.619719-dy/2 + 3.802816+dy)

    lonlim_TB=(82.5-dx/2, 82.5-dx/2 + 15+3*dx)
    latlim_TB=(31.690142-dy/2, 31.690142-dy/2 + 7.6056339)
    
    return lonlim_HK, latlim_HK, lonlim_HM, latlim_HM, lonlim_TB, latlim_TB

import matplotlib.patches as mpatches
import cartopy.crs as ccrs

def plot_zones_IPSL_CM6A_LR(ax):
    # Grid size for LMDZ
    dx=2.5
    dy=1.2676
    
    ax.text(70-dx/3, 31.690142-dy/2+7.6056339-3*dy/4, 'HK')
    ax.add_patch(mpatches.Rectangle(
            xy=[70-dx/2, 31.690142-dy/2], width=10+dx, height=7.6056339+1*dy,
            transform=ccrs.PlateCarree(), fill=False
        ))
    ax.text(77.5+dx-dx/3, 26.619719-dy/2+3.802816-3*dy/4, 'HM')
    ax.add_patch(mpatches.Rectangle(
            xy=[77.5-dx/2+dx, 26.619719-dy/2], width=15+2*dx, height=3.802816+dy,
            transform=ccrs.PlateCarree(), fill=False
        )) # CH
    ax.text(82.5-dx/3, 31.690142-dy/2+7.6056339-dy-3*dy/4, 'TB')
    ax.add_patch(mpatches.Rectangle(
            xy=[82.5-dx/2, 31.690142-dy/2], width=15+3*dx, height=7.6056339,
            transform=ccrs.PlateCarree(), fill=False
        )) # TP
    
    return None