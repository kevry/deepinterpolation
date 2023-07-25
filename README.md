# Deep Interpolation for Chen Lab
Tool developed by the AllenInstitute used to denoise data by removing independent noise

https://github.com/AllenInstitute/deepinterpolation

https://github.com/dlamay/deepinterpolation/tree/master

## Running Deepinterpolation inference

1. Clone this repository to your localc SCC directory
``git clone https://github.com/kevry/deepinterpolation.git``

2.	Create a JSON file with an array of full paths to .mat files
Open create_json.py 
Modify the animal, project, session_list, and areas variables as needed. 
	Run python script on SCC:
-	``cd <deep interpolation directory>``
-	``module load python3``
-	``python create_json.py``
  
“Number of .mat files: X”
This will create a JSON file named {animal}_files.json that contains the full paths of all the .mat files that fit the criteria you selected. The python script also prints the number of file paths in the JSON file.


3. Next, open ``deep_interpolation_scc_CPU.sh``. This is the script used to run deep interpolation. The only thing to modify here is the length of the array (line 4). Change the length of the array to 1-(number of file paths in JSON file created/6). Round up if not an integer.

4. Finally, open ``inference_CPU_SCC.py``. Modify lines below (line ~180 and down) accordingly. 
•	jobdir = full path to deep interpolation folder on SCC
•	json_file = name of JSON file created (include .json extension)
•	model_path = name of .h5 (model) file. Current model is already in deepinterpolation folder (include .h5 extension)
•	drive2select = select drive for where to save deep interpolation files (assuming all drives X/Y/W follow same file structure) (enter either “X:”, “Y:”, "V:", or “W:”)

5.	To run deep interpolation now, run command on SCC: ``qsub deep_interpolation_scc_CPU.sh``


## Utilities
#### Check that all files ran through deep interpolation
After running through deep interpolation, some .mat files may have either been accidentally skipped or weren’t able to be run on the current deep interpolation setup. To check for .mat files that may have not run through deep interpolation, you can use ``check_dp_files.py`` located in the ``utils`` folder. For now, this script only works on a local Windows computer. To run, first open the .py script and modify lines 18-36 depending on your situation.  Code should only require traditional python libraries so if you already have python installed on your computer, all you need to enter is 
-	``python check_dp_files.py``

If .mat files were found to be missed by deep interpolation, a JSON file will be created {animal}_missing_files.json with the mat paths. You can use this new JSON file to rerun deep interpolation.

