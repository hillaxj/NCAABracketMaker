import os
import logging as log
import sys

# define local path to repo
try:
    modulepath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
except NameError:
    modulepath = 'NCAABracketMaker/'

# define package directories
datapath = modulepath + 'TeamData/'
bracketpath = modulepath + 'Brackets/'

log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)-8s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stdout)
