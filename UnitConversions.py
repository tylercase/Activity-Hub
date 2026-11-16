def convert_df(df):
    df["time"] = (df["time"] - df["time"].iloc[0]).dt.total_seconds()
    df["elevation"] *= .280839895
    df["speed"] *= 2.2369362921
    df["d_distance"] *= 0.0006213712
    df["d_elevation"] *= 3.280839895
    df["distance"] *= 0.0006213712
    return df

def s_to_time(time):
    ## Returns time in format "hh:mm:ss" or "mm:ss" if less than 1 hour
    minutes = int(time) // 60
    seconds = int(time) % 60

    if minutes < 60:
        return f"{minutes:02d}:{seconds:02d}"
    
    hours = minutes // 60
    minutes = minutes % 60

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def m_to_miles(meters):
    return meters * 0.0006213712

def m_to_ft(meters):
    return meters * 3.280839895

def mps_to_mph(speed):
    return speed * 2.2369362921
