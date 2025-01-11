#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Final

BASE_PATH: Final = Path(__file__).resolve().parent
ROOT_PATH: Final = BASE_PATH

import dotenv

dotenv.load_dotenv(ROOT_PATH / "service.env", override=False)

import pickle

import pandas as pd
from fpgrowth_py import fpgrowth


def get_playlists_songs (path: str) -> list[list[str]]:
    raw_dataset = pd.read_csv(path, delimiter=',').sort_values(by="pid")

    return raw_dataset.groupby("pid")["track_name"].apply(list).tolist()

# check if there exists the file in "DATASET_PATH":
if not os.path.exists(os.environ["DATASET_PATH"]):
    while True:
        pass

item_set = get_playlists_songs(os.environ["DATASET_PATH"])

# Generate frequent itemsets and rules
growth = fpgrowth(item_set, minSupRatio=0.05, minConf=0.5)
if growth is None:
    raise ValueError("No frequent itemsets found")

freq_set, rules = growth

with open(os.environ["MODEL_PATH"], "wb") as rules_file:
    pickle.dump(rules, rules_file)
