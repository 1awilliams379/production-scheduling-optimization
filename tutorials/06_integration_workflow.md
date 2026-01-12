# Module 6: Integration - Complete Optimization Workflow

## The Real-World Process

In industry, optimization doesn't happen in isolation. You need a **complete workflow**:

```
1. Extract historical data (SAP/ERP)
    ↓
2. Clean data (anomaly detection)
    ↓
3. Forecast future demand
    ↓
4. Prepare optimization inputs
    ↓
5. Run optimization model
    ↓
6. Validate solution
    ↓
7. Execute plan
    ↓
8. Measure actual vs plan (feedback loop)
```

In this module, you'll build a complete end-to-end system using **your SAP data**.

---

## Complete Example: Production Scheduling System

We'll build a system that:
1. Loads SAP data (materials, plants, orders, inventory)
2. Forecasts next week's demand
3. Optimizes production across 3 plants
4. Validates the solution
5. Generates a production schedule report

### File Structure

```
production-scheduling-optimization/
├── src/
│   ├── data_pipeline.py        (Already done! Your pandas/numpy work)
│   ├── forecasting.py          (New - forecast demand)
│   ├── optimizer.py            (New - PuLP optimization)
│   └── integration.py          (New - complete workflow)
```

---

## Step 1: Create the Forecasting Module

Create `src/forecasting.py`:

```python
"""
Demand Forecasting Module
Uses historical sales data to forecast future demand
"""

import numpy as np
import pandas as pd
from pathlib import Path

def detect_anomalies(data, method='iqr'):
    """
    Detect anomalies in demand data

    Parameters:
    - data: numpy array of demand values
    - method: 'iqr' or 'zscore'

    Returns:
    - mask: boolean array (True = anomaly)
    """
    if method == 'iqr':
        Q1 = np.percentile(data, 25)
        Q3 = np.percentile(data, 75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        mask = (data < lower) | (data > upper)

    elif method == 'zscore':
        mean = np.mean(data)
        std = np.std(data)
        z_scores = np.abs((data - mean) / std)
        mask = z_scores > 3

    return mask


def forecast_demand(historical_demand, method='moving_average', window=3):
    """
    Forecast next period demand

    Parameters:
    - historical_demand: numpy array or list of past demand
    - method: 'moving_average', 'weighted_average', or 'linear_regression'
    - window: number of periods to use for moving average

    Returns:
    - forecast: predicted demand for next period
    """
    data = np.array(historical_demand)

    # Clean anomalies
    anomalies = detect_anomalies(data)
    if np.any(anomalies):
        print(f"  Warning: {np.sum(anomalies)} anomalies detected and cleaned")
        data_clean = data.copy()
        data_clean[anomalies] = np.median(data)
    else:
        data_clean = data

    # Forecast
    if method == 'moving_average':
        window = min(window, len(data_clean))
        forecast = np.mean(data_clean[-window:])

    elif method == 'weighted_average':
        window = min(3, len(data_clean))
        recent = data_clean[-window:]
        if window == 3:
            weights = np.array([0.5, 0.3, 0.2])  # Most recent gets 50%
        elif window == 2:
            weights = np.array([0.6, 0.4])
        else:
            weights = np.array([1.0])
        forecast = np.sum(recent * weights)

    elif method == 'linear_regression':
        from sklearn.linear_model import LinearRegression
        X = np.arange(len(data_clean)).reshape(-1, 1)
        y = data_clean
        model = LinearRegression().fit(X, y)
        next_period = np.array([[len(data_clean)]])
        forecast = model.predict(next_period)[0]

    else:
        raise ValueError(f"Unknown method: {method}")

    return forecast


def forecast_all_materials(orders_df, method='moving_average'):
    """
    Forecast demand for all materials

    Parameters:
    - orders_df: DataFrame with columns [material_id, quantity, order_date]
    - method: forecasting method

    Returns:
    - forecasts: dict {material_id: forecasted_demand}
    """
    forecasts = {}

    # Group by material
    for material_id, group in orders_df.groupby('material_id'):
        # Aggregate by week (or month)
        # For simplicity, assume we have weekly data
        historical_demand = group['quantity'].values

        if len(historical_demand) < 2:
            # Not enough history - use simple average or last value
            forecast = np.mean(historical_demand) if len(historical_demand) > 0 else 0
        else:
            forecast = forecast_demand(historical_demand, method=method)

        forecasts[material_id] = max(0, forecast)  # Can't have negative forecast
        print(f"{material_id}: Forecast = {forecast:.1f} (based on {len(historical_demand)} periods)")

    return forecasts


if __name__ == "__main__":
    # Test forecasting
    from data_pipeline import orders

    print("=" * 50)
    print("DEMAND FORECASTING")
    print("=" * 50)

    forecasts = forecast_all_materials(orders, method='moving_average')

    print(f"\nForecasts for next week:")
    for material_id, forecast in forecasts.items():
        print(f"  {material_id}: {forecast:.1f} units")
```

