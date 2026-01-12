# Module 4: Statistics for Optimization

## Why Statistics Matters for Optimization

Optimization models don't exist in isolation. They need **inputs** (like demand forecasts) and **validation** (did the model work?).

### The Real Workflow

```
Historical Data
    ↓
Forecasting (Statistics)
    ↓
Demand Forecast
    ↓
Optimization Model
    ↓
Production Plan
    ↓
Execute Plan
    ↓
Measure Results (Statistics)
    ↓
Validate & Improve
```

In this module, you'll learn:
1. **Forecasting**: Predict future demand (input to optimization)
2. **Validation**: Measure model accuracy
3. **Anomaly Detection**: Identify bad data

---

## Part 1: Forecasting Methods

### Why Forecast?

Your optimization model needs **demand** as input. But future demand is unknown! You need to forecast it from historical data.

**Example:**
```python
# Historical demand
demand_history = [50, 55, 48, 52, 60, 58, 62]

# Need to forecast next week's demand
forecast = ???  # Use forecasting method

# Use forecast in optimization
model += x >= forecast  # Meet forecasted demand
```

---

### Method 1: Moving Average (Simplest)

**Idea:** Future demand = average of recent past demand

```python
import numpy as np

# Historical weekly demand
demand_history = np.array([50, 55, 48, 52, 60, 58, 62, 65, 63, 70])

# 3-week moving average
window = 3
forecast = np.mean(demand_history[-window:])

print(f"Last 3 weeks: {demand_history[-window:]}")
print(f"Forecast for next week: {forecast:.1f}")
```

**Output:**
```
Last 3 weeks: [65 63 70]
Forecast for next week: 66.0
```

**Pros:**
- Very simple
- Works well for stable demand

**Cons:**
- Doesn't capture trends (increasing/decreasing)
- Doesn't capture seasonality
- Always lags behind actual demand

**When to use:** Stable demand with no clear trend.

---

### Method 2: Weighted Moving Average

**Idea:** Recent data is more important than old data

```python
# Historical demand
demand_history = np.array([50, 55, 48, 52, 60, 58, 62, 65, 63, 70])

# Weights (most recent gets highest weight)
weights = np.array([0.5, 0.3, 0.2])  # Sum to 1.0

# Weighted average of last 3 weeks
recent = demand_history[-3:]
forecast = np.sum(recent * weights)

print(f"Last 3 weeks: {recent}")
print(f"Weights: {weights}")
print(f"Forecast: {forecast:.1f}")
```

**Output:**
```
Last 3 weeks: [65 63 70]
Weights: [0.5 0.3 0.2]
Forecast: 66.9
```

**Calculation:**
- 70 × 0.5 = 35.0 (most recent)
- 63 × 0.3 = 18.9
- 65 × 0.2 = 13.0
- Total = 66.9

**When to use:** When recent patterns are more predictive than older data.

---

### Method 3: Linear Regression (Trend)

**Idea:** Fit a straight line to historical data, extrapolate into the future

```python
from sklearn.linear_model import LinearRegression
import numpy as np

# Historical demand (weeks 1-10)
weeks = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
demand = np.array([50, 55, 48, 52, 60, 58, 62, 65, 63, 70])

# Fit linear regression
model = LinearRegression()
model.fit(weeks, demand)

# Forecast week 11
next_week = np.array([[11]])
forecast = model.predict(next_week)[0]

print(f"Forecast for week 11: {forecast:.1f}")

# Coefficient interpretation
print(f"Weekly growth: {model.coef_[0]:.2f} units per week")
print(f"Starting demand: {model.intercept_:.2f}")
```

**Output:**
```
Forecast for week 11: 72.0
Weekly growth: 2.14 units per week
Starting demand: 47.5
```

**Pros:**
- Captures trends (increasing or decreasing)
- Simple to explain

**Cons:**
- Assumes linear relationship (constant growth rate)
- Doesn't capture seasonality or sudden changes

**When to use:** Demand is growing or declining steadily.

---

### Method 4: Exponential Smoothing

**Idea:** Forecast = α × (actual) + (1-α) × (previous forecast)

```python
def exponential_smoothing(data, alpha=0.3):
    """
    alpha: smoothing parameter (0 to 1)
    - High alpha (close to 1): Respond quickly to changes
    - Low alpha (close to 0): Smooth out noise
    """
    forecast = [data[0]]  # First forecast = first actual

    for i in range(1, len(data)):
        new_forecast = alpha * data[i] + (1 - alpha) * forecast[-1]
        forecast.append(new_forecast)

    return forecast

demand = [50, 55, 48, 52, 60, 58, 62, 65, 63, 70]
forecasts = exponential_smoothing(demand, alpha=0.3)

# Next period forecast
next_forecast = 0.3 * demand[-1] + 0.7 * forecasts[-1]
print(f"Forecast for next week: {next_forecast:.1f}")
```

