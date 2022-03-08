"""
Call on functions to pull data and create brackets
"""
from AnalyzeGame import *
from BracketBuilder import *
from TeamData import *


# run bracket simulation
# Offical bracket for NCAA games
bracketfile = 'MCAAMBracket2021.yaml'
# Team data for bracket year
teamdatafile = 'menscollegebasketball2021.csv'
# Runs simulation
bracketSim(bracketfile, teamdatafile)
