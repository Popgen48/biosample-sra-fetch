#! /bin/bash
#SBATCH -J fastq-dump_Braunvieh
#SBATCH -o %x.%j.%N.out
#SBATCH -D ./
#SBATCH --get-user-env
#SBATCH --clusters=serial
#SBATCH --partition=serial_std
#SBATCH --cpus-per-task=56
#SBATCH --time=48:00:00
#SBATCH --export=NONE
#SBATCH --mail-type=END
#SBATCH --mail-user=<user_email_id>

#replace Braunvieh_selected_samples.tsv with your input file; this tsv file is in the directory, step1_e -direct_extract_biosample_ids
#also replace the joblog file and the email id of the user
parallel -j 4 --joblog Braunvieh_selected_samples.log --colsep "\t" ./parallel_fasterq-dump.sh {1} {2} :::: Braunvieh_selected_samples.tsv
