# Module 3: PuLP Implementation (Coding)

## Introduction to PuLP

**PuLP** is a Python library for Linear Programming. It lets you:
- Define optimization problems in Python
- Solve them using powerful solvers (CBC, GLPK, Gurobi, CPLEX)
- Read the optimal solution

**Why PuLP?**
- Easy to learn (simpler than Pyomo or Gurobi)
- Free and open-source
- Includes a solver (CBC) so no extra setup
- Used in industry

---

## Basic PuLP Workflow

Every PuLP program follows these steps:

```python
from pulp import *

# Step 1: Create a model
model = LpProblem("My_Problem", LpMinimize)  # or LpMaximize

# Step 2: Define decision variables
x = LpVariable("x", lowBound=0)  # x ≥ 0

# Step 3: Set the objective function
model += 5*x + 3*y, "Objective"

# Step 4: Add constraints
model += 2*x + y <= 100, "Capacity_Constraint"

# Step 5: Solve
model.solve()

# Step 6: Get results
print(f"Status: {LpStatus[model.status]}")
print(f"x = {x.varValue}")
print(f"Objective = {value(model.objective)}")
```

Let's break down each step with examples.

---

## Step 1: Create a Model

```python
from pulp import *

# For minimization problems
model = LpProblem("Production_Cost_Minimization", LpMinimize)

# For maximization problems
model = LpProblem("Profit_Maximization", LpMaximize)
```

**Parameters:**
- First argument: Name of your problem (use underscores, no spaces)
- Second argument: `LpMinimize` or `LpMaximize`

---

## Step 2: Define Decision Variables

### Simple Variables

```python
# Variable with no bounds (can be any value)
x = LpVariable("x")

# Variable with lower bound (x ≥ 0)
x = LpVariable("x", lowBound=0)

# Variable with upper bound (x ≤ 100)
x = LpVariable("x", upBound=100)

# Variable with both bounds (0 ≤ x ≤ 100)
x = LpVariable("x", lowBound=0, upBound=100)

# Integer variable (must be whole number)
x = LpVariable("x", lowBound=0, cat='Integer')

# Binary variable (must be 0 or 1)
x = LpVariable("x", cat='Binary')
```

**Parameters:**
- `"x"`: Variable name (shows up in solution output)
- `lowBound`: Minimum value (default: no limit)
- `upBound`: Maximum value (default: no limit)
- `cat`: Category - `'Continuous'` (default), `'Integer'`, or `'Binary'`

### Multiple Variables

```python
# Option 1: Define individually
x1 = LpVariable("x1", lowBound=0)
x2 = LpVariable("x2", lowBound=0)
x3 = LpVariable("x3", lowBound=0)

# Option 2: Use a list comprehension
x = [LpVariable(f"x{i}", lowBound=0) for i in range(3)]
# Access as: x[0], x[1], x[2]

# Option 3: Use LpVariable.dicts (best for large problems)
products = ["A", "B", "C"]
x = LpVariable.dicts("Production", products, lowBound=0)
# Access as: x["A"], x["B"], x["C"]
```

### Multi-Dimensional Variables

For problems like production scheduling with plants and materials:

```python
# Method 1: Dictionary with tuple keys
plants = ["PLANT001", "PLANT002", "PLANT003"]
materials = ["SKU001", "SKU002", "SKU003", "SKU004", "SKU005"]

x = {}
for plant in plants:
    for material in materials:
        var_name = f"x_{plant}_{material}"
        x[(plant, material)] = LpVariable(var_name, lowBound=0)

# Access as: x[("PLANT001", "SKU001")]
```

```python
# Method 2: LpVariable.dicts with tuples
x = LpVariable.dicts(
    "Production",
    [(p, m) for p in plants for m in materials],
    lowBound=0
)

# Access as: x[("PLANT001", "SKU001")]
```

**Interview Tip:** Use `LpVariable.dicts` for cleaner code when you have many variables.

---

## Step 3: Set the Objective Function

```python
# Simple objective
model += 5*x + 3*y

# With a name (optional, helps with debugging)
model += 5*x + 3*y, "Total_Profit"

# Using lpSum for many variables
products = ["A", "B", "C"]
profit = {"A": 5, "B": 3, "C": 7}
x = LpVariable.dicts("Production", products, lowBound=0)

model += lpSum([profit[p] * x[p] for p in products]), "Total_Profit"
```

**Key Function: lpSum**
- Use `lpSum` instead of Python's `sum()` for better performance
- Syntax: `lpSum([expression for item in list])`

