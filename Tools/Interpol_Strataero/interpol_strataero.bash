#!/bin/bash

GrilleH=96x95
GrilleV=79
GrilleZ=

RepOri=/workgpfs/rech/psl/rpsl035/IGCM/ATM/STRATAERO/CMIP6/v3/144x142/L${GrilleV}
RepOut=/arch/home/rech/ces/rces604/IGCM/ATM/STRATAERO/CMIP6/v3/${GrilleH}/L${GrilleV}${GrilleZ}
mkdir -p ${RepOut}

FicGRilleCible=${ARCHIVE}/IGCM_OUT/LMDZ/ELI-${GrilleH}x${GrilleV}${GrilleZ}/ATM/Output/Grid/ELI-${GrilleH}x${GrilleV}${GrilleZ}_1979_grilles_gcm.nc

yearbeg=1979
yearend=2023

#-------------------

TMPDIR=$WORKDIR/tmp/itp_strataero-`date +%y%m%d-%H%M`
mkdir $TMPDIR
echo "TMPDIR: " $TMPDIR
cd $TMPDIR

cat <<LAFIN > itp_strataero.f90
PROGRAM itp_strataero
END PROGRAM itp_strataero
LAFIN

for var in tauswstrat taulwstrat ; do

  for year in `seq ${yearbeg} 1 ${yearend}`; do
    echo ${RepOri}/${var}.2D.${year}.nc "-->" ${RepOut}/${var}.2D.${year}.nc
    itp_strataero ${FicGRilleCible} ${RepOri}/${var}.2D.${year}.nc ${RepOut}/${var}.2D.${year}.nc
  done

done
