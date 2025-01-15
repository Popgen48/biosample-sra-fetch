#!/bin/bash
##reference
#https://www.biostars.org/p/124432/
#https://www.biostars.org/p/448799/
#https://www.biostars.org/p/9507933/
#obtaining api key --> https://support.nlm.nih.gov/kbArticle/?pn=KA-05317
#
#run the following command to extract the detail of all biosample of bos taurus species; run only the first time
#esearch -db biosample -query 'Bos taurus[organism]' |efetch -format tsv > Bos_taurus_ncbi_biosample.txt
#the following python script extract biosample id matching a particular breed (replacing the first argument) and the line describing the information about the breed, example--> Braunvieh_biosample.txt
python extract_info.py Bos_taurus_ncbi_biosample.txt ${1}
#after manually verifying that biosamples are as per the expectations, only extract the biosample id, example --> Braunvieh_biosample.1.txt
awk '{print $1}' ${1}_biosample.txt > ${1}_biosample.1.txt
#the following command extract the information specified in xtract command for each biosample id extracted using awk command above, example --> metadata_sra_Braunvieh.txt
while read sample
do	
epost -db biosample -id ${sample} -format acc|elink -target sra|efetch -db sra -format runinfo -mode xml | xtract -pattern Row -def "NA" -element Run bases avgLength InsertSize LibraryStrategy LibrarySelection LibrarySource LibraryLayout Platform BioProject BioSample ScientificName CenterName Consent
sleep 2
done<${1}_biosample.1.txt >> metadata_sra_${1}.txt
#make sure that all sra information extracted above in the file contains 14 columns as we had asked for 14 field as specified in xtract command above, example --> metadata_sra_Braunvieh.1.txt
awk 'BEGIN{FS="\t"}NF==14{print}' metadata_sra_${1}.txt > metadata_sra_${1}.1.txt
#concatenate the header containing the field name, example --> metadata_sra_Braunvieh_runinfo.tsv
cat header.txt metadata_sra_${1}.1.txt  > metadata_sra_${1}_runinfo.tsv 
#only extract biosample id and its respective SRA ids when it satisfies the criteria set in parameters.yaml file
#the pythons script will generate two files--> *_runinfo_selected_samples.csv and *__selected_samples.tsv, the first file will contain all 14 fields of the selected samples and the second file \
#will contans only the two columns --> biosample id and its respective sra ids, example --> Braunvieh_runinfo_selected_samples.csv and Braunvieh_selected_samples.tsv
#20 is the number of samples that we want to select
python select_samples.py metadata_sra_${1}_runinfo.tsv parameters.yaml 20 ${1}