**Example with multi-dimensional variables:**
```python
plants = ["PLANT001", "PLANT002", "PLANT003"]
materials = ["SKU001", "SKU002", "SKU003"]

# Cost data
cost = {
    ("PLANT001", "SKU001"): 100,
    ("PLANT001", "SKU002"): 150,
    # ... more costs
}

# Decision variables
x = LpVariable.dicts(
    "Production",
    [(p, m) for p in plants for m in materials],
    lowBound=0
)

# Objective: Minimize total cost
model += lpSum([cost[(p, m)] * x[(p, m)]
                for p in plants
                for m in materials]), "Total_Cost"
```

---

## Step 4: Add Constraints

### Simple Constraints

```python
# Less than or equal (≤)
model += 2*x + y <= 100, "Capacity_Constraint"

# Greater than or equal (≥)
model += x >= 50, "Minimum_Production"

# Equality (=)
model += x + y == 100, "Exact_Total"
```

**Second argument:** Constraint name (optional but recommended for debugging)

### Multiple Constraints

```python
# Add constraints in a loop
materials = ["SKU001", "SKU002", "SKU003"]
demand = {"SKU001": 50, "SKU002": 30, "SKU003": 75}

for m in materials:
    model += x[m] >= demand[m], f"Demand_{m}"
```

### Constraints with lpSum

**Pattern 1: Sum over one dimension**

```python
# Example: Total production at PLANT001 must not exceed capacity

plants = ["PLANT001", "PLANT002", "PLANT003"]
materials = ["SKU001", "SKU002", "SKU003"]
capacity = {"PLANT001": 100, "PLANT002": 120, "PLANT003": 150}
production_time = {"SKU001": 2, "SKU002": 3, "SKU003": 1.5}

x = LpVariable.dicts(
    "Production",
    [(p, m) for p in plants for m in materials],
    lowBound=0
)

for plant in plants:
    model += (
        lpSum([production_time[m] * x[(plant, m)] for m in materials])
        <= capacity[plant],
        f"Capacity_{plant}"
    )
```

**What's happening:**
- For each plant, sum the hours used across all materials
- Hours used = production time × quantity
- Total hours must be ≤ plant capacity

**Pattern 2: Sum over a different dimension**

```python
# Example: Must meet demand for each material across all plants

demand = {"SKU001": 50, "SKU002": 30, "SKU003": 75}

for material in materials:
    model += (
        lpSum([x[(p, material)] for p in plants])
        >= demand[material],
        f"Demand_{material}"
    )
```

**What's happening:**
- For each material, sum production across all plants
- Total production must be ≥ demand

---

## Step 5: Solve the Model

```python
# Solve using default solver (CBC)
model.solve()

# Solve with a specific solver
model.solve(GLPK(msg=0))  # GLPK solver, no output
model.solve(PULP_CBC_CMD(msg=0))  # CBC solver, no output

# Solve with solver output (for debugging)
model.solve(PULP_CBC_CMD(msg=1))
```

**Common Solvers:**
- `PULP_CBC_CMD()`: Default, free, included with PuLP
- `GLPK()`: Free, open-source
- `GUROBI()`: Commercial, very fast (requires license)
- `CPLEX()`: Commercial, very fast (requires license)

---

## Step 6: Get Results

### Check Solution Status

```python
status = LpStatus[model.status]
print(f"Status: {status}")
```

**Possible statuses:**
- `"Optimal"`: Found the best solution
- `"Infeasible"`: No solution exists (constraints are contradictory)
- `"Unbounded"`: Objective can go to infinity (missing constraints)
- `"Not Solved"`: Solver failed or timed out

### Get Variable Values

```python
# Simple variables
print(f"x = {x.varValue}")
print(f"y = {y.varValue}")

# Variables in a dictionary
for product in products:
    print(f"Production of {product}: {x[product].varValue}")

# Multi-dimensional variables
for plant in plants:
    for material in materials:
        qty = x[(plant, material)].varValue
        if qty > 0:  # Only print non-zero values
            print(f"Produce {qty} of {material} at {plant}")
```

### Get Objective Value

```python
# Method 1
print(f"Total Cost: ${value(model.objective):.2f}")

# Method 2
print(f"Total Cost: ${model.objective.value():.2f}")
```

### Get Slack/Shadow Prices (Advanced)

```python
# Slack: how much of a constraint is unused
for name, constraint in model.constraints.items():
    print(f"{name}: slack = {constraint.slack}")

# Shadow price: how much objective would improve if constraint loosened by 1 unit
for name, constraint in model.constraints.items():
    print(f"{name}: shadow price = {constraint.pi}")
```

---

## Complete Example 1: Simple Product Mix

Let's solve the problem from Module 2:
- Product A: $5 profit, 2 hours
- Product B: $3 profit, 1 hour
- 100 hours available