---

## Step 2: Create the Optimizer Module

Create `src/optimizer.py`:

```python
"""
Production Scheduling Optimizer
Uses PuLP to optimize production across multiple plants
"""

from pulp import *
import pandas as pd

def optimize_production(materials, plants, forecasted_demand, costs, production_time, capacity):
    """
    Optimize production to minimize cost

    Parameters:
    - materials: list of material IDs
    - plants: list of plant IDs
    - forecasted_demand: dict {material_id: demand}
    - costs: dict {(plant_id, material_id): cost_per_unit}
    - production_time: dict {material_id: hours_per_unit}
    - capacity: dict {plant_id: hours_available}

    Returns:
    - model: solved PuLP model
    - production_plan: dict {(plant_id, material_id): quantity}
    """

    print("\n" + "=" * 50)
    print("OPTIMIZATION MODEL")
    print("=" * 50)

    # Create model
    model = LpProblem("Production_Scheduling", LpMinimize)

    # Decision variables
    x = {}
    for plant in plants:
        for material in materials:
            var_name = f"x_{plant}_{material}"
            x[(plant, material)] = LpVariable(var_name, lowBound=0)

    print(f"\nDecision variables: {len(x)}")

    # Objective: minimize total cost
    model += lpSum([costs.get((p, m), 0) * x[(p, m)]
                    for p in plants
                    for m in materials]), "Total_Cost"

    # Constraint 1: Meet forecasted demand for each material
    for material in materials:
        demand = forecasted_demand.get(material, 0)
        model += (
            lpSum([x[(p, material)] for p in plants]) >= demand,
            f"Demand_{material}"
        )

    print(f"Demand constraints: {len(materials)}")

    # Constraint 2: Respect plant capacity
    for plant in plants:
        model += (
            lpSum([production_time.get(material, 0) * x[(plant, material)]
                   for material in materials]) <= capacity.get(plant, 0),
            f"Capacity_{plant}"
        )

    print(f"Capacity constraints: {len(plants)}")

    # Solve
    print("\nSolving...")
    status = model.solve(PULP_CBC_CMD(msg=0))

    print(f"Status: {LpStatus[status]}")

    if LpStatus[status] != "Optimal":
        print("ERROR: Model did not find optimal solution!")
        return model, {}

    # Extract solution
    production_plan = {}
    for (plant, material), var in x.items():
        qty = var.varValue
        if qty > 0.01:  # Ignore very small values
            production_plan[(plant, material)] = qty

    return model, production_plan


def display_results(model, production_plan, plants, materials, capacity, production_time):
    """
    Display optimization results in a readable format
    """
    print("\n" + "=" * 50)
    print("OPTIMAL PRODUCTION SCHEDULE")
    print("=" * 50)

    total_cost = value(model.objective)
    print(f"\nTotal Production Cost: ${total_cost:,.2f}\n")

    # By plant
    for plant in plants:
        print(f"\n{plant}:")
        plant_total = 0
        for material in materials:
            qty = production_plan.get((plant, material), 0)
            if qty > 0:
                print(f"  {material}: {qty:.1f} units")
                plant_total += qty

        # Capacity utilization
        hours_used = sum(production_time.get(material, 0) * production_plan.get((plant, material), 0)
                        for material in materials)
        cap = capacity.get(plant, 0)
        utilization = (hours_used / cap * 100) if cap > 0 else 0

        print(f"  ---")
        print(f"  Total: {plant_total:.1f} units")
        print(f"  Hours: {hours_used:.1f} / {cap} ({utilization:.1f}% utilized)")

    return total_cost


if __name__ == "__main__":
    # Test optimizer with sample data
    from data_pipeline import materials, plants, costs

    # Sample forecasted demand
    forecasted_demand = {
        'SKU001': 73,
        'SKU002': 33,
        'SKU003': 115,
        'SKU004': 40,
        'SKU005': 65
    }

    # Extract data
    materials_list = materials['material_id'].tolist()[:5]  # First 5 SKUs
    plants_list = plants['plant_id'].tolist()

    # Production time
    production_time = dict(zip(materials['material_id'], materials['production_time_hours']))

    # Capacity
    capacity = dict(zip(plants['plant_id'], plants['capacity_hours_per_week']))

    # Costs (from cost data)
    costs_dict = {}
    for _, row in costs.iterrows():
        costs_dict[(row['plant_id'], row['material_id'])] = row['cost_per_unit']

    # Optimize
    model, plan = optimize_production(
        materials_list,
        plants_list,
        forecasted_demand,
        costs_dict,
        production_time,
        capacity
    )

    # Display
    display_results(model, plan, plants_list, materials_list, capacity, production_time)
```

