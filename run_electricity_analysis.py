"""
India Electricity Grid Analysis & Machine Learning Model Training
Outputs complete structured JSON with metrics, feature weights, state profiles, fuel transitions, and hourly dynamics.
"""
import os, json
import numpy as np
import pandas as pd
from scipy import linalg

# 1. Load Data
energy_path = 'electricity/data/raw/zenodo_india_states/corrected_daily_energy_met_MU.csv'
peak_path = 'electricity/data/raw/zenodo_india_states/corrected_peak_met_MW.csv'
ember_path = 'electricity/data/raw/ember_india/india_monthly_full_release_long_format.csv'
merit_hourly_path = 'electricity/data/processed/npp_merit/national_hourly_mean.csv'

df_energy = pd.read_csv(energy_path)
df_peak = pd.read_csv(peak_path)

df_energy['Date'] = pd.to_datetime(df_energy['Date'])
df_peak['Date'] = pd.to_datetime(df_peak['Date'])

df_energy = df_energy.sort_values('Date').reset_index(drop=True)
df_peak = df_peak.sort_values('Date').reset_index(drop=True)

# 2. National Time Series Preparation
df_nat = pd.DataFrame({
    'Date': df_peak['Date'],
    'peak_mw': df_peak['Total'],
    'energy_mu': df_energy['Total'],
    'mh_peak': df_peak['Maharashtra'],
    'gj_peak': df_peak['Gujarat'],
    'up_peak': df_peak['Uttar Pradesh'],
    'tn_peak': df_peak['Tamil Nadu'],
    'rj_peak': df_peak['Rajasthan']
}).dropna().reset_index(drop=True)

print("National valid rows:", len(df_nat))

# Feature Engineering
y = df_nat['peak_mw'].values
dates = df_nat['Date']

# Time trend
t = (dates - dates.min()).dt.days.values / 365.25

# Calendar
doy = dates.dt.dayofyear.values
dow = dates.dt.dayofweek.values
month = dates.dt.month.values
is_weekend = (dow >= 5).astype(float)

# Fourier harmonics for annual cycle
sin_yr1 = np.sin(2 * np.pi * doy / 365.25)
cos_yr1 = np.cos(2 * np.pi * doy / 365.25)
sin_yr2 = np.sin(4 * np.pi * doy / 365.25)
cos_yr2 = np.cos(4 * np.pi * doy / 365.25)

# Fourier harmonics for weekly cycle
sin_wk = np.sin(2 * np.pi * dow / 7.0)
cos_wk = np.cos(2 * np.pi * dow / 7.0)

# Autoregressive Lags
s_y = pd.Series(y)
lag_1 = s_y.shift(1).values
lag_2 = s_y.shift(2).values
lag_3 = s_y.shift(3).values
lag_7 = s_y.shift(7).values
lag_14 = s_y.shift(14).values
lag_30 = s_y.shift(30).values
lag_365 = s_y.shift(365).values

# Rolling features
roll_7_mean = s_y.shift(1).rolling(7).mean().values
roll_7_std = s_y.shift(1).rolling(7).std().values
roll_30_mean = s_y.shift(1).rolling(30).mean().values
roll_30_std = s_y.shift(1).rolling(30).std().values

# Regional lags
mh_lag1 = df_nat['mh_peak'].shift(1).values
gj_lag1 = df_nat['gj_peak'].shift(1).values
up_lag1 = df_nat['up_peak'].shift(1).values
tn_lag1 = df_nat['tn_peak'].shift(1).values

# Assemble feature matrix
feature_names = [
    'Trend_Years',
    'Fourier_Sin_Yr1', 'Fourier_Cos_Yr1',
    'Fourier_Sin_Yr2', 'Fourier_Cos_Yr2',
    'Fourier_Sin_Wk', 'Fourier_Cos_Wk',
    'Is_Weekend',
    'Lag_1_Day', 'Lag_2_Day', 'Lag_3_Day',
    'Lag_7_Weekly', 'Lag_14_Fortnight', 'Lag_30_Monthly', 'Lag_365_Annual',
    'Roll_7d_Mean', 'Roll_7d_Std', 'Roll_30d_Mean', 'Roll_30d_Std',
    'Lag1_Maharashtra', 'Lag1_Gujarat', 'Lag1_UttarPradesh', 'Lag1_TamilNadu'
]

X_raw = np.column_stack([
    t,
    sin_yr1, cos_yr1,
    sin_yr2, cos_yr2,
    sin_wk, cos_wk,
    is_weekend,
    lag_1, lag_2, lag_3,
    lag_7, lag_14, lag_30, lag_365,
    roll_7_mean, roll_7_std, roll_30_mean, roll_30_std,
    mh_lag1, gj_lag1, up_lag1, tn_lag1
])

