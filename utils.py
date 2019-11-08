#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# =============================================================================
# Import modules
# =============================================================================
import psutil
import sys
import numpy as np
import xarray as xr
import pandas as pd
import calendar as cld


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
    return (ds * weights).groupby('time.season').sum(dim='time', skipna=False)


# Custom seasonal climatology (on monthly data set, include just month)
def custom_season_clim(ds, season, calendar='standard'):
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

    if isinstance(season, int):
        return (seasonal_data * weights).sum(dim='time', skipna=False).assign_coords(month=season)
    elif isinstance(season, str) and len(season) > 1:
        return (seasonal_data * weights).sum(dim='time', skipna=False).assign_coords(season=season)
    

# Climatology (on monthly data set)
def clim(ds, calendar='standard'):
    month_length = xr.DataArray(get_dpm(ds.time.to_index(), calendar=calendar), coords=[ds.time], name='month_length')
    weights = month_length / month_length.sum()
    np.testing.assert_allclose(weights.sum().values, np.ones(1))
    return (ds * weights).sum(dim='time', skipna=False)
    

# Yearly mean (on monthly data set)
def year_mean(ds, calendar='standard'):
    month_length = xr.DataArray(get_dpm(ds.time.to_index(), calendar=calendar), coords=[ds.time], name='month_length')
    normalize = month_length.astype(float).groupby('time.year').sum()
    weights = month_length.groupby('time.year') / normalize
    np.testing.assert_allclose(weights.groupby('time.year').sum().values, np.ones(normalize.year.size))
    return (ds * weights).groupby('time.year').sum(dim='time', skipna=False)






