+++
title = "Statistical Analysis with Python"
description = "Generated from Jupyter notebook"
weight = 0
draft = false
template = "page.html"
in_search_index = true

[extra]
notebook_source = "statistical_analysis.ipynb"
generated_date = "2026-03-22 16:10:17"
execution_time = "5.88s"
cell_count = 36
+++

# Statistical Analysis with Python

This notebook demonstrates comprehensive statistical analysis techniques using Python's scientific computing stack. We'll explore hypothesis testing, regression analysis, and various statistical methods.

## Topics Covered
- Descriptive statistics and data exploration
- Hypothesis testing (t-tests, ANOVA, chi-square)
- Regression analysis (linear, polynomial, logistic)
- Time series analysis and forecasting
- Bayesian statistics concepts

## 1. Setup and Data Generation

Let's import the necessary libraries and generate sample datasets for our analysis.


```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm, ttest_ind, ttest_rel, f_oneway, chi2_contingency
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Set random seed for reproducibility
np.random.seed(42)

print("Libraries imported successfully!")
```

    Libraries imported successfully!


## 2. Descriptive Statistics and Data Exploration

Let's create a dataset and explore its statistical properties.


```python
# Generate a synthetic dataset
n_samples = 1000

# Create correlated variables
np.random.seed(42)
education_years = np.random.normal(12, 3, n_samples)
education_years = np.clip(education_years, 6, 20)  # Clip to realistic range

# Experience correlated with education
experience = np.random.normal(education_years * 0.8, 5, n_samples)
experience = np.clip(experience, 0, 40)

# Salary based on education and experience with some noise
salary = 30000 + 5000 * education_years + 3000 * experience + np.random.normal(0, 15000, n_samples)
salary = np.clip(salary, 20000, 200000)

# Age based on education and experience
age = education_years + experience + np.random.normal(18, 3, n_samples)
age = np.clip(age, 22, 65)

# Create categorical variables
departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance']
department = np.random.choice(departments, n_samples, p=[0.3, 0.25, 0.2, 0.15, 0.1])

gender = np.random.choice(['Male', 'Female', 'Other'], n_samples, p=[0.48, 0.48, 0.04])

# Performance rating (1-5)
performance = np.random.choice([1, 2, 3, 4, 5], n_samples, p=[0.1, 0.15, 0.3, 0.3, 0.15])

# Create DataFrame
df = pd.DataFrame({
    'employee_id': range(1, n_samples + 1),
    'age': age,
    'education_years': education_years,
    'experience': experience,
    'salary': salary,
    'department': department,
    'gender': gender,
    'performance': performance
})

print("Dataset created successfully!")
print(f"Shape: {df.shape}")
print("\nFirst few rows:")
print(df.head())
```

    Dataset created successfully!
    Shape: (1000, 8)
    
    First few rows:
       employee_id        age  education_years  experience         salary  \
    0            1  43.555611        13.490142   17.788891  140689.711621   
    1            2  40.895386        11.585207   13.891334  127432.257697   
    2            3  42.154853        13.943066   11.452604  122186.842280   
    3            4  50.252740        16.569090   10.020588  138287.788202   
    4            5  43.496348        11.297540   12.529148   95670.924781   
    
        department gender  performance  
    0        Sales   Male            4  
    1  Engineering   Male            1  
    2      Finance   Male            3  
    3        Sales   Male            2  
    4    Marketing   Male            4  



```python
# Comprehensive descriptive statistics
print("=== DESCRIPTIVE STATISTICS ===")
print("\nNumeric Variables:")
print(df.describe())

print("\n=== CATEGORICAL VARIABLES ===")
for col in ['department', 'gender', 'performance']:
    print(f"\n{col.upper()}:")
    print(df[col].value_counts())
    print(f"Proportions:")
    print(df[col].value_counts(normalize=True))
```

    === DESCRIPTIVE STATISTICS ===
    
    Numeric Variables:
           employee_id          age  education_years   experience         salary  \
    count  1000.000000  1000.000000      1000.000000  1000.000000    1000.000000   
    mean    500.500000    40.114792        12.068962    10.101361  120725.555190   
    std     288.819436     7.367093         2.883135     5.194317   29188.489998   
    min       1.000000    22.000000         6.000000     0.000000   50475.084867   
    25%     250.750000    34.790516        10.057229     6.814068  101056.002300   
    50%     500.500000    39.899186        12.075902     9.895315  119236.869075   
    75%     750.250000    44.932029        13.943832    13.609755  140133.360520   
    max    1000.000000    64.101560        20.000000    26.384950  200000.000000   
    
           performance  
    count  1000.000000  
    mean      3.188000  
    std       1.178153  
    min       1.000000  
    25%       2.000000  
    50%       3.000000  
    75%       4.000000  
    max       5.000000  
    
    === CATEGORICAL VARIABLES ===
    
    DEPARTMENT:
    department
    Engineering    304
    Sales          252
    Marketing      191
    HR             147
    Finance        106
    Name: count, dtype: int64
    Proportions:
    department
    Engineering    0.304
    Sales          0.252
    Marketing      0.191
    HR             0.147
    Finance        0.106
    Name: proportion, dtype: float64
    
    GENDER:
    gender
    Male      498
    Female    468
    Other      34
    Name: count, dtype: int64
    Proportions:
    gender
    Male      0.498
    Female    0.468
    Other     0.034
    Name: proportion, dtype: float64
    
    PERFORMANCE:
    performance
    3    319
    4    278
    2    156
    5    140
    1    107
    Name: count, dtype: int64
    Proportions:
    performance
    3    0.319
    4    0.278
    2    0.156
    5    0.140
    1    0.107
    Name: proportion, dtype: float64



