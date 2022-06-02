import xarray as xr
import pandas as pd
import numpy as np

# For parallelisation
from dask.distributed import Client
client = Client(n_workers=16, threads_per_worker=1, memory_limit='300GB')

path_snow_CCI = 'ESA_CCI_SNOW/dap.ceda.ac.uk/neodc/esacci/snow/data/scfg'
path_AVHRR = path_snow_CCI+'/AVHRR_MERGED/v2.0'
path_MODIS = path_snow_CCI+'/MODIS/v2.0'

path_out = 'ESA_CCI_SNOW/preprocess/scfg'
path_out_AVHRR = path_out+'/AVHRR_MERGED/v2.0'
path_out_MODIS = path_out+'/MODIS/v2.0'

year_start = 2002
year_end = 2003

########################
### Define functions ###
########################
from pandas.tseries.offsets import MonthEnd

# Get previous month for interpolation
def get_prev_month_year(month, year):
    '''
    Returns the previous month and corresponding year.

        Parameters:
            month (string): string of 2 characters (e.g., '01')
            year (string): string (e.g., '2000')

        Returns:
            month_prev (string): string of 2 characters (e.g., '12')
            year_prev (string): string (e.g., '1999')
    '''
    if month == '01':
        year_prev = str(int(year) - 1)
        month_prev = '12'
    else:
        year_prev = year
        month_prev = str(int(month) - 1).zfill(2)
        
    return month_prev, year_prev

# Get next month for interpolation
def get_next_month_year(month, year):
    '''
    Returns the next month and corresponding year.

        Parameters:
            month (string): string of 2 characters (e.g., '01')
            year (string): string (e.g., '2000')

        Returns:
            month_prev (string): string of 2 characters (e.g., '02')
            year_prev (string): string (e.g., '2000')
    '''
    if month == '12':
        year_next = str(int(year) + 1)
        month_next = '01'
    else:
        year_next = year
        month_next = str(int(month) + 1).zfill(2)
        
    return month_next, year_next

# Round latitudes and longitudes to avoid errors with concatenation
def round_latlon(ds, latlon_round):
    '''
    Returns Dataset/DataArray with rounded latitudes and longitudes.

        Parameters:
            ds (Dataset/DataArray): xarray Dataset/Dataarray with coords lat/lon
            latlon_round (int): number of decimals

        Returns:
            xarray Dataset/DataArray
    '''
    return ds.assign_coords(lat=ds.lat.round(latlon_round), lon=ds.lon.round(latlon_round))

# Reindex time to get all days for interpolation
def reindex_time(ds, year, month):
    '''
    Returns Dataset/DataArray with all days in the corresponding month. Missing days will be filled with NaNs.

        Parameters:
            ds (Dataset/DataArray): monthly xarray Dataset/DataArray at daily time frequency
            year (string): string (e.g., '2000')
            month (string): string of 2 characters (e.g., '01')

        Returns:
            xarray Dataset/DataArray
    '''
    begin_date = pd.to_datetime(year+'-'+month+'-01')
    end_date = begin_date + MonthEnd(1) # Get the last day of the month
    return ds.reindex(time=pd.date_range(begin_date, end_date, freq='D'))

# Reindex time to get all days for interpolation
def open_files(path, year, month, common_file_string, chunk_lat, chunk_lon, latlon_round, var):
    '''
    Open all daily files for a given month in parallel.
    Format is e.g., path+'/1994/01/19940101'+common_file_string
        
        Need to have Dask client defined before, e.g.:
            from dask.distributed import Client
            client = Client(n_workers=32, threads_per_worker=1, memory_limit='6GB')

        Parameters:
            path (string): root path (e.g., 'ESA_CCI_SNOW/dap.ceda.ac.uk/neodc/esacci/snow/data/scfg/AVHRR_MERGED/v2.0')
            year (string): string (e.g., '2000')
            month (string): string of 2 characters (e.g., '01')
            common_file_string (string): e.g., '-ESACCI-L3C_SNOW-SCFG-AVHRR_MERGED-fv2.0.nc'
            chunk_lat (int): chunk over the latitude dimension
            chunk_lon (int): chunk over the longitude dimension
            latlon_round (int): number of decimals
            var (string): variable to open (e.g., 'scfg')

        Returns:
            da (DataArray): xarray DataArray
            attrs (dict): attributes from the original dataset
    '''
    ds = xr.open_mfdataset(path+'/'+year+'/'+month+'/*'+common_file_string, 
                           parallel=True, chunks={'lat': chunk_lat, 'lon': chunk_lon})
    da = ds[var]
    da = round_latlon(da, latlon_round) # round coordinates to avoid errors with concatenation
    da = reindex_time(da, year, month) # to fill missing days with NaNs
    print('Read files '+path+'/'+year+'/'+month+'/*'+common_file_string)
            
    return da, ds.attrs

