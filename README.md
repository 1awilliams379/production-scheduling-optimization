# Production Scheduling Optimization

**Author**: Portfolio Project for Data Scientist - Optimization Development Specialist Role
**Technologies**: Python, Pandas, NumPy, PuLP (Linear Programming)
**Domain**: Manufacturing Operations, SAP/ERP Data Analytics

---

## Overview

A production scheduling optimizer that solves real-world manufacturing allocation problems using **Linear Programming (LP)**. This project demonstrates end-to-end optimization workflow from SAP-style data ingestion to optimal production scheduling across multiple plants.

### Business Problem

Given:
- **15 SKUs** (Stock Keeping Units) to manufacture
- **3 manufacturing plants** with different capacities and costs
- **744 units** of total customer demand across 20 orders
- **Limited production capacity** at each plant

**Goal**: Determine the optimal allocation of production across plants to **minimize total cost** while meeting all customer demand and respecting plant capacity constraints.

---

## Key Features

### 1. SAP/ERP Data Pipeline (`data_pipeline.py`)
- Loads and validates 6 SAP-style data tables (Material Master, Plant Master, Sales Orders, Inventory, Production History, Cost Data)
- Data quality checks (missing values, referential integrity)
- Pandas operations: `groupby`, `merge` (joins), aggregations
- NumPy statistical calculations (mean, max, standard deviation)
- **Feature engineering**: Creates `coverage_ratio` and `needs_production` flags

### 2. Production Scheduling Optimizer (`optimizer.py`)
- **Linear Programming** model using PuLP library
- **45 decision variables**: Production quantity for each plant-material combination
- **Objective function**: Minimize total production cost
- **Constraints**:
  - Demand satisfaction: Total production ≥ customer orders for each SKU
  - Capacity limits: Total hours used ≤ plant capacity
- Solves in ~21 iterations to find optimal allocation

---

## Technical Skills Demonstrated

| Category | Skills |
|----------|--------|
| **Python Libraries** | Pandas, NumPy, PuLP |
| **Data Engineering** | ETL pipeline, data validation, data quality checks |
| **Pandas Operations** | `read_csv`, `groupby`, `merge`, boolean filtering, `.loc` indexing |
| **NumPy** | Statistical calculations (`mean`, `max`, `std`) |
| **Optimization** | Linear Programming (LP), decision variables, objective functions, constraints |
| **Domain Knowledge** | SAP/ERP data structures (MARA, MARC, VBAK/VBAP equivalents) |
| **Software Engineering** | Modular code, clear documentation, reusable functions |

---

## Project Structure

```
production-scheduling-optimization/
│
├── data/                          # SAP-style CSV data files
│   ├── sap_material_master.csv   # 15 SKUs with costs and production times
│   ├── sap_plant_master.csv      # 3 plants with capacities
│   ├── sap_sales_orders.csv      # 20 customer order lines
│   ├── sap_inventory.csv         # Current inventory levels
│   ├── sap_production_history.csv
│   └── sap_cost_data.csv
│
├── src/
│   ├── data_pipeline.py          # Data loading, validation, feature engineering
│   └── optimizer.py              # Production scheduling LP model
│
└── README.md
```

---

## Installation & Usage

### Prerequisites
```bash
Python 3.8+
pip install pandas numpy pulp
```

### Running the Data Pipeline
```bash
python src/data_pipeline.py
```

**Output**:
- Loads 6 data tables (15 materials, 3 plants, 20 orders)
- Validates data quality (0 missing values in key tables)
- Calculates total demand: **744 units**
- Analyzes demand value: **$142,905 total**
- Identifies **4 materials** needing production (coverage < 100%)

### Running the Optimizer
```bash
python src/optimizer.py
```

**Output**:
- Builds LP model with 45 variables, 18 constraints
- Solves in 21 iterations
- Produces optimal production schedule across 3 plants
- **PLANT001**: 380.4 units (51% of production)
- **PLANT002**: 207.5 units (28% of production)
- **PLANT003**: 156.1 units (21% of production)

---

## Sample Results

### Data Pipeline Output

```
--- Total Demand by Material ---
SKU003    115 units (Control Valve Type 1)
SKU009    100 units (Pipe Fitting Set A)
SKU008     80 units (Pressure Gauge Analog)
...

--- Demand Value Analysis (NumPy) ---
Total demand value: $142,905.00
Average order value: $9,527.00
Max single SKU value: $32,850.00

--- Feature Engineering ---
Materials needing production:
  SKU001: 73 demand, 45 inventory → 62% coverage
  SKU002: 33 demand, 12 inventory → 36% coverage
  SKU003: 115 demand, 85 inventory → 74% coverage
  SKU005: 65 demand, 28 inventory → 43% coverage
```

