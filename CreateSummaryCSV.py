import pandas as pd
from config import *
from pathlib import Path

def create_summaries():
    folders = (
        HIKE_DIR,
        RUN_DIR,
        WALK_DIR
    )

    summaries = (
        HIKE_SUMMARY,
        RUN_SUMMARY,
        WALK_SUMMARY
    )

    for folder in folders:
        if folder.exists():
            print(f"Folder at {folder} already exists, skipping.")
            continue
        folder.mkdir(parents=True, exist_ok=False)

    for summary in summaries:
        if summary.exists():
            print(f"summary.csv already exists at {summary}, skipping.")
            continue
        empty_df = pd.DataFrame(columns=SUMMARY_COLS)
        empty_df.to_csv(summary)

    print("Folders created")