import os
import sys
import glob
import json


############################################################
#change to animal name (pr060, pr048, ...)
animal = 'pr065'

# change project (ARG, Perirhinal, ...)
project = 'ARG'

# single session do session_list = [n] where n is the session number
# note: to input a range of sessions example: session_list = list(range(min, max+1))
session_list = [6, 7, 8 , 9]

# channel (A0 or A1)
areas = ['A0_Ch0', 'A1_Ch0']

# drive location
drivelocation = 'Y:'
##############################################################

scc2localwind = {'X:': '/net/claustrum2/mnt/data', 'Y:': '/net/claustrum/mnt/data1', 'W:': '/net/claustrum3/mnt/data', 'V:': '/net/claustrum4/mnt/storage/data'}

#change to animal path
animal_path = os.path.join(scc2localwind[drivelocation], 'Projects', project, 'Animals', animal, '2P')

#change to what you want json file to be named
output_name = animal + "_files.json"

# full list of .mat file paths
local_train_paths = []

# run through each session and area needed
for session in session_list:
    for area in areas:
        # get list of .mat files
        local_mat_path = os.path.join(animal_path, '{}-{}'.format(animal, str(session)), 'PreProcess', area)
        mat_files_list = sorted([os.path.join(local_mat_path, file) for file in os.listdir(local_mat_path) if ('.mat' in file) and ('ds_data' not in file)])
        local_train_paths.extend(mat_files_list)
        
# number of .mat files collected        
print('Number of .mat files:', len(local_train_paths))

# save paths to json
json_obj = json.dumps(local_train_paths)
with open(output_name, "w") as outfile:
    outfile.write(json_obj)