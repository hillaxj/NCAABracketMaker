"""
Call on functions to pull data and create brackets
"""
from AnalyzeGame import *
from BracketBuilder import *
from TeamData import *


# run bracket simulation
bracketfile = '2021results.yaml'
teamdatafile = 'menscollegebasketball2021.csv'
bracketSim(bracketfile, teamdatafile)
