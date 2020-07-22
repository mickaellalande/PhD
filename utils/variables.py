#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import proplot as plot

# =============================================================================
# Select variable on CICLAD
# =============================================================================
def get_table(var):
    if var in ['tas', 'pr', 'prsn', 'ta']:
        table = 'Amon'
    elif var in ['snc']:
        table = 'LImon'
    else:
        raise NameError('The variable '+name+' is not defined')
        
    return table

def get_var_infos(var):
    if var in ['snc', 'frac_snow']:
        label = 'Snow Cover Extent'
        units = '%'
        cmap ='viridis'
        levels = plot.arange(0,100,10)
        
    elif var in ['tas', 't2m']:
        label = 'Near-Surface Air Temperature'
        units = '°C'
        cmap = 'CoolWarm'
        levels = plot.arange(-30,30,5)
        
    elif var in ['pr', 'tp', 'precip']:
        label = 'Total Precipitation'
        units = 'mm/day'
        cmap ='DryWet'
        levels = plot.arange(0,5,0.5)
        
    elif var == 'prsn':
        label = 'Snowfall'
        units = 'mm/day'
        cmap ='DryWet'
        levels = plot.arange(0,5,0.5)
        
    elif var == 'ua':
        label = 'Eastward Wind'
        units = 'm/s'
        cmap='CoolWarm'
        levels=plot.arange(-7,7,1)
        
    elif var == 'ta':
        label = 'Air Temperature'
        units = '°C'
        cmap='CoolWarm'
        levels=plot.arange(-7,7,1)
        
    else:
        raise NameError('The variable '+name+' is not defined')
        
    return label, units, cmap, levels
