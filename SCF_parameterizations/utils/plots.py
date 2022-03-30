#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Autopep8: https://pypi.org/project/autopep8/
# Check with http://pep8online.com/

# =============================================================================
# Import modules
# =============================================================================
import numpy as np
import xarray as xr
import proplot as plot
import calendar as cld
import pandas as pd
from scipy import stats


# Personnal functions
import clim as c  # makes weighted montlhy computations
import utils as u  # makes weighted montlhy computations

# =============================================================================
# SCF vs SD
# =============================================================================
def plot_scf_vs_sd(scf, sd, topo_std, mask, param, res, save=False):
    xylim = [[0, 1], [0, 1]]
    bins = 100
    cmap = 'Spectral_r'
    levels = np.logspace(0, 3, 25)
    cmin = 1

    months = [10, 11, 12, 1, 2, 3, 4, 5]
    threshold = 300
    stds = [(True), (topo_std < threshold), (topo_std > threshold)]

    fig, axs = plot.subplots(ncols=len(months), nrows=3, axwidth=1)

    for j, std in enumerate(stds):
        for i, month in enumerate(months):
            ax = axs[j, i]
            m = ax.hist2d(
                sd.where( (sd['time.month'] == month) & (mask < 30) & std).values.flatten(),
                scf.where( (scf['time.month'] == month) & (mask < 30) & std).values.flatten(),
                bins=bins, range=xylim, cmap=cmap, cmin=cmin, levels=levels,
            )
            ax.format(xlabel='SD [m]', ylabel='SCF')

    fig.colorbar(m[3], ticks=np.logspace(0, 3, 4))

    axs.format(
        rowlabels=['All points', 'std < '+str(threshold)+'m', 'std > '+str(threshold)+'m'],
        collabels=[cld.month_name[month] for month in months],
        suptitle=param+' non-permanent daily SCF (predicted from HMASR inputs) vs HMASR SD at '+res+'\n(1999-10-01 to 2017-09-30 with >30% permanent snow grid cells excluded)'
    )

    if save:
        fig.save('img/HMASR_SD_vs_'+param+'_SCF_'+res+'_1999-2017_30_STD_'+str(threshold)+'.jpg')
        

# =============================================================================
# Spatial SCF
# =============================================================================
def plot_spatial_scf(scf_ref, scf_param, topo_std, mask, weights, param, res, save=False):
    seasons=['Annual', 'DJFMA', 'JJAS']; fred='D'
    levels=plot.arange(0, 80, 5); extend='max'; cmap='viridis'
    levels_bias=plot.arange(-40, 40, 10); extend_bias='both'; cmap_bias='RdBu'
    threshold=30 # percentage of permanent snow in a cell
    latlim = slice(mask.lat.min().values.item(0)-0.5, mask.lat.max().values.item(0)+0.5)
    lonlim = slice(mask.lon.min().values.item(0)-0.5, mask.lon.max().values.item(0)+0.5)

    fig, axs = plot.subplots(proj='cyl', ncols=len(seasons), nrows=3, axwidth=3)

    # HMASR
    for i, season in enumerate(seasons):
        data = c.clim(scf_ref, freq=fred, season=season, skipna=True)*100
        m = axs[0, i].pcolormesh(data, levels=levels, extend=extend, cmap=cmap)
        axs[0, i].format(urtitle='{:.1f} %'.format(data.weighted(weights).sum().values.item(0)))

    # param
    for i, season in enumerate(seasons):
        data = c.clim(scf_param, freq=fred, season=season, skipna=True)*100
        axs[1, i].pcolormesh(data, levels=levels, extend=extend, cmap=cmap)
        axs[1, i].format(urtitle='{:.1f} %'.format(data.weighted(weights).sum().values.item(0)))

    # bias
    for i, season in enumerate(seasons):
        scf_param_clim = c.clim(scf_param, freq=fred, season=season, skipna=True)*100
        scf_ref_clim = c.clim(scf_ref, freq=fred, season=season, skipna=True)*100
        
        m_bias = axs[2, i].pcolormesh(scf_param_clim-scf_ref_clim, levels=levels_bias, extend=extend_bias, cmap=cmap_bias)
        
        mb = u.weighted_mean(scf_param_clim-scf_ref_clim, weights).values.item(0)
        rmse = u.weighted_rmse(scf_param_clim, scf_ref_clim, weights).values.item(0)
        r = u.weighted_corr(scf_param_clim, scf_ref_clim, weights).values.item(0)
        axs[2, i].format(ltitle='MB = {:.1f} %'.format(mb), ctitle='RMSE = {:.1f} %'.format(rmse), rtitle='r = {:.2}'.format(r))

    # mask
    for ax in axs:
        ax.pcolormesh(mask.where(mask>threshold)*0+1, cmap='lightgray', levels=[0, 1, 2, 3])
        u.plot_zones(ax=ax)
    #     ax.format(utitle='aze')

    # Colorbars
    fig.colorbar(m, label='non-permanent SCF [%]', rows=(1, 2), ticks=10)
    fig.colorbar(m_bias, label='SCF bias [%]', row=3, ticks=20)

    # Format
    axs.format(
        borders=True, labels=False, 
        latlim=(latlim.start, latlim.stop), lonlim=(lonlim.start, lonlim.stop),
        suptitle=param+' daily non-permanent SCF at '+res+' predicted from HMASR inputs\n(1999-10-01 to 2017-09-30; grid cells with >30% permanent snow are excluded)',
        abc=True, abcloc='ul',
        collabels=seasons, rowlabels=['HMASR', param, param+'\n-      \nHMASR'],
    )
    
    if save:
        fig.save('img/HMASR_SCF_vs_'+param+'_SCF_'+res+'_1999-2017_30.jpg')
        
