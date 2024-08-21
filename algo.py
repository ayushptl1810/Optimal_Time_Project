
import pandas as pd

def create_and_sort_timetable(db):
    # Remove rows with non-numeric time entries
    db = db[~db['TIME'].apply(lambda x: x.isalpha() or x == '.')]
    
    # Create a DataFrame for the timetable
    tt = pd.DataFrame({
        "MON": db["MON"],
        "TUE": db["TUE"],
        "WED": db["WED"],
        "THU": db["THU"],
        "FRI": db["FRI"],
        "SAT": db["SAT"],
    })
    
    # Define time intervals
    time_intervals = ["8:00-8:30", "8:30-9:00", "9:00-9:30", "9:30-10:00", "10:00-10:30", 
                      "10:30-11:00", "11:00-11:30", "11:30-12:00", "12:00-12:30", "12:30-1:00", 
                      "1:00-1:30", "1:30-2:00", "2:00-2:30", "2:30-3:00", "3:00-3:30",
                      "3:30-4:00", "4:00-4:30", "4:30-5:00", "5:00-5:30"]

    # Assign time intervals as the index
    if len(tt) <= len(time_intervals):
        tt.index = time_intervals[:len(tt)]
    else:
        print("Error: The number of rows exceeds the number of time intervals.")
        return None

    return tt

def find_best_time_from_csv(*file_paths):
    # Load the CSV files and create timetables
    timetables = [create_and_sort_timetable(pd.read_csv(file)) for file in file_paths]

    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
    favourable_timings = {day: [] for day in days}  # Initialize dictionary with empty lists for each day

    for day in days:
        # Skip the day if "IPD" is present in any timetable
        if any("IPD" in timetable[day].values for timetable in timetables):
            continue

        # Loop over the time intervals
        for i in range(len(timetables[0][day])):
            # Check if all values at the current time interval are either NaN or single letters
            all_free = all(
                (pd.isna(timetable[day][i]) or  # Check for NaN values
                (isinstance(timetable[day][i], str) and
                 len(timetable[day][i]) == 1 and
                 timetable[day][i].isalpha()))
                for timetable in timetables
            )

            if all_free:
                # Append the time interval
                time_interval = timetables[0].index[i]
                favourable_timings[day].append(time_interval)

    return favourable_timings