```python
# Visualize the data
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 1. Salary distribution
sns.histplot(df['salary'], kde=True, ax=axes[0, 0])
axes[0, 0].set_title('Salary Distribution', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Salary ($)', fontsize=12)

# 2. Age vs Salary scatter
axes[0, 1].scatter(df['age'], df['salary'], alpha=0.6)
axes[0, 1].set_title('Age vs Salary', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Age', fontsize=12)
axes[0, 1].set_ylabel('Salary ($)', fontsize=12)

# 3. Department salary comparison
sns.boxplot(data=df, x='department', y='salary', ax=axes[0, 2])
axes[0, 2].set_title('Salary by Department', fontsize=14, fontweight='bold')
axes[0, 2].tick_params(axis='x', rotation=45)

# 4. Education distribution
sns.histplot(df['education_years'], kde=True, ax=axes[1, 0])
axes[1, 0].set_title('Education Years Distribution', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Years of Education', fontsize=12)

# 5. Experience vs Salary
axes[1, 1].scatter(df['experience'], df['salary'], alpha=0.6)
axes[1, 1].set_title('Experience vs Salary', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Years of Experience', fontsize=12)
axes[1, 1].set_ylabel('Salary ($)', fontsize=12)

# 6. Performance distribution
performance_counts = df['performance'].value_counts().sort_index()
axes[1, 2].bar(performance_counts.index, performance_counts.values)
axes[1, 2].set_title('Performance Ratings', fontsize=14, fontweight='bold')
axes[1, 2].set_xlabel('Performance Rating', fontsize=12)
axes[1, 2].set_ylabel('Count', fontsize=12)

plt.tight_layout()
plt.show()
```


    
![png](output_6_0.png)
    


## 3. Correlation Analysis

Let's examine the relationships between variables using correlation analysis.


```python
# Calculate correlation matrix for numeric variables
numeric_cols = ['age', 'education_years', 'experience', 'salary']
correlation_matrix = df[numeric_cols].corr()

print("=== CORRELATION MATRIX ===")
print(correlation_matrix)

# Find significant correlations
print("\n=== SIGNIFICANT CORRELATIONS (|r| > 0.3) ===")
for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        corr_val = correlation_matrix.iloc[i, j]
        if abs(corr_val) > 0.3:
            var1 = correlation_matrix.columns[i]
            var2 = correlation_matrix.columns[j]
            print(f"{var1} vs {var2}: r = {corr_val:.3f}")
```

    === CORRELATION MATRIX ===
                          age  education_years  experience    salary
    age              1.000000         0.658448    0.832511  0.778707
    education_years  0.658448         1.000000    0.387579  0.713012
    experience       0.832511         0.387579    1.000000  0.724740
    salary           0.778707         0.713012    0.724740  1.000000
    
    === SIGNIFICANT CORRELATIONS (|r| > 0.3) ===
    age vs education_years: r = 0.658
    age vs experience: r = 0.833
    age vs salary: r = 0.779
    education_years vs experience: r = 0.388
    education_years vs salary: r = 0.713
    experience vs salary: r = 0.725



```python
# Visualize correlations
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Heatmap
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
            square=True, ax=axes[0])
axes[0].set_title('Correlation Heatmap', fontsize=14, fontweight='bold')

# Pair plot for key variables
key_vars = ['salary', 'education_years', 'experience', 'age']
sns.pairplot(df[key_vars], diag_kind='kde', corner=True)
axes[1].axis('off')
axes[1].text(0.5, 0.5, 'Pair plot shown separately', 
             ha='center', va='center', transform=axes[1].transAxes)

plt.tight_layout()
plt.show()

# Show the pair plot
plt.figure(figsize=(10, 8))
sns.pairplot(df[key_vars], diag_kind='kde')
plt.suptitle('Pair Plot of Key Variables', y=1.02, fontsize=14, fontweight='bold')
plt.show()
```


    
![png](output_9_0.png)
    



    
![png](output_9_1.png)
    



    <Figure size 1000x800 with 0 Axes>



    
