import pandas as pd
import numpy as np
import tkintermapview

def set_route(map_widget:tkintermapview.TkinterMapView, df:pd.DataFrame):
    coords = df[["latitude", "longitude"]].to_numpy().tolist()
    route = [tuple(c) for c in coords]

    if len(route) < 2:
        return

    map_widget.set_path(route, color="red", width=2)
    lats = [p[0] for p in route]
    lons = [p[1] for p in route]
    map_widget.fit_bounding_box((max(lats), min(lons)), (min(lats), max(lons)))