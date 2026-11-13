import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

# 1. Load the scored portfolio
portfolio = pd.read_csv("UCI_Credit_Card.csv")

# 2. Hypothesis Test (Welch's T-Test for Utilization Velocity)
defaulted = portfolio[portfolio['default_next_month'] == 1]['utilization_velocity_6m']
non_defaulted = portfolio[portfolio['default_next_month'] == 0]['utilization_velocity_6m']
t_stat, p_val = stats.ttest_ind(defaulted, non_defaulted, equal_var=False)

print("--- T-Test: Utilization Velocity by Default Status ---")
print(f"T-statistic: {t_stat:.4f}, P-value: {p_val:.4e}\n")

# 3. Model Calibration & Decile Lift Table
portfolio['pd_decile'] = pd.qcut(portfolio['prob_default_pd'], 10, labels=False) + 1
calibration_summary = portfolio.groupby('pd_decile').agg(
    total_accounts=('client_id', 'count'),
    avg_predicted_pd=('prob_default_pd', 'mean'),
    actual_default_rate=('default_next_month', 'mean'),
    total_ead=('exposure_at_default_ead', 'sum'),
    total_expected_loss=('expected_loss_el', 'sum')
).reset_index().sort_values(by='pd_decile', ascending=False)

print("--- Model Calibration & Decile Lift Table ---")
print(calibration_summary.round(4))

# Export validation report for Power BI
calibration_summary.to_csv('python_model_validation_report.csv', index=False)
print("Validation report saved successfully!")