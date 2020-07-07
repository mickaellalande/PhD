#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.patches as mpatches
import cartopy.crs as ccrs

# =============================================================================
# Zones
# =============================================================================

def get_domain_HMA():
    latlim = slice(20,45)
    lonlim = slice(60,110)
    
    return latlim, lonlim


# HKK: Hindu-Kush / Karakoram / Western Himalay
# HM: Central and Est Himalaya
# TB: Tibetan Plateau
def get_zones():
    lonlim_HK = (70, 81 ); latlim_HK = (31, 40)
    lonlim_HM = (79, 98 ); latlim_HM = (26, 31)
    lonlim_TP = (81, 104); latlim_TP = (31, 39)
    
    return lonlim_HK, latlim_HK, lonlim_HM, latlim_HM, lonlim_TP, latlim_TP


def plot_zones(ax):
    lonlim_HK, latlim_HK, lonlim_HM, latlim_HM, lonlim_TP, latlim_TP = get_zones()
    
    # HKK
    ax.text(lonlim_HK[0]+0.5, latlim_HK[1]-2, 'HKK', zorder=10)
    ax.add_patch(
        mpatches.Rectangle(
            xy = [lonlim_HK[0], latlim_HK[0]], 
            width = lonlim_HK[1]-lonlim_HK[0], height = latlim_HK[1]-latlim_HK[0],
            transform = ccrs.PlateCarree(), fill = False, zorder=10
        )
    )

    # HM
    ax.text(lonlim_HM[0]+0.5, latlim_HM[1]-2, 'HM', zorder=10)
    ax.add_patch(
        mpatches.Rectangle(
            xy = [lonlim_HM[0], latlim_HM[0]], 
            width = lonlim_HM[1]-lonlim_HM[0], height = latlim_HM[1]-latlim_HM[0],
            transform = ccrs.PlateCarree(), fill = False, zorder=10
        )
    )

    # TP
    ax.text(lonlim_TP[0]+0.5, latlim_TP[1]-2, 'TP', zorder=10)
    ax.add_patch(
        mpatches.Rectangle(
            xy = [lonlim_TP[0], latlim_TP[0]], 
            width = lonlim_TP[1]-lonlim_TP[0], height = latlim_TP[1]-latlim_TP[0],
            transform = ccrs.PlateCarree(), fill = False, zorder=10
        )
    )
    
    return None