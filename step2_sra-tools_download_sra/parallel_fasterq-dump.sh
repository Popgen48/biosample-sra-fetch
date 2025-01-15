#!/bin/bash
source ~/.bashrc
conda activate sra-tools
fasterq-dump --threads 14 --split-files -t $SCRATCH/$USER/ -O $SCRATCH/$USER/prefetch/${2}/ $SCRATCH/$USER/prefetch/${2}/${1}
pigz -p 14 $SCRATCH/$USER/prefetch/${2}/${1}_1.fastq
pigz -p 14 $SCRATCH/$USER/prefetch/${2}/${1}_2.fastq
