import os
import json
import glob

# code used to check if individual .mat files have their respective dp.mat files generated from deepinterpolation
# only works on local Windows computer with the necessary mapped drives

## note: this code uses the file structure below ##
# Projects
# - {Project}
#   - Animals
#     - {animal}
#       - 2P
# ex: Projects/Perirhinal/Animals/pr048/2P/

# written by Kevin D.

###################### edit here ##########################
# animal name (ex: "pr065" or "pr061", ...)
animal = 'pr082'

# project name (ex: "ARG" or "Perirhinal")
project = 'ARG'

# sessions to check (ex: [1, 2, 3, 4, 5, ... etc])
session_list = range(1,36)

# areas to check (ex: ['A0_Ch0', 'A1_Ch0'])
areas = ['A0_Ch0', 'A1_Ch0']

# drive where original .mat files are stored (ex: 'Y:')
drive_mat_loc = 'Z:'

# drive where dp.mat files are located
drive_dp_loc = 'Z:'
##########################################################

def convertwindows2linux(path):
	scc2localwind = {'X:': '/net/claustrum2/mnt/data', 'Y:': '/net/claustrum/mnt/data1', 'W:': '/net/claustrum3/mnt/data', 'Z:': '/net/claustrum/mnt/data'}
	path = path.replace('\\', '/')
	path_drive = path[0:2]
	path = path.replace(path_drive, scc2localwind[path_drive])
	return path

# list of mat files not run through deep interpolation
mat_issues_list = []
sess_issues_list = []

# path to 2P folder
local_2p_path = drive_mat_loc + '\\' + os.path.join('Projects', project, 'Animals', animal, '2P')

for session in session_list:
	for area in areas:
		# get list of original .mat files in session folder
		local_mat_path = os.path.join(local_2p_path, '{}-{}'.format(animal, str(session)), 'PreProcess', area)
		mat_files_list = sorted([file for file in os.listdir(local_mat_path) if '.mat' in file and not '_dp' in file])
		
		# get list of generated dp.mat files
		local_dpmat_path = local_mat_path.replace(drive_mat_loc, drive_dp_loc)
		dpmat_files_list = sorted([file.replace('_dp.mat', '.mat') for file in os.listdir(local_dpmat_path) if '_dp.mat' in file])

		for mat_file in mat_files_list:
			if mat_file in dpmat_files_list:
				pass
			else:
				print('{}-{}'.format(animal, str(session)), mat_file, 'not run through deepinterpolation')
				mat_issues_list.append(convertwindows2linux(os.path.join(local_mat_path, mat_file)))

				if session not in sess_issues_list:
					sess_issues_list.append(session)

# if an issue is found, create new json with full path to mat file
if len(mat_issues_list) > 0:
	print('Total files needed for denoising in animal ({}): {}'.format(animal, len(mat_issues_list)))
	print('Sessions with missing denoising files: ', sess_issues_list)

	# write to json file
	json_obj = json.dumps(mat_issues_list)

	output_name = '{}_missing_files.json'.format(animal)
	with open(output_name, "w") as outfile:
		outfile.write(json_obj)
	print('\nSaved paths of .mat files missing denoising to {} in SCC/linux format!'.format(output_name))
else:
	print('All files for {} successfully denoised'.format(animal))