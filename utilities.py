import os


# define local path to repo
try:
    modulepath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
except NameError:
    modulepath = 'NCAABracketMaker/'

# define package directories
datapath = modulepath + 'TeamData/'
bracketpath = modulepath + 'Brackets/'