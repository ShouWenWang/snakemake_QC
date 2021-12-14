import os
import sys
from pathlib import Path

import pandas as pd

#configfile: "config.yaml"  # command line way to set it: --configfile 'path/to/config'
#workdir: config['data_dir'] # set working directory, a command-line way to set it: --directory 'path/to/your/dir'
config['data_dir']=str(os.getcwd())
script_dir=config['script_dir']
raw_data_dir=config['raw_data_dir']
path_format=config['path_format']
    
##################
## preprocessing
################## 

SampleList=config['SampleList']
print(f'SampleList: {SampleList}')

# remove the flag file of the workflow if the sbatch is not actually run to finish
valid_SampleList=os.listdir(raw_data_dir)
for sample in SampleList:
    if sample not in valid_SampleList:
        raise ValueError(f"{sample} is not a valid sample. Should be among {valid_SampleList}")
        
        
def get_fastq_R1(wildcards):
    if path_format == 0:  # format 1
        fq_R1=f"{raw_data_dir}/{wildcards.sample}/{wildcards.sample}_R1.fastq.gz",
    else:
        fq_R1=f"{raw_data_dir}/{wildcards.sample}_R1.fastq.gz",
    return fq_R1 

def get_fastq_R2(wildcards):
    if path_format == 0:  # format 1
        fq_R2=f"{raw_data_dir}/{wildcards.sample}/{wildcards.sample}_R2.fastq.gz",
    else:
        fq_R2=f"{raw_data_dir}/{wildcards.sample}_R2.fastq.gz",
    return fq_R2

##################
## start the rules
################## 
rule all:
    input: 
        "fastqc/multiqc_report.done",
    
rule fastqc:
    input:
        fq_R1=get_fastq_R1,
        fq_R2=get_fastq_R2,
    output:
        touch("fastqc/{sample}_R1_fastqc.done"),
        touch("fastqc/{sample}_R2_fastqc.done"),
    run:
        command_1=f"sh {script_dir}/run_fastqc.sh {input.fq_R1} fastqc"  # can use input[0]
        command_2=f"sh {script_dir}/run_fastqc.sh {input.fq_R2} fastqc"  # can use input[1]
        time=config['QC']['max_run_time']
        mem=config['QC']['requested_memory']
        cores=config['QC']['cores']
        job_name=wildcards.sample
        for command in [command_1,command_2]:
            if config['sbatch']==0:
                print("Run on terminal directly")
                os.system(command)
            else:
                os.system(f"python {script_dir}/run_sbatch.py --job_name {job_name} --cores {cores} --mem {mem} --time {time} --command '{command}' ") # we use ' in '{command}' to avoid bash expansion


rule multiqc_for_fastqc:
    input:
        expand("fastqc/{sample}_R1_fastqc.done",sample=SampleList)
    output:
        touch("fastqc/multiqc_report.done")
    run: 
        files_ready=True
        for sample in SampleList:
            if not os.path.exists(f'fastqc/{sample}_R1_fastqc.html'):
                files_ready=False
            if not os.path.exists(f'fastqc/{sample}_R2_fastqc.html'):
                files_ready=False
                
        time=config['QC']['max_run_time']
        mem=config['QC']['requested_memory']
        cores=config['QC']['cores']
        command=f"sh {script_dir}/run_multiqc.sh fastqc"
        job_name='MultiQC'
        if files_ready:
            if config['sbatch']==0:
                print("Run on terminal directly")
                os.system(command)
            else:
                os.system(f"python {script_dir}/run_sbatch.py --job_name {job_name} --cores {cores}  --time {time} --mem {mem} --command '{command}' ")
        else:
            print("Multi-QC failed. The fastqc files are not ready yet. Please run it at a later time.")
