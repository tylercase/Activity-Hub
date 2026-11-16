import customtkinter
import pandas as pd
import numpy as np
import tkintermapview
import tkinter as tk
from typing import Callable
from api import *
from config import *
from GetData import *
from PlottingView import NewGraph
from UnitConversions import *
from SetRoute import set_route

class ViewWorkout(customtkinter.CTkToplevel):
    def __init__(self, parent, workout:tuple, data:tuple, import_window=False, *args, on_save: Callable[[], None] | None = None, **kwargs):
        super().__init__(parent, *args, **kwargs)
        workout_type, self.run_id = workout
        self.title(f"Import new {workout_type}") if import_window else self.title("View Workout")

        self.data = data     # (df, summary)
        print(self.data[0])
        print(self.data[1])

        info_panel = BasicWorkoutInfoPanel(self, self.data, workout, import_window, on_save=on_save)
        info_panel.pack(padx=10,
                        pady=10)
        

        match workout_type:
            case "hike":
                self.hike_view()
            case "run":
                self.run_view()
            case "walk":
                self.walk_view()
                



    def hike_view(self):
        return

    def run_view(self):
        return

    def walk_view(self):
        return


class BasicWorkoutInfoPanel(customtkinter.CTkFrame):
    def __init__(self, parent, data:tuple, workout_info:tuple, import_window=False, *args, on_save: Callable[[], None] | None = None, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.df, self.summary = data
        self.on_save = on_save
        self.workout_type, self.run_id = workout_info
        if import_window:
            self.df = convert_df(self.df)

        label = customtkinter.CTkLabel(self,
                                text=f"{self.workout_type} workout\nid = {self.run_id}",
                                font=("Helvetica", 14, "bold"))
        label.pack(side="top",
                   pady=10)

        ## Map View
        mapview = tkintermapview.TkinterMapView(self,
                                                width=600,
                                                height=300)
        mapview.pack(side="top",
                     padx=20,
                     pady=10,
                     fill="both",
                     expand=True)
        mapview.set_tile_server(f"https://api.maptiler.com/maps/outdoor-v4/256/{{z}}/{{x}}/{{y}}.png?key={MAP_API}")
        set_route(mapview, self.df)

        ## Summary View
        summary_frame = customtkinter.CTkFrame(self)
        summary_frame.pack(pady=10,
                           padx=10,
                           side="left",
                           anchor="nw",
                           fill="y")
        summary_value_frame = customtkinter.CTkFrame(summary_frame)
        summary_value_frame.pack(pady=10,
                                 padx=10,
                                 side="top",
                                 fill="y")

        summary_values = self.summary.iloc[0].tolist()
        summary_values[1] = s_to_time(summary_values[1])
        summary_values[2] = round(m_to_miles(summary_values[2]), 2)
        summary_values[5] = int(m_to_ft(summary_values[5]))
        summary_values[6] = int(m_to_ft(summary_values[6]))
        summary_values[7] = round(mps_to_mph(summary_values[7]), 2)


        value_boxes = []
        for i in range(1, len(summary_values)):     # skip first item because it is only "run_id"
            value_frame = customtkinter.CTkFrame(summary_value_frame)
            value_frame.pack(pady=5,
                             padx=5,
                             expand=True,
                             fill="y")

            key_label = customtkinter.CTkLabel(value_frame, 
                                               text=f"{SUMMARY_COLS[i]}",
                                               width=100)
            key_label.pack(side="left",
                           padx=5,
                           pady=5)

            value_box = customtkinter.CTkEntry(value_frame)
            value_box.insert(0, f"{summary_values[i]} {SUMMARY_UNITS[i]}")
            value_box.configure(state="disabled")
            value_box.pack(side="right",
                           padx=5,
                           pady=5)
            value_boxes.append(value_box)

        ## If this is an import window, add buttons.
        if import_window:
            btn_frame = customtkinter.CTkFrame(summary_frame)
            btn_frame.pack(pady=10)

            ok_button = customtkinter.CTkButton(btn_frame,
                                                text="Import",
                                                command=lambda wo_type = self.workout_type: self.save_data(wo_type))
            ok_button.pack(padx=5, side="left")

            cancel_button = customtkinter.CTkButton(btn_frame,
                                                    text="Cancel",
                                                    command=self.cancel_save)
            cancel_button.pack(padx=5, side="left")

        ## Graph Tap View
        tabview = customtkinter.CTkTabview(self)
        tabview.pack(side="left",
                     anchor="nw",
                     padx=20,
                     pady=0)

        tabview.add("hr")
        hr_plot = NewGraph(tabview.tab("hr"), self.df, y_column="hr", avg=True)
        hr_plot.pack(padx=10, pady=10)

        tabview.add("speed")
        speed_plot = NewGraph(tabview.tab("speed"), self.df, y_column="speed", avg=True)
        speed_plot.pack(padx=10, pady=10)

        tabview.add("elevation")
        elevation_plot = NewGraph(tabview.tab("elevation"), self.df, y_column="elevation")
        elevation_plot.pack(padx=10, pady=10)

        tabview.add("cadence")
        cadence_plot = NewGraph(tabview.tab("cadence"), self.df, y_column="cadence", scatter=True, avg=True)
        cadence_plot.pack(padx=10, pady=10)

        tabview.add("zone")
        zone_plot = NewGraph(tabview.tab("zone"), self.df, y_column="zone")
        zone_plot.pack(padx=10, pady=10)

    def save_data(self, workout_type:str):
        match workout_type:
            case "hike":
                folder_dir = HIKE_DIR
            case "run":
                folder_dir = RUN_DIR
            case "walk":
                folder_dir = WALK_DIR

        # summary = pd.read_csv(folder_dir / "summary.csv")
        new_row_summary = self.summary
        run_id = new_row_summary["run_id"].iloc[0]

        # If summary file does not exist, then the new row is the summary, skip read and concat
        if not Path(folder_dir / "summary.csv").exists():
            summary_df = new_row_summary
        else:
            old_df = pd.read_csv(folder_dir / "summary.csv")
            summary_df = pd.concat([old_df, new_row_summary], ignore_index=True).drop_duplicates("run_id", keep="last")

        summary_df = summary_df.sort_values(by="run_id", ascending=False)
        summary_df.to_csv(folder_dir / "summary.csv", index=False)

        df:pd.DataFrame = self.df
        df.to_parquet(folder_dir / f"{run_id}.parquet")
        print(f"New {workout_type} workout imported.")
        if self.on_save() is not None:
            self.on_save()

        self.master.destroy()

    def cancel_save(self):
        print("No data was saved.")
        self.master.destroy()
        
        


        
        
        
