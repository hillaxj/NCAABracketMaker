# from NCAABracketMaker.utilities import bracketpath, simbracketpath
# from NCAABracketMaker.AnalyzeGame import scheduleStrength
from NCAABracketMaker.TeamData import nameCheck
# import cProfile
from src.NCAABracketMaker.utilities import teampath, log
# import time
import pandas as pd
import torch
from torch import nn
import matplotlib.pyplot as plt
import numpy as np
from torch.utils.data import Dataset
from typing import Tuple, Dict, List
import os
from torch.utils.data import DataLoader

# Not currently used, for advanced optimization of coefficients based on backtesting. Does not work well


def compareResults(results, simbracket):
    percentAccurate = 0
    # Imports yaml and converts to dict
    # with open(bracketpath + results) as f:
    #     dataResults = yaml.load(f, Loader=yaml.FullLoader)
    # with open(simbracketpath + simbracket) as f:
    #     dataSim = yaml.load(f, Loader=yaml.FullLoader)

    # Import files and converts to dict
    dataResults = pd.read_csv(results, header=None, index_col=0)
    resultsdict = dataResults.to_dict()[1]
    dataSim = pd.read_csv(simbracket, header=None, index_col=0)
    simdict = dataSim.to_dict()[1]

    # Increases percentAccurate if teams in each round match
    # Iterate through each round, skip first round teams
    for x in range(2, 8):
        # Iterates through each region
        for y in range(1, 5):
            seedid = f"d{x}r{y}seed"
            listResultsTeams = [
                v for k, v in resultsdict.items() if k.startswith(seedid)
            ]
            listSimTeams = [v for k, v in simdict.items() if k.startswith(seedid)]
            # If element is in both lists, adds 1 to percentAccurate, perfect is 63 matching elements
            numAccurate = len(
                [
                    z
                    for z in range(len(listResultsTeams))
                    if listResultsTeams[z] in listSimTeams
                ]
            )
            percentAccurate = percentAccurate + (numAccurate * pow(2, (x - 2)))

    return percentAccurate / 192


def format_data_ml(games_data: pd.DataFrame, year: int, league: str):
    # Populates data for past bracket results
    past_bracket_df = pd.read_csv(f"{teampath}Big_Dance_CSV.csv")
    teams_df = pd.read_csv(f"{teampath}{league}{year}.csv", index_col="Team Name")

    # Populates yearlybracket_df for only one year
    yearly_bracket_df = pd.DataFrame()

    for i in range(len(past_bracket_df)):
        if past_bracket_df.at[i, "Year"] == int(year):
            yearly_bracket_df = pd.concat([yearly_bracket_df, past_bracket_df.loc[[i]].get(
                ["Team 0", "Seed 0", "Team 1", "Seed 1", "Team Win"])], ignore_index=True)

    # Checks names in yearly_bracket
    for i in range(len(yearly_bracket_df)):
        yearly_bracket_df.at[i, "Team 0"] = nameCheck(yearly_bracket_df.at[i, "Team 0"])
        yearly_bracket_df.at[i, "Team 1"] = nameCheck(yearly_bracket_df.at[i, "Team 1"])

    seeds_only = yearly_bracket_df.copy()
    # Adds columns for team data
    for i in range(2):
        yearly_bracket_df.insert(2+(i*8), f"Team {i} Win Record", "")
        yearly_bracket_df.insert(3+(i*8), f"Team {i} Loss Record", "")
        yearly_bracket_df.insert(4+(i*8), f"Team {i} Win Ratio", "")
        yearly_bracket_df.insert(5+(i*8), f"Team {i} Schedule Points", "")
        yearly_bracket_df.insert(6+(i*8), f"Team {i} Schedule Wins", "")
        yearly_bracket_df.insert(7+(i*8), f"Team {i} Schedule Rank", "")

    # Populates yearly_bracket_df with team data values
    for i in range(len(yearly_bracket_df)):
        for n in range(2):
            yearly_bracket_df.at[i, f"Team {n} Win Record"] = teams_df.loc[yearly_bracket_df.at[i, f"Team {n}"]][
                "Team Win Record"]
            yearly_bracket_df.at[i, f"Team {n} Loss Record"] = teams_df.loc[yearly_bracket_df.at[i, f"Team {n}"]][
                "Team Loss Record"]
            yearly_bracket_df.at[i, f"Team {n} Win Ratio"] = teams_df.loc[yearly_bracket_df.at[i, f"Team {n}"]][
                "Team Win Ratio"]
            yearly_bracket_df.at[i, f"Team {n} Schedule Points"] = teams_df.loc[yearly_bracket_df.at[i, f"Team {n}"]][
                "Schedule Points"]
            yearly_bracket_df.at[i, f"Team {n} Schedule Wins"] = teams_df.loc[yearly_bracket_df.at[i, f"Team {n}"]][
                "Schedule Wins"]
            yearly_bracket_df.at[i, f"Team {n} Schedule Rank"] = teams_df.loc[yearly_bracket_df.at[i, f"Team {n}"]][
                "Schedule Rank"]
            # Replace team names with team IDs, must be at end to index through teams_df by name
            yearly_bracket_df.at[i, f"Team {n}"] = teams_df.loc[yearly_bracket_df.at[i, f"Team {n}"]]["Team ID"]
            seeds_only.at[i, f"Team {n}"] = teams_df.loc[seeds_only.at[i, f"Team {n}"]]["Team ID"]


