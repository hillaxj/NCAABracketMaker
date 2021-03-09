"""
Call on functions to pull data and create brackets
"""
from AnalyzeGame import *
from BracketBuilder import *
from TeamData import *


# run bracket simulation
bracketfile = 'NCAAMBracket2021.yaml'
teamdatafile = 'menscollegebasketball2021.csv'
df = bracketSim(bracketfile, teamdatafile)
