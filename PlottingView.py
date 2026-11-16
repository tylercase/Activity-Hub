import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from config import PLOTTING_COLOR_DICT
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NewGraph(customtkinter.CTkFrame):
    def __init__(self, parent, data:pd.DataFrame, x_column="time", y_column="elevation", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        data = data.fillna(0)   # set all NaN values to 0 for plotting reasons

        fig = Figure((8, 5), 100)
        ax = fig.add_subplot(111)

        ax.plot(data[x_column], data[y_column], color=PLOTTING_COLOR_DICT[y_column])
        ax.set_title(f"{y_column} vs. {x_column}")
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_ylim(0, max(data[y_column]))
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(side="top",
                                    padx=10,
                                    pady=10,
                                    fill="both",
                                    expand=True)
        canvas.draw()
