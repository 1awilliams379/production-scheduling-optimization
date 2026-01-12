# Module 1: Linear Programming Fundamentals

## What is Linear Programming?

**Linear Programming (LP)** is a mathematical method for finding the best outcome (maximum profit, minimum cost, etc.) when you have:
- A goal you want to optimize (objective)
- Limited resources (constraints)
- Relationships that are linear (straight-line equations)

### Real-World Applications

LP is used everywhere in business and operations:

1. **Production Scheduling** (What you'll build)
   - How much of each product to make?
   - Which plant should make what?
   - Minimize cost while meeting demand

2. **Transportation/Routing**
   - How to ship products from warehouses to customers?
   - Minimize shipping costs
   - Meet delivery requirements

3. **Inventory Management**
   - How much stock to hold?
   - Balance holding costs vs stockout risk

4. **Workforce Scheduling**
   - How many workers per shift?
   - Minimize labor costs
   - Meet coverage requirements

5. **Resource Allocation**
   - How to allocate budget across projects?
   - Maximize ROI with limited budget

---

## The Three Components of Every LP Problem

### 1. Decision Variables (What are we deciding?)

These are the unknowns you're solving for. The things you have control over.

**Examples:**
- x₁ = quantity of Product A to produce
- x₂ = quantity of Product B to produce
- x[plant, material] = how much material to produce at each plant

### 2. Objective Function (What are we optimizing?)

This is your goal. What you want to maximize or minimize.

**Examples:**
- **Maximize:** Total profit = 5x₁ + 3x₂
- **Minimize:** Total cost = 100x₁ + 150x₂
- **Minimize:** Total production cost across all plants

### 3. Constraints (What limits our decisions?)

These are the rules and limitations you must follow.

**Examples:**
- Limited machine hours: 2x₁ + x₂ ≤ 100
- Must meet demand: x₁ ≥ 50
- Can't produce negative quantities: x₁ ≥ 0, x₂ ≥ 0

---

## Simple Example: Product Mix Problem

Let's walk through a complete example from start to finish.

### Business Scenario

You run a small factory that makes two products:
- **Product A**: Sells for $5 profit per unit, takes 2 hours to make
- **Product B**: Sells for $3 profit per unit, takes 1 hour to make

You have **100 hours of machine time** available this week.

**Question:** How many of each product should you make to maximize profit?

### Step 1: Identify Decision Variables

What are we deciding?
- x₁ = number of Product A to make
- x₂ = number of Product B to make

### Step 2: Define Objective Function

What do we want to maximize?
- Profit = (profit per unit A × quantity of A) + (profit per unit B × quantity of B)
- **Maximize: 5x₁ + 3x₂**

### Step 3: List Constraints

What limits us?
1. **Machine hours:** Making A uses 2 hours, making B uses 1 hour, total ≤ 100 hours
   - 2x₁ + x₂ ≤ 100

2. **Can't produce negative quantities:**
   - x₁ ≥ 0
   - x₂ ≥ 0

### Complete Formulation

```
Maximize: 5x₁ + 3x₂

Subject to:
  2x₁ + x₂ ≤ 100    (machine hours)
  x₁ ≥ 0            (non-negativity)
  x₂ ≥ 0            (non-negativity)
```

### Solution (We'll code this in Module 3)

The optimal solution is:
- x₁ = 50 (make 50 units of Product A)
- x₂ = 0 (make 0 units of Product B)
- **Maximum profit = $250**

Why? Product A gives more profit per hour ($5/2hrs = $2.50/hr) than Product B ($3/1hr = $3/hr)... wait, that's wrong! Product B is actually better per hour!

Let me recalculate:
- Product A: $5 profit / 2 hours = $2.50 per hour
- Product B: $3 profit / 1 hour = $3.00 per hour

So we should make only Product B:
- x₁ = 0, x₂ = 100
- **Maximum profit = $300**

This shows why optimization matters - it's not always obvious what the best solution is!

---

## Key Concepts

### Feasible Region

The **feasible region** is the set of all solutions that satisfy ALL constraints.

In our example:
- Any point where 2x₁ + x₂ ≤ 100 AND x₁ ≥ 0 AND x₂ ≥ 0

### Optimal Solution

The **optimal solution** is the point in the feasible region that gives the best objective value.

Key fact: **The optimal solution is always at a corner (vertex) of the feasible region.**

This is why LP solvers work - they only need to check the corners, not every possible point!

### Slack Variables

**Slack** is how much of a constraint is "left over" (unused capacity).

In our example, if we produce x₁=0, x₂=100:
- Machine hours used: 2(0) + 1(100) = 100 hours
- Slack = 100 - 100 = 0 hours (all capacity used)

If we produced x₁=10, x₂=50:
- Machine hours used: 2(10) + 1(50) = 70 hours
- Slack = 100 - 70 = 30 hours (30 hours unused)

---

## When to Use Linear Programming

### Use LP when:
✓ Decision variables are **continuous** (can be fractions: 10.5 units, 23.7 hours)
✓ Relationships are **linear** (doubling input doubles output)
✓ You have one clear objective (max profit OR min cost)
✓ Constraints are linear inequalities or equalities

### Use Mixed-Integer Programming (MIP) when:
✓ Some variables must be **integers** (can't produce 2.5 machines)
✓ Some variables are **binary** (yes/no decisions: build factory or not?)
✓ Everything else is the same as LP

### Use Nonlinear Programming when:
✓ Relationships are **not linear** (economies of scale: cost per unit decreases as volume increases)
✓ Objective or constraints have curves, exponentials, etc.

---

## Common LP Problem Types

### 1. Product Mix
- Decide how much of each product to make
- Maximize profit or minimize cost
- Subject to resource limits (machine hours, materials, labor)

### 2. Transportation
- Decide how much to ship from each source to each destination
- Minimize shipping cost
- Meet demand at destinations, respect supply limits

### 3. Blending
- Decide how to mix ingredients
- Minimize cost while meeting quality requirements
- Example: Animal feed with minimum protein/vitamin levels

### 4. Scheduling
- Decide production schedule over time
- Balance inventory costs vs production costs
- Meet demand each period

### 5. Network Flow
- Decide flows through a network (roads, pipelines, supply chains)
- Minimize cost or maximize throughput
- Respect capacity limits on each edge

---

## Interview Questions You'll Be Asked

### "Explain Linear Programming to a non-technical person"

**Good Answer:**
"Linear Programming is a way to find the best solution when you have limited resources. For example, if you run a factory with limited machine hours and need to decide how much of each product to make, LP finds the production plan that maximizes profit while staying within your constraints. It's called 'linear' because the relationships are proportional - if one unit costs $10, then 10 units cost $100."

### "When would you use LP vs. other optimization methods?"

**Good Answer:**
"I'd use Linear Programming when:
1. Variables can be continuous (fractions are okay)
2. Relationships are linear (doubling input doubles output)
3. I have clear resource constraints

I'd switch to Mixed-Integer Programming if I need whole number decisions, like 'build 3 factories, not 2.7 factories.' And I'd use heuristic methods or simulation if the problem is too complex for exact optimization, like scheduling with many real-world exceptions."

### "Walk me through how you'd formulate an optimization problem"

**Good Answer (use the 5-step process):**
"I follow a systematic process:
1. **Understand the business problem** - What's the real goal? What are the limitations?
2. **Identify decision variables** - What decisions do we control?
3. **Define the objective** - What are we maximizing or minimizing?
4. **List constraints** - What rules must we follow? What are the capacity limits?
5. **Translate to math** - Write everything as equations

For example, for production scheduling, I'd define variables for production quantity at each plant, minimize total cost, and add constraints for meeting demand and respecting plant capacity."

---

## Practice Exercise

### Problem: Farm Planning

A farmer has **100 acres** of land and wants to plant corn and wheat:
- **Corn:** $200 profit per acre, requires 2 hours labor per acre
- **Wheat:** $150 profit per acre, requires 1 hour labor per acre
- The farmer has **150 hours** of labor available

**Your Task:** Formulate this as a Linear Programming problem.

1. What are the decision variables?
2. What is the objective function?
3. What are the constraints?
4. Write the complete mathematical formulation

---

## Solution to Practice Exercise

### 1. Decision Variables
- x₁ = acres of corn to plant
- x₂ = acres of wheat to plant

### 2. Objective Function
- **Maximize:** 200x₁ + 150x₂ (total profit)

### 3. Constraints
- **Land limit:** x₁ + x₂ ≤ 100 (can't plant more than 100 acres)
- **Labor limit:** 2x₁ + x₂ ≤ 150 (can't work more than 150 hours)
- **Non-negativity:** x₁ ≥ 0, x₂ ≥ 0 (can't plant negative acres)

### 4. Complete Formulation

```
Maximize: 200x₁ + 150x₂

Subject to:
  x₁ + x₂ ≤ 100      (land limit)
  2x₁ + x₂ ≤ 150     (labor limit)
  x₁ ≥ 0             (non-negativity)
  x₂ ≥ 0             (non-negativity)
```

**Insight:** The labor constraint is tighter than the land constraint (150 labor-hours can only cover 75 acres of corn, but we have 100 acres available). This means labor is the binding constraint.

---

## What's Next?

In **Module 2: Problem Formulation**, you'll practice translating more complex business problems into mathematical formulations:
- Multi-plant production scheduling (like your data!)
- Transportation problems
- Inventory optimization

In **Module 3: PuLP Implementation**, you'll learn the Python syntax to code these models and get solutions.

---

## Key Takeaways

✓ Linear Programming finds the best solution given limited resources
✓ Every LP has 3 parts: decision variables, objective function, constraints
✓ Relationships must be linear (proportional)
✓ Use LP for continuous variables, MIP for integer decisions
✓ The optimal solution is always at a corner of the feasible region
✓ Formulation is the hardest part - translating business → math
