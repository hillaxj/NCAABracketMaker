# NCAABracketMaker
NCAABracketMaker is designed to create a simulated NCAA march madness bracket with data
from each team's performance. It will save the output the simulated bracket to a folder on the desktop in a csv file
as well as populate a xlsx file formatted to display the results in a populated bracket. In the xlsx file, simulation
results can be selected from a dropdown list to easily compare different parameters.

## Installation
pip install git+https://github.com/hillaxj/NCAABracketMaker

## Usage
Running the bracketmaker function will do all the work. On the first run, it will import each team's data for the given
year and populate the current year's bracket. Importing the data takes a few minutes but after that, each simulation
is fast. The results will be added to the folder SimBrackets on the desktop. If needed, the filepath can be changed in
utilities.py.

```Python
from NCAABracketMaker import bracketmaker
# Example values populated below
league = 'mens'     # Must be 'mens' or 'womens'
year = 2022         # Empty brackets available for 2021 and 2022 only

win = 1             # Recommend: Float between 0 and 1
rank = 1            # Recommend: Float between 0 and 1
points = .5         # Recommend: Float between 0 and 1
schedule = 5        # Recommend: Float between 1 and 10

# Can clear simulated brackets by setting reset to True, default is False
reset = False

# Imports data from current year and simulates bracket with defined parameters. Open Sim_Bracket.xlsx to see results.
bracketmaker(league, year, win, rank, points, schedule, reset)

```
## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

# History
Current version 1.1.0 added quality of life improvements \
Legacy version 1.0.0 it worked but was not user-friendly

## License
MIT License

Copyright (c) 2022 Alex Hill

