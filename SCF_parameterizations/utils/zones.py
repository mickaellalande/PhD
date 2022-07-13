#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Autopep8: https://pypi.org/project/autopep8/
# Check with http://pep8online.com/

import matplotlib.patches as mpatches
import cartopy.crs as ccrs

# =============================================================================
# Zones
# =============================================================================


def get_zone(zone):
    """
        Get the latitude and longitude limits for the corresponding zone.

        Parameters
        ----------
        zone : str
            Zone name. Options are:

            - 'GLOB', 'global', 'GLOBAL', 'GLOB-land'
            - 'NH' : North Hemisphere
            - 'HMA' : High Mountain of Asia
            - 'NA' : North America

        Returns
        -------
        latlim, lonlim : slice
            Latitude and longitude limits of the zone.

        Example
        -------
        >>> import sys
        >>> sys.path.insert(1, '/home/mlalande/notebooks/utils')
        >>> import utils as u
        >>>
        >>>
        >>> latlim, lonlim = u.get_zone('HMA')

    """

    # Global
    if zone in ['GLOB', 'global', 'GLOBAL', 'GLOB-land']:
        latlim = slice(None)
        lonlim = slice(None)
        
    # North Hemisphere
    elif zone in ['NH']:
        latlim = slice(0, 90)
        lonlim = slice(None)

    # High Mountain of Asia (HMA)
    elif zone in ['HMA']:
        latlim = slice(20, 50)
        lonlim = slice(60, 110)
#         latlim = slice(20,45)
#         lonlim = slice(60,110)

    # North America
    elif zone in ['NA']:
        latlim = slice(0, 70)
        lonlim = slice(-150, -80)

    else:
        raise ValueError(
            f"""Invalid zone argument: '{zone}'. Valid zones are:
                - 'GLOB', 'global', 'GLOBAL'
                - 'NH' : North Hemisphere
                - 'HMA' : High Mountain of Asia
                - 'NA' : North America
             """
        )

    return latlim, lonlim


def get_domain_HMA():
    latlim = slice(20, 45)
    lonlim = slice(60, 110)

    return latlim, lonlim


# HKK: Hindu-Kush / Karakoram / Western Himalay
# HM: Central and Est Himalaya
# TB: Tibetan Plateau
def get_zones():
    lonlim_TS = slice(68, 96)
    latlim_TS = slice(40, 45)
    lonlim_HK = slice(68, 80)
    latlim_HK = slice(31, 40)
    lonlim_TP = slice(80, 105)
    latlim_TP = slice(31, 40)
    lonlim_HM = slice(77, 104)
    latlim_HM = slice(26, 31)

    return lonlim_TS, latlim_TS, lonlim_HK, latlim_HK, lonlim_TP, latlim_TP, lonlim_HM, latlim_HM


def plot_zones(ax):
    lonlim_TS, latlim_TS, lonlim_HK, latlim_HK, lonlim_TP, latlim_TP, lonlim_HM, latlim_HM = \
        get_zones()

    # HKK
    ax.text(lonlim_HK.start + 0.5, latlim_HK.stop - 2.5, 'HK', zorder=10)
    ax.add_patch(
        mpatches.Rectangle(
            xy=[lonlim_HK.start, latlim_HK.start],
            width=lonlim_HK.stop - lonlim_HK.start,
            height=latlim_HK.stop - latlim_HK.start,
            transform=ccrs.PlateCarree(),
            fill=False,
            zorder=10
        )
    )

    # HM
    ax.text(lonlim_HM.start + 0.5, latlim_HM.stop - 2.5, 'HM', zorder=10)
    ax.add_patch(
        mpatches.Rectangle(
            xy=[lonlim_HM.start, latlim_HM.start],
            width=lonlim_HM.stop - lonlim_HM.start,
            height=latlim_HM.stop - latlim_HM.start,
            transform=ccrs.PlateCarree(),
            fill=False,
            zorder=10
        )
    )

    # TP
    ax.text(lonlim_TP.start + 0.5, latlim_TP.stop - 2.5, 'TP', zorder=10)
    ax.add_patch(
        mpatches.Rectangle(
            xy=[lonlim_TP.start, latlim_TP.start],
            width=lonlim_TP.stop - lonlim_TP.start,
            height=latlim_TP.stop - latlim_TP.start,
            transform=ccrs.PlateCarree(),
            fill=False,
            zorder=10
        )
    )
    
    
    # TS
    ax.text(lonlim_TS.start + 0.5, latlim_TS.stop - 2.5, 'TS', zorder=10)
    ax.add_patch(
        mpatches.Rectangle(
            xy=[lonlim_TS.start, latlim_TS.start],
            width=lonlim_TS.stop - lonlim_TS.start,
            height=latlim_TS.stop - latlim_TS.start,
            transform=ccrs.PlateCarree(),
            fill=False,
            zorder=10
        )
    )

    return None

def plot_gridcell(ax, lat, lon, color):

    ax.add_patch(
        mpatches.Rectangle(
            xy=[lon.start, lat.start],
            width=lon.stop - lon.start,
            height=lat.stop - lat.start,
            transform=ccrs.PlateCarree(),
            fill=False,
            zorder=10,
            color=color
        )
    )

    return None
