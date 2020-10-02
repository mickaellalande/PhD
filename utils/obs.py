#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Get observations and reanalyses

import numpy as np
import xarray as xr
from regrid import regrid
import utils as u


def get_obs(var, obs_name, period=slice(None), machine='CICLAD', regrid=None):
    """
        Get observation data in a DataArray (http://xarray.pydata.org/en/stable/data-structures.html) on a specific machine and performs a bilinear interpolation using xESMF (https://xesmf.readthedocs.io/en/latest/) if necessary.

        Parameters
        ----------
        var : str 
            Variable name. Options are:
            
            - 'snc'
            - 'tas'
            - 'pr'

        obs_name : str
            Observation name. Options are:
            
            - 'NOAA_CDR_v1' (for 'snc')
            - 'MEaSUREs_v1' (for 'snc')

        period : slice, optional
            Time period (ex: slice('1979','2014')). Default is no slicing.

        machine : str, optional
            Machine name. Default is CICLAD. Options are:
            
            - 'CICLAD'

        regrid : xarray.core.dataarray.DataArray, xarray.core.dataset.Dataset, optional
            Data towards which the observation will be regrided. Default does not 
            make any interpolation.

        Returns
        -------
        obs : xarray.core.dataarray.DataArray
            Observation data on monthly time scale.

        Example
        -------
        >>> import xarray as xr
        >>> import sys
        >>> sys.path.insert(1, '/home/mlalande/notebooks/utils')
        >>> import utils as u
        >>>
        >>> snc_ref = xr.open_dataset(...)
        >>> obs = u.get_obs('snc', 'NOAA_CDR_v1', period=slice('1979','2014'), 
                             machine='CICLAD', regrid=snc_ref)

    """

    #########################
    ### Snow Cover Extent ###
    #########################
    if var in ['snc']:

        # NOAA Climate Data Record (CDR) of Northern Hemisphere (NH) Snow Cover Extent (SCE), Version 1
        # https://data.nodc.noaa.gov/cgi-bin/iso?id=gov.noaa.ncdc:C00756
        if obs_name == 'NOAA_CDR_v1':

            # Select machine
            if machine in ['CICLAD']:
                path = '/data/mlalande/RUTGERS/nhsce_v01r01_19661004_20191202.nc'
            else:
                raise ValueError(
                    f"Invalid machine argument: '{machine}'. Valid names are: 'CICLAD'.")

            # Get raw data
            ds = xr.open_dataset(path)
            u.check_first_last_year(period, ds)

            # Get the snc variable, keep only land data and convert to %
            with xr.set_options(keep_attrs=True):
                obs = ds.sel(time=period).snow_cover_extent.where(ds.land == 1)*100
            obs.attrs['units'] = '%'
            obs.attrs['obs_longname'] = "NOAA/NCDC Climate Data Record, Version 1"
            obs.attrs['obs_shortname'] = 'NOAA/NCDC CDR'

            # Rename lon and lat for the regrid
            obs = obs.rename({'longitude': 'lon', 'latitude': 'lat'})

            # Resamble data per month (from per week)
            obs = obs.resample(time='1MS').mean('time', skipna='False', keep_attrs=True)
            u.check_period_size(period, obs, ds, frequency='monthly')

        # MEaSUREs Northern Hemisphere Terrestrial Snow Cover Extent Daily 25km EASE-Grid 2.0, Version 1
        # https://nsidc.org/data/nsidc-0530
        elif obs_name == 'MEaSUREs_v1':

            # Select machine
            if machine in ['CICLAD']:
                path = '/data/mlalande/MEaSUREs/monthly/nhtsd25e2_*_v01r01.nc'
            else:
                raise ValueError(
                    f"Invalid machine argument: '{machine}'. Valid names are: 'CICLAD'.")

            # Get raw data
            ds = xr.open_mfdataset(path, combine='by_coords')
            u.check_first_last_year(period, ds)

            # Select period
            obs = ds.sel(time=period)
            u.check_period_size(period, obs, ds, frequency='monthly')

            # Get the snc variable and convert to %
            with xr.set_options(keep_attrs=True):
                obs = ds.merged_snow_cover_extent * 100
            obs.attrs['units'] = '%'
            obs.attrs['obs_longname'] = "MEaSUREs Northern Hemisphere Terrestrial Snow Cover Extent Daily 25km EASE-Grid 2.0, Version 1"
            obs.attrs['obs_shortname'] = 'MEaSUREs'

            # Rename lon and lat for the regrid
            obs = obs.rename({'longitude': 'lon', 'latitude': 'lat'})

        else:
            raise ValueError(
                f"Invalid obs_name argument: '{obs_name}'. Valid names are: 'NOAA_CDR_v1'.")

    ######################
    #### Precipitation ###
    ######################
    elif var in ['pr']:
        if obs_name == 'APHRODITE':
            pass
        else:
            raise ValueError(
                f"Invalid obs_name argument: '{obs_name}'. Valid names are: 'APHRODITE'.")

    #####################################
    #### Near-Surface Air Temperature ###
    #####################################
    elif var in ['tas']:
        if obs_name == 'CRU':
            pass
        else:
            raise ValueError(f"Invalid obs_name argument: '{obs_name}'. Valid names are: 'CRU'.")

    else:
        raise ValueError(f"Invalid var argument: '{var}'. Valid names are: 'snc', 'tas', 'pr'.")

    ###############
    #### Regrid ###
    ###############
    if regrid is not None:

        # Chekc if data is global and/or periodic or not
        obs_names_not_global = ['NOAA_CDR_v1', 'MEaSUREs_v1']
        if obs_name in obs_names_not_global:
            globe = False
        else:
            globe = True
            
        obs_names_not_periodic = ['NOAA_CDR_v1']
        if obs_name in obs_names_not_periodic:
            periodic = False
        else:
            periodic = True

        obs = u.regrid(obs, regrid, 'bilinear', globe=globe, periodic=periodic, reuse_weights=True)

    return obs
