# Introduction

Perform fastqc and then multi-qc for multiple files.

You can specify the `config.yaml` files for the analysis

```yaml
script_dir: '/n/groups/klein/shouwen/lili_project/packages/snakemake_multiomics/source'
raw_data_dir: 'raw_data' # relative or absolute dir to the config file
path_format: 0 # format=0, the file is like {raw_data_dir}/{sample}/{sample}.fastq.gz;  
          # format=1, the file is like  {raw_data_dir}/{sample}.fastq.gz
SampleList: ['test_DNA_Lime','test_LARRY_10X'] 
sbatch : 1 # 1, run sbatch job;  
           # 0, run in the interactive mode. 
QC:
    max_run_time : 3 # used only if sbatch=1
    requested_memory : '10G' # used only if sbatch=1
    cores: 2
recompute : 0
```


You can go to the test module and run this following command. 

```bash
 snakemake   -s $X/packages/snakemake_QC/snakefile_QC.py --configfile config.yaml --config script_dir=$X/packages/snakemake_QC/source  --cores 4 
```