# Subclass torch.utils.data.Dataset
class NCAADataCustom(Dataset):

    # Initialize with a targ_data and transform (optional) parameter
    def __init__(self, targ_df: pd.DataFrame(), transform=None) -> None:

        # Create class attributes
        # Setup transforms
        self.transform = transform
        self.targ_data = targ_df

    # Overwrite the __len__() method (optional but recommended for subclasses of torch.utils.data.Dataset)
    def __len__(self) -> int:
        "Returns the total number of samples."
        return len(self.targ_data)

    # Overwrite the __getitem__() method (required for subclasses of torch.utils.data.Dataset)
    def __getitem__(self, index: int) -> Tuple[torch.Tensor, int]:
        "Returns one sample of data, data and label (X, y)."
        game_data = torch.FloatTensor(list(self.targ_data.loc[index])[:-1])
        game_label = self.targ_data.at[index, "Team Win"]

        # Transform if necessary
        if self.transform:
            return self.transform(game_data), game_label  # return data, label (X, y)
        else:
            return game_data, game_label  # return data, label (X, y)


from torch.nn.modules.linear import Linear


# Create a model class
class NCAABracketModelV1(nn.Module):
    def __init__(self, input_shape: int, hidden_units: int, output_shape: int) -> None:
        super().__init__()

        self.layer_stack_1 = nn.Sequential(
            nn.Linear(in_features=input_shape, out_features=hidden_units),
            nn.ReLU(),
            nn.Linear(in_features=hidden_units, out_features=hidden_units),
            nn.ReLU(),
            nn.Linear(in_features=hidden_units, out_features=hidden_units),
        )
        # self.layer_stack_2 = nn.Sequential(
        #     nn.Linear(in_features=hidden_units, out_features=hidden_units),
        #     nn.ReLU(),
        #     nn.Linear(in_features=hidden_units, out_features=hidden_units),
        #     nn.ReLU(),
        #     nn.Linear(in_features=hidden_units, out_features=output_shape),
        # )

    # Define the forward computation (input data x flows through nn.Linear())
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # return self.layer_stack_2(self.layer_stack_1(x))
        return self.layer_stack_1(x)


# @title
from tqdm.auto import tqdm


