import logging as log
from utilities import bracketpath
import pandas as pd
import yaml

with open(bracketpath + 'Bracket2021.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    print(data)