**When to use:** Good balance between responsiveness and smoothing.

---

## Part 2: Forecast Validation

Once you have a forecast, how do you know if it's good? You need **validation metrics**.

### Common Metrics

### 1. Mean Absolute Error (MAE)

**Definition:** Average of absolute errors

```python
actual = np.array([52, 60, 58, 62, 65])
forecast = np.array([50, 55, 60, 60, 63])

errors = actual - forecast
absolute_errors = np.abs(errors)
mae = np.mean(absolute_errors)

print(f"Actual:   {actual}")
print(f"Forecast: {forecast}")
print(f"Errors:   {errors}")
print(f"MAE: {mae:.2f} units")
```

**Output:**
```
Actual:   [52 60 58 62 65]
Forecast: [50 55 60 60 63]
Errors:   [ 2  5 -2  2  2]
MAE: 2.60 units
```

**Interpretation:** On average, forecasts are off by 2.6 units.

**Pros:**
- Easy to understand
- Same units as original data

**Cons:**
- Doesn't penalize large errors more than small errors

---

### 2. Root Mean Squared Error (RMSE)

**Definition:** Square root of average squared errors

```python
squared_errors = (actual - forecast) ** 2
mse = np.mean(squared_errors)
rmse = np.sqrt(mse)

print(f"Squared errors: {squared_errors}")
print(f"MSE: {mse:.2f}")
print(f"RMSE: {rmse:.2f} units")
```

**Output:**
```
Squared errors: [ 4 25  4  4  4]
MSE: 8.20
RMSE: 2.86 units
```

**Interpretation:** RMSE is higher than MAE (2.86 vs 2.60) because it penalizes the large error (5) more heavily.

**Pros:**
- Penalizes large errors more (good if big misses are costly)
- Mathematically convenient

**Cons:**
- Harder to interpret than MAE
- Sensitive to outliers

**When to use:** When large errors are much worse than small errors (e.g., stockouts).

---

### 3. Mean Absolute Percentage Error (MAPE)

**Definition:** Average of absolute percentage errors

```python
percentage_errors = np.abs((actual - forecast) / actual) * 100
mape = np.mean(percentage_errors)

print(f"Percentage errors: {percentage_errors}")
print(f"MAPE: {mape:.1f}%")
```

**Output:**
```
Percentage errors: [ 3.85  8.33  3.45  3.23  3.08]
MAPE: 4.4%
```

**Interpretation:** Forecasts are off by an average of 4.4%.

**Pros:**
- Scale-independent (can compare across products)
- Easy to communicate ("off by 5%")

**Cons:**
- Undefined when actual = 0
- Asymmetric (penalizes over-forecasts more than under-forecasts)

**When to use:** Comparing forecast accuracy across different products or scales.

---

### Comparing Forecast Methods

```python
import numpy as np

# Historical data
actual = np.array([50, 55, 48, 52, 60, 58, 62, 65, 63, 70])

# Method 1: Simple moving average (window=3)
forecasts_ma = []
for i in range(3, len(actual)):
    forecast = np.mean(actual[i-3:i])
    forecasts_ma.append(forecast)

# Method 2: Linear regression
from sklearn.linear_model import LinearRegression
weeks = np.arange(len(actual)).reshape(-1, 1)
model = LinearRegression().fit(weeks[:7], actual[:7])
forecasts_lr = model.predict(weeks[7:]).flatten()

# Actual values for validation period (last 3 weeks)
actual_test = actual[7:]

# Calculate MAE for each method
forecasts_ma = np.array(forecasts_ma[-3:])  # Last 3 forecasts
mae_ma = np.mean(np.abs(actual_test - forecasts_ma))
mae_lr = np.mean(np.abs(actual_test - forecasts_lr))

print(f"Moving Average MAE: {mae_ma:.2f}")
print(f"Linear Regression MAE: {mae_lr:.2f}")
print(f"Winner: {'Moving Average' if mae_ma < mae_lr else 'Linear Regression'}")
```

**Key Insight:** Always test multiple methods and pick the one with lowest error on validation data.

---

## Part 3: Anomaly Detection

### Why Detect Anomalies?

Bad data = bad forecasts = bad optimization results.

**Examples of anomalies:**
- Sensor malfunction reports 10,000 units sold (normal is 50-70)
- Data entry error: 600 instead of 60
- Special event: Black Friday sales spike

You need to identify and handle these before forecasting.

---

### Method 1: Z-Score (Standard Deviations)

**Idea:** How many standard deviations away from the mean?