# @title
def train_step(model: torch.nn.Module,
               dataloader: torch.utils.data.DataLoader,
               loss_fn: torch.nn.Module,
               optimizer: torch.optim.Optimizer):
    # Put model in train mode
    model.train()

    # Setup train loss and train accuracy values
    train_loss, train_acc = 0, 0

    # Loop through data loader data batches
    for batch, (X, y) in enumerate(dataloader):
        # Send data to target device
        X, y = X.to(device), y.to(device)

        # 1. Forward pass
        y_pred = model(X)

        # 2. Calculate  and accumulate loss
        loss = loss_fn(y_pred, y)
        train_loss += loss.item()

        # 3. Optimizer zero grad
        optimizer.zero_grad()

        # 4. Loss backward
        loss.backward()

        # 5. Optimizer step
        optimizer.step()

        # Calculate and accumulate accuracy metric across all batches
        y_pred_class = torch.argmax(torch.softmax(y_pred, dim=1), dim=1)
        train_acc += (y_pred_class == y).sum().item() / len(y_pred)

    # Adjust metrics to get average loss and accuracy per batch
    train_loss = train_loss / len(dataloader)
    train_acc = train_acc / len(dataloader)
    return train_loss, train_acc


# 1. Take in various parameters required for training and test steps
def train(model: torch.nn.Module,
          train_dataloader: torch.utils.data.DataLoader,
          test_dataloader: torch.utils.data.DataLoader,
          optimizer: torch.optim.Optimizer,
          loss_fn: torch.nn.Module = nn.CrossEntropyLoss(),
          epochs: int = 5):
    # 2. Create empty results dictionary
    results = {"train_loss": [],
               "train_acc": [],
               "test_loss": [],
               "test_acc": []
               }

    # 3. Loop through training and testing steps for a number of epochs
    for epoch in tqdm(range(epochs)):
        train_loss, train_acc = train_step(model=model,
                                           dataloader=train_dataloader,
                                           loss_fn=loss_fn,
                                           optimizer=optimizer)
        test_loss, test_acc = test_step(model=model,
                                        dataloader=test_dataloader,
                                        loss_fn=loss_fn)

        # 4. Print out what's happening
        print(
            f"Epoch: {epoch + 1} | "
            f"train_loss: {train_loss:.4f} | "
            f"train_acc: {train_acc:.4f} | "
            f"test_loss: {test_loss:.4f} | "
            f"test_acc: {test_acc:.4f}"
        )

        # 5. Update results dictionary
        results["train_loss"].append(train_loss)
        results["train_acc"].append(train_acc)
        results["test_loss"].append(test_loss)
        results["test_acc"].append(test_acc)

    # 6. Return the filled results at the end of the epochs
    return results


# @title
def test_step(model: torch.nn.Module,
              dataloader: torch.utils.data.DataLoader,
              loss_fn: torch.nn.Module):
    # Put model in eval mode
    model.eval()

    # Setup test loss and test accuracy values
    test_loss, test_acc = 0, 0

    # Turn on inference context manager
    with torch.inference_mode():
        # Loop through DataLoader batches
        for batch, (X, y) in enumerate(dataloader):
            # Send data to target device
            X, y = X.to(device), y.to(device)

            # 1. Forward pass
            test_pred_logits = model(X)

            # 2. Calculate and accumulate loss
            loss = loss_fn(test_pred_logits, y)
            test_loss += loss.item()

            # Calculate and accumulate accuracy
            test_pred_labels = test_pred_logits.argmax(dim=1)
            test_acc += ((test_pred_labels == y).sum().item() / len(test_pred_labels))

    # Adjust metrics to get average loss and accuracy per batch
    test_loss = test_loss / len(dataloader)
    test_acc = test_acc / len(dataloader)
    return test_loss, test_acc


train_df = yearly_bracket_df.sample(frac=0.8, ignore_index=True)
test_df = yearly_bracket_df.loc[~yearly_bracket_df.index.isin(train_df.index)]
train_data = NCAADataCustom(targ_df=train_df)
test_data = NCAADataCustom(targ_df=test_df)
device = "cude" if torch.cuda.is_available() else "cpu"
device

# Setup batch size and number of workers
BATCH_SIZE = 8
NUM_WORKERS = os.cpu_count()
print(f"Creating DataLoader's with batch size {BATCH_SIZE} and {NUM_WORKERS} workers.")

