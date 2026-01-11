# Import libraries
import pandas as pd
from pathlib import Path
from pulp import *  # This is the optimization library!

print("Starting Production Scheduler Optimizer...")

# Load data
DATA_DIR = Path(__file__).parent.parent / "data"

print("\nLoading data...")
materials = pd.read_csv(DATA_DIR / "sap_material_master.csv")
plants = pd.read_csv(DATA_DIR / "sap_plant_master.csv")
orders = pd.read_csv(DATA_DIR / "sap_sales_orders.csv")
costs = pd.read_csv(DATA_DIR / "sap_cost_data.csv")

# Calculate demand
demand = orders.groupby('material_id')['quantity'].sum()

print(f"Loaded: {len(materials)} materials, {len(plants)} plants")
print(f"Total demand: {demand.sum()} units")

# Create the optimization model
print("\n--- Building Optimization Model ---")

# Step 1: Create the model
model = LpProblem("Production_Scheduling", LpMinimize)
print("Model created: Minimize total cost")

# Step 2: Create decision variables
  # For each plant and each material, decide how much to produce        
production = {}

for plant_id in plants['plant_id']:
    for material_id in materials['material_id']:
        # Create a variable: production[(plant, material)]
        var_name = f"Produce_{plant_id}_{material_id}"
        production[(plant_id, material_id)] = LpVariable(var_name, lowBound=0)

print(f"Created {len(production)} decision variables")
print(f"Example: {list(production.keys())[:3]}")

# Step 3: Define objective function - Minimize total cost
print("\n--- Setting Objective Function ---")

# Get production costs from cost data
production_costs = {}
for _, row in costs[costs['cost_type'] == 'Production'].iterrows():   
    production_costs[(row['plant_id'], row['material_id'])] = row['cost_per_unit']

# Objective: Sum of (production × cost) for all plant-material combinations
model += lpSum([
    production[(p, m)] * production_costs.get((p, m), 0)
    for p in plants['plant_id']
    for m in materials['material_id']
    if (p, m) in production_costs
])

print("Objective set: Minimize total production cost")

# Step 4: Add constraints
print("\n--- Adding Constraints ---")

# Constraint 1: Meet demand for each material
for material_id in materials['material_id']:
    if material_id in demand.index:
        model += (
            lpSum([production[(p, material_id)] for p in plants['plant_id']])
            >= demand[material_id],
            f"Demand_{material_id}"
        )

print(f"Added {len(materials)} demand constraints")

# Constraint 2: Don't exceed plant capacity (hours)
for plant_id in plants['plant_id']:
    plant_capacity = plants[plants['plant_id'] == plant_id]['capacity_hours_per_week'].values[0]
    model += (
        lpSum([
            production[(plant_id, m)] * materials[materials['material_id'] == m]['production_time_hours'].values[0]
            for m in materials['material_id']
        ])
        <= plant_capacity,
        f"Capacity_{plant_id}"
    )

print(f"Added {len(plants)} capacity constraints")
print(f"\nTotal constraints: {len(model.constraints)}")

# Step 5: Solve the model
print("\n" + "="*50)
print("SOLVING THE OPTIMIZATION MODEL...")
print("="*50)

model.solve()

# Check if we found an optimal solution
status = LpStatus[model.status]
print(f"\nSolution Status: {status}")

if status == 'Optimal':
    print(f"Optimal Total Cost: ${value(model.objective):,.2f}")      
else:
    print("No optimal solution found!")

# Step 6: Display results
if status == 'Optimal':
    print("\n" + "="*50)
    print("OPTIMAL PRODUCTION SCHEDULE")
    print("="*50)

    # Show production by plant
    for plant_id in plants['plant_id']:
        print(f"\n{plant_id}:")
        plant_total = 0
        for material_id in materials['material_id']:
            qty = production[(plant_id, material_id)].varValue        
            if qty > 0:  # Only show if producing
                material_name = materials[materials['material_id'] == material_id]['description'].values[0]
                print(f"  {material_id} ({material_name}): {qty:.1f} units")
                plant_total += qty
        print(f"  Total: {plant_total:.1f} units")

    print("\n" + "="*50)
    print("Optimization complete!")