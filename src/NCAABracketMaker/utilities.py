import os
import logging
import sys
import shutil


# define log.info output format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)

# define local path to repo
try:
    modulepath = (
        str(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")) + "/"
    )
    # If a different filepath is needed for the results, change deskpath to the desired location
    deskpath = os.environ["HOME"] + "/Desktop/"
except NameError:
    modulepath = "src/NCAABracketMaker/"
    deskpath = "src/NCAABracketMaker/"


# define package directory paths
teampath = modulepath + "TeamData/"
bracketpath = modulepath + "Brackets/"
simbracketpath = deskpath + "SimBrackets/"

# Creates new directory for deskpath if needed
destination_dir = deskpath
os.makedirs(destination_dir, exist_ok=True)

# Set up to move multiple folders to deskpath if needed, only moving SimBracket for now
folder_list = ["SimBrackets/"]
# Fetch all files
for folder in folder_list:
    # Creates directory if needed
    os.makedirs(destination_dir + folder, exist_ok=True)
    os.makedirs(modulepath + folder, exist_ok=True)
    for file_name in os.listdir(modulepath + folder):
        # Construct full file path
        source = modulepath + folder + file_name
        destination = destination_dir + folder + file_name
        # Move only files
        if os.path.exists(source) and not os.path.exists(destination):
            shutil.copy(source, destination)
            logging.info("File Copied:" + file_name)