# Print no file to open
def print_no_file(path, year, month):
    '''
    Print the folder where there is no file.

        Parameters:
            path (string): root path (e.g., 'ESA_CCI_SNOW/dap.ceda.ac.uk/neodc/esacci/snow/data/scfg/AVHRR_MERGED/v2.0')
            year (string): string (e.g., '2000')
            month (string): string of 2 characters (e.g., '01')
    '''
    print('No file to open in: '+path+'/'+year+'/'+month)

# Select last delta_interp days for previous period
def select_last_days(da_prev, year_prev, month_prev, delta_interp):
    '''
    Returns Dataset with the last delta_interp days.

        Parameters:
            da_prev (DataArray): monthly xarray DataArray at daily time frequency
            year_prev (string): string (e.g., '2000')
            month_prev (string): string of 2 characters (e.g., '01')
            delta_interp (int): maximum gap number of days for interpolation

        Returns:
            xarray DataArray
    '''
    end_date = pd.to_datetime(year_prev+'-'+month_prev) + MonthEnd(1) # Get the last day of the month
    begin_date = end_date - pd.DateOffset(days = delta_interp) # Get previous delta_interp days (max window for interpolation)
    return da_prev.sel(time=slice(begin_date, end_date))

# Select next delta_interp days for next period
def select_first_days(da_next, year_next, month_next, delta_interp):
    '''
    Returns Dataset with the last delta_interp days.

        Parameters:
            da_next (DataArray): monthly xarray DataArray at daily time frequency
            year_next (string): string (e.g., '2000')
            month_next (string): string of 2 characters (e.g., '01')
            delta_interp (int): maximum gap number of days for interpolation

        Returns:
            xarray DataArray
    '''
    return da_next.sel(time=slice(year_next+'-'+month_next+'-01', year_next+'-'+month_next+'-'+str(delta_interp).zfill(2)))
     
# Concatenate DataArrays over time
def concat_files(da1, da2, concat_string):
    '''
    Concatenate DataArrays and remove chunks over the time dimension.

        Parameters:
            da1, da2 (DataArray): monthly xarray DataArray at daily time frequency
            concat_string (string): description of concatenation (e.g., '[prev, current]')

        Returns:
            xarray DataArray
    '''
    concat = xr.concat([da1, da2], dim='time').chunk({'time': -1})
    print(' => Concatenate files '+concat_string)
    
    return concat  



#########################
### Run interpolation ###
#########################
import time

chunk_lat = 4500
chunk_lon = 9000
delta_interp = 10 # maximum gap number of days for interpolation
latlon_round = 3 # precision for lat/lon
common_file_string = '-ESACCI-L3C_SNOW-SCFG-MODIS_TERRA-fv2.0.nc'
var = 'scfg'

# for year in [str(y) for y in range(2000, 2021)]:
for year in [str(y) for y in range(year_start, year_end)]:
    for month in [str(m).zfill(2) for m in range(1, 13)]:
