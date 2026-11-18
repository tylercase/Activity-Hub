import pandas as pd
import numpy as np
from UnitConversions import *

class GradeCalculator():
    ## Takes in df of gpx track. returns a df where each row is a section of the trail. 
    ## Columns include: (section_number, start_distance, end_distance, start_elevation, end_elevation, avg_grade)
    def __init__(self, df:pd.DataFrame, miles_per_section=0.1):
        self.M_PER_MILE = 1609.344
        self.split_length = miles_per_section

        split_df = self.split_df(df)
        self.grade_df = self.create_grade_df(split_df)

    def get_grade_df(self):
        return self.grade_df

    def split_df(self, df:pd.DataFrame) -> list[pd.DataFrame]:
        df["split"] = (df["distance"] // self.split_length).astype(int)

        splits = [group for _, group in df.groupby("split")]
        return splits

    def create_grade_df(self, df:pd.DataFrame):
        cols = (
            "section_nr",
            "start_time",
            "end_time",
            "start_distance",
            "end_distance",
            "start_elevation",
            "end_elevation",
            "avg_grade"
        )

        splits_lst = []
        for i in range(len(df)):
            section_number = i
            start_time = int(df[i]["time"].iloc[0])
            end_time = int(df[i]["time"].iloc[-1])
            start_distance = float(df[i]["distance"].iloc[0])
            end_distance = float(df[i]["distance"].iloc[-1])
            start_elevation = float(df[i]["elevation"].iloc[0])
            end_elevation = float(df[i]["elevation"].iloc[-1])

            d_elevation = end_elevation - start_elevation
            d_distance = end_distance - start_distance
            avg_grade = ft_to_miles(d_elevation) / d_distance * 100

            new_row = [
                section_number,
                start_time,
                end_time,
                start_distance,
                end_distance,
                start_elevation,
                end_elevation,
                avg_grade
            ]
            splits_lst.append(new_row)

        df = pd.DataFrame(splits_lst, columns=cols)

        return df





        