from src.utils import load_flight_data
from src.model import AirportModel
from src.analytics import calculate_metrics
import pandas as pd

# --- COST CONSTANTS ---
COST_PER_PLB_STAND = 100    # Daily cost to maintain/staff a PLB stand
COST_PER_OVERFLOW = 500     # Operational cost (bussing/delays) per remote event

def run_scenario(flight_data, plb_count):
    model = AirportModel(flight_data, total_plb_stands=plb_count)
    while model.running:
        model.step()
    return calculate_metrics(model, model.datacollector.get_model_vars_dataframe())

def main():
    print("Loading Flight Data...")
    flight_data = load_flight_data("data/flights.csv")
    
    # --- CHANGE: Test range from 5 to 50 ---
    # range(5, 51) creates numbers: 5, 6, 7 ... up to 50
    scenarios = range(5, 51)
    
    print(f"\nRunning Cost Minimization Analysis (5-50 Stands)...")
    print(f"Weights: Stand Cost=${COST_PER_PLB_STAND} | Overflow Penalty=${COST_PER_OVERFLOW}")
    print("-" * 75)
    print(f"{'Stands':<10} | {'Overflows':<10} | {'Stand Cost':<12} | {'Penalty Cost':<15} | {'TOTAL COST':<12}")
    print("-" * 75)

    best_scenario = None
    min_total_cost = float('inf')

    for plb_count in scenarios:
        metrics = run_scenario(flight_data, plb_count)
        
        overflows = metrics["Remote Overflow Count"]
        
        # Cost Function
        stand_cost = plb_count * COST_PER_PLB_STAND
        penalty_cost = overflows * COST_PER_OVERFLOW
        total_cost = stand_cost + penalty_cost
        
        # Print row
        print(f"{plb_count:<10} | {overflows:<10} | ${stand_cost:<11} | ${penalty_cost:<14} | ${total_cost:<11}")
        
        # Check for new minimum
        if total_cost < min_total_cost:
            min_total_cost = total_cost
            best_scenario = {
                "Stands": plb_count,
                "Overflows": overflows,
                "Total Cost": total_cost,
                "Penalty Cost": penalty_cost,
                "Stand Cost": stand_cost
            }

    print("-" * 75)
    print("\n" + "="*40)
    print("OPTIMIZATION RESULT")
    print("="*40)
    
    if best_scenario:
        print(f"RECOMMENDED CONFIGURATION: {best_scenario['Stands']} PLB Stands")
        print(f"Lowest Possible Cost:      ${best_scenario['Total Cost']}")
        print(f"Breakdown:                 ${best_scenario['Stand Cost']} (Infrastructure) + ${best_scenario['Penalty Cost']} (Penalties)")
        print(f"Operational Result:        {best_scenario['Overflows']} remote overflows")

if __name__ == "__main__":
    main()