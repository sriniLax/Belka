#!/usr/bin/python
import numpy as np
import pandas as pd
from rdkit import Chem
from chembl_structure_pipeline import standardizer
from rdkit.Chem import Descriptors
from rdkit.Chem import AllChem

# set standardize function
def standardize_init(smiles):
    try:
        molecule = Chem.MolFromSmiles(smiles)
        m_no_salts = standardizer.get_parent_mol(molecule)
        tostandarize = m_no_salts[0]
        std_mol = standardizer.standardize_mol(tostandarize)
        canonical_smiles = Chem.MolToSmiles(std_mol)
        return canonical_smiles
    except Exception as e:
        print(f"Error processing SMILES: {smiles}")
        print(e)
        return None
        
        
# Define a function to calculate the molecular properties
def calc_mol_properties(smiles):
    mol = Chem.MolFromSmiles(smiles)
    logP = Descriptors.MolLogP(mol)
    MW = Descriptors.MolWt(mol)
    rotB = Descriptors.NumRotatableBonds(mol)
    HBA = Descriptors.NumHAcceptors(mol)
    HBD = Descriptors.NumHDonors(mol)
    nRING = Descriptors.RingCount(mol)
    TPSA = Descriptors.TPSA(mol)
    
    return pd.Series([logP, MW, rotB, HBA, HBD, nRING, TPSA])


def morgan_fingerprint(smiles, radius, nBits):
    mol = Chem.MolFromSmiles(smiles)
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=nBits)
    return np.array(fp, dtype=np.int8)    