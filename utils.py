#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# =============================================================================
# Import modules
# =============================================================================
import psutil
import os
import sys
import numpy as np
import xarray as xr
import pandas as pd
import calendar as cld
from cartopy.util import add_cyclic_point


# =============================================================================
# Basic functions
# =============================================================================
def check_python_version():
    print(sys.version)

def check_virtual_memory():
    # https://psutil.readthedocs.io/en/latest/#psutil.virtual_memory
    values = psutil.virtual_memory()
    print("Virtual memory usage - " +
          "total: " + str(get_human_readable_size(values.total)) + " / " +
          "available: " + str(get_human_readable_size(values.available)) + " / " +
          "percent used: " + str(values.percent) + " %"
          )

def get_human_readable_size(num):
    # https://stackoverflow.com/questions/21792655/psutil-virtual-memory-units-of-measurement
    exp_str = [ (0, 'B'), (10, 'KB'),(20, 'MB'),(30, 'GB'),(40, 'TB'), (50, 'PB'),]               
    i = 0
    while i+1 < len(exp_str) and num >= (2 ** exp_str[i+1][0]):
        i += 1
        rounded_val = round(float(num) / 2 ** exp_str[i][0], 2)
    return '%s %s' % (int(rounded_val), exp_str[i][1])

def deg2km(nlon, nlat, lat):
    # Gives the size of a grid cell in km at the corresponding latitude
    R_earth = 6371
    x = 2*np.pi*R_earth/nlon*np.cos(np.deg2rad(lat))
    y = np.pi*R_earth/nlat
    return {'x': x, 'y': y, 'units': 'km'}


