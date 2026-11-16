from pathlib import Path

GPX_DF_COLS = (
    "latitude",
    "longitude",
    "elevation",
    "time",
    "speed",
    "cadence",
    "hr"
)

SUMMARY_COLS = (
    "run_id",
    "duration",
    "distance",
    "max_hr",
    "avg_hr",
    "elevation_gain",
    "elevation_loss",
    "avg_speed",
    "avg_cadence",
    "primary_zone"
)

PLOTTING_COLOR_DICT = {
    "hr": "red",
    "speed": "blue",
    "elevation": "green",
    "cadence": "purple",
    "zone": "black"
}

SUMMARY_UNITS = [
    "",
    "",
    "miles",
    "bpm",
    "bpm",
    "ft",
    "ft",
    "mph",
    "",
    ""
]

MAX_HR = 205

HIKE_DIR = Path(r"user_data\hike_data")
RUN_DIR = Path(r"user_data\run_data")
WALK_DIR = Path(r"user_data\walk_data")

HIKE_SUMMARY = Path(r"user_data\hike_data\summary.csv")
RUN_SUMMARY = Path(r"user_data\run_data\summary.csv")
WALK_SUMMARY = Path(r"user_data\walk_data\summary.csv")