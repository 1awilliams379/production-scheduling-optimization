# Module 2: Problem Formulation (Business → Math)

## The Formulation Process

This is the **most important skill** for optimization work. Coding in PuLP is easy once you know the math. The hard part is translating the business problem into the right mathematical model.

### The 5-Step Process

```
1. Understand the business problem
   ↓
2. Identify decision variables (What are we deciding?)
   ↓
3. Define objective function (What are we optimizing?)
   ↓
4. List constraints (What limits our decisions?)
   ↓
5. Translate to math (Write the equations)
```

---

## Problem 1: Simple Product Mix (Beginner)

### Business Scenario

You make two products with limited resources:
- **Product A:** $5 profit per unit, takes 2 hours to produce
- **Product B:** $3 profit per unit, takes 1 hour to produce
- You have **100 hours** of production time available

**Goal:** Maximize profit

### Step 1: Understand the Business Problem

We need to decide how many units of each product to make. We're limited by total production time. We want the most profit.

### Step 2: Identify Decision Variables

What are we deciding? How many units to make.

```
x₁ = quantity of Product A to produce
x₂ = quantity of Product B to produce
```

**Interview Tip:** Always define your variables clearly with units. Not just "x₁" but "x₁ = quantity of Product A in units".

### Step 3: Define Objective Function

What are we optimizing? Total profit.

Total Profit = (profit per A) × (quantity of A) + (profit per B) × (quantity of B)

```
Maximize: 5x₁ + 3x₂
```

### Step 4: List Constraints

What limits us?
1. Production time: Each A takes 2 hours, each B takes 1 hour, total ≤ 100 hours
2. Can't make negative quantities

### Step 5: Translate to Math

```
Maximize: 5x₁ + 3x₂

Subject to:
  2x₁ + x₂ ≤ 100    (production hours)
  x₁ ≥ 0            (non-negativity)
  x₂ ≥ 0            (non-negativity)
```

**Done!** This is a complete LP formulation.

---

## Problem 2: Multi-Plant Production (Intermediate)

This is closer to your actual project. Let's use **your SAP data**.

### Business Scenario

You have:
- **3 plants:** PLANT001, PLANT002, PLANT003
- **5 materials to produce:** SKU001, SKU002, SKU003, SKU004, SKU005
- Each plant has **different costs** to produce each material
- Each plant has **limited capacity** (hours per week)
- You must **meet customer demand** for each material

**Goal:** Minimize total production cost

### Step 1: Understand the Business Problem

We need to decide how much of each material to produce at each plant. We want minimum cost while meeting all demand and respecting each plant's capacity.

### Step 2: Identify Decision Variables

What are we deciding? How much of each material to produce at each plant.

```
x[p,m] = quantity of material m to produce at plant p

Where:
  p ∈ {PLANT001, PLANT002, PLANT003}
  m ∈ {SKU001, SKU002, SKU003, SKU004, SKU005}

Total variables: 3 plants × 5 materials = 15 decision variables
```

**Examples of specific variables:**
- x[PLANT001, SKU001] = how many SKU001 to make at PLANT001
- x[PLANT002, SKU003] = how many SKU003 to make at PLANT002
- x[PLANT003, SKU005] = how many SKU005 to make at PLANT003

**Interview Tip:** For multi-dimensional problems, use indexed variables like x[plant, material]. This scales better than naming 15 individual variables.

### Step 3: Define Objective Function

What are we optimizing? Total production cost.

Total Cost = Sum of (quantity × cost) for all plant-material combinations

```
Minimize: Σ Σ cost[p,m] × x[p,m]
         p  m

Read as: "Sum over all plants p, sum over all materials m, of cost times quantity"
```

**In plain English:**
Add up the cost of producing each material at each plant.

### Step 4: List Constraints

What limits us?

**Type 1: Demand Satisfaction (one constraint per material)**
The total production of each material across all plants must meet demand.

For SKU001:
```
x[PLANT001, SKU001] + x[PLANT002, SKU001] + x[PLANT003, SKU001] ≥ demand[SKU001]
```

Generalizing for all materials:
```
Σ x[p,m] ≥ demand[m]   for all m
p

Translation: "Sum over all plants p: production of material m at plant p must be ≥ demand for material m"
```

