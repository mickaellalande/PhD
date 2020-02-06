#!/bin/bash

# ----------

gridfile=$ARCHIVE/IGCM_OUT/LMDZ/ELI-96x95x79/ATM/Output/Grid/ELI-96x95x79_1979_grilles_gcm.nc

scenario="historical" # ssp585, historical,...
yearbeg=1850
yearend=1850

# ----------

module purge nco
module purge cdo
module purge netcdf

module load nco
module load cdo
module load netcdf

ulimit -s unlimited

# TMPDIR
# ------

TMPDIR=$WORKDIR/tmp/aerosols-`date +%y%m%d-%H%M`
mkdir $TMPDIR
echo "TMPDIR: " $TMPDIR
cd $TMPDIR

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

  # Versions CMIP5
  # orig=aerosols_11YearsClim_${year}_v5.nc
  # mfget /arch/home/rech/psl/rpsl035/IGCM/ATM/LMD144142/AR5/HISTORIQUE/$orig

  orig=aerosols${year}_from_inca.nc

  if [ ${scenario} == "historical" ] ; then
    mfget /arch/home/rech/psl/rpsl035/IGCM/ATM/AEROSOLS/CMIP6/v1/144x142/L79/$orig
  else
    mfget /arch/home/rech/psl/rpsl035/IGCM/ATM/AEROSOLS/CMIP6/Scenarios/${scenario}/144x142/L79/$orig
  fi

  # Interpolation
  # --------------
  # Un cdo direct ne marche pas. Il faut donner la liste des variables ...
  vars="" ; for var in `ncdump -h $orig | grep float | sed -e 's/^.*.float //' | cut -d'(' -f1 | sed -e 's/ ;//'` ; do  vars="$vars,$var" ; done

  cdo remapcon,grille_phys.nc -selvar,$vars $orig aerosols_INCA_${scenario}_${year}.nc
  ncks -v p0,ap,b,lev $orig -A aerosols_INCA_${scenario}_${year}.nc
  rm $orig

done

