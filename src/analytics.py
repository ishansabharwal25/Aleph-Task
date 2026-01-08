import pandas as pd

def calculate_metrics(model, results_df):
    """
    Computes 4 key metrics from the simulation data.
    
    Args:
        model: The AirportModel instance (to access counters like remote_counter).
        results_df: The DataFrame returned by DataCollector.
        
    Returns:
        dict: A dictionary containing the 4 calculated metrics.
    """
    
    # --- Metric 1: PLB Utilization Rate ---
    # Formula: Average occupied PLB stands / Total PLB capacity * 100
    avg_plb_occupied = results_df["PLB_Occupied"].mean()
    total_plb_capacity = len(model.plb_stands)
    plb_utilization = (avg_plb_occupied / total_plb_capacity) * 100

    # --- Metric 2: Remote Overflow Count ---
    # The total number of flights that were forced to use a Remote stand.
    remote_overflow_count = model.remote_counter

    # --- Metric 3: Service Type Distribution ---
    # Percentage split: What % of flights got PLB vs Remote?
    total_flights = len(model.flight_data)
    
    # Calculate counts
    remote_flights = remote_overflow_count
    plb_flights = total_flights - remote_flights
    
    # Safety check (in case of weird data inputs)
    if plb_flights < 0: plb_flights = 0
    
    service_dist_plb = (plb_flights / total_flights) * 100
    service_dist_remote = (remote_flights / total_flights) * 100

    # --- Metric 4: Penalty Impact (Remote Minutes) ---
    # The sum of all minutes spent by all aircraft in remote stands.
    # This represents the total "cost" of the overflow.
    total_remote_minutes = results_df["Remote_Occupied"].sum()

    return {
        "PLB Utilization (%)": round(plb_utilization, 2),
        "Remote Overflow Count": remote_overflow_count,
        "Service Distribution": f"PLB: {round(service_dist_plb, 1)}% | Remote: {round(service_dist_remote, 1)}%",
        "Penalty Impact (Remote Minutes)": int(total_remote_minutes)
    }