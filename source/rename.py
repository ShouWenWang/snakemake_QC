import os
from pathlib import Path
import os
import pandas as pd
import argparse
from os import listdir
from os.path import isfile, join
# parse cmd line arguments
parser = argparse.ArgumentParser(description="rename files")

parser.add_argument(
    "--data_path",
    type=str,
    default=".",
    help="Path to rename files",
)
parser.add_argument(
    "--suffix",
    type=str,
    default=".fq.gz",
    help="suffix of the file",
)


args=parser.parse_args()


all_files = sorted(
    Path(args.data_path).glob(
        os.path.join(
            "*",
            f"*{args.suffix}",
        )
    )
)


for file in all_files:
    file=str(file)
    print(file)
    sample=file.split('/')[0]
    print(f'Sample: {sample}')
    if (f'_1{args.suffix}' in file) or (f'_R1{args.suffix}' in file):
        os.system(f'mv {file} {sample}/{sample}_R1.fastq.gz')
    if (f'_2{args.suffix}' in file) or (f'_R2{args.suffix}' in file):
        os.system(f'mv {file} {sample}/{sample}_R2.fastq.gz')
        