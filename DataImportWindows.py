import customtkinter
import tkinter as tk
import tkintermapview
from tkinter import ttk, filedialog
from ZeppImporter import import_workout
from config import *
from typing import Callable
import pandas as pd
import numpy as np
from SetRoute import set_route

class ImportZeppWindow(customtkinter.CTkToplevel):
    ## Window that lets user pick the type of workout that they want to import, 
    ## Which then opens a filedialog window to select the file they want to import.
    def __init__(self, *args, on_save: Callable[[], None] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_save = on_save
        self.export_window: customtkinter.CTkToplevel = None

        # First asks what type of workout was done
        label = customtkinter.CTkLabel(self, 
                                       text="What type of workout are you importing?",
                                       font=("Helvetica", 20))
        label.pack(pady=20, padx=20, side="top")

        self.workout_select_frm = customtkinter.CTkFrame(self)
        self.workout_select_frm.pack(pady=10, padx=10)

        self.hike_btn = customtkinter.CTkButton(self.workout_select_frm,
                                                text="Hike",
                                                font=("Helvetica", 16, "bold"),
                                                text_color="black",
                                                fg_color="darkgreen",
                                                height=30,
                                                width=90,
                                                corner_radius=10,
                                                command=lambda input = "hike": self.select_workout(input))
        self.run_btn = customtkinter.CTkButton(self.workout_select_frm,
                                                text="Run",
                                                font=("Helvetica", 16, "bold"),
                                                text_color="black",
                                                fg_color="darkblue",
                                                height=30,
                                                width=90,
                                                corner_radius=10,
                                                command=lambda input = "run": self.select_workout(input))
        self.walk_btn = customtkinter.CTkButton(self.workout_select_frm,
                                                text="Walk",
                                                font=("Helvetica", 16, "bold"),
                                                text_color="black",
                                                fg_color="grey",
                                                height=30,
                                                width=90,
                                                corner_radius=10,
                                                command=lambda input = "walk": self.select_workout(input))
        self.hike_btn.pack(side="left", padx=10, pady=10)
        self.run_btn.pack(side="left", padx=10, pady=10)
        self.walk_btn.pack(side="left", padx=10, pady=10)

        self.selected_worukout_label = customtkinter.CTkLabel(self,
                                                              text="No file selected")
        self.selected_worukout_label.pack(padx=20, pady=8)

        button = customtkinter.CTkButton(self.workout_select_frm, text="self destruct", command=self.self_destruct)
        button.pack(pady=10)

    def select_workout(self, workout_type: str):
        ## Method to select a workout, and reads the data from the gpx file via ZeppImporter.import_workout()
        ## Once workout is selected, it opens a new window where user can edit any data from the summary page.
        workout_type = workout_type.strip().lower()
        path = filedialog.askopenfilename(
            title=f"Select a {workout_type} activity",
            filetypes=[("GPX Files", "*.gpx"), ("All Files", "*.*")]
        )

        if not path:    # when clicking cancel returns an empty string.
            self.selected_worukout_label.configure(text="No file selected")
            return

        self.file_path = path
        self.selected_worukout_label.configure(text=path)

        match workout_type:
            case "hike":
                self.workout_data = import_workout(path, "hike")
            case "run":
                self.workout_data = import_workout(path, "run")
            case "walk":
                self.workout_data = import_workout(path, "walk")

        self.open_export_window()
        self.destroy()

    def open_export_window(self):
        if self.export_window is None or not self.export_window.winfo_exists():
            self.export_window = WorkoutExportWindow(self.master, self.workout_data, on_save=self.on_save)
            self.export_window.after(10, self.export_window.lift)
        else:
            self.export_window.focus()
            self.export_window.after(10, self.export_window.lift)

    def self_destruct(self):
        self.destroy()

class WorkoutExportWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, data:tuple, *args, on_save: Callable[[], None] | None = None, fg_color = None, **kwargs):
        super().__init__(parent, *args, fg_color=fg_color, **kwargs)
        self.on_save = on_save
        self.df = data[0]
        self.workout_dict:dict = data[1]
        # print(self.workout_dict)
        self.workout_type = data[2]

        self.title("Data Export Window")
        self.label = customtkinter.CTkLabel(self,
                                            text="Check that data seems correct.",
                                            font=("Helvetica", 20, "bold"))
        self.label.pack(pady=20)

        self.mapview = tkintermapview.TkinterMapView(self)
        self.mapview.pack(fill="both", expand=True, padx=20, pady=20)
        set_route(self.mapview, self.df)

        self.entry_boxes:list[customtkinter.CTkEntry] = []

        for key, value in self.workout_dict.items():
            frame = customtkinter.CTkFrame(self)
            frame.pack(pady=5)

            label = customtkinter.CTkLabel(frame, text=f"{key}")
            label.pack(padx=30, side="left")

            entry = customtkinter.CTkEntry(frame)
            entry.insert(0, value)
            entry.pack(padx=30, side="left")
            self.entry_boxes.append(entry)

        keys = list(self.workout_dict.keys())
        for i in range(len(keys)):
            self.workout_dict[keys[i]] = self.entry_boxes[i].get()

        btn_frame = customtkinter.CTkFrame(self)
        btn_frame.pack(pady=10)

        ok_button = customtkinter.CTkButton(btn_frame,
                                            text="Confirm",
                                            command=lambda wo_type = self.workout_type: self.save_data(wo_type))
        ok_button.pack(padx=5, side="left")

        cancel_button = customtkinter.CTkButton(btn_frame,
                                                text="Cancel",
                                                command=self.cancel_save)
        cancel_button.pack(padx=5, side="left")

    # def set_route(self, map_widget:tkintermapview.TkinterMapView, df:pd.DataFrame):
    #     coords = df[["latitude", "longitude"]].to_numpy().tolist()
    #     route = [tuple(c) for c in coords]

    #     if len(route) < 2:
    #         return

    #     map_widget.set_path(route, color="red", width=2)
    #     lats = [p[0] for p in route]
    #     lons = [p[1] for p in route]
    #     map_widget.fit_bounding_box((max(lats), min(lons)), (min(lats), max(lons)))

    def save_data(self, workout_type:str):
        match workout_type:
            case "hike":
                folder_dir = HIKE_DIR
            case "run":
                folder_dir = RUN_DIR
            case "walk":
                folder_dir = WALK_DIR

        # summary = pd.read_csv(folder_dir / "summary.csv")
        new_row_summary = pd.DataFrame([self.workout_dict])
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

        self.self_destroy()

    def cancel_save(self):
        print("No data was saved.")
        self.self_destroy()

    def self_destroy(self):
        self.destroy()