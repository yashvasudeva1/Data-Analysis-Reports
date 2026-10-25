# run_flipkart_analysis.py
import json
import re
import numpy as np
import pandas as pd
from scipy import stats
from scipy.linalg import lstsq

# Load dataset
df_raw = pd.read_csv('flipkart_data/phones_full.csv')

def parse_record(row):
    title = str(row['title'])
    desc = str(row['description'])
    brand = str(row['brand']).strip()
    
    # Clean Brand
    if brand.upper() == 'APPLE':
        brand = 'Apple'
    elif brand.upper() == 'REDMI':
        brand = 'Redmi'
    elif brand.upper() == 'MOTOROLA':
        brand = 'Motorola'
    elif brand.upper() == 'POCO':
        brand = 'Poco'
        
    # RAM
    ram = np.nan
    m = re.search(r'(\d+)\s*GB\s*RAM', desc, re.I)
    if m:
        ram = int(m.group(1))
    else:
        m2 = re.search(r'\((\d+)\s*GB(?:\s*R|\.\.\.|\s*RAM)', title, re.I)
        if m2:
            ram = int(m2.group(1))
        elif 'iPhone' in title or brand == 'Apple':
            ram = 8
            
    # ROM / Storage
    rom = np.nan
    m = re.search(r'(\d+)\s*GB\s*ROM', desc, re.I)
    if m:
        rom = int(m.group(1))
    else:
        m2 = re.search(r'(\d+)\s*GB(?!\s*RAM)', title, re.I)
        if m2:
            rom = int(m2.group(1))
        elif re.search(r'(\d+)\s*TB', title, re.I):
            rom = int(re.search(r'(\d+)\s*TB', title, re.I).group(1)) * 1024
            
    # Battery mAh
    battery = np.nan
    m = re.search(r'(\d+)\s*mAh\s*Battery', desc, re.I)
    if m:
        battery = int(m.group(1))
    elif 'iPhone 17' in title or brand == 'Apple':
        battery = 3600
        
    # Rear Camera MP
    rear_cam = np.nan
    m = re.search(r'(\d+)\s*MP\s*back\s*camera', desc, re.I)
    if m:
        rear_cam = int(m.group(1))
        
    # Front Camera MP
    front_cam = np.nan
    m = re.search(r'(\d+)\s*MP\s*front\s*camera', desc, re.I)
    if m:
        front_cam = int(m.group(1))
        
    # 5G
    is_5g = 1 if re.search(r'\b5G\b', title + ' ' + desc, re.I) else 0
    
    # Screen Size (inches)
    screen = row['feature_rating::Camera']
    if pd.isna(screen):
        if 'iPhone' in title or brand == 'Apple':
            screen = 6.3
        elif 'S25' in title:
            screen = 6.2
        elif 'BOLTT' in title.upper():
            screen = 6.5
        else:
            screen = 6.7
    else:
        screen = float(screen)
        
    # Model extraction
    clean_model = title.split('(')[0].strip()
    
    return pd.Series([brand, clean_model, ram, rom, battery, rear_cam, front_cam, is_5g, screen],
                     index=['brand_clean', 'model_clean', 'ram_gb', 'rom_gb', 'battery_mah', 'rear_cam_mp', 'front_cam_mp', 'is_5g', 'screen_inch'])

ext = df_raw.apply(parse_record, axis=1)
for col in ext.columns:
    df_raw[col] = ext[col]

# Impute median front camera where missing
df_raw['front_cam_mp'] = df_raw['front_cam_mp'].fillna(df_raw['front_cam_mp'].median())

# Derived metrics
df_raw['price_per_gb_ram'] = (df_raw['price_inr'] / df_raw['ram_gb']).round(1)
df_raw['price_per_gb_rom'] = (df_raw['price_inr'] / df_raw['rom_gb']).round(1)
df_raw['mah_per_1000_inr'] = ((df_raw['battery_mah'] / df_raw['price_inr']) * 1000).round(1)
df_raw['rev_to_rat_pct'] = ((df_raw['num_reviews'] / df_raw['num_ratings']) * 100).round(2)

# Price tiers
def assign_tier(p):
    if p < 15000:
        return 'Budget (<15k)'
    elif p < 25000:
        return 'Mid-Range (15k-25k)'
    elif p < 45000:
        return 'Upper Mid-Range (25k-45k)'
    else:
        return 'Flagship (>=45k)'

df_raw['price_tier'] = df_raw['price_inr'].apply(assign_tier)

# MRP discount analysis
df_raw['has_mrp'] = df_raw['mrp_inr'].notnull()
df_raw['true_discount_pct'] = np.where(df_raw['has_mrp'], ((df_raw['mrp_inr'] - df_raw['price_inr']) / df_raw['mrp_inr'] * 100).round(1), np.nan)

# OLS & Ridge Regression using numpy/scipy
brand_dummies = pd.get_dummies(df_raw['brand_clean'], drop_first=True, prefix='b', dtype=float)
ml_features = ['ram_gb', 'rom_gb', 'battery_mah', 'rear_cam_mp', 'front_cam_mp', 'is_5g', 'screen_inch']
X_df = pd.concat([df_raw[ml_features], brand_dummies], axis=1)
X = X_df.values
y = df_raw['price_inr'].values

