import pandas as pd
import numpy as np
from config import *

hikes_summary = pd.read_csv(HIKE_SUMMARY)
runs_summary = pd.read_csv(RUN_SUMMARY)
walks_summary = pd.read_csv(WALK_SUMMARY)


def get_hikes_summary():
    summary = pd.read_csv(HIKE_SUMMARY)
    return summary

def get_runs_summary():
    summary = pd.read_csv(RUN_SUMMARY)
    return summary

def get_walks_summary():
    summary = pd.read_csv(WALK_SUMMARY)
    return summary

def get_hikes_ids() -> list[str]:
    summary = pd.read_csv(HIKE_SUMMARY)
    return summary["run_id"].tolist()

def get_runs_ids() -> list[str]:
    summary = pd.read_csv(RUN_SUMMARY)
    return summary["run_id"].tolist()

def get_walks_ids() -> list[str]:
    summary = pd.read_csv(WALK_SUMMARY)
    return summary["run_id"].tolist()