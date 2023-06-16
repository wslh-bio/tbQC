#!/usr/bin/env python3
import sys
import glob
import pandas as pd
from functools import reduce

with open(sys.argv[1], 'r') as krakenFile:
    for l in krakenFile.readlines():
        if "kraken DB:" in l.strip():
            krakenDB_version = l.strip().split(':')[1].strip()

files = glob.glob('*.tsv')

dfs = []

for file in files:
    df = pd.read_csv(file, header=0, delimiter='\t')
    dfs.append(df)

merged = reduce(lambda  left,right: pd.merge(left,right,on=['Sample'],how='left'), dfs)
merged = merged.assign(krakenDB=krakenDB_version)
merged = merged.assign(tbqc=sys.argv[2])
merged = merged[['Sample','Total Reads','Reads Removed','Median Coverage','Average Coverage','Contigs','Assembly Length (bp)','N50','Primary Species (%)','Secondary Species (%)','Unclassified Reads (%)','krakenDB','Primary Mash Species (Identity)','Secondary Mash Species (Identity)','MLST Scheme','tbqc']]
merged = merged.rename(columns={'Contigs':'Contigs (#)','Average Coverage':'Mean Coverage','krakenDB':'Kraken Database Verion','tbqc':'tbqc Version'})

merged.to_csv('tbqc_report.csv', index=False, sep=',', encoding='utf-8')
