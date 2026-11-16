import customtkinter
import pandas as pd
import numpy as np
import tkintermapview
import tkinter as tk
from config import *
from GetData import *
from PlottingView import NewGraph
from UnitConversions import *
from SetRoute import set_route

class ViewWorkout(customtkinter.CTkToplevel):
    def __init__(self, parent, workout:tuple, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("View Workout")
        workout_type, self.run_id = workout

        self.data = get_workout_data_package(workout_type, self.run_id)     # (df, summary)
        print(self.data[0])
        print(self.data[1])

        info_panel = BasicWorkoutInfoPanel(self, self.data, workout)
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
    def __init__(self, parent, data:tuple, workout_info:tuple, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.df, self.summary = data
        self.workout_type, self.run_id = workout_info
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
        set_route(mapview, self.df)

        ## Summary View
        summary_frame = customtkinter.CTkFrame(self)
        summary_frame.pack(pady=10,
                           padx=10,
                           side="left",
                           anchor="nw")

        summary_values = self.summary.iloc[0].tolist()
        summary_values[1] = s_to_time(summary_values[1])
        summary_values[2] = round(m_to_miles(summary_values[2]), 2)
        summary_values[5] = int(m_to_ft(summary_values[5]))
        summary_values[6] = int(m_to_ft(summary_values[6]))
        summary_values[7] = round(mps_to_mph(summary_values[7]), 2)


        value_boxes = []
        for i in range(1, len(summary_values)):     # skip first item because it is only "run_id"
            value_frame = customtkinter.CTkFrame(summary_frame)
            value_frame.pack(pady=5,
                             padx=5)

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

        ## Graph Tap View
        tabview = customtkinter.CTkTabview(self)
        tabview.pack(side="left",
                     anchor="nw",
                     padx=20,
                     pady=10)

        tabview.add("hr")
        hr_plot = NewGraph(tabview.tab("hr"), self.df, y_column="hr")
        hr_plot.pack(padx=10, pady=10)

        tabview.add("speed")
        speed_plot = NewGraph(tabview.tab("speed"), self.df, y_column="speed")
        speed_plot.pack(padx=10, pady=10)

        tabview.add("elevation")
        elevation_plot = NewGraph(tabview.tab("elevation"), self.df, y_column="elevation")
        elevation_plot.pack(padx=10, pady=10)

        tabview.add("cadence")
        cadence_plot = NewGraph(tabview.tab("cadence"), self.df, y_column="cadence")
        cadence_plot.pack(padx=10, pady=10)

        tabview.add("zone")
        zone_plot = NewGraph(tabview.tab("zone"), self.df, y_column="zone")
        zone_plot.pack(padx=10, pady=10)
        
        


        
        
        
