# analyze_flipkart.py
import json
import re
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

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

print('=== DATASET OVERVIEW ===')
num_brands = df_raw['brand_clean'].nunique()
p_min = df_raw['price_inr'].min()
p_max = df_raw['price_inr'].max()
p_mean = df_raw['price_inr'].mean()
p_med = df_raw['price_inr'].median()
tot_ratings = df_raw['num_ratings'].sum()
tot_reviews = df_raw['num_reviews'].sum()
mean_rat = df_raw['rating'].mean()
pct_5g_val = df_raw['is_5g'].mean() * 100
sum_5g = df_raw['is_5g'].sum()

print(f'Total Phones Analyzed: {len(df_raw)}')
print(f'Brands Represented: {num_brands}')
print(f'Price Range: INR {p_min:,.0f} - {p_max:,.0f}')
print(f'Mean Price: INR {p_mean:,.2f} | Median: INR {p_med:,.2f}')
print(f'Total Consumer Ratings: {tot_ratings:,}')
print(f'Total Consumer Reviews: {tot_reviews:,}')
print(f'Mean Rating: {mean_rat:.2f}')
print(f'5G Penetration: {pct_5g_val:.1f}% ({sum_5g}/{len(df_raw)} models)')

print('\n=== BRAND BREAKDOWN ===')
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
print(brand_stats.to_string())

print('\n=== PRICE TIER BREAKDOWN ===')
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
print(tier_stats.to_string())

print('\n=== 5G vs 4G COMPARISON ===')
g_stats = df_raw.groupby('is_5g').agg(
    count=('pid', 'count'),
    mean_price=('price_inr', 'mean'),
    median_price=('price_inr', 'median'),
    mean_rating=('rating', 'mean'),
    mean_ram=('ram_gb', 'mean'),
    mean_rom=('rom_gb', 'mean'),
    mean_battery=('battery_mah', 'mean'),
    total_ratings=('num_ratings', 'sum')
)
print(g_stats.to_string())

# Machine Learning Modeling
brand_dummies = pd.get_dummies(df_raw['brand_clean'], drop_first=True, prefix='b')
ml_features = ['ram_gb', 'rom_gb', 'battery_mah', 'rear_cam_mp', 'front_cam_mp', 'is_5g', 'screen_inch', 'rating', 'num_ratings']
X = pd.concat([df_raw[ml_features], brand_dummies], axis=1)
y = df_raw['price_inr']

kf = KFold(n_splits=5, shuffle=True, random_state=42)

models = {
    'Ridge Regression': Ridge(alpha=1.0),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, max_depth=6),
    'Gradient Boosting (GBRT)': GradientBoostingRegressor(n_estimators=120, learning_rate=0.07, random_state=42, max_depth=4)
}

print('\n=== ML MODEL PERFORMANCE (5-Fold Cross-Validation) ===')
results = {}
for name, mod in models.items():
    cv_r2 = cross_val_score(mod, X, y, cv=kf, scoring='r2')
    cv_mae = -cross_val_score(mod, X, y, cv=kf, scoring='neg_mean_absolute_error')
    cv_rmse = np.sqrt(-cross_val_score(mod, X, y, cv=kf, scoring='neg_mean_squared_error'))
    
    mod.fit(X, y)
    preds = mod.predict(X)
    full_r2 = r2_score(y, preds)
    full_mae = mean_absolute_error(y, preds)
    full_rmse = np.sqrt(mean_squared_error(y, preds))
    
    results[name] = {
        'cv_r2_mean': round(float(cv_r2.mean()), 4),
        'cv_r2_std': round(float(cv_r2.std()), 4),
        'cv_mae': round(float(cv_mae.mean()), 2),
        'cv_rmse': round(float(cv_rmse.mean()), 2),
        'full_r2': round(float(full_r2), 4),
        'full_mae': round(float(full_mae), 2),
        'full_rmse': round(float(full_rmse), 2)
    }
    print(f'{name:25s} -> Test CV R2: {cv_r2.mean():.4f} (+/- {cv_r2.std():.4f}) | Test CV MAE: INR {cv_mae.mean():,.2f} | Full R2: {full_r2:.4f} | Full MAE: INR {full_mae:,.2f}')

best_model = models['Gradient Boosting (GBRT)']
importances = pd.Series(best_model.feature_importances_, index=X.columns).sort_values(ascending=False)
print('\nTop Feature Importances (Gradient Boosting):')
for feat, imp in importances.head(10).items():
    print(f'  {feat:20s}: {imp*100:.2f}%')

# Value analysis: Predicted vs Actual price
df_raw['predicted_price'] = best_model.predict(X).round(0)
df_raw['price_residual'] = (df_raw['price_inr'] - df_raw['predicted_price']).round(0)
df_raw['value_ratio'] = (df_raw['predicted_price'] / df_raw['price_inr']).round(2)

# Save processed dataframe to json for easy charting
export_dict = {
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
    },
    'model_results': results,
    'feature_importances': {feat: round(float(imp*100), 2) for feat, imp in importances.head(10).items()},
    'brand_stats': brand_stats.reset_index().to_dict(orient='records'),
    'tier_stats': tier_stats.reset_index().to_dict(orient='records'),
    'top_undervalued': df_raw.sort_values(by='value_ratio', ascending=False)[['title', 'brand_clean', 'price_inr', 'predicted_price', 'value_ratio', 'ram_gb', 'rom_gb', 'battery_mah', 'rating']].head(5).to_dict(orient='records'),
    'top_overpriced': df_raw.sort_values(by='value_ratio', ascending=True)[['title', 'brand_clean', 'price_inr', 'predicted_price', 'value_ratio', 'ram_gb', 'rom_gb', 'battery_mah', 'rating']].head(5).to_dict(orient='records'),
    'top_rated_volume': df_raw.sort_values(by='num_ratings', ascending=False)[['title', 'brand_clean', 'price_inr', 'rating', 'num_ratings', 'num_reviews']].head(10).to_dict(orient='records'),
}

with open('flipkart_analysis_results.json', 'w', encoding='utf-8') as f:
    json.dump(export_dict, f, indent=2)

print('\nAnalysis finished! Results saved to flipkart_analysis_results.json')
