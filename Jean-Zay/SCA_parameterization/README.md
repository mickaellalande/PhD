# To implement new Snow Cover Fraction (SCF) parameterization in LMDZ/ORCHIDEE

This folder is intended for making the analyze of the simulations made on Jean-Zay for the following repository: https://github.com/mickaellalande/SCA_parameterization

https://docs.google.com/document/d/1gK69TtH3feRFu4q0MjmuouC8xG6Gcth6Qe9cbeY5vIM/edit?usp=sharing

## ELC-144x142x79-GMTED-STD

Initial conditions `EXPERIMENTS/LMDZ/CREATE_clim_360d/config.card` with the new elevation file from GMTED2010 (`/gpfsstore/rech/goe/ufz23bm/topo/Relief_GMTED2010_15n015_00625deg.nc` from http://www.temis.nl/data/gmted2010/) and the additionnal variables ZMEA_NOT_FILTERED and ZSTD_NOT_FILTERED (https://github.com/mickaellalande/SCA_parameterization/compare/test).

- Jean-Zay WORK: `/gpfswork/rech/goe/ufz23bm/SCA_parameterization/modipsl/config/LMDZOR_v6/ELC-144x142x79-GMTED-STD`
- Jean-Zay STORE: `/gpfsstore/rech/goe/ufz23bm/IGCM_OUT/LMDZ/ELC-144x142x79-GMTED-STD`
- THREDDS: `/gpfsdsmnt/ipsl/dods/pub/ufz23bm/IGCM_OUT/LMDZ/ELC-144x142x79-GMTED-STD`
- CICLAD: `/thredds/idris/work/ufz23bm/IGCM_OUT/LMDZ/ELC-144x142x79-GMTED-STD` 
- https://vesg.ipsl.upmc.fr/thredds/catalog/idris_work/ufz23bm/IGCM_OUT/LMDZ/catalog.html


## LMDZOR-STD-TEST (1 an)

```fortran
frac_snow_veg(:) = tanh(snowdepth(:)/(0.025*(snowrho_ave(:)*(1+zstd_not_filtered(:)/200.)/50.)))
```

zstd physiq -> conveg compil ok (with Laurent)

 lmdz-zstd-to-condveg
@mickaellalande
mickaellalande committed 22 hours ago 
1 parent 8bcc93a commit fec3ee5485f5a946abc5cd26c3ecf6f0749c6610

- Jean-Zay WORK: `/gpfswork/rech/goe/ufz23bm/SCA_parameterization/modipsl/config/LMDZOR_v6/LMDZOR-STD-TEST`
- Jean-Zay STORE: `/gpfsscratch/rech/goe/ufz23bm/IGCM_OUT/LMDZOR/TEST/clim/LMDZOR-STD-TEST`
- THREDDS: `/gpfsdsmnt/ipsl/dods/pub/ufz23bm/IGCM_OUT/LMDZOR/TEST/clim/LMDZOR-STD-TEST/`
- CICLAD: `/thredds/idris/work/ufz23bm/IGCM_OUT/LMDZOR/TEST/clim/LMDZOR-STD-TEST/` 
- https://vesg.ipsl.upmc.fr/thredds/catalog/idris_work/ufz23bm/IGCM_OUT/LMDZOR/TEST/clim/LMDZOR-STD-TEST/catalog.html


## LMDZOR-STD-REF

```fortran
! LMDZOR-STD-REF
frac_snow_veg(:) = tanh(snowdepth(:)/(0.025*(snowrho_ave(:)/50.)))
```
https://github.com/mickaellalande/PhD/blob/master/local/SCE_SWE_parametization/Niu2007.ipynb

- Jean-Zay WORK: `/gpfsdswork/projects/rech/goe/ufz23bm/SCA_parameterization/modipsl/config/LMDZOR_v6/LMDZOR-STD-REF`
- Jean-Zay STORE: `/gpfsstore/rech/goe/ufz23bm/IGCM_OUT/LMDZOR/PROD/clim/LMDZOR-STD-REF`
- THREDDS: `/gpfsdsmnt/ipsl/dods/pub/ufz23bm/IGCM_OUT/LMDZOR/PROD/clim/LMDZOR-STD-REF/`
- CICLAD: `/thredds/idris/work/ufz23bm/IGCM_OUT/LMDZOR/PROD/clim/LMDZOR-STD-REF/` 
- https://vesg.ipsl.upmc.fr/thredds/catalog/idris_work/ufz23bm/IGCM_OUT/LMDZOR/PROD/clim/LMDZOR-STD-REF/catalog.html


## LMDZOR-STD-NY07-CUSTOM-200

```fortran
! LMDZOR-STD-NY07-CUSTOM-200
frac_snow_veg(:) = tanh(snowdepth(:)/(0.025*(snowrho_ave(:)*(1+zstd_not_filtered(:)/200.)/50.)))
```
https://github.com/mickaellalande/PhD/blob/master/local/SCE_SWE_parametization/Niu2007-std.ipynb

- Jean-Zay WORK: `/gpfswork/rech/goe/ufz23bm/SCA_parameterization/modipsl/config/LMDZOR_v6/LMDZOR-STD-NY07-CUSTOM-200`
- Jean-Zay STORE: `/gpfsscratch/rech/goe/ufz23bm/IGCM_OUT/LMDZOR/PROD/clim/LMDZOR-STD-NY07-CUSTOM-200`
- THREDDS: `/gpfsdsmnt/ipsl/dods/pub/ufz23bm/IGCM_OUT/LMDZOR/PROD/clim/LMDZOR-STD-NY07-CUSTOM-200/`
- CICLAD: `/thredds/idris/work/ufz23bm/IGCM_OUT/LMDZOR/PROD/clim/LMDZOR-STD-NY07-CUSTOM-200T/` 
- https://vesg.ipsl.upmc.fr/thredds/catalog/idris_work/ufz23bm/IGCM_OUT/LMDZOR/PROD/clim/LMDZOR-STD-NY07-CUSTOM-200/catalog.html
