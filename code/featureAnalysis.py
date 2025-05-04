#!/usr/bin/python

import pandas as pd
import numpy as np
import os
import pickle
import gzip
import glob


file_path = r"C:\Users\Ramakrishna\Documents\WorkFolder\ProgramPractice\python\Belka\Data"

file_list = sorted(glob.glob(file_path+os.sep+'*.gz'),reverse=True)

mol_feats = np.empty((0,7),dtype='float16')
morgan_feats = np.empty((0,1024),dtype='uint8')
targs = np.empty((0,3),dtype='uint8')
for fls in file_list:
  with gzip.open(fls, 'rb') as f:
    data = pickle.load(f)
    mol_feats=np.append(mol_feats,data['mol_feats'].astype('float16'),axis=0)
    morgan_feats=np.append(morgan_feats,data['morgan_feats'].astype('uint8'),axis=0)
    targs=np.append(targs,data['targs'].astype('uint8'),axis=0)
  

    

mol_feat_names = ['logP', 'MW', 'rotB', 'HBA', 'HBD', 'nRING', 'TPSA']
morgan_feat_names = []
for k in range(1024):
  morgan_feat_names.append('morgan_'+str(k))

targ_names = ['BRD4','HSA','sEH']



data={'mol_feats': mol_feats,'morgan_feats': morgan_feats,'targs': targs,'mol_feat_names': mol_feat_names, 'morgan_feat_names':morgan_feat_names,'targ_names':targ_names}

import json
with gzip.open(file_path+os.sep+'FeaturesTargets2070K', 'wb') as f:
    pickle.dump(data, f,protocol=pickle.HIGHEST_PROTOCOL)







































  


'''
import json
import zipfile
# Convert dictionary to JSON string
json_str = json.dumps(data)

# Define the file paths
json_filename = 'data.json'
zip_filename = 'data.zip'

# Write JSON string to a file
with open(json_filename, 'w') as json_file:
    json_file.write(json_str)

# Compress the JSON file into a zip file
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(json_filename)

# Optionally, remove the original JSON file
os.remove(json_filename)
'''