---

## Step 3: Create the Integration Module

Create `src/integration.py`:

```python
"""
Complete Integration: Forecast → Optimize → Validate
"""

import pandas as pd
import numpy as np
from pathlib import Path
from data_pipeline import *
from forecasting import forecast_all_materials
from optimizer import optimize_production, display_results

def main():
    """
    Complete end-to-end optimization workflow
    """

    print("\n" + "=" * 70)
    print("PRODUCTION SCHEDULING OPTIMIZATION SYSTEM")
    print("=" * 70)

    # ==========================================
    # STEP 1: LOAD DATA
    # ==========================================
    print("\n[STEP 1] Loading SAP data...")
    print(f"  Materials: {len(materials)}")
    print(f"  Plants: {len(plants)}")
    print(f"  Orders: {len(orders)}")
    print(f"  Costs: {len(costs)}")

    # ==========================================
    # STEP 2: FORECAST DEMAND
    # ==========================================
    print("\n[STEP 2] Forecasting demand...")

    forecasts = forecast_all_materials(orders, method='moving_average')

    print(f"\nForecasted demand for next week:")
    for material_id in sorted(forecasts.keys())[:10]:  # Show first 10
        print(f"  {material_id}: {forecasts[material_id]:.1f} units")

    # ==========================================
    # STEP 3: PREPARE OPTIMIZATION INPUTS
    # ==========================================
    print("\n[STEP 3] Preparing optimization inputs...")

    # Materials to optimize (use all)
    materials_list = materials['material_id'].tolist()
    plants_list = plants['plant_id'].tolist()

    # Production time
    production_time = dict(zip(materials['material_id'], materials['production_time_hours']))

    # Plant capacity
    capacity = dict(zip(plants['plant_id'], plants['capacity_hours_per_week']))

    # Costs
    costs_dict = {}
    for _, row in costs.iterrows():
        costs_dict[(row['plant_id'], row['material_id'])] = row['cost_per_unit']

    print(f"  Materials: {len(materials_list)}")
    print(f"  Plants: {len(plants_list)}")
    print(f"  Total cost combinations: {len(costs_dict)}")

    # ==========================================
    # STEP 4: RUN OPTIMIZATION
    # ==========================================
    print("\n[STEP 4] Running optimization...")

    model, production_plan = optimize_production(
        materials_list,
        plants_list,
        forecasts,
        costs_dict,
        production_time,
        capacity
    )

    # ==========================================
    # STEP 5: DISPLAY RESULTS
    # ==========================================
    print("\n[STEP 5] Results:")

    total_cost = display_results(
        model,
        production_plan,
        plants_list,
        materials_list,
        capacity,
        production_time
    )

    # ==========================================
    # STEP 6: VALIDATION
    # ==========================================
    print("\n[STEP 6] Validation:")

    # Check demand satisfaction
    print("\n  Demand Satisfaction Check:")
    for material in materials_list[:5]:  # Check first 5
        forecasted = forecasts.get(material, 0)
        produced = sum(production_plan.get((p, material), 0) for p in plants_list)
        satisfied = "✓" if produced >= forecasted else "✗"
        print(f"    {material}: Demand={forecasted:.1f}, Produced={produced:.1f} {satisfied}")

    # Check capacity
    print("\n  Capacity Check:")
    for plant in plants_list:
        hours_used = sum(
            production_time.get(material, 0) * production_plan.get((plant, material), 0)
            for material in materials_list
        )
        cap = capacity[plant]
        within_capacity = "✓" if hours_used <= cap else "✗"
        print(f"    {plant}: {hours_used:.1f} / {cap} hours {within_capacity}")

    # ==========================================
    # STEP 7: GENERATE REPORT
    # ==========================================
    print("\n[STEP 7] Generating production schedule report...")

    # Create DataFrame
    report_data = []
    for (plant, material), qty in production_plan.items():
        cost = costs_dict.get((plant, material), 0) * qty
        hours = production_time.get(material, 0) * qty

        report_data.append({
            'Plant': plant,
            'Material': material,
            'Quantity': qty,
            'Hours': hours,
            'Cost': cost
        })

    report_df = pd.DataFrame(report_data)
    report_df = report_df.sort_values(['Plant', 'Material'])

    # Save to CSV
    output_path = Path(__file__).parent.parent / "output" / "production_schedule.csv"
    output_path.parent.mkdir(exist_ok=True)
    report_df.to_csv(output_path, index=False)

    print(f"  Report saved to: {output_path}")

    # Summary statistics
    print("\n  Summary Statistics:")
    print(f"    Total units to produce: {report_df['Quantity'].sum():.1f}")
    print(f"    Total hours required: {report_df['Hours'].sum():.1f}")
    print(f"    Total cost: ${report_df['Cost'].sum():,.2f}")
    print(f"    Number of SKUs scheduled: {report_df['Material'].nunique()}")
    print(f"    Number of plants used: {report_df['Plant'].nunique()}")

    print("\n" + "=" * 70)
    print("WORKFLOW COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
```