# =============================================================================
# Time series
# =============================================================================     
def plot_ts(scf_ref, scf_param, param, topo_std, mask, weights, zones_df, res, y_max=80, save=False):
    train_period = slice('1999-10-01', '2013-09-30') # ~80%
    val_period = slice('2013-10-01', '2017-09-30') # ~20%
    
    import warnings
    warnings.filterwarnings("ignore")
    zones = ['HMA', 'TS', 'HK', 'TP', 'HM']
    
    fig, axs = plot.subplots(nrows=len(zones), ncols=3, axwidth=8, ref=1, wratios=(6, 1, 1), aspect=6)

    ###################
    ### Time series ###
    ###################
    for i, zone in enumerate(zones):
        ax = axs[i, 0]


        ts_list = []
        for da, label in zip([scf_ref, scf_param], ['HMASR', param]):
            ts = da.sel(lat=zones_df.loc[zone].latlim, lon=zones_df.loc[zone].lonlim).weighted(weights).mean(('lat', 'lon'))*100
            ax.plot(ts, label=label)
            ts_list.append(ts)

        # Validation shading
#         ax.fill_between(da.sel(time=train_period).time, 0, y_max, alpha=0.2)
        ax.fill_between([da.time.values[0], da.sel(time=train_period).time.values[-1]], 0, y_max, alpha=0.2)

        # Compute metrics
        df = pd.DataFrame(index=['train', 'val'], columns=['mb', 'rmse', 'r'])
        for period, dataset in zip([train_period, val_period], ['train', 'val']):
            mb = (ts_list[1]-ts_list[0]).sel(time=period).mean().item(0)
            rmse = np.sqrt(((ts_list[1]-ts_list[0])**2).sel(time=period).mean().item(0))
            r = stats.pearsonr(ts_list[1].sel(time=period), ts_list[0].sel(time=period))[0]
            df.loc[dataset] = [mb, rmse, r]

        ax.format(
            ylabel='non-permanent SCF [%]',
            xlim=(da.time.values[0], da.time.values[-1]),
            ltitle='MB = {:.1f} % (train) / {:.1f} % (val)'.format(df.loc['train'].mb, df.loc['val'].mb),
            ctitle='RMSE = {:.1f} % (train) / {:.1f} % (val)'.format(df.loc['train'].rmse, df.loc['val'].rmse),
            rtitle='r = {:.2f} (train) / {:.2f} (val)'.format(df.loc['train'].r, df.loc['val'].r),
        )

    axs[0].text(np.datetime64('2006-01-01'), y_max-7, 'train period', color='C0', weight='bold')
    axs[0].text(np.datetime64('2015-01-01'), y_max-7, 'val period', color='gray7', weight='bold')
    axs[0].legend(loc='ul')

    ####################
    ### Annual cycle ###
    ####################
    for i, zone in enumerate(zones):
        for j, period in enumerate([train_period, val_period]):
            ax = axs[i, j+1]

            ac_list = []
            for da in [scf_ref, scf_param]:
                ac = da.sel(lat=zones_df.loc[zone].latlim, lon=zones_df.loc[zone].lonlim, time=period) \
                            .groupby('time.month').mean() \
                            .weighted(weights).mean(('lat', 'lon'))*100
                std = da.sel(lat=zones_df.loc[zone].latlim, lon=zones_df.loc[zone].lonlim, time=period) \
                            .weighted(weights).mean(('lat', 'lon')) \
                            .resample(time='M').mean() \
                            .groupby('time.month').std()*100

                ac_list.append(ac)

                ac_shift = ac.reindex(month=np.roll(ac.month,3))
                std_shift = std.reindex(month=np.roll(std.month,3))
                shadedata = [(ac_shift-std_shift).values, (ac_shift+std_shift).values]

                ax.plot(ac_shift.values, shadedata=shadedata, label='SCF')

            if j == 0:
                # Validation shading
                ax.fill_between(range(12), 0, y_max, alpha=0.2)


            # Compute metrics
            mb = (ac_list[1]-ac_list[0]).mean().item(0)
            rmse = np.sqrt(((ac_list[1]-ac_list[0])**2).mean().item(0))
            r = stats.pearsonr(ac_list[1], ac_list[0])[0]

            ax.format(
                xlocator='index', xformatter=[cld.month_abbr[month][0] for month in ac.reindex(month=np.roll(ac.month,3)).month.values],
                urtitle='RMSE = {:.1f} %\nr = {:.2f}'.format(rmse, r),
            )


    axs[1].format(title='train period')
    axs[2].format(title='val period')

    for ax in axs:
        ax.autoscale(tight=True)

    axs.format(
        suptitle=param+' daily non-permanent SCF at '+res+' predicted from HMASR inputs\n' \
                 '(1999-10-01 to 2017-09-30; grid cells with >30% permanent snow are excluded)',
        rowlabels=zones,
        abc=True, abcloc='ul',
        ylim=(0, y_max), ylabel='non-permanent SCF [%]',
    )
    
    if save:
        fig.save('img/HMASR_vs_'+param+'_SCF_ts_ac_'+res+'_1999-2017_30.jpg')

# =============================================================================
# All
# ============================================================================= 
def plots(scf, sd, scf_param, topo_std, mask, weights, zones_df, param, res, y_max=80, save=False):
    plot_scf_vs_sd(scf_param, sd, topo_std, mask, param, res, save=False)
    plot_spatial_scf(scf, scf_param, topo_std, mask, weights, param, res, save=False)
    plot_ts(scf, scf_param, param, topo_std, mask, weights, zones_df, res, y_max=80, save=False)
