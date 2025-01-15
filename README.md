# in-house scripts to download NCBI biosample ids and sra files efficiently and in bulk !
**Motivation**
1). Download biosample ids matching the breed names
2). Select and Download the SRA files of these biosample ids that matches the criteria of approx. coverage.

# Step 1: Download biosample ids matching the breed names

First, run the following command to create conda enviornment of the required tools:
```
mamba create -n e-direct_env -c conda-forge -c bioconda pandas==2.2.3 pyyaml==6.0.2
```
next, all the commands and the examples files are described in the folder step1_e -direct_extract_biosample_ids. 

# Step 2: Download SRA files of the selected biosample ids

First, run the following command to create conda enviornment of the required tools:
```
mamba create -n sra-tools -c conda-forge -c bioconda sra-tools==3.1.1 parallel
```
next, all the commands and the examples files are described in the folder step2_sra-tools_download_sra