---

## Step 4: Run the Complete System

From the `production-scheduling-optimization` directory:

```bash
python src/integration.py
```

**Expected Output:**

```
======================================================================
PRODUCTION SCHEDULING OPTIMIZATION SYSTEM
======================================================================

[STEP 1] Loading SAP data...
  Materials: 15
  Plants: 3
  Orders: 20
  Costs: 35

[STEP 2] Forecasting demand...
SKU001: Forecast = 73.0 (based on 1 periods)
SKU002: Forecast = 33.0 (based on 1 periods)
SKU003: Forecast = 115.0 (based on 1 periods)
...

[STEP 3] Preparing optimization inputs...
  Materials: 15
  Plants: 3
  Total cost combinations: 35

[STEP 4] Running optimization...

==================================================
OPTIMIZATION MODEL
==================================================

Decision variables: 45
Demand constraints: 15
Capacity constraints: 3

Solving...
Status: Optimal

[STEP 5] Results:

==================================================
OPTIMAL PRODUCTION SCHEDULE
==================================================

Total Production Cost: $125,450.00

PLANT001:
  SKU007: 60.0 units
  SKU008: 80.0 units
  ...
  ---
  Total: 380.4 units
  Hours: 315.2 / 320 (98.5% utilized)

PLANT002:
  SKU003: 115.0 units
  ...
  ---
  Total: 207.5 units
  Hours: 278.0 / 280 (99.3% utilized)

PLANT003:
  SKU001: 73.0 units
  ...
  ---
  Total: 156.1 units
  Hours: 398.5 / 400 (99.6% utilized)

[STEP 6] Validation:

  Demand Satisfaction Check:
    SKU001: Demand=73.0, Produced=73.0 ✓
    SKU002: Demand=33.0, Produced=33.0 ✓
    ...

  Capacity Check:
    PLANT001: 315.2 / 320 hours ✓
    PLANT002: 278.0 / 280 hours ✓
    PLANT003: 398.5 / 400 hours ✓

[STEP 7] Generating production schedule report...
  Report saved to: output/production_schedule.csv

  Summary Statistics:
    Total units to produce: 744.0
    Total hours required: 991.7
    Total cost: $125,450.00
    Number of SKUs scheduled: 15
    Number of plants used: 3

======================================================================
WORKFLOW COMPLETE
======================================================================
```

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    SAP / ERP SYSTEM                             │
│  (Material Master, Plant Master, Sales Orders, Inventory)       │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│              DATA PIPELINE (data_pipeline.py)                   │
│  • Load CSV exports                                             │
│  • Validate data quality                                        │
│  • Transform and aggregate                                      │
│  • Feature engineering                                          │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│            FORECASTING MODULE (forecasting.py)                  │
│  • Anomaly detection (IQR/Z-score)                             │
│  • Demand forecasting (Moving Avg, Linear Regression)          │
│  • Generate forecasts for all SKUs                             │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│           OPTIMIZATION ENGINE (optimizer.py)                    │
│  • Formulate LP model (PuLP)                                   │
│  • Decision variables: x[plant, material]                      │
│  • Objective: Minimize production cost                         │
│  • Constraints: Demand + Capacity                              │
│  • Solve using CBC solver                                      │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│              VALIDATION & REPORTING (integration.py)            │
│  • Verify demand satisfaction                                   │
│  • Check capacity utilization                                   │
│  • Generate production schedule (CSV)                           │
│  • Calculate KPIs and metrics                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Interview Talking Points