# Create DataLoader's
train_dataloader = DataLoader(train_data,
                                     batch_size=BATCH_SIZE,
                                     shuffle=True,
                                     num_workers=NUM_WORKERS)

test_dataloader = DataLoader(test_data,
                                    batch_size=BATCH_SIZE,
                                    shuffle=False,
                                    num_workers=NUM_WORKERS)

# Set random seeds
# torch.manual_seed(42)
# torch.cuda.manual_seed(42)
# Set random seeds
# torch.manual_seed(42)
# torch.cuda.manual_seed(42)

# Set number of epochs
NUM_EPOCHS = 200

# Recreate an instance of TinyVGG
model_3 = NCAABracketModelV1(input_shape=4,
                  hidden_units=8,
                  output_shape=1).to(device)

# Setup loss function and optimizer
loss_fn = nn.L1Loss()
optimizer = torch.optim.SGD(params=model_3.parameters(), lr=0.001)

# Start the timer
from timeit import default_timer as timer
# Set number of epochs
NUM_EPOCHS = 200

# Recreate an instance of TinyVGG
model_3 = NCAABracketModelV1(input_shape=4,
                  hidden_units=8,
                  output_shape=1).to(device)

# Setup loss function and optimizer
loss_fn = nn.L1Loss()
optimizer = torch.optim.SGD(params=model_3.parameters(), lr=0.001)

start_time = timer()

# Train model_0
model_3_results = train(model=model_3,
                        train_dataloader=train_seeds_dataloader,
                        test_dataloader=test_seeds_dataloader,
                        optimizer=optimizer,
                        loss_fn=loss_fn,
                        epochs=NUM_EPOCHS)

# End the timer and print out how long it took
end_time = timer()
print(f"Total training time: {end_time-start_time:.3f} seconds")
# Start the timer
from timeit import default_timer as timer
# Below used for back testing ONLY
# Gets team data from web, run once ESPN has data from 2006 - current year
# Takes a long time to import data, ~10 min per year
# for x in range(2006, 2023):
#     getTeamData(league, x)

# Populate yaml/csv files from past brackets, run once CSV has data from 1985 - 2019
# for x in range(2006, 2023):
#     populateResults(x)

# increment = 0.25
# for i in numpy.arange(1.2, 2.5, .1):
#     for j in numpy.arange(1.2, 2.5, .1):
#         # for k in numpy.arange(0, 1.3, .1):
#         # for m in numpy.arange(.8, 2.5, .1):
# compareList = []
# # Calculate schedule strength, before bracketSim
# log.info(f'NextSim {i} {j} {k} {m}')
# scheduleWeight = i + j +  0.0001
#
# for x in range(year, 2020):
#     teamdatacsv = f'mens{x}.csv'
#     bracketresultsyaml = f'{x}results.yaml'
#     bracketSim(bracketresultsyaml, teamdatacsv)
#     compareList.append(compareYamls(bracketresultsyaml, f'mens{x}SimResults.yaml'))
#
# compareValue = sum(compareList) / len(compareList)
# print(compareValue)
# # Poorly simulate results based on starting 64 or 68 teams
# if compareValue > averageAccuracy:
#     averageAccuracy = compareValue
#     winWeight = i
#     rankWeight = j
#     pointsWeight = k
#     scheduleWeight = m
#     log.info(f'{averageAccuracy} {i} {j} {k} {m}')
#
# print('Accuracy : ' + str(averageAccuracy))
# print('winWeight : ' + str(winWeight))
# print('rankWeight : ' + str(rankWeight))
# print('pointWeight : ' + str(pointsWeight))
# print('scheduleWeight : ' + str(scheduleWeight))


# Use to sim current year bracket
# getTeamData(league, str(2022))
# bracketSim('NCAAMBracket2022.yaml', f'{league}{year}.csv', i, j, k, m)
# print(compareYamls(f'{year}results.yaml', f'{league}{year}-{i}-{j}-{k}-{m}-SimResults.csv'))