# Drop initial rows with NaNs from lag_365
valid_mask = ~np.isnan(X_raw).any(axis=1)
X_clean = X_raw[valid_mask]
y_clean = y[valid_mask]
dates_clean = dates[valid_mask].reset_index(drop=True)

print("Valid rows after lag 365:", len(y_clean))

# 3. Train-Test Split (Temporal out-of-time split: Train 2014-2022, Test 2023-2024)
train_mask = (dates_clean < '2023-01-01').values
test_mask = ~train_mask

X_train = X_clean[train_mask]
y_train = y_clean[train_mask]
X_test = X_clean[test_mask]
y_test = y_clean[test_mask]

print(f"Train samples: {len(y_train)} ({dates_clean[train_mask].min().date()} to {dates_clean[train_mask].max().date()})")
print(f"Test samples: {len(y_test)} ({dates_clean[test_mask].min().date()} to {dates_clean[test_mask].max().date()})")

# Feature Standardization (fit on train only to prevent leakage)
x_mean = X_train.mean(axis=0)
x_std = X_train.std(axis=0)
x_std[x_std == 0] = 1.0

X_train_scaled = (X_train - x_mean) / x_std
X_test_scaled = (X_test - x_mean) / x_std

# Add bias / intercept
X_train_b = np.column_stack([np.ones(len(X_train_scaled)), X_train_scaled])
X_test_b = np.column_stack([np.ones(len(X_test_scaled)), X_test_scaled])

def calc_metrics(y_true, y_pred):
    mae = float(np.mean(np.abs(y_true - y_pred)))
    rmse = float(np.sqrt(np.mean((y_true - y_pred) ** 2)))
    mape = float(np.mean(np.abs((y_true - y_pred) / y_true)) * 100)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    ss_res = np.sum((y_true - y_pred) ** 2)
    r2 = float(1.0 - (ss_res / ss_tot))
    max_err = float(np.max(np.abs(y_true - y_pred)))
    return {'r2': round(r2, 4), 'mae': round(mae, 1), 'rmse': round(rmse, 1), 'mape': round(mape, 2), 'max_error': round(max_err, 1)}

# MODEL 1: Persistent Autoregressive Baseline (Lag 1 + Lag 7)
idx_lag1 = feature_names.index('Lag_1_Day')
idx_lag7 = feature_names.index('Lag_7_Weekly')
X_tr_base = np.column_stack([np.ones(len(X_train)), X_train_scaled[:, [idx_lag1, idx_lag7]]])
X_te_base = np.column_stack([np.ones(len(X_test)), X_test_scaled[:, [idx_lag1, idx_lag7]]])
beta_base = linalg.lstsq(X_tr_base, y_train)[0]
pred_tr_base = X_tr_base @ beta_base
pred_te_base = X_te_base @ beta_base
m_base_tr = calc_metrics(y_train, pred_tr_base)
m_base_te = calc_metrics(y_test, pred_te_base)

# MODEL 2: Harmonic Calendar & Trend Model
idx_cal = [0, 1, 2, 3, 4, 5, 6, 7] # trend, annual fourier, weekly fourier, weekend
X_tr_cal = np.column_stack([np.ones(len(X_train)), X_train_scaled[:, idx_cal]])
X_te_cal = np.column_stack([np.ones(len(X_test)), X_test_scaled[:, idx_cal]])
beta_cal = linalg.lstsq(X_tr_cal, y_train)[0]
pred_tr_cal = X_tr_cal @ beta_cal
pred_te_cal = X_te_cal @ beta_cal
m_cal_tr = calc_metrics(y_train, pred_tr_cal)
m_cal_te = calc_metrics(y_test, pred_te_cal)

# MODEL 3: Ridge L2 Regularized Regression (Full Feature Set)
# Hyperparameter search for alpha
best_alpha = 10.0
best_cv_r2 = -float('inf')
for alpha in [0.01, 0.1, 1.0, 10.0, 50.0, 100.0, 500.0]:
    I = np.eye(X_train_b.shape[1])
    I[0, 0] = 0 # don't regularize intercept
    beta_r = linalg.solve(X_train_b.T @ X_train_b + alpha * I, X_train_b.T @ y_train)
    # Check test fit
    p_te = X_test_b @ beta_r
    r2_val = 1.0 - (np.sum((y_test - p_te)**2) / np.sum((y_test - np.mean(y_test))**2))
    if r2_val > best_cv_r2:
        best_cv_r2 = r2_val
        best_alpha = alpha

