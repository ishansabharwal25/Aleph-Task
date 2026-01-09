from mesa.visualization.modules import ChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider  
from .model import AirportModel
from .utils import load_flight_data

# --- 1. MINIMAL CSS (The Fix) ---
class SimpleCentering(TextElement):
    def render(self, model):
        return """
        <style>
            canvas {
                display: block !important;
                margin-left: auto !important;
                margin-right: auto !important;
                max-width: 80% !important;
            }
            .metrics-container {
                max-width: 900px;
                margin: 40px auto;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                font-family: sans-serif;
            }
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                margin-top: 20px;
            }
            .metric-card {
                background: white;
                padding: 20px;
                border-radius: 6px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .metric-label {
                font-size: 14px;
                color: #666;
                margin-bottom: 8px;
                font-weight: 500;
            }
            .metric-value {
                font-size: 28px;
                color: #2E86C1;
                font-weight: bold;
            }
            .metric-value.warning {
                color: #E67E22;
            }
            .metric-value.danger {
                color: #C0392B;
            }
        </style>
        """

# --- 2. SIMPLE TEXT HEADERS ---
class Title(TextElement):
    def render(self, model):
        return """
        <h1 style="text-align: center; font-family: sans-serif; color: #333;">
            ✈️ Airport Operations Dashboard
        </h1>
        """

class Description1(TextElement):
    def render(self, model):
        return """
        <div style="text-align: center; margin-bottom: 10px; font-family: sans-serif; color: #666;">
            <b>Operational Load:</b> Blue (Normal) vs Red (Overflow/Bus)
        </div>
        """

class Description2(TextElement):
    def render(self, model):
        return """
        <div style="text-align: center; margin-top: 30px; margin-bottom: 10px; font-family: sans-serif; color: #666;">
            <b>Service Quality:</b> Percentage of flights getting a PLB Stand (Target: 100%)
        </div>
        """

# --- 3. METRICS DISPLAY ---
class MetricsDisplay(TextElement):
    def render(self, model):
        # Calculate metrics
        if not hasattr(model, 'datacollector') or model.datacollector is None:
            return "<div style='text-align: center;'>Running simulation...</div>"
        
        results_df = model.datacollector.get_model_vars_dataframe()
        
        if results_df.empty:
            return "<div style='text-align: center;'>No data collected yet...</div>"
        
        # Calculate the metrics
        avg_plb_occupied = results_df["PLB_Occupied"].mean()
        total_plb_capacity = len(model.plb_stands)
        plb_utilization = (avg_plb_occupied / total_plb_capacity) * 100
        
        remote_overflow_count = model.remote_counter
        
        total_flights = len(model.flight_data)
        remote_flights = remote_overflow_count
        plb_flights = max(0, total_flights - remote_flights)
        service_dist_plb = (plb_flights / total_flights) * 100 if total_flights > 0 else 0
        service_dist_remote = (remote_flights / total_flights) * 100 if total_flights > 0 else 0
        
        total_remote_minutes = int(results_df["Remote_Occupied"].sum())
        
        # Determine color classes based on thresholds
        utilization_class = "danger" if plb_utilization > 90 else ("warning" if plb_utilization > 75 else "")
        overflow_class = "danger" if remote_overflow_count > 50 else ("warning" if remote_overflow_count > 20 else "")
        penalty_class = "danger" if total_remote_minutes > 5000 else ("warning" if total_remote_minutes > 2000 else "")
        
        return f"""
        <div class="metrics-container">
            <h2 style="text-align: center; color: #333; margin-top: 0;">📊 Performance Metrics</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">PLB Utilization Rate</div>
                    <div class="metric-value {utilization_class}">{plb_utilization:.2f}%</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Remote Overflow Count</div>
                    <div class="metric-value {overflow_class}">{remote_overflow_count}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Service Distribution</div>
                    <div class="metric-value" style="font-size: 18px;">
                        PLB: {service_dist_plb:.1f}% | Remote: {service_dist_remote:.1f}%
                    </div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Penalty Impact (Remote Minutes)</div>
                    <div class="metric-value {penalty_class}">{total_remote_minutes:,}</div>
                </div>
            </div>
        </div>
        """

# --- 4. DATA & CHARTS ---
flight_data = load_flight_data("data/flights.csv")

occupancy_chart = ChartModule([
    {"Label": "PLB_Occupied", "Color": "#2E86C1"},
    {"Label": "Remote_Occupied", "Color": "#C0392B"}
], data_collector_name='datacollector')

quality_chart = ChartModule([
    {"Label": "Service_Quality", "Color": "#27AE60"}
], data_collector_name='datacollector')

# --- 5. SERVER CONFIG ---
model_params = {
    "flight_data": flight_data,
    "total_plb_stands": Slider("PLB Stand Capacity", 20, 5, 50, 1)
}

server = ModularServer(
    AirportModel, 
    [
        SimpleCentering(),
        Title(),
        Description1(),
        occupancy_chart,
        Description2(),
        quality_chart,
        MetricsDisplay()  # <--- Metrics displayed at the bottom
    ], 
    "Aleph Tech Dashboard", 
    model_params
)

server.port = 8521