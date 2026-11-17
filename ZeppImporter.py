from pathlib import Path
from collections import Counter
from config import *
from geopy.distance import geodesic
import gpxpy
import pandas as pd
import numpy as np

def import_workout(path:str, workout_type:str):
    file_path = get_file_path(path)
    if file_path == None:
        print(f"File does not exist or is in the wrong format, please check again.\n Filepath: {path}")
        return

    df = extract_basic_data(file_path)
    summary = get_summary(df)
    print(summary)

    # print(f"New {workout_type} imported")
    return (df, summary)

def import_workouts(path:str, workout_type:str):
    file_paths = get_file_paths(path)
    dfs = []
    summaries = []

    for file in file_paths:
        df = extract_basic_data(file)
        dfs.append(df)
        summaries.append(get_summary(df))

    return (dfs, summaries)
        


def get_file_paths(folder:str):
    folder_path = Path(folder)
    file_paths = []

    for file in folder_path.iterdir():
        if file.is_file() and file.suffix == ".gpx":
            file_paths.append(file)

    return file_paths


def get_info(workout_type, workout_data):
    return (workout_type, workout_data[1]["run_id"].iloc[0])

def get_summary(df:pd.DataFrame) -> pd.DataFrame:
    lst = [
        "-".join(str(df["time"].iloc[0]).split("-")[:-1]).replace(":","_"),     # run_id
        (df["time"].iloc[-1] - df["time"].iloc[0]).total_seconds(),             # duration
        round(float(df["distance"].iloc[-1]), 2),                               # distance
        int(df["hr"].max()),                                                    # max_hr
        int(df["hr"].mean()),                                                   # avg_hr
        round(sum([i for i in df["d_elevation"] if i > 0]), 2),                 # elevation_gain
        round(sum([i for i in df["d_elevation"] if i < 0]), 2),                 # elevation_loss
        round(float(df["speed"].mean()), 2),                                    # avg_speed
        int(df["cadence"].mean()),                                              # avg_cadence
        int(df["zone"].mode().iloc[0])                                          # zone
    ]


    df = pd.DataFrame([lst], columns=SUMMARY_COLS)
    return df

def extract_basic_data(path:Path) -> pd.DataFrame:
    # All workout types have these same points of data,
    # Then each workout type gets their own additional data if applicable
    with open(path) as fh:
        gpx = gpxpy.parse(fh)

    # gpx_tags = list_extensions(gpx)

    data = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                new_row = [
                    point.latitude,
                    point.longitude,
                    point.elevation,
                    point.time,
                    get_extension_value(point, "speed"),
                    get_extension_value(point, "cad"),
                    get_extension_value(point, "hr")
                ]

                data.append(new_row)
    df = pd.DataFrame(data, columns=GPX_DF_COLS)
    df = clean_df(df)
    df = get_hr_zones(df)
    df = get_deltas(df)
    
    return df

def clean_df(df:pd.DataFrame) -> pd.DataFrame:
    # force important values to numerical
    df[["latitude", "longitude", "elevation", "speed", "hr", "cadence"]] = \
        df[["latitude", "longitude", "elevation", "speed", "hr", "cadence"]].apply(pd.to_numeric)

    df["time"] = pd.to_datetime(df['time'], utc=True).dt.tz_convert("America/Los_Angeles")
    df["speed"] = df["speed"].interpolate(limit=5)
    df["hr"] = df["hr"].interpolate(limit=5)
    df["elevation"] = df["elevation"].interpolate(limit=5)
    df["cadence"] *= 2
    return df

def get_hr_zones(df: pd.DataFrame) -> pd.DataFrame:
    # Determines hr zones based on hr data
    max_hr = MAX_HR
    df_length = df.shape[0]
    df["zone"] = 1

    for i in range(df_length):
        hr = df["hr"][i]

        match hr:
            case x if x > 0.98 * max_hr:
                df.loc[i, "zone"] = 5
            case x if x > 0.9 * max_hr:
                df.loc[i, "zone"] = 4
            case x if x > 0.82 * max_hr:
                df.loc[i, "zone"] = 3
            case x if x > 0.67 * max_hr:
                df.loc[i, "zone"] = 2

    return df

def get_deltas(df: pd.DataFrame) -> pd.DataFrame:
    # Calculates and appends delta distance and elevation data
    df_length = df.shape[0]
    df["d_distance"] = 0.0
    df["d_elevation"] = 0.0
    df["distance"] = 0.0

    for i in range(1, df_length):
        # Delta distance 
        coord1 = (df["latitude"][i-1], df["longitude"][i-1])
        coord2 = (df["latitude"][i], df["longitude"][i])

        dist = geodesic(coord1, coord2).m
        df.loc[i, "d_distance"] = dist                  # finds distance travelled since last point
        df.loc[i, "distance"] = df["d_distance"].sum()  # finds total travelled distance to this point


        # Delta elevation
        elevation1 = df["elevation"][i-1]
        elevation2 = df["elevation"][i]
        delta_elevation = elevation2 - elevation1
        df.loc[i, "d_elevation"] = delta_elevation

    return df


def get_file_path(path:str):
    file_path = Path(path)
    if not file_path.exists() or file_path.suffix != ".gpx":
        return None
    return file_path

def list_extensions(gpx) -> Counter:
    # Method for Debugging
    # Prints how many total data points are in the file, 
    # and the name and count of each extension in the file
    # Returns Counter of all tags
    tags: Counter = Counter()
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                for ext in point.extensions:
                    for el in ext.iter():
                        tags[el.tag.split("}")[-1]] += 1   # strip "{namespace}" 

    num_points = gpx.get_track_points_no()
    print(f"Total Points: {num_points} points")

    for tag, count in tags.most_common():
        print(f"    {tag} : {count} points")
    return tags

def get_extension_value(point, tag: str):
    # Gets the value of an extension with a specific tag at a point
    # Returns tag as string, and None if value is empty
    for ext in point.extensions:
        for el in ext.iter():
            if el.tag.split("}")[-1] == tag:
                return el.text

    return None