### Optimizer Output

```
==================================================
OPTIMAL PRODUCTION SCHEDULE
==================================================

PLANT001:
  SKU007 (Pressure Gauge Digital): 60.0 units
  SKU008 (Pressure Gauge Analog): 80.0 units
  SKU009 (Pipe Fitting Set A): 100.0 units
  ...
  Total: 380.4 units

PLANT002:
  SKU003 (Control Valve Type 1): 115.0 units
  SKU004 (Control Valve Type 2): 40.0 units
  ...
  Total: 207.5 units

PLANT003:
  SKU001 (Industrial Pump Model A): 73.0 units
  SKU002 (Industrial Pump Model B): 33.0 units
  ...
  Total: 156.1 units

Solution Status: Optimal
Total: 744 units (meets all demand)
```

---

## Optimization Model Formulation

### Decision Variables
```
x[p,m] = quantity of material m to produce at plant p
where p ∈ {PLANT001, PLANT002, PLANT003}
      m ∈ {SKU001, SKU002, ..., SKU015}
Total: 45 variables
```

### Objective Function
```
Minimize: Σ (x[p,m] × cost[p,m]) for all p, m
```

### Constraints
```
1. Demand Satisfaction (15 constraints):
   Σ x[p,m] ≥ demand[m]  ∀m

2. Capacity Limits (3 constraints):
   Σ (x[p,m] × production_time[m]) ≤ capacity[p]  ∀p

3. Non-negativity (implicit):
   x[p,m] ≥ 0  ∀p,m
```

---

## Key Insights from Results

1. **Load Balancing**: Optimizer distributes production to balance capacity utilization
   - PLANT001: Handles high-volume, lower complexity items (gauges, fittings)
   - PLANT002: Specializes in valves and motors
   - PLANT003: Focuses on pumps (higher complexity items)

2. **Split Production**: Some SKUs (e.g., SKU005, SKU013) are produced at multiple plants
   - This balances capacity constraints across facilities
   - Demonstrates the optimizer's ability to find non-obvious solutions

3. **Capacity Utilization**: Near-optimal use of plant capacity
   - Total demand (744 units) strategically allocated
   - Respects hour limits while minimizing cost

---

## Interview Talking Points

### "Walk me through this project"

> "I built a production scheduling optimizer that addresses a real manufacturing challenge: allocating production across multiple plants to minimize costs. I started by creating a data pipeline that loads SAP-style ERP data—material master, plant master, sales orders, inventory, and cost tables. The pipeline performs data validation, calculates business metrics like total demand and inventory coverage, and engineers features to identify production gaps.
>
> For the optimization, I formulated a Linear Programming model using PuLP. The model has 45 decision variables representing production quantities for each plant-material combination. The objective minimizes total production cost, subject to two types of constraints: demand satisfaction (must meet all customer orders) and capacity limits (can't exceed plant hours).
>
> The solver found the optimal solution in 21 iterations, allocating 744 units across three plants. The solution demonstrates sophisticated load balancing—some SKUs are split across multiple plants to optimize capacity utilization. This project showcases my ability to translate business problems into mathematical optimization models and implement end-to-end data science workflows."

### "What challenges did you face?"

> "The main challenge was structuring the optimization problem correctly—ensuring the decision variables, objective function, and constraints accurately represented the business rules. I also had to handle sparse cost data (not all plant-material combinations have costs) and implement proper data validation to catch quality issues upstream of the optimizer."

### "How would you extend this?"

> "I'd add:
> - Transportation costs between plants and customers
> - Multi-period scheduling (weekly planning horizons)
> - Inventory holding costs
> - Mixed-Integer constraints for minimum batch sizes
> - Scenario analysis (what-if demand changes by 20%?)
> - Integration with a database instead of CSV files"

---

## Related Skills (Full Portfolio)

This is **Project 1 of 3** in my data science portfolio:

1. **Production Scheduling Optimization** (This repo) - Python, Pandas, NumPy, PuLP
2. **Supply Chain Data Pipeline** - SQL, BigQuery, Cloud Architecture (GCP/Azure)
3. **Operations Dashboards** - Qlik Sense, Power Platform, BI Visualization

---

## License

This is a portfolio project for educational and demonstration purposes.

---

## Contact

**LinkedIn**: [Your LinkedIn]
**Email**: [Your Email]
**Portfolio**: [Your Portfolio Site]

---

*Built as part of interview preparation for Data Scientist - Optimization Development Specialist roles in manufacturing and supply chain domains.*