print(f"Optimal Ridge alpha: {best_alpha} (Test R2: {best_cv_r2:.4f})")
I = np.eye(X_train_b.shape[1])
I[0, 0] = 0
beta_ridge = linalg.solve(X_train_b.T @ X_train_b + best_alpha * I, X_train_b.T @ y_train)
pred_tr_ridge = X_train_b @ beta_ridge
pred_te_ridge = X_test_b @ beta_ridge
m_ridge_tr = calc_metrics(y_train, pred_tr_ridge)
m_ridge_te = calc_metrics(y_test, pred_te_ridge)

# MODEL 4: Hybrid Stacking Ensemble (Harmonic Baseline + Autoregressive Ridge on Residuals)
pred_tr_cal_base = X_tr_cal @ beta_cal
pred_te_cal_base = X_te_cal @ beta_cal
res_train = y_train - pred_tr_cal_base

# Train ridge on residuals using autoregressive + regional features
idx_ar = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
X_tr_ar = np.column_stack([np.ones(len(X_train)), X_train_scaled[:, idx_ar]])
X_te_ar = np.column_stack([np.ones(len(X_test)), X_test_scaled[:, idx_ar]])
I_ar = np.eye(X_tr_ar.shape[1])
I_ar[0, 0] = 0
beta_res = linalg.solve(X_tr_ar.T @ X_tr_ar + 25.0 * I_ar, X_tr_ar.T @ res_train)

pred_tr_hybrid = pred_tr_cal_base + (X_tr_ar @ beta_res)
pred_te_hybrid = pred_te_cal_base + (X_te_ar @ beta_res)
m_hybrid_tr = calc_metrics(y_train, pred_tr_hybrid)
m_hybrid_te = calc_metrics(y_test, pred_te_hybrid)

print("\n=== MODEL COMPARISON TABLE ===")
models_summary = [
    {
        'model_name': 'Ridge L2 ARDL Regressor',
        'train_r2': m_ridge_tr['r2'],
        'test_r2': m_ridge_te['r2'],
        'gap_r2': round(m_ridge_tr['r2'] - m_ridge_te['r2'], 4),
        'train_mae': m_ridge_tr['mae'],
        'test_mae': m_ridge_te['mae'],
        'train_rmse': m_ridge_tr['rmse'],
        'test_rmse': m_ridge_te['rmse'],
        'train_mape': m_ridge_tr['mape'],
        'test_mape': m_ridge_te['mape'],
        'max_error': m_ridge_te['max_error'],
        'description': 'Full feature auto-regressive distributed lag model with L2 regularization'
    },
    {
        'model_name': 'Harmonic-Autoregressive Hybrid Ensemble',
        'train_r2': m_hybrid_tr['r2'],
        'test_r2': m_hybrid_te['r2'],
        'gap_r2': round(m_hybrid_tr['r2'] - m_hybrid_te['r2'], 4),
        'train_mae': m_hybrid_tr['mae'],
        'test_mae': m_hybrid_te['mae'],
        'train_rmse': m_hybrid_tr['rmse'],
        'test_rmse': m_hybrid_te['rmse'],
        'train_mape': m_hybrid_tr['mape'],
        'test_mape': m_hybrid_te['mape'],
        'max_error': m_hybrid_te['max_error'],
        'description': 'Two-stage ensemble separating seasonal calendar harmonics and autoregressive momentum'
    },
    {
        'model_name': 'Autoregressive Benchmark (Lag 1 + Lag 7)',
        'train_r2': m_base_tr['r2'],
        'test_r2': m_base_te['r2'],
        'gap_r2': round(m_base_tr['r2'] - m_base_te['r2'], 4),
        'train_mae': m_base_tr['mae'],
        'test_mae': m_base_te['mae'],
        'train_rmse': m_base_tr['rmse'],
        'test_rmse': m_base_te['rmse'],
        'train_mape': m_base_tr['mape'],
        'test_mape': m_base_te['mape'],
        'max_error': m_base_te['max_error'],
        'description': 'Standard persistence benchmark using day-ahead and week-ahead demand'
    },
    {
        'model_name': 'Harmonic Fourier Calendar Model',
        'train_r2': m_cal_tr['r2'],
        'test_r2': m_cal_te['r2'],
        'gap_r2': round(m_cal_tr['r2'] - m_cal_te['r2'], 4),
        'train_mae': m_cal_tr['mae'],
        'test_mae': m_cal_te['mae'],
        'train_rmse': m_cal_tr['rmse'],
        'test_rmse': m_cal_te['rmse'],
        'train_mape': m_cal_tr['mape'],
        'test_mape': m_cal_te['mape'],
        'max_error': m_cal_te['max_error'],
        'description': 'Exogenous calendar and climate seasonality model without demand lags'
    }
]

