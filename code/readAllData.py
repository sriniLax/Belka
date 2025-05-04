from zipfile import ZipFile
import pandas as pd
import numpy as np
import os


import polars as pl


import timeit


tstart = timeit.default_timer()

# Path to your zip file
zip_file_path = ".."+os.sep+"Data"+os.sep+"leash-BELKA.zip"

N=int(10e+6)

'''
# Extract the CSV file from the zip
with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
  csv_file_name = "train.csv"  # Replace with the actual CSV file name
  with zip_ref.open(csv_file_name) as csv_file:
    df = pl.read_csv(csv_file, n_rows=N-1,columns=['buildingblock1_smiles', 'buildingblock2_smiles','buildingblock3_smiles','molecule_smiles','protein_name','binds'])#,low_memory=True) # ,skiprows=0,
'''
pl.read_csv(ZipFile(zip_file_path).open("train.csv", 'r').read(),n_rows=N-1,columns=['buildingblock1_smiles', 'buildingblock2_smiles','buildingblock3_smiles','molecule_smiles','protein_name','binds'])

   
tend = timeit.default_timer()

print('File reading time (s): ',tend-tstart)


tstart=timeit.default_timer()
d1=df.pivot(index='molecule_smiles',columns='protein_name',values='binds')

d1=d1.astype(bool)

d2=df.loc[:,['buildingblock1_smiles', 'buildingblock2_smiles','buildingblock3_smiles','molecule_smiles']].group_by('molecule_smiles').first()

dk=pd.concat([d2,d1],axis=1)

dk.index=dk.index.str.replace('[Dy]','')

tend = timeit.default_timer()

print('dataframe rearrangement time (s): ',tend-tstart)

#dk=dk.reset_index() # make molecule_smiles a column of the dataframe