#/usr/bin/python
import zipfile
import pandas as pd
import numpy as np
import os
# Path to your zip file
zip_file_path = ".."+os.sep+"Data"+os.sep+"leash-BELKA.zip"

# Extract the CSV file from the zip
with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
  csv_file_name = "train.csv"  # Replace with the actual CSV file name
  with zip_ref.open(csv_file_name) as csv_file:
    df = pd.read_csv(csv_file, skiprows=0, nrows=10000000-1)
    



ibnds=df.binds
ib=df.protein_name=='BRD4'
ih=df.protein_name=='HSA'
ie=df.protein_name=='sEH'

mol_brd=set(df.loc[ib&ibnds,'molecule_smiles'].unique())
mol_hsa=set(df.loc[ih&ibnds,'molecule_smiles'].unique())
mol_eph=set(df.loc[ie&ibnds,'molecule_smiles'].unique())






#df.to_csv(".."+os.sep+"Data"+os.sep+"TenPercSet.csv",compression='.zip',index=False)

'''
import matplotlib.pyplot as plt
from matplotlib_venn import venn3


# Plot the Venn diagram
venn3([mol_hsa, mol_brd, mol_eph], ('HSA', 'BRD', 'EPH'))
plt.title("Venn Diagram for Three Sets")
plt.show()
'''

def printSummary(df):
  ibnds=df.binds
  ib=df.protein_name=='BRD4'
  ih=df.protein_name=='HSA'
  ie=df.protein_name=='sEH'  
  mol_hsa=set(df.loc[ih&ibnds,'molecule_smiles'])
  mol_brd=set(df.loc[ib&ibnds,'molecule_smiles'])
  mol_eph=set(df.loc[ie&ibnds,'molecule_smiles'])  
  molt=mol_hsa.intersection(mol_brd)
  molt=molt.intersection(mol_eph)
  print(f'Molecules that bind to all 3 protiens {len(molt)}')
  print(f'Molecules that bind to HSA and also bind to BRD4 {len(mol_hsa.intersection(mol_brd))}')
  print(f'Molecules that bind to HSA and also bind to EPH {len(mol_hsa.intersection(mol_eph))}')
  print(f'Molecules that bind to EPH and also bind to BRD4 {len(mol_eph.intersection(mol_brd))}')  
  mol1=mol_hsa.difference(mol_brd)
  mol2=mol1.difference(mol_eph)
  print(f'Molecules that bind to HSA but not to BRD4 or EPH {len(mol2)}')
  mol1=mol_brd.difference(mol_hsa)
  mol2=mol1.difference(mol_eph)
  print(f'Molecules that bind to BRD4 but not to HSA or EPH {len(mol2)}')
  mol1=mol_eph.difference(mol_hsa)
  mol2=mol1.difference(mol_brd)
  print(f'Molecules that bind to EPH but not to BRD4 or HSA {len(mol2)}')  
  print(f'%prevalence binding to HSA: {100*np.sum(ih&ibnds)/np.sum(ih)}')
  print(f'%prevalence binding to BRD: {100*np.sum(ib&ibnds)/np.sum(ib)}')
  print(f'%prevalence binding to EPH: {100*np.sum(ie&ibnds)/np.sum(ie)}')
  print('Binding numbers, HSA, BRD, EPH: ', np.sum(ih&ibnds),np.sum(ib&ibnds),np.sum(ie&ibnds) )
  print('Total numbers, HSA, BRD, EPH: ', np.sum(ih),np.sum(ib),np.sum(ie))

'''
# 3 molecules that bind to HSA and BRD4
C=CCC[C@@H](Nc1nc(NCC2CS(=O)(=O)c3ccccc32)nc(Nc2ccc(=O)n(C)c2)n1)C(=O)N[Dy]
C=CCC[C@@H](Nc1nc(Nc2ccc(=O)n(C)c2)nc(Nc2nc[nH]n2)n1)C(=O)N[Dy]
C=CCC[C@@H](Nc1nc(NCc2cc3c(s2)CCSC3)nc(Nc2ccc(OC)c(OC)c2)n1)C(=O)N[Dy]
'''

printSummary(df)

from Needed_Functions.utils import *

d1=df.pivot(index='molecule_smiles',columns='protein_name',values='binds')

d1=d1.astype(bool)

d2=df.loc[:,['id','buildingblock1_smiles', 'buildingblock2_smiles','buildingblock3_smiles','molecule_smiles']].groupby('molecule_smiles').first()

dk=pd.concat([d2,d1],axis=1)

dk.index=dk.index.str.replace('[Dy]','')
dk=dk.reset_index() # make molecule_smiles a column of the dataframe

# write out the csv file for 10% of the data
dk.to_csv('..'+os.sep+'Data'+os.sep+'TenPercData.zip',compression='zip',index=False)



#dk['Morgan_Fingerprint'] = dk['molecule_smiles'].apply(morgan_fingerprint, radius=2, nBits=1024)
'''
stan=np.vectorize(standardize_init)
#dk['molecule_smiles'] = dk['molecule_smiles'].apply(standardize_init)

stan=np.vectorize(standardize_init)
stan_mols=stan(dk['molecule_smiles'].values)

dk.index=stan_mols
'''
'''
df['molecule_smiles'] = df['molecule_smiles'].str.replace('[Dy]','')

stan=np.vectorize(standardize_init)
df['molecule_smiles'] = df['molecule_smiles'].apply(standardize_init)

df['Morgan_Fingerprint'] = df['molecule_smiles'].apply(morgan_fingerprint, radius=2, nBits=1024)

df[["logP", "MW", "rotB", "HBA", "HBD", "nRING", "TPSA"]] = df["Smiles_stand"].apply(calc_mol_properties)

print(df.shape)



# set seed for NumPy
seed=2024
rng = np.random.default_rng(seed)
np.random.seed(seed)

rng.choice(df.shape)

from sklearn.model_selection import train_test_split as tts

train,test=tts(df,test_size=0.4,random_state=seed)

train,valid=tts(train,test_size=0.3,random_state=2024)


  
  

printSummary(train)
printSummary(valid)
printSummary(test)  


train.to_csv(".."+os.sep+"Data"+os.sep+"Train_TenPercSet.zip",compression='zip',index=False)
valid.to_csv(".."+os.sep+"Data"+os.sep+"Valid_TenPercSet.zip",compression='zip',index=False)
test.to_csv(".."+os.sep+"Data"+os.sep+"Test_TenPercSet.zip",compression='zip',index=False)

'''