#     for month in [str(m).zfill(2) for m in range(12, 13)]:
        start_time = time.time() # Check time per loop
        
        # Get previous and next months for interpolation         
        month_prev, year_prev = get_prev_month_year(month, year)
        month_next, year_next = get_next_month_year(month, year)
        print('\n### '+year+'-'+month+' (prev: '+year_prev+'-'+month_prev+' / next: '+year_next+'-'+month_next+')')
        
        ##################
        ### Open files ###
        ##################
        # Test if there are files (ex: 1994-11 to 1995-01 no files for AVHRR)
        try:
            da, attrs = open_files(path_MODIS, year, month, common_file_string, chunk_lat, chunk_lon, latlon_round, var)
        except OSError:
            print_no_file(path_MODIS, year, month)
            continue # If there is no file, go to next iteration
        
        # Prev
        try:
            da_prev, _ = open_files(path_MODIS, year_prev, month_prev, common_file_string, chunk_lat, chunk_lon, latlon_round, var)
            da_prev = select_last_days(da_prev, year_prev, month_prev, delta_interp)
            concat = concat_files(da_prev, da, '[prev, current]')
            
            # Next
            try:
                da_next, _ = open_files(path_MODIS, year_next, month_next, common_file_string, chunk_lat, chunk_lon, latlon_round, var)
                da_next = select_first_days(da_next, year_next, month_next, delta_interp)
                concat = concat_files(concat, da_next, '[concat, next]')
            except OSError:
                print_no_file(path_MODIS, year_next, month_next)

        except OSError:
            print_no_file(path_MODIS, year_prev, month_prev)
        
            # Next
            try:
                da_next, _ = open_files(path_MODIS, year_next, month_next, common_file_string, chunk_lat, chunk_lon, latlon_round, var)
                da_next = select_first_days(da_next, year_next, month_next, delta_interp)
                concat = concat_files(da, da_next, '[current, next]')
            except OSError:
                print_no_file(path_MODIS, year_next, month_next)
                concat = da.chunk({'time': -1})

        ###############################################
        ### Get SCF values and, water and ice masks ###
        ###############################################
        scf = concat.where(concat <= 100)
        water = concat.where(concat == 210)
        ice = concat.where(concat == 215)
        
        ###############################
        ### Linear temporal gapfill ###
        ###############################
        scf_interp = scf.interpolate_na('time', method='linear', max_gap=pd.Timedelta(days=delta_interp))
        print(' => Doing interpolation...')

        # Deal with attributes
        scf_interp.name = var+'_interp'
        del scf_interp.attrs['valid_range']
        del scf_interp.attrs['flag_values']
        del scf_interp.attrs['flag_meanings']
        scf_interp.attrs['ancillary_variables'] = 'coverage, coverage_interp'
        scf_interp.attrs['method'] = var+".interpolate_na('time', method='linear', max_gap=pd.Timedelta(days=10))"

        # Compute time coverage
        coverage = scf.sel(time=year+'-'+month).count('time')
        coverage.name = 'coverage'
        coverage.attrs['long_name'] = 'Time Coverage'
        coverage.attrs['units'] = 'number of days'
        coverage.attrs['ancillary_variables'] = var

        coverage_interp = scf_interp.sel(time=year+'-'+month).count('time')
        coverage_interp.name = 'coverage_interp'
        coverage_interp.attrs['long_name'] = 'Time Coverage'
        coverage_interp.attrs['units'] = 'number of days'
        coverage_interp.attrs['ancillary_variables'] = var+'_interp'

        ice.name = 'mask_ice'
        ice.attrs['long_name'] = 'Permanent_Snow_and_Ice'
        del ice.attrs['units']
        del ice.attrs['standard_name']
        del ice.attrs['valid_range']
        del ice.attrs['actual_range']
        ice.attrs['flag_value'] = 215
        del ice.attrs['flag_values']
        del ice.attrs['flag_meanings']
        del ice.attrs['grid_mapping']
        del ice.attrs['ancillary_variables']

        water.name = 'mask_water'
        water.attrs['long_name'] = 'Water'
        del water.attrs['units']
        del water.attrs['standard_name']
        del water.attrs['valid_range']
        del water.attrs['actual_range']
        water.attrs['flag_value'] = 210
        del water.attrs['flag_values']
        del water.attrs['flag_meanings']
        del water.attrs['grid_mapping']
        del water.attrs['ancillary_variables']

        # Combine in a new dataset
        ds_interp = scf_interp.sel(time=year+'-'+month).to_dataset()
        ds_interp['coverage'] = coverage
        ds_interp['coverage_interp'] = coverage_interp
        ds_interp['mask_ice'] = ice[0]
        ds_interp['mask_water'] = water[0]
        ds_interp.attrs = {**{'processed': 'A linear interpolation on the time dimension is performed in this dataset. ' \
            'A maximum window of 10 days is imposed, if the gap is more than 10 days, the missing values are kept. ' \
            'Before interpolation the time dimension is reindexed in order to cover all days of the month, and fill missing days with NaNs.' \
            'Also the latitudes and longitudes are rounded to 3 digits after de decimal to avoid concatenation errors.' \
            'The temporal coverage of the data before and after interpolation is stored in the variables "coverage" and "coverage_interp". ' \
            'The permanent snow and ice, and water masks are also kept for later processing if needed. The original dataset is described below. ' \
            'Preprocess performed by Mickaël Lalande (https://mickaellalande.github.io/) on May 13, 2022. ' \
            'The same compression level is kept compared to the original dataset (zlib=True, complevel=4).'}, **attrs}

        # Compression
        comp = dict(zlib=True, complevel=4)
        encoding = {var: comp for var in ds_interp.data_vars}
        ds_interp.to_netcdf(path_out_MODIS+'/daily/'+year+'/'+year+month+'-ESACCI-L3C_SNOW-SCFG-MODIS_TERRA-fv2.0_interp.nc', encoding=encoding)
        print('Interpolated file saved to '+path_out_MODIS+'/daily/'+year+'/'+year+month+'-ESACCI-L3C_SNOW-SCFG-MODIS_TERRA-fv2.0_interp.nc')
        print("--- %s seconds ---" % (time.time() - start_time))
        
        