# Standardize X for Ridge
X_mean = X.mean(axis=0)
X_std = X.std(axis=0)
X_std[X_std == 0] = 1.0
X_scaled = (X - X_mean) / X_std
X_design = np.column_stack([np.ones(len(X)), X_scaled])

# Ridge regression function
def fit_ridge(X_in, y_in, alpha=1.0):
    n_features = X_in.shape[1]
    I = np.eye(n_features)
    I[0, 0] = 0.0  # don't penalize intercept
    beta = np.linalg.solve(X_in.T @ X_in + alpha * I, X_in.T @ y_in)
    return beta

# 5-fold cross validation
np.random.seed(42)
indices = np.random.permutation(len(X_design))
folds = np.array_split(indices, 5)

cv_r2_list = []
cv_mae_list = []
cv_rmse_list = []

for i in range(5):
    val_idx = folds[i]
    train_idx = np.setdiff1d(indices, val_idx)
    
    beta_fold = fit_ridge(X_design[train_idx], y[train_idx], alpha=5.0)
    y_pred_val = X_design[val_idx] @ beta_fold
    
    r2_val = 1 - np.sum((y[val_idx] - y_pred_val)**2) / np.sum((y[val_idx] - y[val_idx].mean())**2)
    mae_val = np.mean(np.abs(y[val_idx] - y_pred_val))
    rmse_val = np.sqrt(np.mean((y[val_idx] - y_pred_val)**2))
    
    cv_r2_list.append(r2_val)
    cv_mae_list.append(mae_val)
    cv_rmse_list.append(rmse_val)

# Full model fit
beta_full = fit_ridge(X_design, y, alpha=5.0)
y_pred_full = X_design @ beta_full
full_r2 = 1 - np.sum((y - y_pred_full)**2) / np.sum((y - y.mean())**2)
full_mae = np.mean(np.abs(y - y_pred_full))
full_rmse = np.sqrt(np.mean((y - y_pred_full)**2))

df_raw['predicted_price'] = np.round(y_pred_full, 0)
df_raw['price_residual'] = np.round(df_raw['price_inr'] - df_raw['predicted_price'], 0)
df_raw['value_ratio'] = np.round(df_raw['predicted_price'] / df_raw['price_inr'], 2)

# Feature weights (scaled)
feat_names = ['intercept'] + list(X_df.columns)
weight_series = pd.Series(beta_full[1:], index=X_df.columns).sort_values(ascending=False)

# Correlation matrix
corr_cols = ['price_inr', 'mrp_inr', 'true_discount_pct', 'rating', 'num_ratings', 'num_reviews', 'ram_gb', 'rom_gb', 'battery_mah', 'is_5g', 'screen_inch']
corr_matrix = df_raw[corr_cols].corr(method='pearson').round(3)

# Print Summary
print('=== FLIPKART DATASET OVERVIEW ===')
print(f'Total Devices: {len(df_raw)}')
print(f'Total Brands: {df_raw["brand_clean"].nunique()}')
print(f'Price Range: INR {df_raw["price_inr"].min():,.0f} - {df_raw["price_inr"].max():,.0f}')
print(f'Mean Price: INR {df_raw["price_inr"].mean():,.2f} | Median: INR {df_raw["price_inr"].median():,.2f}')
print(f'Total Ratings: {df_raw["num_ratings"].sum():,}')
print(f'Total Reviews: {df_raw["num_reviews"].sum():,}')
print(f'Mean Rating: {df_raw["rating"].mean():.2f}')
print(f'5G Penetration: {df_raw["is_5g"].mean()*100:.1f}% ({df_raw["is_5g"].sum()}/{len(df_raw)})')

print('\n=== ML MODEL PERFORMANCE (Ridge L2-Regularized Regression) ===')
print(f'5-Fold Test CV R2: {np.mean(cv_r2_list):.4f} (+/- {np.std(cv_r2_list):.4f})')
print(f'5-Fold Test CV MAE: INR {np.mean(cv_mae_list):,.2f}')
print(f'5-Fold Test CV RMSE: INR {np.mean(cv_rmse_list):,.2f}')
print(f'Full Dataset R2: {full_r2:.4f}')
print(f'Full Dataset MAE: INR {full_mae:,.2f}')

print('\n=== TOP FEATURE CONTRIBUTIONS (Scaled Beta Weights) ===')
for feat, w in weight_series.head(10).items():
    print(f'  {feat:20s}: INR {w:+,.1f}')

print('\n=== BOTTOM FEATURE CONTRIBUTIONS (Discount/Budget Weights) ===')
for feat, w in weight_series.tail(5).items():
    print(f'  {feat:20s}: INR {w:+,.1f}')

