# Simple Data Loader
# Loads all 6 SAP tables

import pandas as pd
from pathlib import Path
from typing import Dict
import numpy as np

# Where the data is
DATA_DIR = Path(__file__).parent.parent / "data"

# Load each table
print("Loading data...")

materials = pd.read_csv(DATA_DIR / "sap_material_master.csv")
plants = pd.read_csv(DATA_DIR / "sap_plant_master.csv")
orders = pd.read_csv(DATA_DIR / "sap_sales_orders.csv")
inventory = pd.read_csv(DATA_DIR / "sap_inventory.csv")
production = pd.read_csv(DATA_DIR / "sap_production_history.csv")
costs = pd.read_csv(DATA_DIR / "sap_cost_data.csv")

print(f"\nLoaded:")
print("\nMaterials table sample:")
print(f"  - {len(materials)} materials")
print(materials.head())
print("\nPlants table sample:")
print(f"  - {len(plants)} plants")
print(plants.head())
print("\nOrders table sample:")
print(f"  - {len(orders)} orders")
print(orders.head())
print("\nInventory table sample:")
print(f"  - {len(inventory)} inventory records")
print(inventory.head())
print("\nProduction table sample:")
print(f"  - {len(production)} production records")
print(production.head())
print("\nCost table sample:")
print(f"  - {len(costs)} cost records")
print(costs.head())
# Now all dataframes are available for further processing

###### Pandas Analysis ######

# Calculate total demand by material
print("\n--- Total Demand by Material ---")
demand = orders.groupby('material_id')['quantity'].sum()
print(demand.sort_values(ascending=False).head(10))

# Check for missing values
print("\n--- Data Quality Check ---")
# Check for Nan values materials table sum of all rows in each column plus the sum of all columns
print(f"Materials missing values: {materials.isnull().sum().sum()}")
# Check for Nan values plants table sum of all rows in each column plus the sum of all columns
print(f"Plants missing values: {plants.isnull().sum().sum()}")
# Check for Nan values orders table sum of all rows in each column plus the sum of all columns
print(f"Orders missing values: {orders.isnull().sum().sum()}")

# Join demand with material descriptions
print("\n--- Top Demand with Product Names ---")
demand_df = demand.reset_index()  # Convert Series to DataFrame
#merge is SQL join
demand_with_names = demand_df.merge(
    materials[['material_id', 'description']],
    on='material_id'
)
print(demand_with_names.sort_values('quantity', ascending=False).head(5))

###### NumPy Analysis ######

print("\n--- Demand Value Analysis (NumPy) ---")
print("\nBusiness question: What's the total value of demand? (quantity × unit cost)")

# Merge demand with costs
demand_with_cost = demand_df.merge(
    materials[['material_id', 'unit_cost']],
    on='material_id'
)

# Calculate total value (quantity × cost)
demand_with_cost['total_value'] = demand_with_cost['quantity'] * demand_with_cost['unit_cost']


print("\nDemand with costs sample:")
print(demand_with_cost.head())

# NumPy calculations
print(f"\nTotal demand value: ${demand_with_cost['total_value'].sum():,.2f}")
print(f"Average order value: ${np.mean(demand_with_cost['total_value']):,.2f}")
print(f"Max single SKU value: ${np.max(demand_with_cost['total_value']):,.2f}")
print(f"Standard deviation: ${np.std(demand_with_cost['total_value']):,.2f}")


###### Feature Engineering ######

# Create useful columns
print("\n--- Feature Engineering ---")
print("\nBusiness question: Which materials have high demand but low inventory?")

# Calculate inventory coverage (inventory / demand)
inventory_summary = inventory.groupby('material_id')['quantity_on_hand'].sum()

print("\nInventory summary sample:")
print(inventory_summary.head())

coverage = demand_df.merge(
    inventory_summary.reset_index().rename(columns={'quantity_on_hand': 'inventory'}),
    on='material_id'
)

# Display coverage sample
print("\n Coverage sample:")
print(coverage.head())

# Create new feature: days of supply
coverage['coverage_ratio'] = coverage['inventory'] / coverage['quantity']
coverage['needs_production'] = coverage['coverage_ratio'] < 1.0  # True if need to produce

print("\nMaterials needing production:")
needs_prod = coverage['needs_production']
cols = ['material_id', 'quantity', 'inventory', 'coverage_ratio']
coverage_results = coverage.loc[needs_prod, cols] 
print(coverage_results.head(10))