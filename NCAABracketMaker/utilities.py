import os
import logging as log
import sys
import shutil


# define log.info output format
log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)-8s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stdout)

source_dir = str(os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')) + '/'
modulepath = source_dir

# define local path to repo
def get_savepath(local_dir):
    global modulepath
    try:
        if local_dir != str(os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')) + '/':
            modulepath = local_dir + '/BracketMaker'
        else:
            modulepath = local_dir
    except NameError:
        modulepath = 'NCAABracketMaker/'


# define package directories
teampath = source_dir + 'TeamData/'
bracketpath = source_dir + 'Brackets/'
simbracketpath = modulepath + 'SimBrackets/'

# Creates new directories
destination_dir = modulepath
os.makedirs(destination_dir, exist_ok=True)

folder_list = ['SimBrackets/']
# Fetch all files
for folder in folder_list:
    # Creates directory if needed
    os.makedirs(destination_dir + folder, exist_ok=True)
    for file_name in os.listdir(source_dir + folder):
        # Construct full file path
        source = source_dir + folder + file_name
        destination = destination_dir + folder + file_name
        # Move only files
        if os.path.exists(source) and not os.path.exists(destination):
            shutil.copy(source, destination)
            log.info('File Copied:' + file_name)
