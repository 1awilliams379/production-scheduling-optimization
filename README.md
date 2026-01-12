# Production Scheduling Optimization

An end-to-end production scheduling optimizer that solves multi-plant allocation problems using linear programming.

## Overview

This system addresses manufacturing allocation challenges by optimizing production across multiple plants while minimizing costs and respecting operational constraints. The solution processes SAP/ERP-style data and generates optimal production schedules using linear programming techniques.

**Problem Scale:**
- 15 SKUs across 3 manufacturing plants
- 744 units of customer demand from 20 orders
- Variable production costs and capacities by plant
- Constraint: Meet all demand while respecting plant capacity limits

**Solution:** Linear programming model that minimizes total production cost while satisfying all constraints.

## Technical Implementation

### Optimization Model

**Decision Variables:**
```
x[p,m] = quantity of material m to produce at plant p
where p ∈ {PLANT001, PLANT002, PLANT003}
      m ∈ {SKU001, ..., SKU015}
Total: 45 decision variables
```

**Objective Function:**
```
Minimize: Σ Σ cost[p,m] × x[p,m]
         p  m
```

**Constraints:**
```
1. Demand Satisfaction (15 constraints):
   Σ x[p,m] ≥ demand[m]  ∀m
   p

2. Plant Capacity (3 constraints):
   Σ production_time[m] × x[p,m] ≤ capacity[p]  ∀p
   m

3. Non-negativity:
   x[p,m] ≥ 0  ∀p,m
```

### Data Pipeline

The ETL pipeline processes 6 SAP-style data tables:
- **Material Master:** SKU costs and production times
- **Plant Master:** Facility capacities and labor costs
- **Sales Orders:** Customer demand by SKU
- **Inventory:** Current stock levels
- **Production History:** Historical manufacturing data
- **Cost Data:** Plant-specific production costs

Pipeline includes data validation, quality checks, and feature engineering (inventory coverage ratios, production gap identification).

## Results

The optimizer successfully allocates 744 units across three plants:

```
PLANT001: 380.4 units (51% of total, 98.5% capacity utilization)
PLANT002: 207.5 units (28% of total, 99.3% capacity utilization)
PLANT003: 156.1 units (21% of total, 99.6% capacity utilization)

Status: Optimal solution found in ~21 iterations
```

**Key Outcomes:**
- **Optimal Load Balancing:** Production distributed to maximize capacity utilization (98-99%)
- **Cost Minimization:** Solver finds lowest-cost allocation across plants
- **Split Production:** Some SKUs produced at multiple plants to balance constraints
- **Full Demand Coverage:** All 744 units of customer demand satisfied

## Technology Stack

**Core:**
- Python 3.8+
- PuLP (Linear Programming solver)
- Pandas, NumPy (Data manipulation)

**Data:**
- SAP/ERP-style CSV data structures
- SQLite (optional for database integration)

## Project Structure

```
production-scheduling-optimization/
├── data/
│   ├── sap_material_master.csv
│   ├── sap_plant_master.csv
│   ├── sap_sales_orders.csv
│   ├── sap_inventory.csv
│   ├── sap_production_history.csv
│   └── sap_cost_data.csv
├── src/
│   ├── data_pipeline.py          # ETL and data validation
│   ├── optimizer.py               # LP model implementation
│   ├── forecasting.py             # Demand forecasting
│   └── integration.py             # End-to-end workflow
└── tutorials/                     # Documentation
```

## Installation & Usage

**Install dependencies:**
```bash
pip install pandas numpy pulp scikit-learn
```

**Run the optimizer:**
```bash
# Process data and validate
python src/data_pipeline.py

# Run optimization
python src/optimizer.py

# Full pipeline with forecasting
python src/integration.py
```

**Output:**
- Optimal production schedule by plant and SKU
- Capacity utilization metrics
- Total cost and demand coverage analysis

## Technical Skills

| Category | Technologies |
|----------|-------------|
| **Optimization** | Linear Programming, PuLP, constraint formulation |
| **Data Engineering** | ETL pipelines, data validation, quality checks |
| **Python** | Pandas, NumPy, SciPy |
| **Statistics** | Forecasting (moving average, linear regression), anomaly detection |
| **Domain Knowledge** | SAP/ERP data structures (MARA, MARC, VBAK/VBAP) |

## Extensions

Potential enhancements for production deployment:
- Multi-period scheduling with inventory holding costs
- Transportation cost optimization (plant → customer routing)
- Mixed-Integer Programming for minimum batch sizes
- Scenario analysis and sensitivity testing
- Database integration (PostgreSQL/BigQuery)
- Real-time optimization with live ERP data

## License

MIT License - See LICENSE file for details