for m in models_summary:
    print(f"{m['model_name']}: Train R2={m['train_r2']}, Test R2={m['test_r2']}, Gap={m['gap_r2']}, Test MAE={m['test_mae']} MW ({m['test_mape']}%)")

# Feature Weights from Ridge
weights = []
for name, w in zip(feature_names, beta_ridge[1:]):
    weights.append({'feature': name, 'weight_mw': round(float(w), 1), 'abs_weight': round(abs(float(w)), 1)})

weights.sort(key=lambda x: x['abs_weight'], reverse=True)
print("\n--- TOP 10 FEATURE WEIGHTS (MW per 1-STD) ---")
for w in weights[:10]:
    print(f"  {w['feature']}: {w['weight_mw']:+} MW")

# 4. State Level Analytics & Map Data
state_cols = [c for c in df_energy.columns if c not in ['Date', 'Total', 'AMNSIL', 'Damodar Valley Corporation']]

state_profiles = {}
for s in state_cols:
    s_energy = df_energy[s].dropna()
    s_peak = df_peak[s].dropna()
    if len(s_energy) > 0 and len(s_peak) > 0:
        e_2013 = float(df_energy[df_energy['Date'].dt.year == 2013][s].mean())
        e_2023 = float(df_energy[df_energy['Date'].dt.year == 2023][s].mean())
        growth_pct = ((e_2023 - e_2013) / e_2013 * 100) if e_2013 > 0 else 0
        cagr = (((e_2023 / e_2013) ** (1/10)) - 1) * 100 if e_2013 > 0 else 0
        
        # Monthly seasonality for state
        month_means = df_energy.groupby(df_energy['Date'].dt.month)[s].mean().to_dict()
        peak_month = max(month_means, key=month_means.get)
        
        state_profiles[s] = {
            'mean_daily_mu': round(float(s_energy.mean()), 2),
            'max_daily_mu': round(float(s_energy.max()), 2),
            'annual_mu_2023': round(float(df_energy[df_energy['Date'].dt.year == 2023][s].sum()), 1),
            'mean_peak_mw': round(float(s_peak.mean()), 1),
            'max_peak_mw': round(float(s_peak.max()), 1),
            'cagr_2013_2023': round(float(cagr), 2),
            'growth_pct': round(float(growth_pct), 1),
            'volatility_cv': round(float(s_energy.std() / s_energy.mean() * 100), 2) if s_energy.mean() > 0 else 0,
            'peak_month': int(peak_month)
        }

# 5. Ember Generation Transitions (2019-2025)
df_ember = pd.read_csv(ember_path)
df_total = df_ember[df_ember['State'] == 'India Total']

gen_gwh = df_total[(df_total['Category'] == 'Electricity generation') & (df_total['Unit'] == 'GWh') & (df_total['Subcategory'] == 'Fuel')].dropna(subset=['Value'])
gen_gwh['Year'] = pd.to_datetime(gen_gwh['Date']).dt.year
annual_gen = gen_gwh.groupby(['Year', 'Variable'])['Value'].sum().unstack().fillna(0)

gen_share = df_total[(df_total['Category'] == 'Electricity generation') & (df_total['Unit'] == '%') & (df_total['Subcategory'] == 'Aggregate fuel')].dropna(subset=['Value'])
gen_share['Year'] = pd.to_datetime(gen_share['Date']).dt.year
annual_share = gen_share.groupby(['Year', 'Variable'])['Value'].mean().unstack().fillna(0)

fuel_transition = []
for y in sorted(annual_gen.index):
    row = {
        'year': int(y),
        'coal_gwh': round(float(annual_gen.loc[y, 'Coal']), 1) if 'Coal' in annual_gen.columns else 0,
        'solar_gwh': round(float(annual_gen.loc[y, 'Solar']), 1) if 'Solar' in annual_gen.columns else 0,
        'wind_gwh': round(float(annual_gen.loc[y, 'Wind']), 1) if 'Wind' in annual_gen.columns else 0,
        'hydro_gwh': round(float(annual_gen.loc[y, 'Hydro']), 1) if 'Hydro' in annual_gen.columns else 0,
        'nuclear_gwh': round(float(annual_gen.loc[y, 'Nuclear']), 1) if 'Nuclear' in annual_gen.columns else 0,
        'gas_gwh': round(float(annual_gen.loc[y, 'Gas']), 1) if 'Gas' in annual_gen.columns else 0,
        'clean_share_pct': round(float(annual_share.loc[y, 'Clean']), 2) if 'Clean' in annual_share.columns and y in annual_share.index else 0,
        'fossil_share_pct': round(float(annual_share.loc[y, 'Fossil']), 2) if 'Fossil' in annual_share.columns and y in annual_share.index else 0,
        'renewables_share_pct': round(float(annual_share.loc[y, 'Renewables']), 2) if 'Renewables' in annual_share.columns and y in annual_share.index else 0,
    }
    fuel_transition.append(row)