```python
from pulp import *

# Step 1: Create model
model = LpProblem("Product_Mix", LpMaximize)

# Step 2: Define variables
x_A = LpVariable("Product_A", lowBound=0)
x_B = LpVariable("Product_B", lowBound=0)

# Step 3: Set objective
model += 5*x_A + 3*x_B, "Total_Profit"

# Step 4: Add constraints
model += 2*x_A + x_B <= 100, "Production_Hours"

# Step 5: Solve
model.solve()

# Step 6: Get results
print(f"Status: {LpStatus[model.status]}")
print(f"Product A: {x_A.varValue} units")
print(f"Product B: {x_B.varValue} units")
print(f"Total Profit: ${value(model.objective):.2f}")
```

**Output:**
```
Status: Optimal
Product A: 0.0 units
Product B: 100.0 units
Total Profit: $300.00
```

**Interpretation:** Make only Product B (it's more profitable per hour).

---

## Complete Example 2: Multi-Plant Production

Now let's use your SAP data structure:

```python
from pulp import *

# Data (from your data_pipeline.py)
plants = ["PLANT001", "PLANT002", "PLANT003"]
materials = ["SKU001", "SKU002", "SKU003", "SKU004", "SKU005"]

# Plant capacities (hours per week)
capacity = {
    "PLANT001": 320,
    "PLANT002": 280,
    "PLANT003": 400
}

# Production time (hours per unit)
production_time = {
    "SKU001": 2.5,
    "SKU002": 3.0,
    "SKU003": 1.5,
    "SKU004": 2.0,
    "SKU005": 1.8
}

# Demand (units)
demand = {
    "SKU001": 73,
    "SKU002": 33,
    "SKU003": 115,
    "SKU004": 40,
    "SKU005": 65
}

# Production costs ($ per unit)
cost = {
    ("PLANT001", "SKU001"): 450,
    ("PLANT001", "SKU002"): 650,
    ("PLANT001", "SKU003"): 280,
    ("PLANT001", "SKU004"): 310,
    ("PLANT001", "SKU005"): 195,
    ("PLANT002", "SKU001"): 470,
    ("PLANT002", "SKU002"): 680,
    ("PLANT002", "SKU003"): 265,
    ("PLANT002", "SKU004"): 295,
    ("PLANT002", "SKU005"): 210,
    ("PLANT003", "SKU001"): 430,
    ("PLANT003", "SKU002"): 620,
    ("PLANT003", "SKU003"): 295,
    ("PLANT003", "SKU004"): 325,
    ("PLANT003", "SKU005"): 180,
}

# Step 1: Create model
model = LpProblem("Production_Scheduling", LpMinimize)

# Step 2: Define variables
x = LpVariable.dicts(
    "Production",
    [(p, m) for p in plants for m in materials],
    lowBound=0
)

# Step 3: Objective - minimize total cost
model += lpSum([cost[(p, m)] * x[(p, m)]
                for p in plants
                for m in materials]), "Total_Cost"

# Step 4a: Demand constraints (one per material)
for m in materials:
    model += (
        lpSum([x[(p, m)] for p in plants]) >= demand[m],
        f"Demand_{m}"
    )

# Step 4b: Capacity constraints (one per plant)
for p in plants:
    model += (
        lpSum([production_time[m] * x[(p, m)] for m in materials])
        <= capacity[p],
        f"Capacity_{p}"
    )

# Step 5: Solve
status = model.solve()

# Step 6: Display results
print("=" * 50)
print("OPTIMAL PRODUCTION SCHEDULE")
print("=" * 50)
print(f"\nStatus: {LpStatus[model.status]}")
print(f"Total Cost: ${value(model.objective):,.2f}\n")

for plant in plants:
    print(f"\n{plant}:")
    plant_total = 0
    for material in materials:
        qty = x[(plant, material)].varValue
        if qty > 0:
            print(f"  {material}: {qty:.1f} units")
            plant_total += qty
    print(f"  Plant Total: {plant_total:.1f} units")

# Check demand satisfaction
print("\n" + "=" * 50)
print("DEMAND VERIFICATION")
print("=" * 50)
for m in materials:
    total_produced = sum(x[(p, m)].varValue for p in plants)
    print(f"{m}: Demand={demand[m]}, Produced={total_produced:.1f}")

# Check capacity utilization
print("\n" + "=" * 50)
print("CAPACITY UTILIZATION")
print("=" * 50)
for p in plants:
    hours_used = sum(production_time[m] * x[(p, m)].varValue for m in materials)
    utilization = (hours_used / capacity[p]) * 100
    print(f"{p}: {hours_used:.1f}/{capacity[p]} hours ({utilization:.1f}% utilized)")
```

---

## Common PuLP Patterns

### Pattern 1: Dictionary of Variables

```python
# Instead of x1, x2, x3, x4, x5...
products = ["A", "B", "C", "D", "E"]
x = LpVariable.dicts("Production", products, lowBound=0)

# Access: x["A"], x["B"], etc.
```

### Pattern 2: lpSum for Objective

```python
# Instead of: model += profit["A"]*x["A"] + profit["B"]*x["B"] + ...
model += lpSum([profit[p] * x[p] for p in products])
```

### Pattern 3: lpSum for Constraints

```python
# Sum over one dimension
model += lpSum([x[(plant, material)] for plant in plants]) >= demand[material]

# Sum over both dimensions
model += lpSum([x[(p, m)] for p in plants for m in materials]) >= total_demand
```

### Pattern 4: Conditional Constraints

```python
# Only add constraint if condition is met
for plant in plants:
    if plant_is_operational[plant]:
        model += lpSum([x[(plant, m)] for m in materials]) <= capacity[plant]
```

### Pattern 5: Filtering Results

```python
# Only print non-zero production
for p in plants:
    for m in materials:
        qty = x[(p, m)].varValue
        if qty > 0.01:  # Small threshold to handle floating point precision
            print(f"{p}, {m}: {qty:.2f}")
```

---

## Debugging Tips

### Problem: Infeasible

```python
if LpStatus[model.status] == "Infeasible":
    print("Problem is infeasible!")
    print("Check your constraints - they may be contradictory")
    print("Common issues:")
    print("- Demand exceeds total capacity")
    print("- Upper bound < lower bound")
    print("- Two constraints that can't both be satisfied")
```

**How to debug:**
1. Relax constraints one by one to find which is causing infeasibility
2. Check your data (capacities, demands)
3. Add slack variables to identify bottlenecks

### Problem: Unbounded

```python
if LpStatus[model.status] == "Unbounded":
    print("Problem is unbounded!")
    print("Objective can go to infinity")
    print("You're missing constraints")
```

**Common cause:** Maximizing profit without capacity limits.

### Problem: Wrong Results

1. **Print the model** to verify formulation:
   ```python
   print(model)
   ```

2. **Check variable values:**
   ```python
   for v in model.variables():
       print(f"{v.name} = {v.varValue}")
   ```

3. **Check constraints:**
   ```python
   for name, c in model.constraints.items():
       print(f"{name}: {c}")
   ```

---

## Practice Coding Exercise

Using the formulation from Module 2, Exercise 1 (Production Planning), implement it in PuLP.

**Reminder:**
- Product A: $10 profit, 3 hours on Machine 1, 2 hours on Machine 2
- Product B: $8 profit, 2 hours on Machine 1, 4 hours on Machine 2
- Product C: $12 profit, 4 hours on Machine 1, 1 hour on Machine 2
- Machine 1: 120 hours available
- Machine 2: 100 hours available

### Your Task

1. Create a file called `production_planning_exercise.py`
2. Implement the LP model in PuLP
3. Solve and print results
4. Answer: How much of each product should you make?

### Solution

```python
from pulp import *

# Data
products = ["A", "B", "C"]
profit = {"A": 10, "B": 8, "C": 12}
machine1_hours = {"A": 3, "B": 2, "C": 4}
machine2_hours = {"A": 2, "B": 4, "C": 1}
capacity = {"Machine1": 120, "Machine2": 100}

# Model
model = LpProblem("Production_Planning", LpMaximize)

# Variables
x = LpVariable.dicts("Production", products, lowBound=0)

# Objective
model += lpSum([profit[p] * x[p] for p in products]), "Total_Profit"

# Constraints
model += lpSum([machine1_hours[p] * x[p] for p in products]) <= capacity["Machine1"], "Machine1_Hours"
model += lpSum([machine2_hours[p] * x[p] for p in products]) <= capacity["Machine2"], "Machine2_Hours"

# Solve
model.solve()

# Results
print(f"Status: {LpStatus[model.status]}")
for p in products:
    print(f"Product {p}: {x[p].varValue:.2f} units")
print(f"Total Profit: ${value(model.objective):.2f}")
```

---

## What's Next?

In **Module 4: Statistics for Optimization**, you'll learn:
- Forecasting demand (input to optimization)
- Validating model accuracy
- Anomaly detection

In **Module 5: Practice Problems**, you'll solve 5 complete optimization problems end-to-end.

---

## Key Takeaways

✓ PuLP workflow: Create model → Define variables → Set objective → Add constraints → Solve → Get results
✓ Use `LpVariable.dicts` for many variables
✓ Use `lpSum` instead of `sum()` for performance
✓ Constraints use `<=`, `>=`, or `==`
✓ Always check solution status before reading results
✓ Filter results with `if qty > 0` to ignore zero values
✓ Print the model (`print(model)`) to debug formulations
✓ Infeasible = constraints contradict, Unbounded = missing constraints
