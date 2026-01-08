from mesa import Agent

class StandAgent(Agent):
    """
    Represents a parking spot for an aircraft.
    Attributes:
        stand_type (str): "PLB" or "Remote"
        occupied_by (AircraftAgent): The aircraft currently parked here (or None)
    """
    def __init__(self, unique_id, model, stand_type):
        super().__init__(unique_id, model)
        self.stand_type = stand_type
        self.occupied_by = None  # Initially empty

    def step(self):
        # Stands are passive; they don't 'do' anything every step
        pass


class AircraftAgent(Agent):
    """
    Represents an Aircraft.
    Attributes:
        arrival_time (int): Minute of arrival (0-360)
        departure_time (int): Minute of departure
        state (str): "In_Air", "Parked", "Completed"
        assigned_stand (StandAgent): The stand assigned to this aircraft
    """
    def __init__(self, unique_id, model, arrival_time, departure_time):
        super().__init__(unique_id, model)
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.state = "In_Air"
        self.assigned_stand = None

    def step(self):
        # 1. Arrival Logic is handled by the Model to ensure correct ordering
        # 2. Departure Logic
        if self.state == "Parked" and self.model.schedule.steps >= self.departure_time:
            self.state = "Completed"
            # Free the stand
            if self.assigned_stand:
                self.assigned_stand.occupied_by = None
                self.assigned_stand = None
                # Remove from scheduler so we stop processing this agent
                self.model.schedule.remove(self)