# Export comprehensive stats to json
brand_stats = df_raw.groupby('brand_clean').agg(
    count=('pid', 'count'),
    mean_price=('price_inr', 'mean'),
    median_price=('price_inr', 'median'),
    mean_rating=('rating', 'mean'),
    total_ratings=('num_ratings', 'sum'),
    total_reviews=('num_reviews', 'sum'),
    pct_5g=('is_5g', 'mean')
).sort_values(by='count', ascending=False)
brand_stats['pct_5g'] = (brand_stats['pct_5g'] * 100).round(1)
brand_stats['mean_price'] = brand_stats['mean_price'].round(0)
brand_stats['mean_rating'] = brand_stats['mean_rating'].round(2)

tier_stats = df_raw.groupby('price_tier').agg(
    count=('pid', 'count'),
    mean_price=('price_inr', 'mean'),
    mean_rating=('rating', 'mean'),
    mean_ram=('ram_gb', 'mean'),
    mean_rom=('rom_gb', 'mean'),
    mean_battery=('battery_mah', 'mean'),
    pct_5g=('is_5g', 'mean')
).loc[['Budget (<15k)', 'Mid-Range (15k-25k)', 'Upper Mid-Range (25k-45k)', 'Flagship (>=45k)']]
tier_stats['pct_5g'] = (tier_stats['pct_5g'] * 100).round(1)
tier_stats['mean_price'] = tier_stats['mean_price'].round(0)
tier_stats['mean_rating'] = tier_stats['mean_rating'].round(2)
tier_stats['mean_battery'] = tier_stats['mean_battery'].round(0)
tier_stats['mean_ram'] = tier_stats['mean_ram'].round(1)
tier_stats['mean_rom'] = tier_stats['mean_rom'].round(0)

export_data = {
    'summary': {
        'total_phones': int(len(df_raw)),
        'total_brands': int(df_raw['brand_clean'].nunique()),
        'total_ratings': int(df_raw['num_ratings'].sum()),
        'total_reviews': int(df_raw['num_reviews'].sum()),
        'mean_price': float(round(df_raw['price_inr'].mean(), 2)),
        'median_price': float(df_raw['price_inr'].median()),
        'min_price': float(df_raw['price_inr'].min()),
        'max_price': float(df_raw['price_inr'].max()),
        'mean_rating': float(round(df_raw['rating'].mean(), 2)),
        'pct_5g': float(round(df_raw['is_5g'].mean() * 100, 1)),
        'in_stock_count': int((df_raw['availability'] == 'InStock').sum()),
        'out_of_stock_count': int((df_raw['availability'] != 'InStock').sum()),
        'total_catalog_gmv': float(df_raw['price_inr'].sum()),
    },
    'ml_metrics': {
        'model_name': 'Ridge L2-Regularized Regression',
        'cv_r2': float(round(np.mean(cv_r2_list), 4)),
        'cv_r2_std': float(round(np.std(cv_r2_list), 4)),
        'cv_mae': float(round(np.mean(cv_mae_list), 2)),
        'cv_rmse': float(round(np.mean(cv_rmse_list), 2)),
        'full_r2': float(round(full_r2, 4)),
        'full_mae': float(round(full_mae, 2)),
        'full_rmse': float(round(full_rmse, 2)),
        'features_count': int(X_design.shape[1] - 1),
    },
    'brand_stats': brand_stats.reset_index().to_dict(orient='records'),
    'tier_stats': tier_stats.reset_index().to_dict(orient='records'),
    'feature_weights': {feat: round(float(w), 2) for feat, w in weight_series.items()},
    'correlations': corr_matrix.to_dict(),
    'top_undervalued': df_raw.sort_values(by='value_ratio', ascending=False)[['title', 'brand_clean', 'price_inr', 'predicted_price', 'value_ratio', 'ram_gb', 'rom_gb', 'battery_mah', 'rating']].head(6).to_dict(orient='records'),
    'top_overpriced': df_raw.sort_values(by='value_ratio', ascending=True)[['title', 'brand_clean', 'price_inr', 'predicted_price', 'value_ratio', 'ram_gb', 'rom_gb', 'battery_mah', 'rating']].head(6).to_dict(orient='records'),
    'top_rated_volume': df_raw.sort_values(by='num_ratings', ascending=False)[['title', 'brand_clean', 'price_inr', 'rating', 'num_ratings', 'num_reviews']].head(10).to_dict(orient='records'),
    'ram_dist': df_raw['ram_gb'].value_counts().sort_index().to_dict(),
    'rom_dist': df_raw['rom_gb'].value_counts().sort_index().to_dict(),
    'battery_dist': df_raw['battery_mah'].value_counts().head(8).to_dict(),
    'camera_dist': df_raw['rear_cam_mp'].value_counts().to_dict(),
}

with open('flipkart_analysis_clean.json', 'w', encoding='utf-8') as f:
    json.dump(export_data, f, indent=2)

# Also save cleaned csv for record
df_raw.to_csv('flipkart_data/phones_cleaned_features.csv', index=False)
print('Analysis successfully finished and exported to flipkart_analysis_clean.json & phones_cleaned_features.csv!')