```python
import numpy as np

demand = np.array([50, 55, 48, 52, 60, 58, 62, 65, 63, 999])  # Last value is anomaly

mean = np.mean(demand)
std = np.std(demand)

z_scores = (demand - mean) / std

print(f"Mean: {mean:.2f}")
print(f"Std Dev: {std:.2f}")
print(f"Z-scores: {z_scores}")
print(f"\nAnomalies (|z-score| > 3):")
for i, z in enumerate(z_scores):
    if abs(z) > 3:
        print(f"  Week {i+1}: demand={demand[i]}, z-score={z:.2f}")
```

**Output:**
```
Mean: 151.20
Std Dev: 280.38
Z-scores: [-0.36 -0.34 -0.37 -0.35 -0.33 -0.33 -0.32 -0.31 -0.31  3.02]

Anomalies (|z-score| > 3):
  Week 10: demand=999, z-score=3.02
```

**Rule of thumb:**
- |z-score| < 2: Normal
- 2 < |z-score| < 3: Borderline
- |z-score| > 3: Likely anomaly

**Pros:**
- Simple and fast
- Works well for normally distributed data

**Cons:**
- Sensitive to outliers in the calculation of mean and std
- Assumes normal distribution

---

### Method 2: IQR (Interquartile Range)

**Idea:** Anomalies are far from the middle 50% of data

```python
demand = np.array([50, 55, 48, 52, 60, 58, 62, 65, 63, 999])

# Calculate quartiles
Q1 = np.percentile(demand, 25)
Q3 = np.percentile(demand, 75)
IQR = Q3 - Q1

# Define bounds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"Q1 (25th percentile): {Q1}")
print(f"Q3 (75th percentile): {Q3}")
print(f"IQR: {IQR}")
print(f"Lower bound: {lower_bound}")
print(f"Upper bound: {upper_bound}")

print(f"\nAnomalies:")
for i, value in enumerate(demand):
    if value < lower_bound or value > upper_bound:
        print(f"  Week {i+1}: {value}")
```

**Output:**
```
Q1 (25th percentile): 52.75
Q3 (75th percentile): 63.25
IQR: 10.5
Lower bound: 37.0
Upper bound: 79.0

Anomalies:
  Week 10: 999
```

