import sys
import re
import random
import pandas as pd
import yaml
from yaml.loader import SafeLoader

#this python script will filter the samples based on the parameters set in the yaml_file
#further, it will reshuffle the biosample ids and then select it--> to minimize the probability that the samples selected are related
#the preference will be given to the biosample id having only one SRA file

in_file = sys.argv[1]
yaml_file = sys.argv[2]
n_sample = int(sys.argv[3])
output_prefix = sys.argv[4]

biosample_sra_count_dict = {}


###############this function filter the df based on the compulsosry quantitative criteria defined in the parameter yam file######################
def filter_df_quant_col(df, params_dict, n_sample, is_single_srr_df):
    min_base = (
        int(re.match("[0-9]+", params_dict["reference_size"])[0])
        * int(re.match("[0-9]+", params_dict["min_cov"])[0])
        * 1000000000
    )
    df = df[((df["InsertSize"] == 0) & (df["avgLength"]>=params_dict["avgLength"])) | (df["InsertSize"]>=params_dict["min_insert_size"])]
    if is_single_srr_df:
        df = df.loc[df["bases"] >= min_base]
    else:
        df_s=df[["BioSample","bases"]].groupby("BioSample").sum().reset_index()
        df_s = df_s.loc[df_s["bases"] >= min_base]
        df_s_sample = list(df_s["BioSample"])
        df = df.loc[df["BioSample"].isin(df_s_sample)]

    for i in range(10):
        df = df.sample(frac=1)

    selected_samples = random.sample(
        list(set(list(df["BioSample"]))), min(n_sample,len(list(set(list(df["BioSample"])))))
    )


    df = df.loc[df["BioSample"].isin(selected_samples)]

    return df, len(selected_samples)


#######################################################################################################################

##first read yaml file and make dictionary of parameters##
with open(yaml_file, "r") as _:
    params_dict = yaml.load(_, Loader=SafeLoader)

##check if all the quantitative arguments are present in yaml file##
if (
    "min_insert_size" not in params_dict
    or "reference_size" not in params_dict
    or "min_cov" not in params_dict
):
    print(
        "Error: min_cov and min_insert_size and reference_size parameters should be present in parameter yaml file"
    )
    sys.exit(1)

##read csv file containing SRR runinfo data##
df = pd.read_csv(in_file, index_col=None, sep="\t")

col_names = list(df.columns)

qual_dict = {i: v for i, v in params_dict.items() if type(v) == str and i in col_names}

###remove the row that does not match the qualitative criteria##
if (
    len([i for i in col_names if i in params_dict]) == len(params_dict) - 3
):  # check if all parameters are present in the header of runinfo csv file
    for key in qual_dict:
        values = qual_dict[key].split(",")
        df = df.loc[df[key].isin(values)]


###count the SRR files for each biosample
for sample in df["BioSample"]:
    if sample not in biosample_sra_count_dict:
        biosample_sra_count_dict[sample] = 0
    biosample_sra_count_dict[sample] += 1


# now separate the dataframe between biosample having one SRR file and multiple SRR files as each file will be processed separately, single srr has priority
biosample_single_srr = {i: v for i, v in biosample_sra_count_dict.items() if v == 1}

biosample_multi_srr = {i: v for i, v in biosample_sra_count_dict.items() if v > 1}

biosample_single_srr_df = df.loc[df["BioSample"].isin(biosample_single_srr)]

biosample_multi_srr_df = df.loc[df["BioSample"].isin(biosample_multi_srr)]

selected_samples_single_srr_df, n_selected_samples = filter_df_quant_col(biosample_single_srr_df, params_dict, n_sample,True)

if n_selected_samples < n_sample:
    if len(biosample_multi_srr_df["BioSample"]) > 0:
        n_remaining_sample = n_sample - n_selected_samples
        selected_samples_multi_srr_df, n_selected_samples = filter_df_quant_col(
            biosample_multi_srr_df, params_dict, n_remaining_sample,False
        )
        selected_samples_df = pd.concat(
            [selected_samples_single_srr_df, selected_samples_multi_srr_df], ignore_index=True
        )
    else:
        selected_samples_df = selected_samples_single_srr_df
else:
    selected_samples_df = selected_samples_single_srr_df

selected_samples_df.to_csv(f"{output_prefix}_runinfo_selected_samples.csv", index=False)

selected_samples_df[["Run","BioSample"]].to_csv(f"{output_prefix}_selected_samples.tsv", index=False,sep="\t",header=False)
