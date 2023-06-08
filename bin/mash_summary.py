#!/usr/bin/env python3

import os
import glob
import pandas as pd
from pandas import DataFrame

# function for summarizing Mash result files
def summarize_mash(file):
    # get sample id from file name
    sample_id = os.path.basename(file).split('.')[0].replace('.mash.tsv','')
    # read tsv file and add column names
    df = pd.read_csv(file, sep='\t', names=['RefSeq ID','Sample','Identity','P-value','Shared Hashes'])
    df = df.head(2)
    # keep only Sample RefSeq ID and Identity columns in data frame
    df = df[['Sample','RefSeq ID','Identity']]
    # check if data frame has two rows
    if len(df) == 0:
        # add two empty rows to species data frame
        df = df.append(pd.Series(), ignore_index=True)
        df = df.append(pd.Series(), ignore_index=True)
    if len(df) == 1:
        # add one empty row to species data frame
        df = df.append(pd.Series(), ignore_index=True)
    # if primary species is nan, replace with NA
    if str(df.iloc[0]['RefSeq ID']) == 'nan':
        primary_species = 'NA'
    # else, get primary RefSeq ID match and put Identity in parentheses
    else:
        primary_species = df.iloc[0]['RefSeq ID'] + ' (' + str(df.iloc[0]['Identity']) + ')'
    # repeat for secondary species
    if str(df.iloc[1]['RefSeq ID']) == 'nan':
        secondary_species = 'NA'
    else:
        print(df.iloc[1]['RefSeq ID'])
        secondary_species = df.iloc[1]['RefSeq ID'] + ' (' + str(df.iloc[1]['Identity']) + ')'
    # list of lists
    combined = [[sample_id, primary_species, secondary_species]]
    # convert list of lists to data frame
    combined_df = DataFrame(combined, columns=['Sample','Primary Mash Species (Identity)','Secondary Mash Species (Identity)'])
    return combined_df


# get all mash result files
files = glob.glob("data/*.mash.tsv")

# summarize kraken2 report files
results = map(summarize_mash, files)

# concatenate summary results and write to tsv
results = list(results)

if len(results) > 1:
    data_concat = pd.concat(results)
    data_concat.to_csv(f'mash_results.tsv',sep='\t', index=False, header=True, na_rep='NaN')
else:
    results = results[0]
    results.to_csv(f'mash_results.tsv',sep='\t', index=False, header=True, na_rep='NaN')