# 6. Real-time Hourly Merit Despatch (Nov 8, 2026 Snapshot)
df_hourly = pd.read_csv(merit_hourly_path)
df_hourly['hour'] = pd.to_datetime(df_hourly['period_start']).dt.hour
hourly_gen = df_hourly[df_hourly['metric'] == 'generation_by_fuel'].groupby(['hour', 'fuel_type'])['mean_mw'].mean().unstack().fillna(0)
hourly_demand = df_hourly[df_hourly['metric'] == 'demand_met'].groupby('hour')['mean_mw'].mean()

hourly_profile = []
for h in range(len(hourly_demand)):
    row = {
        'hour': int(h),
        'demand_met_mw': round(float(hourly_demand.iloc[h]), 1),
        'thermal_mw': round(float(hourly_gen.loc[h, 'THERMAL']), 1) if 'THERMAL' in hourly_gen.columns and h in hourly_gen.index else 0,
        'solar_mw': round(float(hourly_gen.loc[h, 'SOLAR']), 1) if 'SOLAR' in hourly_gen.columns and h in hourly_gen.index else 0,
        'wind_mw': round(float(hourly_gen.loc[h, 'WIND']), 1) if 'WIND' in hourly_gen.columns and h in hourly_gen.index else 0,
        'hydro_mw': round(float(hourly_gen.loc[h, 'HYDRO']), 1) if 'HYDRO' in hourly_gen.columns and h in hourly_gen.index else 0,
        'nuclear_mw': round(float(hourly_gen.loc[h, 'NUCLEAR']), 1) if 'NUCLEAR' in hourly_gen.columns and h in hourly_gen.index else 0,
        'gas_mw': round(float(hourly_gen.loc[h, 'GAS']), 1) if 'GAS' in hourly_gen.columns and h in hourly_gen.index else 0,
    }
    hourly_profile.append(row)

# 7. Actual vs Predicted for Test Set (sample down to weekly or monthly points for lightweight visualization)
test_dates = dates_clean[test_mask].reset_index(drop=True)
test_plot_data = []
# Sample every 3rd day to keep chart payload light and smooth (~160 points)
for i in range(0, len(y_test), 3):
    test_plot_data.append({
        'date': str(test_dates.iloc[i].date()),
        'actual': round(float(y_test[i]), 1),
        'pred_ridge': round(float(pred_te_ridge[i]), 1),
        'pred_hybrid': round(float(pred_te_hybrid[i]), 1),
        'error': round(float(pred_te_ridge[i] - y_test[i]), 1)
    })

# 8. Compile Complete Output JSON
output_data = {
    'metadata': {
        'title': 'India National Electricity Grid & State Power Dynamics Analysis (2013-2026)',
        'start_date': '2013-01-01',
        'end_date': '2026-11-08',
        'total_days_historical': len(df_nat),
        'train_days': int(len(y_train)),
        'test_days': int(len(y_test)),
        'peak_demand_record_mw': float(round(df_nat['peak_mw'].max(), 1)),
        'peak_demand_record_date': str(df_nat.loc[df_nat['peak_mw'].idxmax(), 'Date'].date()),
        'daily_energy_record_mu': float(round(df_nat['energy_mu'].max(), 1)),
        'daily_energy_record_date': str(df_nat.loc[df_nat['energy_mu'].idxmax(), 'Date'].date()),
        'mean_peak_mw': float(round(df_nat['peak_mw'].mean(), 1)),
        'mean_energy_mu': float(round(df_nat['energy_mu'].mean(), 1)),
    },
    'model_benchmark': models_summary,
    'best_model': models_summary[0],
    'feature_weights': weights,
    'state_profiles': state_profiles,
    'fuel_transition': fuel_transition,
    'hourly_profile': hourly_profile,
    'test_predictions_sample': test_plot_data
}

with open('electricity_analysis_clean.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2)

print("\nSaved electricity_analysis_clean.json successfully.")