**Why ≥ and not =?**
We use ≥ (greater than or equal) because it's okay to overproduce if it's cheaper. The optimizer will naturally avoid overproduction because it costs money (and we're minimizing cost).

**Type 2: Capacity Limits (one constraint per plant)**
Each plant has limited production hours.

For PLANT001:
```
(production_time[SKU001] × x[PLANT001, SKU001]) +
(production_time[SKU002] × x[PLANT001, SKU002]) +
(production_time[SKU003] × x[PLANT001, SKU003]) +
(production_time[SKU004] × x[PLANT001, SKU004]) +
(production_time[SKU005] × x[PLANT001, SKU005]) ≤ capacity[PLANT001]
```

Generalizing for all plants:
```
Σ production_time[m] × x[p,m] ≤ capacity[p]   for all p
m

Translation: "Sum over all materials m: hours to make material m at plant p must be ≤ plant p's capacity"
```

**Type 3: Non-negativity**
Can't produce negative quantities.

```
x[p,m] ≥ 0   for all p, m
```

### Step 5: Complete Mathematical Formulation

```
Minimize: Σ Σ cost[p,m] × x[p,m]
         p  m

Subject to:

  DEMAND CONSTRAINTS (5 constraints, one per material):
  Σ x[p, SKU001] ≥ demand[SKU001]
  p
  Σ x[p, SKU002] ≥ demand[SKU002]
  p
  Σ x[p, SKU003] ≥ demand[SKU003]
  p
  Σ x[p, SKU004] ≥ demand[SKU004]
  p
  Σ x[p, SKU005] ≥ demand[SKU005]
  p

  CAPACITY CONSTRAINTS (3 constraints, one per plant):
  Σ time[m] × x[PLANT001, m] ≤ capacity[PLANT001]
  m
  Σ time[m] × x[PLANT002, m] ≤ capacity[PLANT002]
  m
  Σ time[m] × x[PLANT003, m] ≤ capacity[PLANT003]
  m

  NON-NEGATIVITY (15 constraints, one per variable):
  x[p,m] ≥ 0   for all p, m
```

**Summary:**
- 15 decision variables
- 5 + 3 + 15 = 23 constraints total
- Minimize total cost
- Must meet demand, respect capacity

---

## Problem 3: Transportation/Routing (Advanced)

### Business Scenario

You need to ship products from warehouses to customers:
- **3 warehouses:** Each has a supply limit
- **4 customers:** Each has a demand requirement
- **Shipping costs:** Different cost to ship from each warehouse to each customer

**Goal:** Minimize total transportation cost

### Step 1: Understand the Business Problem

Decide how much to ship from each warehouse to each customer. Minimize shipping cost. Can't ship more than warehouse supply. Must meet customer demand.

### Step 2: Identify Decision Variables

```
x[i,j] = quantity shipped from warehouse i to customer j

Where:
  i ∈ {WAREHOUSE1, WAREHOUSE2, WAREHOUSE3}
  j ∈ {CUSTOMER1, CUSTOMER2, CUSTOMER3, CUSTOMER4}

Total variables: 3 × 4 = 12 decision variables
```

### Step 3: Define Objective Function

```
Minimize: Σ Σ shipping_cost[i,j] × x[i,j]
         i  j
```

### Step 4: List Constraints

**Type 1: Supply Limits (one per warehouse)**
Can't ship more than available at each warehouse.

```
Σ x[i,j] ≤ supply[i]   for all i
j

Translation: "Sum over all customers j: total shipped from warehouse i must be ≤ supply at warehouse i"
```

**Type 2: Demand Requirements (one per customer)**
Must meet each customer's demand.

```
Σ x[i,j] ≥ demand[j]   for all j
i

Translation: "Sum over all warehouses i: total received by customer j must be ≥ demand of customer j"
```

**Type 3: Non-negativity**
```
x[i,j] ≥ 0   for all i, j
```

### Step 5: Complete Formulation

```
Minimize: Σ Σ shipping_cost[i,j] × x[i,j]
         i  j

Subject to:
  Σ x[i,j] ≤ supply[i]      for all warehouses i   (3 constraints)
  j

  Σ x[i,j] ≥ demand[j]      for all customers j    (4 constraints)
  i

  x[i,j] ≥ 0                for all i, j           (12 constraints)
```

**Summary:**
- 12 decision variables
- 3 + 4 + 12 = 19 constraints total

---

## Common Formulation Patterns

### Pattern 1: "At Least" Constraints (≥)

Use when you need to **meet a minimum requirement**.

**Examples:**
- Production must meet demand: `Σ production ≥ demand`
- Must have minimum staff coverage: `Σ workers ≥ min_required`
- Portfolio must have minimum return: `Σ returns × investment ≥ target_return`

### Pattern 2: "At Most" Constraints (≤)

Use when you have **capacity limits or maximum allowances**.

**Examples:**
- Can't exceed machine hours: `Σ hours_used ≤ capacity`
- Budget limit: `Σ costs ≤ budget`
- Maximum inventory space: `Σ units × volume ≤ warehouse_space`

### Pattern 3: "Exactly" Constraints (=)

Use when something must be **exactly a value**.

**Examples:**
- Must use entire budget: `Σ spending = budget`
- Must assign each task to one person: `Σ assignments = 1` (for each task)
- Flow conservation: `inflow = outflow` (at each node in a network)

### Pattern 4: Multi-Dimensional Summation (Σ Σ)

Use when you have **nested index structures**.

**Examples:**
- Total cost across plants and materials: `Σ Σ cost[p,m] × x[p,m]`
- Total shipments across warehouses and customers: `Σ Σ ship[i,j]`

**How to read:** "Sum over i, then for each i sum over j"

---

## Interview Framework: How to Approach Any Problem

When given a business scenario in an interview:

### Step 1: Ask Clarifying Questions (30 seconds)
- "What are we trying to optimize - minimize cost or maximize profit?"
- "Are there capacity limits I should know about?"
- "Must we meet all demand or is underproduction allowed?"

### Step 2: Define Decision Variables (1 minute)
- "The decision variables are..." (write them down)
- Check: Did I capture all the decisions we need to make?

### Step 3: State the Objective (30 seconds)
- "We want to minimize total cost, which is..."
- Or: "We want to maximize profit, which is..."

### Step 4: List Constraints (2 minutes)
- Go through each resource or requirement
- "We have a capacity constraint for each plant..."
- "We have a demand constraint for each material..."
- "We have non-negativity constraints..."

### Step 5: Write the Math (1 minute)
- Write it out in mathematical notation
- Use Σ for summations
- Label each constraint type

**Total time: ~5 minutes for a complete formulation**

---

## Practice Exercises

### Exercise 1: Production Planning

A company makes 3 products using 2 machines:
- Product A: $10 profit, uses 3 hours on Machine 1, 2 hours on Machine 2
- Product B: $8 profit, uses 2 hours on Machine 1, 4 hours on Machine 2
- Product C: $12 profit, uses 4 hours on Machine 1, 1 hour on Machine 2

Machine 1 has 120 hours available, Machine 2 has 100 hours available.

**Task:** Formulate as an LP to maximize profit.

### Exercise 2: Shift Scheduling

A call center needs staff for 3 shifts:
- Morning (8am-4pm): needs 15 workers
- Afternoon (4pm-12am): needs 20 workers
- Night (12am-8am): needs 10 workers

Workers can be assigned to:
- Morning shift only: $80/day
- Afternoon shift only: $90/day
- Night shift only: $100/day
- Morning + Afternoon: $150/day
- Afternoon + Night: $170/day

**Task:** Formulate as an LP to minimize labor cost while meeting coverage requirements.

### Exercise 3: Using Your SAP Data

Using the 6 SAP tables you loaded in your data_pipeline.py:
- Materials table (15 SKUs with costs and production times)
- Plants table (3 plants with capacities)
- Sales orders table (customer demand)
- Inventory table (current stock)
- Production history (past production)
- Cost data (plant-specific costs)

**Task:** Formulate a production scheduling problem to minimize cost.

Hints:
1. Decision variables: x[plant, material] for all combinations
2. Objective: Minimize total production cost
3. Constraints:
   - Meet demand (use sales orders)
   - Respect plant capacity (use plants table)
   - Non-negativity

---

## Solutions to Practice Exercises

### Solution 1: Production Planning

**Decision Variables:**
```
x₁ = quantity of Product A
x₂ = quantity of Product B
x₃ = quantity of Product C
```

**Objective:**
```
Maximize: 10x₁ + 8x₂ + 12x₃
```

**Constraints:**
```
3x₁ + 2x₂ + 4x₃ ≤ 120    (Machine 1 hours)
2x₁ + 4x₂ + x₃ ≤ 100     (Machine 2 hours)
x₁, x₂, x₃ ≥ 0           (non-negativity)
```

### Solution 2: Shift Scheduling

**Decision Variables:**
```
x₁ = workers on morning only
x₂ = workers on afternoon only
x₃ = workers on night only
x₄ = workers on morning + afternoon
x₅ = workers on afternoon + night
```

**Objective:**
```
Minimize: 80x₁ + 90x₂ + 100x₃ + 150x₄ + 170x₅
```

**Constraints:**
```
x₁ + x₄ ≥ 15              (morning coverage)
x₂ + x₄ + x₅ ≥ 20         (afternoon coverage)
x₃ + x₅ ≥ 10              (night coverage)
x₁, x₂, x₃, x₄, x₅ ≥ 0    (non-negativity)
```

### Solution 3: SAP Data Problem

**Decision Variables:**
```
x[p,m] = quantity of material m to produce at plant p

Where p ∈ {PLANT001, PLANT002, PLANT003}
      m ∈ {SKU001, ..., SKU015}
```

**Objective:**
```
Minimize: Σ Σ cost[p,m] × x[p,m]
         p  m
```

**Constraints:**
```
Σ x[p,m] ≥ demand[m]                           for all m (15 constraints)
p

Σ production_time[m] × x[p,m] ≤ capacity[p]    for all p (3 constraints)
m

x[p,m] ≥ 0                                     for all p,m (45 constraints)
```

**Total:** 45 variables, 63 constraints

---

## What's Next?

In **Module 3: PuLP Implementation**, you'll learn the Python syntax to code these formulations:
- How to create LpProblem
- How to define LpVariable (including dictionaries of variables)
- How to write objective functions
- How to add constraints
- How to solve and read results

Get ready to turn your math into code!

---

## Key Takeaways

✓ Formulation is a 5-step process: understand, variables, objective, constraints, math
✓ Decision variables are what you're deciding (quantities, assignments, etc.)
✓ Objective function is what you're optimizing (max profit, min cost)
✓ Constraints are limits and requirements (≥ for minimums, ≤ for maximums)
✓ Use indexed variables x[i,j] for multi-dimensional problems
✓ Use Σ (summation) when adding over multiple indices
✓ Practice is key - the more problems you formulate, the faster you get
