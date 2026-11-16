import customtkinter
import tkinter as tk
import tkintermapview
from tkinter import ttk, filedialog
from ZeppImporter import import_workout
from DataImportWindows import *
from config import *
from GetData import *
from CTkListbox import CTkListbox
from CreateSummaryCSV import create_summaries
from ViewWorkout import ViewWorkout
import pandas as pd
import numpy as np



#########################################################################################################
################################    Main Methods    #####################################################
#########################################################################################################

def main():
    create_summaries()
    app = App()
    app.mainloop()

class App(customtkinter.CTk):
    ## Default app, has all the methods for opening new windows and pages
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Activity Hub v1.0")
        self.configure(
            fg_color="black"
        )

        self.button_frame = customtkinter.CTkFrame(self, bg_color="black", fg_color="black")
        self.button_frame.pack(pady=20, padx=20, side="right")
        
        # Button to import new workout
        self.import_window = None
        self.import_zepp_data_btn = customtkinter.CTkButton(self.button_frame, 
                                                            text="Import Zepp Workout", 
                                                            command=self.open_import_window,
                                                            width=120,
                                                            height=40,
                                                            corner_radius=20,
                                                            bg_color="black",
                                                            fg_color="darkgrey",
                                                            font=("Helvetica", 14, "bold"),
                                                            text_color="black",
                                                            hover_color="grey")

        self.import_zepp_data_btn.pack(side="top", pady=20, padx=10)


        self.view_workout_window = None
        self.view_workout_btn = customtkinter.CTkButton(self.button_frame,
                                                        text="View Workout",
                                                        command=self.view_workout,
                                                        width=120,
                                                        height=40,
                                                        corner_radius=20,
                                                        bg_color="black",
                                                        fg_color="darkgrey",
                                                        font=("Helvetica", 14, "bold"),
                                                        text_color="black",
                                                        hover_color="grey")
        self.view_workout_btn.pack(side="top", pady=20, padx=10)


        self.recent_workouts_view = WorkoutViewFrame(self)
        self.recent_workouts_view.pack(pady=10, padx=20, side="left")

    def view_workout(self):
        workout_to_view = self.recent_workouts_view.get_selection()
        print(workout_to_view)
        data = get_workout_data_package(workout_to_view[0], workout_to_view[1])
        if self.view_workout_window is None or not self.view_workout_window.winfo_exists():
            self.view_workout_window = ViewWorkout(self, workout_to_view, data)
            self.view_workout_window.after(10, self.view_workout_window.lift)
        else:
            self.view_workout_window.destroy()
            self.view_workout_window = ViewWorkout(self, workout_to_view)
            self.view_workout_window.after(10, self.view_workout_window.lift)
        return

    def open_import_window(self):
        if self.import_window is None or not self.import_window.winfo_exists():
            self.import_window = ImportZeppWindow(self, on_save=self.recent_workouts_view.update_listboxes)
            self.import_window.after(10, self.import_window.lift)
        else:
            self.import_window.focus()
            self.import_window.after(10, self.import_window.lift)


class WorkoutViewFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(
            corner_radius=20,
            bg_color="black",
            fg_color="darkgrey"
        )
        self.listbox_selection = None

        self.workout_frames = []
        self.listboxes = []
        for i in range(3):
            frame = customtkinter.CTkFrame(self)
            frame.pack(side="left", padx=5, pady=5)
            frame.configure(
                corner_radius=18,
                bg_color="darkgrey",
                fg_color="grey",
                width=100
            )

            match i:
                case i if i == 0:
                    # Hike frame
                    title = customtkinter.CTkLabel(
                        frame, 
                        text="Recent Hikes",
                        font=("Helvetica", 14, "bold"),
                        text_color="darkgreen"
                    )
                    listbox = CTkListbox(frame,
                                        command=lambda _value: self.selected_option("hike"))
                case i if i == 1:
                    # Run frame
                    title = customtkinter.CTkLabel(
                        frame, 
                        text="Recent Runs",
                        font=("Helvetica", 14, "bold"),
                        text_color="darkblue"
                    )
                    listbox = CTkListbox(frame,
                                        command=lambda _value: self.selected_option("run"))
                case i if i == 2:
                    # Walk frame
                    title = customtkinter.CTkLabel(
                        frame, 
                        text="Recent Walks",
                        font=("Helvetica", 14, "bold"),
                        text_color="black"
                    )
                    listbox = CTkListbox(frame,
                                        command=lambda _value: self.selected_option("walk"))

            title.pack(side="top", pady=5)
            listbox.pack(side="top", pady=5, padx=5)
            
            self.listboxes.append(listbox)
            self.workout_frames.append(frame)

        self.update_listboxes()

    def selected_option(self, workout_type:str):
        print(f"workout type {workout_type} selected")
        skip_idx = None
        if workout_type == "hike":
            skip_idx = 0
        elif workout_type == "run":
            skip_idx = 1
        elif workout_type == "walk":
            skip_idx = 2

        # Deselect all other options
        for i in range(len(self.listboxes)):
            if i == skip_idx:
                continue

            for j in range(self.listboxes[i].size()):
                self.listboxes[i].deactivate(j)
        
        self.listbox_selection = (workout_type, self.listboxes[skip_idx].get())

    def get_selection(self):
        return self.listbox_selection


    def update_listboxes(self):
        idx = 0
        for i in self.listboxes:
            if idx == 0:
                self.fill_listbox(i, get_ids("hike"))
            elif idx == 1:
                self.fill_listbox(i, get_ids("run"))
            elif idx == 2:
                self.fill_listbox(i, get_ids("walk"))
            
            idx += 1
            
    
    def fill_listbox(self, listbox:CTkListbox, data:list[str]):
        listbox.delete("all")
        for i in data:
            listbox.insert("END", i)


        
main()

