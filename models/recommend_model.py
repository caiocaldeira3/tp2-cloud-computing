#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Final

BASE_PATH: Final = Path(__file__).resolve().parent
ROOT_PATH: Final = BASE_PATH

import dotenv

dotenv.load_dotenv(ROOT_PATH / "service.env", override=False)

import logging
import pickle

import pandas as pd
from fpgrowth_py import fpgrowth

log = logging.getLogger(__name__)


def get_playlists_songs (path: str) -> list[list[str]]:
    log.info(f"reading dataset from path: {path}")
    raw_dataset = pd.read_csv(path, delimiter=',').sort_values(by="pid")

    return raw_dataset.groupby("pid")["track_name"].apply(list).tolist()

item_set = get_playlists_songs(os.environ["DATASET_PATH"])

log.info("item set correctly extracted")

# Generate frequent itemsets and rules
growth = fpgrowth(item_set, minSupRatio=0.05, minConf=0.5)
if growth is None:
    log.info("no frequent item sets were found")
    raise ValueError("No frequent itemsets found")


freq_set, rules = growth

model_path = os.environ["MODEL_PATH"]
log.info(f"saving the pickle model into {model_path}")

with open(model_path, "wb") as rules_file:
    pickle.dump(rules, rules_file)
