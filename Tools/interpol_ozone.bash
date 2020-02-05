#!/bin/bash

# Faire avec Job_ELI... au moins une fois (en esperant que Ã§a marche). Ensuite rÃcupÃrer le fichier d'O3 pour la grille. Ensuite se debrouiller

# RepOri=/workgpfs/rech/psl/rpsl035/IGCM/ATM/OZONE/UReading/historical.v20160711.v2/interpol/256x256/
RepOri=/workgpfs/rech/psl/rpsl035/IGCM/ATM/OZONE/UReading/Scenarios/CCMI-ssp585.v20181101/interpol/144x142/

Grille=256x256x79

RepOut=/arch/home/rech/ces/rces604/IGCM_OUT/LMDZ/ELI-${Grille}/ATM/Output/Boundary/

FicOZGRilleCible=${RepOut}/ELI-${Grille}_1979_climoz_LMDZ.nc

yearbeg=2015
yearend=2100

# suffixout="climoz_LMDZ.nc"
suffixout="climoz_LMDZ_ssp585.nc"

#-------------------

TMPDIR=$WORKDIR/tmp/ozone-`date +%y%m%d-%H%M`
mkdir $TMPDIR
echo "TMPDIR: " $TMPDIR
cd $TMPDIR

cdo griddes ${FicOZGRilleCible} > grille.txt

for year in `seq ${yearbeg} 1 ${yearend}`; do
  cdo -remapbil,grille.txt ${RepOri}/climoz_LMDZ_${year}.nc ${RepOut}/ELI-${Grille}_${year}_${suffixout}
done
