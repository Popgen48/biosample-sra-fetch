#!/bin/bash
source ~/.bashrc
conda sra-tools
mkdir -p $SCRATCH/$USER/prefetch/${2}; prefetch ${1} --force all --max-size 200G -O $SCRATCH/$USER/prefetch/${2}/
