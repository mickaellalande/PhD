#!/bin/bash

gridfile=$STORE/IGCM_OUT/LMDZ/ELI-144x142x79-zoomx2-himalaya-test/ATM/Output/Grid/ELI-144x142x79-zoomx2-himalaya-test_1979_grilles_gcm.nc

yearbeg=1979
yearend=1980

cd $STORE/IGCM_OUT/LMDZ/ELI-144x142x79-zoomx2-himalaya-test/ATM/Output/Boundary


# Extraction d'un fichier de grille physique a partir de grilles_gcm.nc
# ---------------------------------------------------------------------

cp ${gridfile} grilles_gcm.nc

imp1=`ncdump -h grilles_gcm.nc | grep lonv | head -1 | awk ' { print $3 } '`
echo $imp1
(( imm1 = $imp1 - 2 ))
echo $imm1
ncks -d lonv,0,$imm1 grilles_gcm.nc -v phis -O grille_phys.nc
ncrename -v lonv,lon -v latu,lat -d lonv,lon -d latu,lat -O grille_phys.nc
ncap2 -s "lon=-360.+lon" grille_phys.nc -O tmp.nc
\mv -f tmp.nc grille_phys.nc


# Boucle sur les annees
# ---------------------

for year in `seq ${yearbeg} 1 ${yearend}`; do

  # Recuperation des fichiers d'origine
  # -----------------------------------

  orig=/gpfswork/rech/psl/commun/IGCM/ATM/AEROSOLS/CMIP6/v1/144x142/L79/aerosols${year}_from_inca.nc

  # Interpolation
  # --------------

  cdo remapcon,grille_phys.nc $orig aerosols${year}_from_inca.nc

done

