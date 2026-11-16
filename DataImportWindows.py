import customtkinter
import tkinter as tk
import tkintermapview
from tkinter import ttk, filedialog
from ZeppImporter import import_workout, get_info
from config import *
from typing import Callable
from ViewWorkout import *
import pandas as pd
import numpy as np
from SetRoute import set_route

class ImportZeppWindow(customtkinter.CTkToplevel):
    ## Window that lets user pick the type of workout that they want to import, 
    ## Which then opens a filedialog window to select the file they want to import.
    def __init__(self, *args, on_save: Callable[[], None] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_save = on_save
        self.import_window: customtkinter.CTkToplevel = None

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

        self.workout_data = import_workout(path, workout_type)
        self.workout_info = get_info(workout_type, self.workout_data)

        self.open_import_window(self.workout_info, self.workout_data)
        self.destroy()

    def open_import_window(self, info, data):
        if self.import_window is None or not self.import_window.winfo_exists():
            self.import_window = ViewWorkout(self.master, info, data, import_window=True, on_save=self.on_save)
            self.import_window.after(10, self.import_window.lift)
        else:
            self.import_window.focus()
            self.import_window.after(10, self.import_window.lift)

    def self_destruct(self):
        self.destroy()