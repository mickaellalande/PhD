#!/bin/bash

# read -p "Enter path to experiment (IGCM_OUT/...): " path_to_exp
# read -p "Enter experiment name: " exp
# read -p "Enter period: " period

path_to_exp="IGCM_OUT/LMDZOR/DEVT/amip"
exp="LMDZORnudge-STD-NY07"
period="20040101_20131231"

path=$STORE"/"$path_to_exp"/"$exp

echo $path

mfthredds $path_to_exp"/"exp"/ATM/Analyse/TS_MO" $path"/ATM/Analyse/TS_MO/"$exp"_"$period"_1M_t2m.nc"