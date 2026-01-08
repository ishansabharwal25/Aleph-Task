import csv
from datetime import datetime

def load_flight_data(filepath):
    """
    Reads CSV and converts HH:MM times to integer minutes from 06:00.
    """
    flights = []
    base_time = datetime.strptime("06:00", "%H:%M")
    
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse times
            arr_dt = datetime.strptime(row['arrival_time'], "%H:%M")
            dep_dt = datetime.strptime(row['departure_time'], "%H:%M")
            
            # Calculate minutes from 06:00 start
            arrival_tick = int((arr_dt - base_time).total_seconds() / 60)
            departure_tick = int((dep_dt - base_time).total_seconds() / 60)
            
            # Only include flights inside the 0-360 window
            if 0 <= arrival_tick <= 360:
                flights.append({
                    'id': row['aircraft_id'],
                    'arrival_tick': arrival_tick,
                    'departure_tick': departure_tick
                })
                
    return flights