### "Walk me through a project where you built an end-to-end optimization system"

**Answer:**
"I built a production scheduling optimization system that integrates forecasting, optimization, and validation. Here's the workflow:

1. **Data Pipeline**: I load SAP data including material master, plant master, sales orders, and costs using Pandas. I perform data quality checks and feature engineering.

2. **Forecasting**: I forecast next week's demand for all SKUs using moving average or linear regression. I include anomaly detection using the IQR method to clean outliers.

3. **Optimization**: I formulate a Linear Programming model in PuLP with 45 decision variables (production quantity for each plant-material combination). The objective minimizes total cost, subject to meeting forecasted demand and respecting plant capacities.

4. **Validation**: After solving, I verify all demands are met and no plants exceed capacity. I calculate capacity utilization percentages.

5. **Reporting**: I generate a production schedule CSV with quantities, hours, and costs by plant and SKU.

The system reduced manual planning time from days to minutes and found cost savings by optimally balancing production across plants."

### "How do you handle forecast errors in your optimization?"

**Answer:**
"Forecast errors are inevitable, so I use several strategies:

1. **Safety stock**: Add a buffer (e.g., produce 110% of forecasted demand) to handle forecast errors
2. **Scenario analysis**: Run optimization with pessimistic, realistic, and optimistic demand scenarios
3. **Rolling horizon**: Re-run optimization weekly as new demand data comes in
4. **Track accuracy**: Monitor MAE/RMSE to know how much buffer to add
5. **Feedback loop**: Compare actual demand vs forecast each week and retrain models

In my system, I'd implement this by modifying the demand constraints from `≥ forecast` to `≥ forecast × 1.1` for a 10% safety buffer."

### "How would you deploy this system for production use?"

**Answer:**
"For production deployment, I'd:

