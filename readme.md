# Preparation
## Prepare virtual environment

Run the ```prepare_env.ps1``` or follow the steps in the file to prepare the virtual environment for the project.

## Create executable file from the project

Run ```create_installer.ps1``` of follow the steps in the file to prepare the executable.

# Usage

1. Input preparation
	1. Prepare the dictionary files:
		1. it shall contains comma separated values in a row: ```original name; new name```
		1. each dictionary record shall be separated by a new line.
		1. if multiple files linked to the same renaming process, the dictionary files will be concatenated.
		1. the following file extensions are allowed: '.txt', '.csv'
	1. prepare the list of the measurement files.
		1. the following file extensions are allowed: '.mf4', '.dat'
	1. use the the following key to determine the file name extension of the ```new_fname_ext=_renamed```
		1. the default is '_renamed'
1. After successful environment installation, you can run it as a python script:
	e.g. ```python.exe .\mdf_channel_rename.py .\test.mf4 .\channel_name_list.csv  new_fname_ext=_renamed```
2. You can do the same wih the binary version:
	e.g. ```.\mdf-channel-rename_3b71fc9.exe .\test.mf4 .\channel_name_list.csv```
3. ... or you can just drag the input files and drop it on the executable version.
