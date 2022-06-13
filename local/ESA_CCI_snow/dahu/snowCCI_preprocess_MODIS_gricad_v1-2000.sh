#!/bin/bash

#OAR -n snowCCI2000
#OAR -l /nodes=1/core=16,walltime=08:00:00
#OAR --stdout debug/snowCCI_preprocess_MODIS_gricad_v1-2000.out
#OAR --stderr debug/snowCCI_preprocess_MODIS_gricad_v1-2000.err
#OAR --project regional-climate
#OAR -t fat

python snowCCI_preprocess_MODIS_gricad_v1-2000.py
