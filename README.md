# Airport Stand Allocation Simulation

A simplified agent-based simulation that models aircraft-to-stand allocation at an airport over a fixed operational period, considering limited preferred stands and fallback remote stands.

---

## 📌 What Was Built

This project implements a **simplified airport stand allocation simulation** that models how arriving aircraft are assigned to available stands over time during a **6-hour operational window**.

Aircraft arrive based on input schedules and require a stand for the duration of their ground time. The allocation logic is **First Come First Serve** which prioritizes **PLB stands (limited, preferred)** and falls back to **remote stands (unlimited)** when PLB capacity is exhausted.

In addition to the core simulation, the project includes a **sensitivity analysis module** built in `main.py` that evaluates system performance across varying PLB capacities ranging from **5 to 50 stands**. For each PLB capacity, the simulation computes cost and performance metrics to assess trade-offs between infrastructure availability and operational efficiency.

### Key Features
- **Agent-based simulation** of aircraft-to-stand allocation
- **Sensitivity analysis** across multiple PLB capacity scenarios (5–50)
- **Cost and performance evaluation** using multiple metrics
- **Interactive visualization dashboard** with charts and sliders to explore results dynamically

### Metrics Tracked
- **PLB Utilization (%)**: Percentage of time PLB stands are occupied
- **Remote Overflow Count**: Number of aircraft assigned to remote stands
- **Service Distribution**: Proportion of aircraft served by PLB vs remote stands
- **Penalty Impact (Remote Minutes)**: Total penalty incurred due to remote stand usage

### Key Components

- **agents.py**  
  Defines the aircraft agents and stand entities, including their state, and release logic during the simulation.

- **model.py**  
  Implements the core airport simulation model, initializes stands and agents, and enforces allocation rules between PLB and remote stands.

- **analytics.py**  
  Computes performance and cost metrics such as PLB utilization, remote overflow, service distribution, and penalty impact for each simulation run and PLB capacity scenario.

- **server.py**  
  Launches the interactive visualization server, providing real-time charts and slider-based controls to explore simulation behavior and sensitivity analysis results.

- **data/flights.csv**  
  Input dataset containing aircraft arrival schedules and ground time information used by the simulation.

- **data/generate_data.py**  
  Utility script to generate synthetic flight arrival data for testing and experimentation.


---

## 🔄 Data Flow & Execution Flow

The project follows a clear, modular data and execution pipeline:

1. **Data Generation** (`data/generate_data.py`)  
   Generates synthetic flight schedules and writes them to `data/flights.csv`.

2. **Simulation Execution** (`model.py`)  
   - Loads flight data  
   - Initializes the airport model, aircraft agents, and stands  
   - Advances the simulation over discrete time steps  
   - Collects step-wise simulation outputs

3. **Orchestration & Sensitivity Analysis** (`main.py`)  
   - Calls the simulation with different PLB capacities (5–50)  
   - Aggregates results across scenarios  
   - Triggers analytics computation

4. **Analytics Computation** (`analytics.py`)  
   Computes performance and cost metrics such as utilization, overflow, service distribution, and penalty impact.

5. **Visualization** (`run_vis.py`)  
   Loads simulation and analytics outputs and displays them using interactive charts and sliders.

This structure ensures a clean separation between **data generation**, **simulation logic**, **analysis**, and **presentation**, making the system easier to extend and reason about.

---

## ▶️ How to Run

### Environment Requirements
- **Python version**: Python 3.11.4
- Tested on Python 3.11.4 with the dependencies listed below

### Create and Activate a Virtual Environment (Recommended)
Before installing dependencies, create and activate a virtual environment to isolate the project environment.

```bash
python -m venv venv 
venv\Scripts\activate
```

### Install Dependencies
It is recommended to use a virtual environment.

```bash
pip install -r requirements.txt
```
---
## 🚀 Usage Guide

Follow the steps below to generate data, run the simulation and sensitivity analysis, and visualize the results.

### Step 1: Generate Input Data (Optional)

If you need to create fresh synthetic flight data for the simulation, run the data generator. This script creates or overwrites **data/flights.csv**

```bash
python data/generate_data.py
```

### Step 2: Run Simulation & Sensitivity Analysis

Execute the core simulation to perform a "What-If" analysis. This script runs the model through various PLB capacity scenarios (from 5 to 50 stands) to find the optimal configuration.

```bash
python -u .\main.py 
```

