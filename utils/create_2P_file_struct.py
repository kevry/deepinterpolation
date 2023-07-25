import os

# run code to create THIS structure in preferred network drive. 
# Usually this is done before running deep interpolation on the SCC

# the file structure is as follows
# Projects
# - {Project name}
#   - Animals
#     - {animal}
#       - 2P
#         - {animal}-{session-no}
#           - A0_Ch0
#    		- A1_Ch0
#           - ... 

# written by Kevin D.

########## edit here ##########
animal = 'pr077' # change for animal (pr060, pr048, ...)

project = 'Perirhinal' # change to project being used

num_of_sessions = 30 # change to number of total sessions for animal (4, 5, 6, 7, 8, ...)

drive_selection = 'W:' # select which drive to create file structure (X:, Y:, W:, Z:, ...)

channel_array = ['A0_Ch0', 'A1_Ch0'] # list of channel folders to create
##############################


def makedir(path):
	""" create single directory avoiding thrown error if directory already exists """
	try:
		os.mkdir(path)
		print('Path: {} created'.format(path))
	except:
		print('Path: {} already exists'.format(path))


main_2P_path = drive_selection + os.path.join('Projects', project, 'Animals', animal, '2P')
os.makedirs(main_2P_path, exist_ok = True)

for i in range(1, num_of_sessions + 1):

	folder_session = '{}-{}'.format(animal, str(i))
	path = os.path.join(main_2P_path, folder_session)
	makedir(path)

	path = os.path.join(path, 'PreProcess')
	makedir(path)

	for channel in channel_array:
		area_path = os.path.join(path, channel)
		makedir(area_path)

print('File structure setup!')