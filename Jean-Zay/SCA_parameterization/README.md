# To implement new Snow Cover Area (SCA) parameterization in LMDZ/ORCHIDEE

This folder is intended for making the analyze of the simulations made on Jean-Zay for the following repository: https://github.com/mickaellalande/SCA_parameterization

https://docs.google.com/document/d/1gK69TtH3feRFu4q0MjmuouC8xG6Gcth6Qe9cbeY5vIM/edit?usp=sharing

## ELC-144x142x79-GMTED-STD

Initial conditions `EXPERIMENTS/LMDZ/CREATE_clim_360d/config.card` with the new elevation file from GMTED2010 (`/gpfsstore/rech/goe/ufz23bm/topo/Relief_GMTED2010_15n015_00625deg.nc` from http://www.temis.nl/data/gmted2010/) and the additionnal variables ZMEA_NOT_FILTERED and ZSTD_NOT_FILTERED (https://github.com/mickaellalande/SCA_parameterization/compare/test).

- Jean-Zay WORK: `/gpfswork/rech/goe/ufz23bm/SCA_parameterization/modipsl/config/LMDZOR_v6/ELC-144x142x79-GMTED-STD`
- Jean-Zay STORE: `/gpfsstore/rech/goe/ufz23bm/IGCM_OUT/LMDZ/ELC-144x142x79-GMTED-STD`
- THREDDS: `/gpfsdsmnt/ipsl/dods/pub/ufz23bm/IGCM_OUT/LMDZ/ELC-144x142x79-GMTED-STD`
- CICLAD: `/thredds/idris/work/ufz23bm/IGCM_OUT/LMDZ/ELC-144x142x79-GMTED-STD` 
- https://vesg.ipsl.upmc.fr/thredds/catalog/idris_work/ufz23bm/IGCM_OUT/LMDZ/catalog.html