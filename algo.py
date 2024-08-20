import pandas as pd

def createTimetable(db):
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
    
    # Clean up the timetable
    return sortTimetable(tt)

def sortTimetable(timetable):
    # Check the number of rows
    num_rows = len(timetable)
    print(f"Number of rows: {num_rows}")

    # Define time intervals
    time_intervals = ["8:00-8:30", "8:30-9:00", "9:00-9:30", "9:30-10:00", "10:00-10:30", 
                      "10:30-11:00", "11:00-11:30", "11:30-12:00", "12:00-12:30", "12:30-1:00", 
                      "1:00-1:30", "1:30-2:00", "2:00-2:30", "2:30-3:00", "3:00-3:30",
                      "3:30-4:00", "4:00-4:30", "4:30-5:00", "5:00-5:30"]

    # Assign time intervals as the index
    if num_rows <= len(time_intervals):
        timetable.index = time_intervals[:num_rows]
    else:
        print("Error: The number of rows exceeds the number of time intervals.")

    return timetable

# Load the CSV file
db1 = pd.read_csv("first.csv")
db2 = pd.read_csv("second.csv")

# Create and sort the timetable
timetable1 = createTimetable(db1)
timetable2 = createTimetable(db2)

def findBestTime(timetable1, timetable2):
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
    favourable_timings = {
    "MON": [],
    "TUE": [],
    "WED": [],
    "THU": [],
    "FRI": [],
    "SAT": []
    }  

    for day in days:
        for i in range(len(timetable1[day])):  # Loop over the indices of the day
            val1 = timetable1[day][i]
            val2 = timetable2[day][i]

            # Check if both values are "NaN" or a single letter
            if (val1 == val2 == "NaN") or (
                isinstance(val1, str) and isinstance(val2, str) and
                len(val1) == 1 and len(val2) == 1 and
                val1.isalpha() and val2.isalpha()
            ):
                # Append the time interval instead of the index
                time_interval = timetable1.index[i]
                favourable_timings[day].append(time_interval)

    return favourable_timings

favourable_timings = findBestTime(timetable1, timetable2)
print("Favourable Timings:")
print(favourable_timings)