#########################
### Make monthly mean ###
#########################
root_path_in = '/bettik/lalandmi/phd/ESA_CCI_SNOW/preprocess/scfg/MODIS/v2.0/daily'
root_path_out = '/bettik/lalandmi/phd/ESA_CCI_SNOW/preprocess/scfg/MODIS/v2.0/monthly'

chunk_lat = 4500
chunk_lon = 9000

# for year in [str(y) for y in range(2000, 2021)]:
for year in [str(y) for y in range(year_start, year_end)]:
    start_time = time.time() # Check time per loop
    
    print('\n### '+year)
    
    ds = xr.open_mfdataset(root_path_in+'/'+year+'/*-ESACCI-L3C_SNOW-SCFG-MODIS_TERRA-fv2.0_interp.nc', parallel=True, chunks={'lat': chunk_lat, 'lon': chunk_lon})
    print('Read files '+root_path_in+'/'+year+'/*-ESACCI-L3C_SNOW-SCFG-MODIS_TERRA-fv2.0_interp.nc')
    
#     ds_month = ds.chunk({'time': -1}).resample(time='1M').mean() # too heavy
    ds_month = ds.resample(time='1M').mean()
    print(' => Perform monthly resample average...')
    
    ds_month.attrs = ds.attrs
    
     # Compression
    comp = dict(zlib=True, complevel=4)
    encoding = {var: comp for var in ds_month.data_vars}
    ds_month.to_netcdf(root_path_out+'/'+year+'-monthly-ESACCI-L3C_SNOW-SCFG-MODIS_TERRA-fv2.0_interp.nc', encoding=encoding)
    print('Monthly file saved to '+root_path_out+'/'+year+'-monthly-ESACCI-L3C_SNOW-SCFG-MODIS_TERRA-fv2.0_interp.nc')
    print("--- %s seconds ---" % (time.time() - start_time))
    
    
    
############################
### Make spatial average ###
############################
res_orig = 0.01

# for year in [str(y) for y in range(2000, 2021)]:
for year in [str(y) for y in range(year_start, year_end)]:
    
    print('\n### '+year)
    
    ds = xr.open_dataset(root_path_out+'/'+year+'-monthly-ESACCI-L3C_SNOW-SCFG-MODIS_TERRA-fv2.0_interp.nc', chunks={'time': 1})
    print('Read files '+root_path_out+'/'+year+'-monthly-ESACCI-L3C_SNOW-SCFG-MODIS_TERRA-fv2.0_interp.nc')
    
    for res in [0.1, 0.25, 0.5, 1]:
        start_time = time.time() # Check time per loop
        print(res)
        n_coarse = int(res/res_orig)
        da_coarse = ds.scfg_interp.coarsen(lat=n_coarse, lon=n_coarse).mean()
        da_coarse.name = 'scfg_interp_'+str(res)+'deg'

        da_coarse_icefilled = ds.scfg_interp.where(ds.mask_ice != 215, 100).coarsen(lat=n_coarse, lon=n_coarse).mean()
        da_coarse_icefilled.name = 'scfg_interp_'+str(res)+'deg_icefilled'

        ds_coarse = da_coarse.to_dataset()
        ds_coarse['scfg_interp_'+str(res)+'deg_icefilled'] = da_coarse_icefilled
        ds_coarse.attrs = ds.attrs

        print(' => Coarsen dataset to '+str(res)+'deg...')

         # Compression
        comp = dict(zlib=True, complevel=4)
        encoding = {var: comp for var in ds_coarse.data_vars}
        ds_coarse.to_netcdf(root_path_out+'_'+str(res)+'deg/'+year+'-monthly-ESACCI-L3C_SNOW-SCFG-MODIS_TERRA-fv2.0_interp_'+str(res)+'deg.nc', encoding=encoding)
        print('Monthly file saved to '+root_path_out+'_'+str(res)+'deg/'+year+'-monthly-ESACCI-L3C_SNOW-SCFG-MODIS_TERRA-fv2.0_interp_'+str(res)+'deg.nc')
        print("--- %s seconds ---" % (time.time() - start_time))
