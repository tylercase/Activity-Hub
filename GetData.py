import numpy as np
import pandas as pd
from pathlib import Path
from config import *

def get_workout_data_package(workout_type:str, run_id:str):
    df = get_data(workout_type, run_id)
    summary = get_workout_summary(workout_type, run_id)
    return (df, summary)


def get_data(workout_type:str, run_id:str):
    df = pd.read_parquet(get_path(workout_type, run_id))
    print(df)
    return df

def get_path(workout_type:str, run_id:str):
    path = Path(fr"user_data\{workout_type}_data\{run_id}.parquet")
    if not path.exists():
        print(f"Path to {path} does not exist")
        return
    return path

def get_workout_summary(workout_type:str, run_id:str):
    summary = get_summary(workout_type)
    return summary[summary["run_id"] == run_id]


def get_summary(workout_type:str):
    match workout_type:
        case "hike":
            summary = pd.read_csv(HIKE_SUMMARY)
        case "run":
            summary = pd.read_csv(RUN_SUMMARY)
        case "walk":
            summary = pd.read_csv(WALK_SUMMARY)
    return summary

def get_ids(workout_type:str):
    return get_summary(workout_type)["run_id"].tolist()