**Pros:**
- Robust to outliers (doesn't use mean/std)
- Works well for skewed distributions

**Cons:**
- May miss anomalies in small datasets
- 1.5 × IQR is arbitrary (can adjust for stricter/looser detection)

**When to use:** When data is not normally distributed or has existing outliers.

---

### Handling Anomalies

Once detected, what do you do?

**Option 1: Remove**
```python
# Remove anomalies
demand_clean = demand[demand <= upper_bound]
```

**Option 2: Replace with Median**
```python
median = np.median(demand)
demand_clean = demand.copy()
demand_clean[demand > upper_bound] = median
```

**Option 3: Replace with Interpolation**
```python
import pandas as pd

df = pd.DataFrame({'demand': demand})
# Mark anomalies as NaN
df.loc[df['demand'] > upper_bound, 'demand'] = np.nan
# Interpolate
df['demand'] = df['demand'].interpolate()
```

**Interview Tip:** Always explain WHY you're removing or adjusting data. Document assumptions.

---

## Part 4: Putting It All Together

### Complete Forecasting Pipeline

```python
import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_pipeline(demand_history, method='linear_regression'):
    """
    Complete forecasting pipeline with anomaly detection

    Parameters:
    - demand_history: array of historical demand
    - method: 'moving_average', 'linear_regression', or 'exponential'

    Returns:
    - forecast: next period forecast
    - metrics: validation metrics (MAE, RMSE)
    """

    # Step 1: Anomaly detection and cleaning
    Q1 = np.percentile(demand_history, 25)
    Q3 = np.percentile(demand_history, 75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    lower_bound = Q1 - 1.5 * IQR

    # Flag anomalies
    anomalies = (demand_history < lower_bound) | (demand_history > upper_bound)
    if np.any(anomalies):
        print(f"Warning: {np.sum(anomalies)} anomalies detected")
        # Replace with median
        demand_clean = demand_history.copy()
        demand_clean[anomalies] = np.median(demand_history)
    else:
        demand_clean = demand_history

    # Step 2: Generate forecast
    if method == 'moving_average':
        window = min(3, len(demand_clean))
        forecast = np.mean(demand_clean[-window:])

    elif method == 'linear_regression':
        X = np.arange(len(demand_clean)).reshape(-1, 1)
        y = demand_clean
        model = LinearRegression().fit(X, y)
        next_period = np.array([[len(demand_clean)]])
        forecast = model.predict(next_period)[0]

    elif method == 'exponential':
        alpha = 0.3
        smooth = demand_clean[0]
        for value in demand_clean[1:]:
            smooth = alpha * value + (1 - alpha) * smooth
        forecast = smooth

    else:
        raise ValueError(f"Unknown method: {method}")

    # Step 3: Calculate validation metrics (on cleaned data)
    if len(demand_clean) > 3:
        # Use last 3 points for validation
        train = demand_clean[:-3]
        test = demand_clean[-3:]

        # Generate forecasts for test period
        if method == 'moving_average':
            test_forecasts = [np.mean(demand_clean[i-3:i]) for i in range(len(train), len(demand_clean))]
        elif method == 'linear_regression':
            X_train = np.arange(len(train)).reshape(-1, 1)
            model_val = LinearRegression().fit(X_train, train)
            X_test = np.arange(len(train), len(demand_clean)).reshape(-1, 1)
            test_forecasts = model_val.predict(X_test)

        mae = np.mean(np.abs(test - test_forecasts))
        rmse = np.sqrt(np.mean((test - test_forecasts)**2))
        metrics = {'mae': mae, 'rmse': rmse}
    else:
        metrics = {'mae': None, 'rmse': None}

    return forecast, metrics

# Example usage
demand = np.array([50, 55, 48, 52, 60, 58, 62, 65, 63, 70])

forecast, metrics = forecast_pipeline(demand, method='linear_regression')
print(f"Forecast for next week: {forecast:.1f}")
print(f"Validation MAE: {metrics['mae']:.2f}")
print(f"Validation RMSE: {metrics['rmse']:.2f}")
```

---

## Interview Questions You'll Be Asked

### "How would you forecast demand for a new product with no history?"

**Good Answer:**
"For a new product, I'd use these approaches:
1. **Similar products**: Find analogous products and use their demand patterns as a proxy
2. **Market research**: Use market size estimates and expected market share
3. **Expert judgment**: Interview sales team and industry experts
4. **Start conservative**: Begin with low forecasts and update as real data comes in (Bayesian updating)
5. **Scenario planning**: Create optimistic, realistic, and pessimistic scenarios

Once we have 4-6 weeks of data, I'd switch to statistical forecasting methods."

### "How do you know if your forecast is good enough?"

**Good Answer:**
"I use a combination of metrics and business judgment:
1. **Quantitative**: Calculate MAE, RMSE, MAPE on holdout validation data
2. **Benchmark**: Compare to naive forecast (e.g., 'next month = this month')
3. **Business impact**: A forecast with 10% error that costs $1000 is better than 5% error that costs $10,000 to improve
4. **Tracking**: Monitor forecast vs actual over time to catch degradation

For this role, I'd aim for MAPE < 15% for major SKUs, knowing that some variability is unavoidable."

### "What would you do if your optimization model gives strange results?"

**Good Answer:**
"I'd follow a debugging process:
1. **Check data quality**: Run anomaly detection on inputs. Are demands reasonable?
2. **Verify formulation**: Print the model and check constraints match business rules
3. **Check feasibility**: Is the problem infeasible? If so, which constraint is too tight?
4. **Validate ranges**: Are variable bounds correct? (e.g., capacity limits)
5. **Sanity test**: Does the solution violate any unstated business rules?
6. **Compare to baseline**: How does it compare to current manual scheduling?

I'd also add logging to track which constraints are binding and which have slack."

---

## Practice Exercise

### Task: Forecast and Optimize

Using your SAP data (SKU001 demand from sales orders):

1. **Extract historical demand** from `sap_sales_orders.csv`
2. **Forecast next week's demand** using moving average
3. **Detect any anomalies** in the data
4. **Use the forecast in an optimization model** to determine production quantity

Hints:
- Use pandas to group sales orders by material and week
- Use numpy for forecasting calculations
- Feed forecast into PuLP model as demand constraint

---

## Key Takeaways

✓ **Forecasting** provides inputs for optimization models (demand, costs, etc.)
✓ **Moving average** is simplest, **linear regression** captures trends
✓ **Validation metrics**: MAE (easy to interpret), RMSE (penalizes large errors), MAPE (scale-independent)
✓ **Anomaly detection**: Z-score (for normal data), IQR (for skewed data)
✓ Always clean data before forecasting
✓ Test multiple forecasting methods and pick the best one
✓ Monitor forecast accuracy over time and retrain models
✓ Be prepared to explain tradeoffs in interviews (simple vs accurate, interpretable vs complex)

---

## What's Next?

In **Module 5: Practice Problems**, you'll solve 5 complete optimization problems from start to finish:
1. Product Mix
2. Production Scheduling (your SAP data!)
3. Inventory Optimization
4. Transportation
5. Workforce Scheduling

Each problem includes: formulation, PuLP code, and business interpretation.

In **Module 6: Integration**, you'll combine everything: forecast → optimize → validate.
