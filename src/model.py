from mesa import Model
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
from .agents import AircraftAgent, StandAgent

class AirportModel(Model):
    """
    Simulates airport stand allocation over a 6-hour window.
    1 Step = 1 Minute.
    """
    def __init__(self, flight_data, total_plb_stands):
        self.schedule = BaseScheduler(self)
        self.running = True
        self.flight_data = flight_data # List of dicts from CSV
        
        # --- Create Stand Agents ---
        self.plb_stands = []
        self.remote_stands = []
        
        # Create fixed PLB stands
        for i in range(total_plb_stands):
            s = StandAgent(f"PLB_{i}", self, "PLB")
            self.plb_stands.append(s)
            self.schedule.add(s)
            
        # Remote stands are created dynamically as needed (Unlimited)
        self.remote_counter = 0

        # --- Data Collection Setup ---
        # self.datacollector = DataCollector(
        #     model_reporters={
        #         "PLB_Occupied": lambda m: sum(1 for s in m.plb_stands if s.occupied_by),
        #         "Remote_Occupied": lambda m: sum(1 for s in m.remote_stands if s.occupied_by),
        #         "Total_Parked": lambda m: sum(1 for s in m.plb_stands + m.remote_stands if s.occupied_by)
        #     }
        # )
        self.datacollector = DataCollector(
            model_reporters={
                "PLB_Occupied": lambda m: sum(1 for s in m.plb_stands if s.occupied_by),
                "Remote_Occupied": lambda m: sum(1 for s in m.remote_stands if s.occupied_by),
                
                # NEW METRIC: Service Quality Index (%)
                # Formula: (PLB_Planes / Total_Planes) * 100
                # We use "or 1" to prevent crashing if Total_Planes is 0.
                "Service_Quality": lambda m: (
                    sum(1 for s in m.plb_stands if s.occupied_by) / 
                    (sum(1 for s in m.plb_stands + m.remote_stands if s.occupied_by) or 1)
                ) * 100
            }
        )


    def step(self):
        current_time = self.schedule.steps
        
        # 1. Spawn Aircraft (Arrival Logic)
        # Find all flights arriving at this specific minute
        arriving_flights = [f for f in self.flight_data if f['arrival_tick'] == current_time]
        
        for flight in arriving_flights:
            plane = AircraftAgent(flight['id'], self, flight['arrival_tick'], flight['departure_tick'])
            self.schedule.add(plane)
            self.allocate_stand(plane)

        # 2. Advance all agents (handles Departures)
        self.schedule.step()
        
        # 3. Collect Data
        self.datacollector.collect(self)
        
        # 4. Stop condition (after 6 hours / 360 mins)
        if current_time >= 360:
            self.running = False

    def allocate_stand(self, aircraft):
        """
        FCFS Logic:
        1. Try to find an empty PLB stand.
        2. If all PLBs full, create/assign a Remote stand.
        """
        # Try PLB First
        for stand in self.plb_stands:
            if stand.occupied_by is None:
                stand.occupied_by = aircraft
                aircraft.assigned_stand = stand
                aircraft.state = "Parked"
                return

        # Fallback to Remote (Unlimited)
        self.remote_counter += 1
        remote_stand = StandAgent(f"Remote_{self.remote_counter}", self, "Remote")
        remote_stand.occupied_by = aircraft
        
        # We track remote stands to calculate metrics later
        self.remote_stands.append(remote_stand) 
        self.schedule.add(remote_stand)
        
        aircraft.assigned_stand = remote_stand
        aircraft.state = "Parked"