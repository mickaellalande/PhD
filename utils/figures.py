#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Autopep8: https://pypi.org/project/autopep8/
# Check with http://pep8online.com/

# Make different plot types

import proplot as plot
from variables import get_var_infos


def plot_ref_new_obs(
    var, ref, new, obs, label, units,
    levels, cmap, extend,
    levels_diff, cmap_diff, extend_diff,
    levels_bias, cmap_bias, extend_bias,
    save=False, dpi=300
):
    """
        Plot 2 simulations versus observations. First row contains the 2
        simulations and their differences (diff). Second raw contains their
        bias regarding to observation and the observation itself.

        Parameters
        ----------
        var : str
            Variable name. Options are:

            - 'snc', 'frac_snow'
            - 'tas'
            - 'pr'

        label : str
            Name of the variable.

        units : str
            Units of the variables.

        ref, new, obs : DataArray
            Reference, new simulation and observation. Needs to have the
            attributes 'title' for the name of the plots and 'period' for the
            suptitle and saving the figure.

        levels, levels_diff, levels_bias : numpy.ndarray, optional
            Levels for the plots.

        cmap, cmap_diff, cmap_bias : colormap spec
            Colormaps for the plots.

        extend, extend_diff, extend_bias : numpy.ndarray
            Extends for the plots.

        save : bool, optional
            Save the figure or not. Default is None (does not save the figure).
            Save figures to jpg, png and pdf.

        dpi : int, optional
            DPI of the figure. Default is 300.

        Example
        -------
        >>> import xarray as xr
        >>> import proplot as plot
        >>> import sys
        >>> sys.path.insert(1, '/home/mlalande/notebooks/utils')
        >>> import utils as u
        >>>
        >>> period = slice('1979','2014')
        >>> var = 'snc'
        >>> label, units, cmap = u.get_var_infos('snc')
        >>>
        >>> ref = xr.open_dataarray(...); ref.attrs['title'] = ...
        >>> new = xr.open_dataarray(...); new.attrs['title'] = ...
        >>> obs = xr.open_dataarray(...); obs.attrs['title'] = ...
        >>>
        >>> clim_ref = u.clim(ref.sel(time=period))
        >>> clim_new = u.clim(ref.sel(time=period))
        >>> clim_obs = u.clim(ref.sel(time=period))
        >>>
        >>> levels = plot.arange(0,100,10)
        >>> extend = 'neither'
        >>>
        >>> levels_diff = plot.arange(-30,30,5)
        >>> cmap_diff = 'BuRd_r'
        >>> extend_diff = 'both'
        >>>
        >>> levels_bias = plot.arange(-100,100,20)
        >>> cmap_bias = 'BuRd_r'
        >>> extend_bias = 'neither'
        >>>
        >>> u.plot_ref_new_obs(
                var, clim_ref, clim_new, clim_obs, label, units,
                levels, cmap, extend,
                levels_diff, cmap_diff, extend_diff,
                levels_bias, cmap_bias, extend_bias,
                save=False, dpi=300
            )


    """

    fig, axs = plot.subplots(proj='cyl', ncols=3, nrows=2)

    # Reference simulation
    m0 = axs[0].pcolormesh(ref, cmap=cmap, levels=levels, extend=extend)
    axs[0].format(title=ref.title)

    # New simulation
    axs[1].pcolormesh(new, cmap=cmap, levels=levels, extend=extend)
    axs[1].format(title=new.title)
    axs[1].colorbar(m0, label=label + ' [' + units + ']')

    # Differences between the new and reference simulation
    m2 = axs[2].pcolormesh(new - ref, cmap=cmap_diff, levels=levels_diff,
                           extend=extend_diff)
    axs[2].format(title=ref.title + '\n - ' + new.title)
    axs[2].colorbar(m2, label='Bias of ' + label + ' [' + units + ']')

    # Bias of reference simulation regarding to observation
    m3 = axs[3].pcolormesh(ref - obs, cmap=cmap_bias, levels=levels_bias,
                           extend=extend_bias)
    axs[3].format(title=ref.title + '\n - ' + obs.obs_name)

    # Bias of new simulation regarding to observation
    axs[4].pcolormesh(new - obs, cmap=cmap_bias, levels=levels_bias,
                      extend=extend_bias)
    axs[4].format(title=new.title + '\n - ' + obs.obs_name)
    axs[4].colorbar(m3, label='Bias of ' + label + ' [' + units + ']')

    # Observation
    axs[5].pcolormesh(obs, cmap=cmap, levels=levels, extend=extend)
    axs[5].format(title=obs.obs_name)
    axs[5].colorbar(m0, label=label + ' [' + units + ']')

    axs.format(
        labels=True,
        coast=True,
        borders=True,
        latlim=(ref.lat.min(), ref.lat.max()),
        lonlim=(ref.lon.min(), ref.lon.max()),
        suptitle=label + " annual climatology: " + new.period,
        abc=True
    )

    if save:
        for extension in ['jpg', 'png', 'pdf']:
            fig.save(
                'img/' +
                var +
                '_' +
                new.title +
                '_REF_' +
                obs.obs_name +
                '_' +
                new.period +
                '.' +
                extension)