This command performs the following:
- Runs the simulation over a 6-hour operational period (1 Step = 1 Minute).
- Evaluates multiple capacity scenarios.
- Computes cost metrics (Stand Upkeep vs. Overflow Penalties).
- Writes aggregated results to **simulation_results.csv**.
- Performs Senstivity Analysis and gives optimal PLB Capacity.

### Step 3: Launch Interactive Visualization

To explore the simulation results using interactive charts and sliders, run:

```bash
python -u .\run_vis.py
```
This starts a local visualization server that allows:
- Dynamic exploration of PLB capacity
- Real-time visualization of utilization, overflow, service distribution, and penalty impact

---
## 📥 Inputs

The simulation uses both **configuration parameters** and **input data files**.

### Simulation Parameters

- **PLB Count**  
  Number of Passenger Loading Bridge (PLB) stands available at the airport.  
  This parameter is varied during sensitivity analysis to evaluate system performance.

- **Flight Count**  
  Number of flights generated when creating synthetic input data.  
  This controls the overall traffic load in the simulation.

---

### Input Data File

#### `data/flights.csv`

This file contains the flight schedule used by the simulation.

**Format:**

```text
aircraft_id, arrival_time, departure_time
```
- aircraft_id: Unique identifier for each aircraft
- arrival_time: Arrival time as a string (e.g., HH:MM)
- departure_time: Departure time as a string (e.g., HH:MM)

```text
Example:
AI101, 08:30, 09:45
AI102, 08:50, 10:10
AI103, 09:15, 10:00
```

The **flights.csv** file can be:

- Generated automatically using data/generate_data.py, or
- Manually edited to test custom traffic scenarios

---
## 📤 Outputs

The simulation produces both **file-based outputs** and **analytical metrics** to evaluate airport stand allocation performance.

---

### Simulation Output File

#### `simulation_results.csv`

This file contains step-wise simulation results capturing stand occupancy status.

**Format:**

```text
id, PLB_Occupied, Remote_Occupied, Service Quality Index
```
- id: Simulation step or time index
- PLB_Occupied: Number of PLB stands occupied at that step
- Remote_Occupied: Number of remote stands occupied at that step
- Service Quality Index: (PLB_Planes / Total_Planes) * 100

### Analytical Metrics Output

The `analytics.py` module computes the following aggregate performance metrics for each simulation run:

- **PLB Utilization (%)**  
  Percentage of time PLB stands are occupied during the simulation.

- **Remote Overflow Count**  
  Total number of aircraft assigned to remote stands.

- **Service Distribution**  
  Distribution of aircraft served by PLB stands versus remote stands.

- **Penalty Impact (Remote Minutes)**  
  Total penalty incurred due to aircraft being parked at remote stands.

---

### Sensitivity Analysis Output

During sensitivity analysis, the simulation is executed across multiple **PLB capacity scenarios (5–50)**.

For each PLB capacity, the following are recorded:
- Aggregate performance metrics
- Cost and penalty impacts
- Comparative utilization trends

These results are:
- Printed to the console
- Visualized through interactive charts
- Used to compare trade-offs between PLB availability and operational efficiency

---
## ⚠️ Assumptions, Simplifications, and Trade-offs

To keep the simulation focused, interpretable, and computationally efficient, the following assumptions and simplifications were made, along with their associated trade-offs:

### Assumptions
- **Deterministic Arrival and Departure Times**  
  Flight schedules are assumed to be fixed and known in advance, without modeling real-world delays or uncertainties.

- **Priority-Based Allocation**  
  Aircraft are always assigned to PLB stands first when available, with remote stands used only as a fallback.

- **Unlimited Remote Stands**  
  Remote stands are assumed to be unlimited, ensuring that aircraft are never rejected due to capacity constraints.

- **No Reassignment After Allocation**  
  Once an aircraft is assigned to a stand, it is not reassigned even if a preferred stand becomes available later.

- **Discrete Time Steps**  
  The simulation advances in discrete time steps instead of continuous time.

---

### Trade-offs
- **Realism vs Interpretability**  
  The model sacrifices operational realism in favor of clarity and ease of understanding.

- **Accuracy vs Speed**  
  Simplified rules and deterministic schedules allow fast simulation runs and sensitivity analysis across many scenarios.

- **Flexibility vs Complexity**  
  The simple priority-based allocation logic makes the model flexible and easy to modify but less expressive of real airport policies.

These choices ensure the simulation remains **transparent, explainable, and useful for high-level analysis**, rather than attempting to model the full complexity of real airport operations.
