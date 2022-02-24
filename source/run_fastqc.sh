#!/bin/bash

############## FASTQC
module load fastqc/0.11.3
# module load gcc/6.2.0
# module load star/2.5.2b
# module load samtools/1.3.1
# export PATH=/n/app/bcbio/tools/bin:$PATH        # for using featureCounts if not already in $PATH

input_dir=$1
sample=$2
fastqc_out=$3
mkdir -p $fastqc_out
file=`find  ${input_dir} -name "${sample}*.gz"`
fastqc -o $fastqc_out  $file