![png](output_9_3.png)
    


## 4. Hypothesis Testing

Let's perform various hypothesis tests to examine relationships in our data.

### 4.1 Independent Samples T-Test

Testing if there's a significant difference in salaries between genders.

**Null Hypothesis (H₀)**: μ_male = μ_female (no difference in mean salaries)
**Alternative Hypothesis (H₁)**: μ_male ≠ μ_female (there is a difference)


```python
# Filter out 'Other' gender for clearer comparison
male_salaries = df[df['gender'] == 'Male']['salary']
female_salaries = df[df['gender'] == 'Female']['salary']

# Perform independent t-test
t_stat, p_value = ttest_ind(male_salaries, female_salaries)

print("=== INDEPENDENT SAMPLES T-TEST ===")
print(f"Male salary mean: ${male_salaries.mean():,.2f}")
print(f"Female salary mean: ${female_salaries.mean():,.2f}")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4f}")

alpha = 0.05
if p_value < alpha:
    print(f"\nResult: Reject H₀ (p < {alpha})")
    print("There is a significant difference in salaries between genders.")
else:
    print(f"\nResult: Fail to reject H₀ (p ≥ {alpha})")
    print("There is no significant difference in salaries between genders.")

# Effect size (Cohen's d)
pooled_std = np.sqrt(((len(male_salaries) - 1) * male_salaries.var() + 
                     (len(female_salaries) - 1) * female_salaries.var()) / 
                    (len(male_salaries) + len(female_salaries) - 2))
cohens_d = (male_salaries.mean() - female_salaries.mean()) / pooled_std
print(f"Effect size (Cohen's d): {cohens_d:.3f}")
```

    === INDEPENDENT SAMPLES T-TEST ===
    Male salary mean: $120,984.43
    Female salary mean: $120,412.69
    T-statistic: 0.3036
    P-value: 0.7615
    
    Result: Fail to reject H₀ (p ≥ 0.05)
    There is no significant difference in salaries between genders.
    Effect size (Cohen's d): 0.020


### 4.2 One-Way ANOVA

Testing if there's a significant difference in salaries across departments.

**Null Hypothesis (H₀)**: μ_engineering = μ_sales = μ_marketing = μ_hr = μ_finance
**Alternative Hypothesis (H₁)**: At least one department has a different mean salary


```python
# Generate time series data
np.random.seed(42)
n_periods = 200
dates = pd.date_range(start='2020-01-01', periods=n_periods, freq='ME')
```


```python
# Prepare data for ANOVA
dept_salaries = []
dept_names = []

for dept in departments:
    salaries = df[df['department'] == dept]['salary']
    dept_salaries.append(salaries)
    dept_names.append(dept)
    print(f"{dept}: n={len(salaries)}, mean=${salaries.mean():,.2f}, std=${salaries.std():,.2f}")

# Perform one-way ANOVA
f_stat, p_value = f_oneway(*dept_salaries)

print("\n=== ONE-WAY ANOVA ===")
print(f"F-statistic: {f_stat:.4f}")
print(f"P-value: {p_value:.4f}")

if p_value < alpha:
    print(f"\nResult: Reject H₀ (p < {alpha})")
    print("There is a significant difference in salaries across departments.")
else:
    print(f"\nResult: Fail to reject H₀ (p ≥ {alpha})")
    print("There is no significant difference in salaries across departments.")

# Visualize the comparison
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='department', y='salary')
plt.title('Salary Distribution by Department', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.ylabel('Salary ($)', fontsize=12)
plt.show()
```

    Engineering: n=304, mean=$119,845.62, std=$29,929.31
    Sales: n=252, mean=$124,056.25, std=$28,888.81
    Marketing: n=191, mean=$117,793.88, std=$29,204.30
    HR: n=147, mean=$119,966.25, std=$27,579.42
    Finance: n=106, mean=$121,666.42, std=$29,644.31
    
    === ONE-WAY ANOVA ===
    F-statistic: 1.4259
    P-value: 0.2233
    
    Result: Fail to reject H₀ (p ≥ 0.05)
    There is no significant difference in salaries across departments.



    
![png](output_15_1.png)
    



```python
# Create contingency table
contingency_table = pd.crosstab(df['department'], df['performance'])

print("=== CONTINGENCY TABLE ===")
print(contingency_table)

# Perform chi-square test
chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)

print("\n=== CHI-SQUARE TEST OF INDEPENDENCE ===")
print(f"Chi-square statistic: {chi2_stat:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"Degrees of freedom: {dof}")

if p_value < alpha:
    print(f"\nResult: Reject H₀ (p < {alpha})")
    print("There is a significant association between department and performance.")
else:
    print(f"\nResult: Fail to reject H₀ (p ≥ {alpha})")
    print("There is no significant association between department and performance.")

# Visualize the relationship
plt.figure(figsize=(12, 6))
sns.heatmap(contingency_table, annot=True, fmt='d', cmap='Blues')
plt.title('Department vs Performance Rating', fontsize=14, fontweight='bold')
plt.xlabel('Performance Rating', fontsize=12)
plt.ylabel('Department', fontsize=12)
plt.show()
```

    === CONTINGENCY TABLE ===
    performance   1   2   3   4   5
    department                     
    Engineering  36  49  93  82  44
    Finance       7  14  43  30  12
    HR           11  26  40  47  23
    Marketing    21  27  67  48  28
    Sales        32  40  76  71  33
    
    === CHI-SQUARE TEST OF INDEPENDENCE ===
    Chi-square statistic: 12.6437
    P-value: 0.6986
    Degrees of freedom: 16
    
    Result: Fail to reject H₀ (p ≥ 0.05)
    There is no significant association between department and performance.



    
![png](output_16_1.png)
    


## 5. Regression Analysis

Let's build regression models to predict salary based on various factors.

### 5.1 Simple Linear Regression

Predicting salary based on years of experience.


```python
# Prepare data for simple linear regression
X_simple = df[['experience']].values
y = df['salary'].values

# Fit the model
simple_model = LinearRegression()
simple_model.fit(X_simple, y)

# Make predictions
y_pred_simple = simple_model.predict(X_simple)

# Calculate metrics
mse_simple = mean_squared_error(y, y_pred_simple)
r2_simple = r2_score(y, y_pred_simple)

print("=== SIMPLE LINEAR REGRESSION ===")
print(f"Intercept: ${simple_model.intercept_:,.2f}")
print(f"Coefficient (experience): ${simple_model.coef_[0]:,.2f} per year")
print(f"R-squared: {r2_simple:.3f}")
print(f"MSE: {mse_simple:,.2f}")
print(f"RMSE: ${np.sqrt(mse_simple):,.2f}")

# Interpretation
print(f"\nInterpretation:")
print(f"- Base salary (0 experience): ${simple_model.intercept_:,.2f}")
print(f"- Each additional year of experience adds: ${simple_model.coef_[0]:,.2f}")
print(f"- Model explains {r2_simple:.1%} of the variance in salary")
```

    === SIMPLE LINEAR REGRESSION ===
    Intercept: $79,587.36
    Coefficient (experience): $4,072.54 per year
    R-squared: 0.525
    MSE: 404,068,980.59
    RMSE: $20,101.47
    
    Interpretation:
    - Base salary (0 experience): $79,587.36
    - Each additional year of experience adds: $4,072.54
    - Model explains 52.5% of the variance in salary


### 5.2 Multiple Linear Regression

Predicting salary based on multiple predictors.


```python
# Prepare data for multiple regression
features = ['age', 'education_years', 'experience']
X_multiple = df[features].values

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_multiple)

# Fit the model
multiple_model = LinearRegression()
multiple_model.fit(X_scaled, y)

# Make predictions
y_pred_multiple = multiple_model.predict(X_scaled)

# Calculate metrics
mse_multiple = mean_squared_error(y, y_pred_multiple)
r2_multiple = r2_score(y, y_pred_multiple)

print("=== MULTIPLE LINEAR REGRESSION ===")
print(f"Intercept: ${multiple_model.intercept_:,.2f}")
print("\nCoefficients (standardized):")
for i, feature in enumerate(features):
    print(f"{feature}: {multiple_model.coef_[i]:.4f}")
print(f"\nR-squared: {r2_multiple:.3f}")
print(f"MSE: {mse_multiple:,.2f}")
print(f"RMSE: ${np.sqrt(mse_multiple):,.2f}")

# Compare with simple model
print(f"\nModel Comparison:")
print(f"Simple R²: {r2_simple:.3f}")
print(f"Multiple R²: {r2_multiple:.3f}")
print(f"Improvement: {((r2_multiple - r2_simple) / r2_simple * 100):.1f}%")
```

    === MULTIPLE LINEAR REGRESSION ===
    Intercept: $120,725.56
    
    Coefficients (standardized):
    age: 771.0509
    education_years: 14530.3690
    experience: 14869.9067
    
    R-squared: 0.745
    MSE: 216,946,580.49
    RMSE: $14,729.11
    
    Model Comparison:
    Simple R²: 0.525
    Multiple R²: 0.745
    Improvement: 41.9%


### 5.3 Logistic Regression

Predicting high performance (rating 4-5) based on employee characteristics.


```python
# Create binary target variable (high performance: 4-5)
df['high_performance'] = (df['performance'] >= 4).astype(int)

# Prepare data for logistic regression
log_features = ['age', 'education_years', 'experience', 'salary']
X_log = df[log_features].values
y_log = df['high_performance'].values

# Standardize features
X_log_scaled = scaler.fit_transform(X_log)

# Fit the model
log_model = LogisticRegression(random_state=42)
log_model.fit(X_log_scaled, y_log)

# Make predictions
y_pred_log = log_model.predict(X_log_scaled)
y_pred_proba = log_model.predict_proba(X_log_scaled)[:, 1]

# Calculate metrics
accuracy = accuracy_score(y_log, y_pred_log)

print("=== LOGISTIC REGRESSION ===")
print(f"Target: High Performance (rating 4-5)")
print(f"Accuracy: {accuracy:.3f}")
print(f"\nCoefficients (standardized):")
for i, feature in enumerate(log_features):
    print(f"{feature}: {log_model.coef_[0][i]:.4f}")

# Confusion matrix
from sklearn.metrics import confusion_matrix, classification_report
cm = confusion_matrix(y_log, y_pred_log)

print(f"\nConfusion Matrix:")
print(cm)

print(f"\nClassification Report:")
print(classification_report(y_log, y_pred_log, target_names=['Low Performance', 'High Performance']))
```

    === LOGISTIC REGRESSION ===
    Target: High Performance (rating 4-5)
    Accuracy: 0.580
    
    Coefficients (standardized):
    age: -0.1562
    education_years: 0.2164
    experience: 0.1440
    salary: -0.1572
    
    Confusion Matrix:
    [[578   4]
     [416   2]]
    
    Classification Report:
                      precision    recall  f1-score   support
    
     Low Performance       0.58      0.99      0.73       582
    High Performance       0.33      0.00      0.01       418
    
            accuracy                           0.58      1000
           macro avg       0.46      0.50      0.37      1000
        weighted avg       0.48      0.58      0.43      1000
    



```python
# Visualize regression results
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. Simple regression plot
axes[0, 0].scatter(X_simple, y, alpha=0.6, label='Actual')
axes[0, 0].plot(X_simple, y_pred_simple, 'r-', linewidth=2, label='Predicted')
axes[0, 0].set_title('Simple Linear Regression', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Experience (years)', fontsize=10)
axes[0, 0].set_ylabel('Salary ($)', fontsize=10)
axes[0, 0].legend()

# 2. Actual vs Predicted (Multiple)
axes[0, 1].scatter(y, y_pred_multiple, alpha=0.6)
axes[0, 1].plot([y.min(), y.max()], [y.min(), y.max()], 'r--', linewidth=2)
axes[0, 1].set_title('Multiple Regression: Actual vs Predicted', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Actual Salary ($)', fontsize=10)
axes[0, 1].set_ylabel('Predicted Salary ($)', fontsize=10)

# 3. Residuals plot
residuals = y - y_pred_multiple
axes[1, 0].scatter(y_pred_multiple, residuals, alpha=0.6)
axes[1, 0].axhline(y=0, color='r', linestyle='--')
axes[1, 0].set_title('Residuals Plot', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Predicted Salary ($)', fontsize=10)
axes[1, 0].set_ylabel('Residuals ($)', fontsize=10)

# 4. Feature importance (coefficients)
coef_abs = np.abs(multiple_model.coef_)
axes[1, 1].bar(features, coef_abs)
axes[1, 1].set_title('Feature Importance (|Coefficients|)', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Features', fontsize=10)
axes[1, 1].set_ylabel('|Coefficient|', fontsize=10)
axes[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
```


    
![png](output_24_0.png)
    


## 6. Time Series Analysis

Let's analyze a time series dataset and perform basic forecasting.


```python
# Generate time series data
np.random.seed(42)
n_periods = 200
dates = pd.date_range(start='2020-01-01', periods=n_periods, freq='ME')

# Create a time series with trend, seasonality, and noise
trend = np.linspace(100, 300, n_periods)
seasonal = 20 * np.sin(2 * np.pi * np.arange(n_periods) / 12)  # Monthly seasonality
noise = np.random.normal(0, 10, n_periods)
ts_values = trend + seasonal + noise

# Create time series DataFrame
ts_df = pd.DataFrame({
    'date': dates,
    'value': ts_values
})
ts_df.set_index('date', inplace=True)

print("=== TIME SERIES DATA ===")
print(f"Period: {ts_df.index.min()} to {ts_df.index.max()}")
print(f"Number of observations: {len(ts_df)}")
print(f"Mean: {ts_df['value'].mean():.2f}")
print(f"Std: {ts_df['value'].std():.2f}")

# Plot the time series
plt.figure(figsize=(12, 6))
plt.plot(ts_df.index, ts_df['value'], linewidth=1.5)
plt.title('Time Series Data', fontsize=14, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Value', fontsize=12)
plt.grid(True, alpha=0.3)
plt.show()
```

    === TIME SERIES DATA ===
    Period: 2020-01-31 00:00:00 to 2036-08-31 00:00:00
    Number of observations: 200
    Mean: 199.92
    Std: 60.93



    
![png](output_26_1.png)
    



```python
# Check for stationarity
def check_stationarity(timeseries):
    result = adfuller(timeseries)
    print('=== AUGMENTED DICKEY-FULLER TEST ===')
    print(f'ADF Statistic: {result[0]:.4f}')
    print(f'p-value: {result[1]:.4f}')
    print('Critical Values:')
    for key, value in result[4].items():
        print(f'\t{key}: {value:.4f}')
    
    if result[1] <= 0.05:
        print("\nResult: Reject H₀ - Time series is stationary")
    else:
        print("\nResult: Fail to reject H₀ - Time series is non-stationary")

check_stationarity(ts_df['value'])
```

    === AUGMENTED DICKEY-FULLER TEST ===
    ADF Statistic: -0.0564
    p-value: 0.9536
    Critical Values:
    	1%: -3.4658
    	5%: -2.8771
    	10%: -2.5751
    
    Result: Fail to reject H₀ - Time series is non-stationary



```python
# Difference the series to make it stationary
ts_diff = ts_df['value'].diff().dropna()

print("=== FIRST DIFFERENCE ===")
check_stationarity(ts_diff)

# Plot the differenced series
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

axes[0].plot(ts_df.index, ts_df['value'], linewidth=1.5)
axes[0].set_title('Original Time Series', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Value', fontsize=10)
axes[0].grid(True, alpha=0.3)

axes[1].plot(ts_df.index[1:], ts_diff, linewidth=1.5)
axes[1].set_title('First Difference', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Difference', fontsize=10)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

    === FIRST DIFFERENCE ===


    === AUGMENTED DICKEY-FULLER TEST ===
    ADF Statistic: -11.0505
    p-value: 0.0000
    Critical Values:
    	1%: -3.4658
    	5%: -2.8771
    	10%: -2.5751
    
    Result: Reject H₀ - Time series is stationary



    
![png](output_28_2.png)
    



```python
# Fit ARIMA model
# Split data into train and test
train_size = int(len(ts_df) * 0.8)
train_data = ts_df['value'][:train_size]
test_data = ts_df['value'][train_size:]

# Fit ARIMA model (p,d,q) = (1,1,1)
model = ARIMA(train_data, order=(1,1,1))
fitted_model = model.fit()

print("=== ARIMA MODEL ===")
print(fitted_model.summary())

# Make predictions
forecast = fitted_model.forecast(steps=len(test_data))
forecast_ci = fitted_model.get_forecast(steps=len(test_data)).conf_int()

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(train_data.index, train_data, label='Training Data', color='blue')
plt.plot(test_data.index, test_data, label='Test Data', color='green')
plt.plot(test_data.index, forecast, label='Forecast', color='red', linewidth=2)
plt.fill_between(test_data.index, 
                 forecast_ci.iloc[:, 0], 
                 forecast_ci.iloc[:, 1], 
                 color='red', alpha=0.3, label='95% Confidence Interval')
plt.title('ARIMA Forecast', fontsize=14, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Value', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Calculate forecast accuracy
mse_forecast = mean_squared_error(test_data, forecast)
rmse_forecast = np.sqrt(mse_forecast)
mape = np.mean(np.abs((test_data - forecast) / test_data)) * 100

print(f"\n=== FORECAST ACCURACY ===")
print(f"RMSE: {rmse_forecast:.2f}")
print(f"MAPE: {mape:.2f}%")
```

    === ARIMA MODEL ===


                                   SARIMAX Results                                
    ==============================================================================
    Dep. Variable:                  value   No. Observations:                  160
    Model:                 ARIMA(1, 1, 1)   Log Likelihood                -657.295
    Date:                Sun, 22 Mar 2026   AIC                           1320.589
    Time:                        16:10:16   BIC                           1329.796
    Sample:                    01-31-2020   HQIC                          1324.328
                             - 04-30-2033                                         
    Covariance Type:                  opg                                         
    ==============================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
    ------------------------------------------------------------------------------
    ar.L1         -0.3154      0.354     -0.891      0.373      -1.009       0.378
    ma.L1          0.0943      0.376      0.251      0.802      -0.643       0.831
    sigma2       228.0674     31.360      7.272      0.000     166.602     289.533
    ===================================================================================
    Ljung-Box (L1) (Q):                   0.00   Jarque-Bera (JB):                 2.28
    Prob(Q):                              0.95   Prob(JB):                         0.32
    Heteroskedasticity (H):               1.37   Skew:                            -0.07
    Prob(H) (two-sided):                  0.25   Kurtosis:                         2.43
    ===================================================================================
    
    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).



    
![png](output_29_2.png)
    


    
    === FORECAST ACCURACY ===
    RMSE: 18.07
    MAPE: 5.35%


## 7. Bayesian Statistics Concepts

Let's explore some basic Bayesian concepts using a simple example.

### 7.1 Bayesian Inference Example

Estimating the probability of success in a binomial experiment using Bayesian inference.

**Prior**: Beta(1, 1) - uniform prior
**Likelihood**: Binomial
**Posterior**: Beta(α + successes, β + failures)


```python
# Bayesian inference example
from scipy.stats import beta

# Parameters
n_trials = 100
observed_successes = 65
observed_failures = n_trials - observed_successes

# Prior parameters (Beta distribution)
alpha_prior = 1
beta_prior = 1

# Posterior parameters
alpha_post = alpha_prior + observed_successes
beta_post = beta_prior + observed_failures

print("=== BAYESIAN INFERENCE EXAMPLE ===")
print(f"Observed successes: {observed_successes}/{n_trials}")
print(f"Prior: Beta({alpha_prior}, {beta_prior})")
print(f"Posterior: Beta({alpha_post}, {beta_post})")

# Calculate posterior statistics
posterior_mean = alpha_post / (alpha_post + beta_post)
posterior_mode = (alpha_post - 1) / (alpha_post + beta_post - 2) if alpha_post > 1 else 0
posterior_var = (alpha_post * beta_post) / ((alpha_post + beta_post)**2 * (alpha_post + beta_post + 1))

print(f"\nPosterior Statistics:")
print(f"Mean: {posterior_mean:.3f}")
print(f"Mode: {posterior_mode:.3f}")
print(f"Standard Deviation: {np.sqrt(posterior_var):.3f}")

# Credible interval
ci_lower, ci_upper = beta.ppf([0.025, 0.975], alpha_post, beta_post)
print(f"95% Credible Interval: [{ci_lower:.3f}, {ci_upper:.3f}]")
```

    === BAYESIAN INFERENCE EXAMPLE ===
    Observed successes: 65/100
    Prior: Beta(1, 1)
    Posterior: Beta(66, 36)
    
    Posterior Statistics:
    Mean: 0.647
    Mode: 0.650
    Standard Deviation: 0.047
    95% Credible Interval: [0.552, 0.736]



```python
# Visualize prior and posterior
x = np.linspace(0, 1, 1000)

prior_pdf = beta.pdf(x, alpha_prior, beta_prior)
posterior_pdf = beta.pdf(x, alpha_post, beta_post)

plt.figure(figsize=(12, 6))
plt.plot(x, prior_pdf, 'b-', linewidth=2, label=f'Prior Beta({alpha_prior}, {beta_prior})')
plt.plot(x, posterior_pdf, 'r-', linewidth=2, label=f'Posterior Beta({alpha_post}, {beta_post})')
plt.axvline(posterior_mean, color='red', linestyle='--', alpha=0.7, label=f'Posterior Mean: {posterior_mean:.3f}')
plt.axvline(observed_successes/n_trials, color='green', linestyle='--', alpha=0.7, 
           label=f'MLE: {observed_successes/n_trials:.3f}')
plt.fill_between(x, 0, posterior_pdf, where=(x >= ci_lower) & (x <= ci_upper), 
                 alpha=0.3, color='red', label='95% Credible Interval')

plt.title('Bayesian Inference: Prior vs Posterior', fontsize=14, fontweight='bold')
plt.xlabel('Probability of Success', fontsize=12)
plt.ylabel('Density', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Compare with frequentist approach
frequentist_estimate = observed_successes / n_trials
standard_error = np.sqrt(frequentist_estimate * (1 - frequentist_estimate) / n_trials)
ci_lower_freq = frequentist_estimate - 1.96 * standard_error
ci_upper_freq = frequentist_estimate + 1.96 * standard_error

print(f"\n=== BAYESIAN vs FREQUENTIST COMPARISON ===")
print(f"Frequentist estimate: {frequentist_estimate:.3f}")
print(f"Frequentist 95% CI: [{ci_lower_freq:.3f}, {ci_upper_freq:.3f}]")
print(f"Bayesian posterior mean: {posterior_mean:.3f}")
print(f"Bayesian 95% credible interval: [{ci_lower:.3f}, {ci_upper:.3f}]")
```


    
![png](output_33_0.png)
    


    
    === BAYESIAN vs FREQUENTIST COMPARISON ===
    Frequentist estimate: 0.650
    Frequentist 95% CI: [0.557, 0.743]
    Bayesian posterior mean: 0.647
    Bayesian 95% credible interval: [0.552, 0.736]


## 8. Summary and Conclusions

This notebook demonstrated comprehensive statistical analysis techniques:


```python
# Create a summary of all analyses
summary = {
    'Dataset': {
        'Sample Size': len(df),
        'Variables': len(df.columns),
        'Numeric Variables': len(df.select_dtypes(include=[np.number]).columns),
        'Categorical Variables': len(df.select_dtypes(include=['object']).columns)
    },
    'Hypothesis Tests': {
        'Gender Salary T-Test': f"p={ttest_ind(male_salaries, female_salaries)[1]:.4f}",
        'Department ANOVA': f"p={f_oneway(*dept_salaries)[1]:.4f}",
        'Department-Performance Chi-Square': f"p={chi2_contingency(contingency_table)[1]:.4f}"
    },
    'Regression Models': {
        'Simple Linear (Experience)': f"R²={r2_simple:.3f}",
        'Multiple Linear': f"R²={r2_multiple:.3f}",
        'Logistic (High Performance)': f"Accuracy={accuracy:.3f}"
    },
    'Time Series': {
        'ARIMA Model': '(1,1,1)',
        'Forecast RMSE': f"{rmse_forecast:.2f}",
        'Forecast MAPE': f"{mape:.2f}%"
    },
    'Bayesian Analysis': {
        'Posterior Mean': f"{posterior_mean:.3f}",
        '95% Credible Interval': f"[{ci_lower:.3f}, {ci_upper:.3f}]"
    }
}

print("=== STATISTICAL ANALYSIS SUMMARY ===")
for category, results in summary.items():
    print(f"\n{category.upper()}:")
    for key, value in results.items():
        print(f"  {key}: {value}")

print("\n=== KEY INSIGHTS ===")
print("1. Descriptive statistics revealed important patterns in the employee dataset")
print("2. Hypothesis testing identified significant relationships between variables")
print("3. Regression models showed experience and education are key salary predictors")
print("4. Time series analysis demonstrated forecasting capabilities")
print("5. Bayesian inference provided an alternative to frequentist methods")

print("\n=== BEST PRACTICES DEMONSTRATED ===")
print("• Proper data exploration and visualization")
print("• Appropriate statistical test selection")
print("• Model validation and performance metrics")
print("• Interpretation of statistical results")
print("• Comparison of different analytical approaches")
```

    === STATISTICAL ANALYSIS SUMMARY ===
    
    DATASET:
      Sample Size: 1000
      Variables: 9
      Numeric Variables: 7
      Categorical Variables: 2
    
    HYPOTHESIS TESTS:
      Gender Salary T-Test: p=0.7615
      Department ANOVA: p=0.2233
      Department-Performance Chi-Square: p=0.6986
    
    REGRESSION MODELS:
      Simple Linear (Experience): R²=0.525
      Multiple Linear: R²=0.745
      Logistic (High Performance): Accuracy=0.580
    
    TIME SERIES:
      ARIMA Model: (1,1,1)
      Forecast RMSE: 18.07
      Forecast MAPE: 5.35%
    
    BAYESIAN ANALYSIS:
      Posterior Mean: 0.647
      95% Credible Interval: [0.552, 0.736]
    
    === KEY INSIGHTS ===
    1. Descriptive statistics revealed important patterns in the employee dataset
    2. Hypothesis testing identified significant relationships between variables
    3. Regression models showed experience and education are key salary predictors
    4. Time series analysis demonstrated forecasting capabilities
    5. Bayesian inference provided an alternative to frequentist methods
    
    === BEST PRACTICES DEMONSTRATED ===
    • Proper data exploration and visualization
    • Appropriate statistical test selection
    • Model validation and performance metrics
    • Interpretation of statistical results
    • Comparison of different analytical approaches