# =============================================================================
# Compute monthly weighted data
# =============================================================================
# http://xarray.pydata.org/en/stable/examples/monthly-means.html
dpm = {'noleap': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       '365_day': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       'standard': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       'gregorian': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       'proleptic_gregorian': [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       'all_leap': [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       '366_day': [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
       '360_day': [0, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]}

def leap_year(year, calendar='standard'):
    """Determine if year is a leap year"""
    leap = False
    if ((calendar in ['standard', 'gregorian',
        'proleptic_gregorian', 'julian']) and
        (year % 4 == 0)):
        leap = True
        if ((calendar == 'proleptic_gregorian') and
            (year % 100 == 0) and
            (year % 400 != 0)):
            leap = False
        elif ((calendar in ['standard', 'gregorian']) and
                 (year % 100 == 0) and (year % 400 != 0) and
                 (year < 1583)):
            leap = False
    return leap

def get_dpm(time, calendar='standard'):
    """
    return a array of days per month corresponding to the months provided in `months`
    """
    month_length = np.zeros(len(time), dtype=np.int)

    cal_days = dpm[calendar]

    for i, (month, year) in enumerate(zip(time.month, time.year)):
        month_length[i] = cal_days[month]
        if leap_year(year, calendar=calendar) and month == 2:
            month_length[i] += 1
    return month_length


# Seasonal climatology (on monthly data set)
def season_clim(ds, calendar='standard'):
    # Make a DataArray with the number of days in each month, size = len(time)
    month_length = xr.DataArray(get_dpm(ds.time.to_index(), calendar=calendar),
                                coords=[ds.time], name='month_length')
    # Calculate the weights by grouping by 'time.season'
    weights = month_length.groupby('time.season') / month_length.groupby('time.season').sum()

    # Test that the sum of the weights for each season is 1.0
    np.testing.assert_allclose(weights.groupby('time.season').sum().values, np.ones(4))

    # Calculate the weighted average
    with xr.set_options(keep_attrs=True):
        return (ds * weights).groupby('time.season').sum(dim='time', skipna=False)


# Custom seasonal climatology (on monthly data set, include just month)
def custom_season_clim(ds, calendar='standard', season=1):
    month_length = xr.DataArray(get_dpm(ds.time.to_index(), calendar=calendar), coords=[ds.time], name='month_length')
    
    # Deal with custom season (string or int for single month)
    month = ds['time.month']
    
    if isinstance(season, int):
        season_sel = (month == season)
    elif isinstance(season, str) and len(season) > 1:
        season_str = 'JFMAMJJASONDJFMAMJJASOND'
        
        month_start = season_str.index(season) + 1
        month_end = month_start + len(season) - 1

        if month_end > 12:
            month_end -= 12
            season_sel = (month >= month_start) | (month <= month_end)
        else:
            season_sel = (month >= month_start) & (month <= month_end)
        
    else:
        raise ValueError('The season is not valid (string or int for single month)')
        
    seasonal_data = ds.sel(time=season_sel)
    weights = month_length.sel(time=season_sel) / month_length.astype(float).sel(time=season_sel).sum()
    np.testing.assert_allclose(weights.sum().values, np.ones(1))
    
    with xr.set_options(keep_attrs=True):
        if isinstance(season, int):
            return (seasonal_data * weights).sum(dim='time', skipna=False).assign_coords(month=season)
        elif isinstance(season, str) and len(season) > 1:
            return (seasonal_data * weights).sum(dim='time', skipna=False).assign_coords(season=season)
    

# Climatology (on monthly data set)
def clim(ds, calendar='standard'):
    month_length = xr.DataArray(get_dpm(ds.time.to_index(), calendar=calendar), coords=[ds.time], name='month_length')
    weights = month_length / month_length.sum()
    np.testing.assert_allclose(weights.sum().values, np.ones(1))
    with xr.set_options(keep_attrs=True):
        return (ds * weights).sum(dim='time', skipna=False)
    

# Yearly mean (on monthly data set)
def year_mean(da, calendar='standard', season='annual'):
    # season = 'DJF' can be string
    # season = 1 or int for a single month

    month_length = xr.DataArray(get_dpm(da.time.to_index(), calendar=calendar), coords=[da.time], name='month_length')
    # Deal with custom season (string or int for single month)
    month = da['time.month']

    if isinstance(season, int):
        season_sel = (month == season)
        with xr.set_options(keep_attrs=True):
            season_mean = da.sel(time=season_sel)

    elif isinstance(season, str) and len(season) > 1:
        
        if season == 'annual':
            normalize = month_length.astype(float).groupby('time.year').sum()
            weights = month_length.groupby('time.year') / normalize
            np.testing.assert_allclose(weights.groupby('time.year').sum().values, np.ones(normalize.year.size))
            with xr.set_options(keep_attrs=True):
                season_mean = (da * weights).groupby('time.year').sum(dim='time', skipna=False)
        
        else:
            season_str = 'JFMAMJJASONDJFMAMJJASOND'

            month_start = season_str.index(season) + 1
            month_end = month_start + len(season) - 1

            if month_end > 12:
                # Remove one year (.isel(time=slice(month_end,-(12-month_start+1)))) to have continious months
                # The month/year label is from the starting month

                # Checked with cdo: !cdo yearmonmean -selmon,10,11,12 -shifttime,-2mo in.nc out.nc
                # -> slight differences, is CDO do not take the right month weights when shifted?
                # -> or do I use the wrong weights?
                # https://code.mpimet.mpg.de/boards/1/topics/826
                # 
                # !cdo yearmean -selmon,10,11,12 -shifttime,-2mo in.nc out.nc
                # Same results with the calendar=360_day
                #
                # Try with cdo season selection?
                
                # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects

                month_end -= 12
                season_sel = (month >= month_start) | (month <= month_end)
                seasonal_data = da.sel(time=season_sel).isel(time=slice(month_end,-(12-month_start+1)))
                seasonal_month_length = month_length.astype(float).sel(time=season_sel).isel(time=slice(month_end,-(12-month_start+1)))
                weights = xr.DataArray(
                   [value/seasonal_month_length.resample(time='AS-'+cld.month_abbr[month_start]).sum().values[i//len(season)] \
                         for i, value in enumerate(seasonal_month_length.values)],
                    coords = [month_length.sel(time=season_sel).isel(time=slice(month_end,-(12-month_start+1))).time],
                    name = 'weights'
                                      )
                sum_weights = weights.resample(time='AS-'+cld.month_abbr[month_start]).sum()
                np.testing.assert_allclose(sum_weights.values, np.ones(sum_weights.size))
                with xr.set_options(keep_attrs=True):
                    season_mean = (seasonal_data * weights).resample(time='AS-'+cld.month_abbr[month_start])\
                                                           .sum('time', skipna=False)
                # To keep same format as the version bellow (be aware that the year label will be from the first month)
                season_mean = season_mean.assign_coords({"time": season_mean['time.year']})
                season_mean = season_mean.rename({'time': 'year'})


            else:
                # Checked with CDO (!cdo yearmonmean -selmonth,'' in.nc out.nc)
                season_sel = (month >= month_start) & (month <= month_end)
                seasonal_data = da.sel(time=season_sel)
                normalize = month_length.astype(float).sel(time=season_sel).groupby('time.year').sum()
                weights = month_length.sel(time=season_sel).groupby('time.year') / normalize
                np.testing.assert_allclose(weights.groupby('time.year').sum().values, np.ones(normalize.size))
                with xr.set_options(keep_attrs=True):
                    season_mean = (seasonal_data * weights).groupby('time.year').sum('time', skipna=False)


    else:
        raise ValueError('The season is not valid (string or int for single month)')
        
    return season_mean

# Annual cycle (on monthly data set)
def annual_cycle(ds, calendar='standard'):
    month_length = xr.DataArray(get_dpm(ds.time.to_index(), calendar=calendar), coords=[ds.time], name='month_length')
    weights = month_length.groupby('time.month') / month_length.astype(float).groupby('time.month').sum()
    np.testing.assert_allclose(weights.groupby('time.month').sum().values, np.ones(12))
    with xr.set_options(keep_attrs=True):
        return (ds * weights).groupby('time.month').sum(dim='time', skipna=False)



# =============================================================================
# Compute spatial average
# =============================================================================
# https://pangeo.io/use_cases/physical-oceanography/sea-surface-height.html
def spatial_average(da):
    
    # Get the longitude and latitude names + other dimensions to test that the sum of weights is right
    lat_str = ''
    lon_str = ''
    other_dims_str = []
    for dim in da.dims:
        if dim in ['lat', 'latitude']: 
            lat_str = dim
        elif dim in ['lon', 'longitude']: 
            lon_str = dim
        else:
            other_dims_str.append(dim)
    
    # Compute the weights
    coslat = np.cos(np.deg2rad(da.lat)).where(~da.isnull())
    weights = coslat / coslat.sum(dim=(lat_str, lon_str))
    
    # Test that the sum of weights equal 1
    np.testing.assert_allclose(
        weights.sum(dim=(lat_str,lon_str)).values, 
        np.ones([da.coords[dim_str].size for dim_str in other_dims_str]),
        rtol=1e-06
    )
    
    with xr.set_options(keep_attrs=True):
        return (da * weights).sum(dim=(lat_str,lon_str))
    

    
# =============================================================================
# Add cyclic point
# =============================================================================
# https://github.com/darothen/plot-all-in-ncfile/blob/master/plot_util.py
def cyclic_dataarray(da, coord='lon'):
    """ Add a cyclic coordinate point to a DataArray along a specified
    named coordinate dimension.
    """
    assert isinstance(da, xr.DataArray)

    lon_idx = da.dims.index(coord)
    cyclic_data, cyclic_coord = add_cyclic_point(da.values,
                                                 coord=da.coords[coord],
                                                 axis=lon_idx)

    # Copy and add the cyclic coordinate and data
    new_coords = dict(da.coords)
    new_coords[coord] = cyclic_coord
    new_values = cyclic_data

    new_da = xr.DataArray(new_values, dims=da.dims, coords=new_coords)

    # Copy the attributes for the re-constructed data and coords
    for att, val in da.attrs.items():
        new_da.attrs[att] = val
    for c in da.coords:
        for att in da.coords[c].attrs:
            new_da.coords[c].attrs[att] = da.coords[c].attrs[att]

    return new_da


# =============================================================================
# Get data
# =============================================================================
def get_data_IPSL_CM6A_LR(
    variable, 
    experiment='historical', 
    n_realization = 'all', 
    time=None, lat=None, lon=None, plev=None, chunks=None
):
    
#     warning  : no file found for {'domain': 'global', 'experiment': 'historical', 'institute': '*', 'table': 'LImon', 'period': 1979-2008, 'simulation': '', 'project': 'CMIP6', 'version': 'latest', 'grid': 'g*', 'realization': '*', 'variable': 'snc', 'mip': '*', 'model': 'IPSL-CM6A-LR', 'root': '/bdd'}, at these data locations ['${root}/CMIP6/${mip}/${institute}/${model}/${experiment}/${realization}/${table}/${variable}/${grid}/${version}/${variable}_${table}_${model}_${experiment}_${realization}_${grid}_${PERIOD}.nc', '${root}/CMIP6/${mip}/${institute}/${model}/${experiment}/${realization}/${table}/${variable}/${grid}/${version}/${variable}_${table}_${model}_${experiment}_${realization}_${grid}.nc'] 
# warning  : Please check these empty attributes ['simulation']
    
    # For concatenating all members
    list_da = []
    
    # Define the table depending the variable
    if variable in ['snc']: table = 'LImon'
    if variable in ['pr', 'ua', 'va']: table = 'Amon' 
        
    # Define the mip depending of the experiment
    if experiment in ['historical', 'amip']: mip = 'CMIP'
    if experiment in ['land-hist']: mip = 'LS3MIP'
    
    # Check the number of realizations
    if n_realization == 'all':
        realization_names = [name for name in os.listdir('/bdd/CMIP6/'+mip+'/IPSL/IPSL-CM6A-LR/'+experiment+'/')]
        # I don't take directly the realization_names because they are not sorted 
        # and even .sort() doesn't work because the numbers are not on 2 digits (like 01 instead of 1)
        n_realization = len(realization_names)
    
    for i in range(1,n_realization+1):
        
#         path = '/bdd/CMIP6/'+mip+'/IPSL/IPSL-CM6A-LR/'+experiment+'/r'+str(i)+'i1p1f1/'+table+'/'+variable+'/gr/latest/'\
#                +variable+'_'+table+'_IPSL-CM6A-LR_'+experiment+'_r'+str(i)+'i1p1f1_gr_185001-201412.nc'
        
        # use xr.open_mfdataset instead of xr.open_dataset to be able to put * file so I don't have to specify the time
        # for now I saw only one file per folder on ciclad
        path = '/bdd/CMIP6/'+mip+'/IPSL/IPSL-CM6A-LR/'+experiment+'/r'+str(i)+'i1p1f1/'+table+'/'+variable+'/gr/latest/*'
        
        temp = xr.open_mfdataset(path, chunks=chunks, combine='by_coords')[variable]
        
        if time is not None: temp = temp.sel(time=time)
        if lat is not None: temp = temp.sel(lat=lat)
        if lon is not None: temp = temp.sel(lon=lon)
        if plev is not None: temp = temp.sel(plev=plev)
            
        list_da.append(temp)


    data = xr.concat(
        list_da, 
        pd.Index(['r'+str(i)+'i1p1f1' for i in range(1,n_realization+1)], name='realization')
    )
    
    return data


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



# =============================================================================
# Select model on CICLAD
# =============================================================================
def select_model(name, var):
    if name in ['AWI-CM-1-1-MR']:
        institude = 'AWI'
        grid = 'gn'
        
    elif name in ['BCC-CSM2-MR', 'BCC-ESM1']:
        institude = 'BCC'
        grid = 'gn'
        
    elif name in ['CAMS-CSM1-0']:
        institude = 'CAMS'
        grid = 'gn'
        
    elif name in ['CESM2', 'CESM2-FV2', 'CESM2-WACCM', 'CESM2-WACCM-FV2']:
        institude = 'NCAR'
        grid = 'gn'
        
    elif name in ['CanESM5']:
        institude = 'CCCma'
        grid = 'gn'
        
    elif name in ['E3SM-1-0', 'E3SM-1-1']:
        institude = 'E3SM-Project'
        grid = 'gr'
    
    elif name in ['EC-Earth3-Veg']:
        institude = 'EC-Earth-Consortium'
        grid = 'gr'
        
    elif name in ['FGOALS-f3-L', 'FGOALS-g3']:
        institude = 'CAS'
        grid = 'gr'
        if var == 'snc': grid = 'gn'
        
    elif name in ['FIO-ESM-2-0']:
        institude = 'FIO-QLNM'
        grid = 'gn'
        
    elif name in ['GFDL-CM4', 'GFDL-ESM4']:
        institude = 'NOAA-GFDL'
        grid = 'gr1'
        
    elif name in ['GISS-E2-1-G', 'GISS-E2-1-G-CC', 'GISS-E2-1-H']:
        institude = 'NASA-GISS'
        grid = 'gn'
        
    elif name in ['INM-CM4-8', 'INM-CM5-0']:
        institude = 'INM'
        grid = 'gr1'
        
    elif name in ['IPSL-CM6A-LR']:
        institude = 'IPSL'
        grid = 'gr'
        
    elif name in ['MCM-UA-1-0']:
        institude = 'UA'
        grid = 'gn'
        
    elif name in ['MIROC6']:
        institude = 'MIROC'
        grid = 'gn'
        
    elif name in ['MPI-ESM-1-2-HAM']:
        institude = 'HAMMOZ-Consortium'
        grid = 'gn'
        
    elif name in ['MPI-ESM1-2-HR', 'MPI-ESM1-2-LR']:
        institude = 'MPI-M'
        grid = 'gn'
        
    elif name in ['MRI-ESM2-0']:
        institude = 'MRI'
        grid = 'gn'
        
    elif name in ['NESM3']:
        institude = 'NUIST'
        grid = 'gn'
        
    elif name in ['NorCPM1', 'NorESM2-LM', 'NorESM2-MM']:
        institude = 'NCC'
        grid = 'gn'
        
    elif name in ['SAM0-UNICON']:
        institude = 'SNU'
        grid = 'gn'
        
    elif name in ['TaiESM1']:
        institude = 'AS-RCEC'
        grid = 'gn'
        
    else:
        raise NameError('The model '+name+' is not defined')
        

    return institude, grid




# =============================================================================
# Select variable on CICLAD
# =============================================================================
def get_table(var):
    if var in ['tas', 'pr', 'ta']:
        table = 'Amon'
    elif var in ['snc']:
        table = 'LImon'
    else:
        raise NameError('The variable '+name+' is not defined')
        
    return table


