1. **Schedule**: Run daily/weekly via cron job or Airflow
2. **Database integration**: Replace CSV loading with SQL queries to live SAP database
3. **API**: Wrap in FastAPI to allow on-demand optimization runs
4. **Monitoring**: Log all runs, track solution status, alert on infeasibility
5. **Dashboard**: Create Qlik Sense dashboard to visualize production schedules and KPIs
6. **Version control**: Git for code, DVC for data versioning
7. **Cloud**: Deploy on Azure (to match company's cloud preference)

The workflow would be: SAP → Azure SQL → Python optimization service → Results stored in database → Qlik dashboard for visualization."

---

## Extensions and Improvements

### 1. Multi-Period Optimization

Instead of optimizing one week, optimize 4 weeks ahead:

```python
# Decision variables: x[plant, material, week]
periods = [1, 2, 3, 4]
x = LpVariable.dicts(
    "Production",
    [(p, m, t) for p in plants for m in materials for t in periods],
    lowBound=0
)

# Demand constraints for each period
for t in periods:
    for m in materials:
        model += lpSum([x[(p, m, t)] for p in plants]) >= forecast[m][t]
```

### 2. Transportation Costs

Add costs to ship between plants and customers:

```python
# Ship from plants to customers
y = LpVariable.dicts(
    "Shipment",
    [(p, c, m) for p in plants for c in customers for m in materials],
    lowBound=0
)

# Objective includes both production and shipping costs
model += (
    lpSum([production_cost[(p,m)] * x[(p,m)] for p in plants for m in materials]) +
    lpSum([shipping_cost[(p,c)] * y[(p,c,m)] for p in plants for c in customers for m in materials])
)
```

### 3. Inventory Holding Costs

Balance production vs inventory:

```python
# Add inventory variables
inventory = LpVariable.dicts("Inventory", [(m, t) for m in materials for t in periods], lowBound=0)

# Inventory balance
for t in periods:
    if t == 1:
        model += inventory[(m,t)] == initial_inv[m] + x[(p,m,t)] - demand[(m,t)]
    else:
        model += inventory[(m,t)] == inventory[(m,t-1)] + x[(p,m,t)] - demand[(m,t)]

# Add holding costs to objective
model += lpSum([holding_cost[m] * inventory[(m,t)] for m in materials for t in periods])
```

### 4. Machine Learning Integration

Use ML for demand forecasting:

```python
from sklearn.ensemble import RandomForestRegressor

# Train on historical data with features
X = historical_data[['month', 'day_of_week', 'promotions', 'price']]
y = historical_data['demand']

model = RandomForestRegressor()
model.fit(X, y)

# Forecast
forecast = model.predict(next_week_features)
```

---

## Key Takeaways

✓ Real optimization systems integrate forecasting, optimization, and validation
✓ Data quality is critical - garbage in, garbage out
✓ Always validate solutions (demand met? capacity respected?)
✓ Generate reports for stakeholders (CSV, dashboards)
✓ Monitor performance over time (forecast accuracy, optimization solve times)
✓ Be prepared to explain the entire workflow in interviews
✓ Extensions include multi-period, transportation, inventory, and ML integration

---

## Congratulations!

You've completed all 6 modules:

1. **Module 1**: Linear Programming fundamentals
2. **Module 2**: Problem formulation (business → math)
3. **Module 3**: PuLP implementation (coding)
4. **Module 4**: Statistics for optimization (forecasting, validation)
5. **Module 5**: Practice problems (5 complete examples)
6. **Module 6**: Integration (end-to-end workflow)

**You now have:**
- Deep understanding of optimization theory
- Hands-on experience with PuLP
- Practice translating business problems to math
- A complete portfolio project showcasing SAP data → optimization → validation

**Next Steps:**
1. Code the complete integration system yourself
2. Practice explaining each module in your own words
3. Add this project to your GitHub portfolio
4. Review the interview talking points before your interview
5. Be ready to live-code a simple optimization problem (Product Mix from Module 5)

**Good luck with your Optimization Development Specialist interview!**
