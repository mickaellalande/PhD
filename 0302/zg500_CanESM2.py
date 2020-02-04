#!/usr/bin/env python3
#i -*- coding: utf-8 -*-
"""
Created on Feb 3, 2020

@author: gkrinner
"""

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc

fig, axs = plt.subplots(2, 2, figsize=(9, 5))

data = nc.Dataset('zg500_CanESM2_amip-bias-cor_vs_CNRM_198101-200012.nc')
zg500_bc_p = data.variables['ERR']
lat = data.variables['LAT'][:]
lon = data.variables['LON'][:]
lon, lat = np.meshgrid(lon, lat)
axs[0,0] = Basemap(projection='robin',lon_0=0,resolution='c')
axs[0,0].pcolormesh(lon, lat, zg500_bc_p[0,:,:], latlon=True, cmap='RdBu_r')
axs[0,0].drawcoastlines(color='lightgray')
data.close()

data = nc.Dataset('zg500_CanESM2_amip-bias-cor_vs_CNRM_208101-210012.nc')
zg500_bc_f = data.variables['ERR']
axs[0,1] = Basemap(projection='robin',lon_0=0,resolution='c')
axs[0,1].pcolormesh(lon, lat, zg500_bc_f[0,:,:], latlon=True, cmap='RdBu_r')
axs[0,1].drawcoastlines(color='lightgray')
data.close()

plt.show()

