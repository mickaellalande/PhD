#!/bin/bash

##########################################################
### Interpolate stratosphere aerosol files to new grid ###
##########################################################

# Mickaël LALANDE (mickael.lalande@univ-grenoble-alpes.fr)
# 10/02/2020
# Adapted from Olivier Boucher?

# Compile before itp_strataero.f90 (on Jean-Zay):
# module load intel-all/19.0.4
# module load hdf5/1.10.5-mpi
# module load netcdf/4.7.2-mpi
# module load netcdf-fortran/4.5.2-mpi
# ifort itp_strataero.f90 -lnetcdff -o itp_strataero

# Better to use volc.sh (http://forge.ipsl.jussieu.fr/igcmg/svn/TOOLS/CMIP6_FORCING/AER_STRAT/)
# -> generate new strataero files from 1 year simuation? 
# Conctact Olivier Boucher (olivier.boucher@ipsl.fr) for more informations

# The path needs to be changed + the years

GrilleH=144x142
GrilleV=79
GrilleZ=

RepOri=/gpfswork/rech/psl/commun/IGCM/ATM/STRATAERO/CMIP6/v3/${GrilleH}/L${GrilleV}
RepOut=/gpfsstore/rech/goe/ufz23bm/IGCM_OUT/LMDZ/ELI-144x142x79-zoomx2-himalaya-test/ATM/Output/Boundary

FicGRilleCible=/gpfsstore/rech/goe/ufz23bm/IGCM_OUT/LMDZ/ELI-144x142x79-zoomx2-himalaya-test/ATM/Output/Grid/ELI-144x142x79-zoomx2-himalaya-test_1979_grilles_gcm.nc
yearbeg=1979
yearend=1980


for var in tauswstrat taulwstrat ; do

  for year in `seq ${yearbeg} 1 ${yearend}`; do
    echo ${RepOri}/${var}.2D.${year}.nc "-->" ${RepOut}/${var}.2D.${year}.nc
    ./itp_strataero ${FicGRilleCible} ${RepOri}/${var}.2D.${year}.nc ${RepOut}/${var}.2D.${year}.nc
  done

done
