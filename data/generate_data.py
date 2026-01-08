import pandas as pd
import random
from datetime import datetime, timedelta

def generate_flight_data(num_flights=150):
    flights = []
    
    # Simulation Start: 06:00
    base_time = datetime.strptime("06:00", "%H:%M")
    
    for i in range(1, num_flights + 1):
        # 1. Generate Arrival Time (Randomly within the 6-hour window)
        # We concentrate more flights in the middle to create a "peak" and force overflow
        minutes_offset = int(random.triangular(0, 360, 180)) 
        arrival_dt = base_time + timedelta(minutes=minutes_offset)
        
        # 2. Generate Ground Time (Randomly between 30 and 90 mins)
        ground_minutes = random.randint(30, 90)
        departure_dt = arrival_dt + timedelta(minutes=ground_minutes)
        
        # 3. Format Strings
        arrival_str = arrival_dt.strftime("%H:%M")
        departure_str = departure_dt.strftime("%H:%M")
        
        # 4. Append to list
        flights.append({
            "aircraft_id": f"A{i}",
            "arrival_time": arrival_str,
            "departure_time": departure_str,
            # We leave stands blank or 'TBD' because your simulation logic decides this
            "arrival_stand": "TBD", 
            "departure_stand": "TBD"
        })
    
    # Sort by arrival time so the simulation processes them in order
    df = pd.DataFrame(flights)
    df = df.sort_values(by="arrival_time")
    
    # Save to CSV
    df.to_csv("data/flights.csv", index=False)
    print(f"Successfully generated data/flights.csv with {num_flights} flights.")
    print(df.head())

if __name__ == "__main__":
    # Ensure the directory exists
    import os
    if not os.path.exists('data'):
        os.makedirs('data')
        
    generate_flight_data(150) # 50 flights ensures competition for the 20 stands