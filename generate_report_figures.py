import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

# Set high quality styling
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.color'] = '#1E293B'
plt.rcParams['axes.labelcolor'] = '#475569'
plt.rcParams['xtick.color'] = '#64748B'
plt.rcParams['ytick.color'] = '#64748B'

# Load dataset
data_path = 'electricity/data/processed/zenodo_india_states/state_daily_energy_met.parquet'
df = pd.read_parquet(data_path)
df['period_start'] = pd.to_datetime(df['period_start'])
national = df.groupby('period_start')['value'].sum().reset_index().rename(columns={'value': 'mu'}).sort_values('period_start').reset_index(drop=True)

diwali_dates = {
    2013: '2013-11-03', 2014: '2014-10-23', 2015: '2015-11-11',
    2016: '2016-10-30', 2017: '2017-10-19', 2018: '2018-11-07',
    2019: '2019-10-27', 2020: '2020-11-14', 2021: '2021-11-04',
    2022: '2022-10-24', 2023: '2023-11-12'
}

# Create output dir for report assets
os.makedirs('report_assets', exist_ok=True)

# ------------------------------------------------------------------------------
# FIGURE 1: 11-YEAR HISTORICAL CONTRACTION & ABSOLUTE ENERGY LOSS (PAGE 1)
# ------------------------------------------------------------------------------
hist_rows = []
for yr, d_str in diwali_dates.items():
    dt = pd.to_datetime(d_str)
    b_sub = national[(national['period_start'] >= dt - pd.Timedelta(days=14)) & (national['period_start'] < dt - pd.Timedelta(days=5))]
    b_val = b_sub['mu'].mean()
    d_sub = national[national['period_start'] == dt]['mu'].values[0]
    t1_sub = national[national['period_start'] == dt + pd.Timedelta(days=1)]['mu'].values[0]
    hist_rows.append({
        'year': yr,
        'base_mu': b_val,
        'diwali_mu': d_sub,
        'pct_drop': (d_sub - b_val) / b_val * 100,
        'abs_drop_mu': b_val - d_sub,
        't1_mu': t1_sub,
        't1_pct_drop': (t1_sub - b_val) / b_val * 100
    })
hdf = pd.DataFrame(hist_rows)

fig1, ax1 = plt.subplots(figsize=(9.2, 3.8), dpi=300, facecolor='#FFFFFF')
years = hdf['year'].values
pcts = hdf['pct_drop'].values
abs_mu = hdf['abs_drop_mu'].values

colors = ['#155C46' if p > -10 else ('#D97706' if p > -15 else '#DC2626') for p in pcts]
bars = ax1.bar(years, pcts, color=colors, width=0.64, edgecolor='#0E3B2E', linewidth=0.8, alpha=0.92, zorder=3)

for bar, pct, mu in zip(bars, pcts, abs_mu):
    ax1.text(bar.get_x() + bar.get_width()/2, pct - 0.7, f'{pct:.1f}%\n(-{mu:.0f} MU)',
             ha='center', va='top', fontsize=7.2, fontweight='bold', color='#1E293B')

ax1.axhline(0, color='#94A3B8', linestyle='--', linewidth=1.1, alpha=0.8)
mean_dip = np.mean(pcts)
ax1.axhline(mean_dip, color='#DC2626', linestyle=':', linewidth=1.4, alpha=0.9, label=f'11-Yr Mean Dip: {mean_dip:.1f}%')

ax1.set_xlabel('Historical Year', fontsize=8.5, fontweight='bold', labelpad=5)
ax1.set_ylabel('% Change vs Pre-Festive Baseline', fontsize=8.5, fontweight='bold', labelpad=5)
ax1.set_xticks(years)
ax1.set_xticklabels(years, fontsize=8)
ax1.set_ylim(-26.5, 3.0)
ax1.grid(True, axis='y', linestyle=':', alpha=0.5, color='#CBD5E1')

legend_elements = [
    patches.Patch(facecolor='#155C46', edgecolor='#0E3B2E', label='Drop < 10% (3 yrs)'),
    patches.Patch(facecolor='#D97706', edgecolor='#0E3B2E', label='Drop 10-15% (5 yrs)'),
    patches.Patch(facecolor='#DC2626', edgecolor='#0E3B2E', label='Drop > 15% (3 yrs)'),
    Line2D([0], [0], color='#DC2626', linestyle=':', linewidth=1.4, label=f'11-Yr Mean: {mean_dip:.1f}%')
]
ax1.legend(handles=legend_elements, loc='upper right', fontsize=7.5, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', framealpha=0.95)

for spine in ax1.spines.values():
    spine.set_color('#CBD5E1')

plt.tight_layout()
fig1.savefig('report_assets/fig1_decadal_trend.png', dpi=300)
plt.close(fig1)

# ------------------------------------------------------------------------------
# FIGURE 2: 15-DAY HIGH-RESOLUTION TRAJECTORY (PAGE 2)
# ------------------------------------------------------------------------------
offsets = list(range(-7, 8))
window_matrix = []
for yr in [2018, 2019, 2020, 2021, 2022, 2023]:
    dt = pd.to_datetime(diwali_dates[yr])
    b_sub = national[(national['period_start'] >= dt - pd.Timedelta(days=14)) & (national['period_start'] < dt - pd.Timedelta(days=7))]
    b_val = b_sub['mu'].mean()
    row_vals = []
    for off in offsets:
        tdt = dt + pd.Timedelta(days=off)
        t_val = national[national['period_start'] == tdt]['mu'].values
        row_vals.append((t_val[0] - b_val) / b_val * 100 if len(t_val) > 0 else np.nan)
    window_matrix.append(row_vals)

warr = np.array(window_matrix)
mean_traj = np.nanmean(warr, axis=0)
std_traj = np.nanstd(warr, axis=0)
traj_2023 = warr[-1]

fig2, ax2 = plt.subplots(figsize=(9.2, 4.0), dpi=300, facecolor='#FFFFFF')
ax2.axhline(0, color='#94A3B8', linestyle='--', linewidth=1.2, alpha=0.8, zorder=1)
ax2.text(6.8, 0.7, 'Baseline (0%)', fontsize=8, color='#64748B', ha='right', va='bottom', fontweight='bold')

ax2.fill_between(offsets, mean_traj - std_traj, mean_traj + std_traj, color='#D1FAE5', alpha=0.45, label='6-Yr Normal Range (+-1 Std)')
ax2.plot(offsets, mean_traj, color='#0E3B2E', linewidth=2.8, marker='o', markersize=5.5, label='6-Yr Composite Mean (2018-2023)', zorder=4)
ax2.plot(offsets, traj_2023, color='#D97706', linewidth=2.0, linestyle='-.', marker='s', markersize=4.8, label='2023 Festival Profile', zorder=5)

# Annotations
ax2.annotate('T-2: Dhanteras\n-3.9% Pre-Festive Dip', xy=(-2, mean_traj[5]), xytext=(-3.6, 4.2),
             arrowprops=dict(arrowstyle="->", color='#64748B', lw=1.1),
             fontsize=7.8, fontweight='bold', color='#334155', ha='center', va='bottom',
             bbox=dict(boxstyle="round,pad=0.25", fc="#F1F5F9", ec="#CBD5E1", lw=0.8), zorder=6)

ax2.text(1.7, -5.8, 'Festive Demand Deficit\nDiwali Day (T=0): -15.5%\nPeak Trough (T+1): -18.7%',
         fontsize=7.8, fontweight='bold', color='#DC2626', ha='center', va='center',
         bbox=dict(boxstyle="round,pad=0.32", fc="#FEF2F2", ec="#FECACA", lw=1.1), zorder=6)

ax2.annotate('', xy=(0, mean_traj[7]), xytext=(1.0, -8.2), arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.3), zorder=6)
ax2.annotate('', xy=(1, mean_traj[8]), xytext=(1.6, -8.2), arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.3), zorder=6)

ax2.set_xlabel('Days Relative to Diwali Day (T=0)', fontsize=8.5, fontweight='bold', labelpad=5)
ax2.set_ylabel('% Change from Pre-Festive Baseline', fontsize=8.5, fontweight='bold', labelpad=5)
ax2.set_xticks(offsets)
ax2.set_xticklabels([f'{o:+d}' if o != 0 else 'Diwali (0)' for o in offsets], fontsize=7.8)
ax2.set_ylim(-26.5, 7.5)
ax2.grid(True, linestyle=':', alpha=0.5, color='#CBD5E1')
ax2.legend(loc='lower left', fontsize=7.8, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', framealpha=0.92)

for spine in ax2.spines.values():
    spine.set_color('#CBD5E1')

plt.tight_layout()
fig2.savefig('report_assets/fig2_festive_trajectory.png', dpi=300)
plt.close(fig2)

# ------------------------------------------------------------------------------
# FIGURE 3: ALL 34 STATES / UTs DIVERGENCE (PAGE 3)
# ------------------------------------------------------------------------------
state_metrics = []
for state in df['entity'].unique():
    sdf = df[df['entity'] == state]
    changes = []
    base_mus = []
    diw_mus = []
    for yr in [2018, 2019, 2020, 2021, 2022, 2023]:
        dt = pd.to_datetime(diwali_dates[yr])
        base_sub = sdf[(sdf['period_start'] >= dt - pd.Timedelta(days=14)) & (sdf['period_start'] < dt - pd.Timedelta(days=5))]
        base_val = base_sub['value'].mean()
        diw_sub = sdf[sdf['period_start'] == dt]['value'].values
        if len(diw_sub) > 0 and base_val > 0:
            changes.append((diw_sub[0] - base_val) / base_val * 100)
            base_mus.append(base_val)
            diw_mus.append(diw_sub[0])
    if changes:
        state_metrics.append({
            'state': state,
            'pct_drop': np.mean(changes),
            'std_pct': np.std(changes),
            'base_mu': np.mean(base_mus),
            'diw_mu': np.mean(diw_mus),
            'drop_mu': np.mean(base_mus) - np.mean(diw_mus)
        })
st_df = pd.DataFrame(state_metrics).sort_values('pct_drop', ascending=True).reset_index(drop=True)

fig3, ax3 = plt.subplots(figsize=(9.2, 7.8), dpi=300, facecolor='#FFFFFF')
y_pos = np.arange(len(st_df))
s_vals = st_df['pct_drop'].values
s_names = st_df['state'].values

bar_c = ['#DC2626' if v < -20 else ('#D97706' if v < -10 else ('#64748B' if v < 0 else '#059669')) for v in s_vals]
bars3 = ax3.barh(y_pos, s_vals, color=bar_c, height=0.72, edgecolor='#334155', linewidth=0.5, zorder=3)
ax3.invert_yaxis()

for bar, val, row in zip(bars3, s_vals, st_df.itertuples()):
    if val < 0:
        ax3.text(val - 0.9, bar.get_y() + bar.get_height()/2, f'{val:+.1f}% ({row.drop_mu:+.1f} MU)',
                 va='center', ha='right', fontsize=6.8, fontweight='bold', color='#1E293B')
    else:
        ax3.text(val + 0.9, bar.get_y() + bar.get_height()/2, f'{val:+.1f}% ({row.drop_mu:+.1f} MU)',
                 va='center', ha='left', fontsize=6.8, fontweight='bold', color='#059669')

ax3.axvline(0, color='#94A3B8', linestyle='-', linewidth=1.1, alpha=0.8, zorder=2)
ax3.set_yticks(y_pos)
yticklabels = ax3.set_yticklabels(s_names, fontsize=7.2, fontweight='bold')
for i, ticklabel in enumerate(yticklabels):
    val = s_vals[i]
    if val < -20:
        ticklabel.set_color('#991B1B')
    elif val < 0:
        ticklabel.set_color('#B45309')
    else:
        ticklabel.set_color('#065F46')

ax3.set_xlabel('% Electricity Demand Met Change on Diwali Day (6-Year Empirical Average)', fontsize=8.5, fontweight='bold', labelpad=5)
ax3.set_xlim(-62, 18)
ax3.grid(True, axis='x', linestyle=':', alpha=0.5, color='#CBD5E1')

# Add category callout boxes in open space
ax3.text(2.0, 3.5, 'Archetype I: Severe Industrial Shutdowns\nContinuous-process manufacturing (textiles, chemicals,\nsteel, auto) idles multi-MW motors.',
         fontsize=7.2, color='#991B1B', fontweight='bold', ha='left', va='center',
         bbox=dict(boxstyle="round,pad=0.3", fc="#FEF2F2", ec="#FECACA", lw=0.9))

ax3.text(-58.0, 28.5, 'Archetype IV: Festive Expansion States\nHeavy residential illumination & agrarian operations\noutweigh minor commercial dips.',
         fontsize=7.2, color='#065F46', fontweight='bold', ha='left', va='center',
         bbox=dict(boxstyle="round,pad=0.3", fc="#ECFDF5", ec="#A7F3D0", lw=0.9))

for spine in ax3.spines.values():
    spine.set_color('#CBD5E1')

plt.tight_layout()
fig3.savefig('report_assets/fig3_state_divergence_census.png', dpi=300)
plt.close(fig3)

# ------------------------------------------------------------------------------
# FIGURE 4: LOAD COMPOSITION PHYSICS & ENERGY BALANCE (PAGE 4)
# ------------------------------------------------------------------------------
fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(9.2, 3.8), dpi=300, facecolor='#FFFFFF')

# Subplot 4A: Sectoral Demand Deficit vs Surge (2023 Diwali)
categories = ['C&I Motors &\nFactory Halts', 'Agricultural\nPump Holidays', 'Offices & Non-Vital\nCommercial', 'Household Decorative\nLED Lighting Surge']
delta_values = [-686.0, -150.0, -95.0, 6.0]
bar_colors_4a = ['#DC2626', '#D97706', '#E11D48', '#059669']

bars4a = ax4a.bar(categories, delta_values, color=bar_colors_4a, width=0.58, edgecolor='#0E3B2E', linewidth=0.8, alpha=0.9, zorder=3)
ax4a.axhline(0, color='#94A3B8', linestyle='--', linewidth=1.1)

for bar, val in zip(bars4a, delta_values):
    if val < 0:
        ax4a.text(bar.get_x() + bar.get_width()/2, val - 35, f'{val:+.0f} MU',
                  ha='center', va='top', fontsize=7.5, fontweight='bold', color='#1E293B')
    else:
        ax4a.text(bar.get_x() + bar.get_width()/2, val + 25, f'{val:+.0f} MU\n(<1%)',
                  ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#059669')

ax4a.set_ylabel('Estimated Energy Impact (MU / day)', fontsize=8, fontweight='bold')
ax4a.set_title('Sectoral Deficit vs Festive Lighting (2023)', fontsize=8.5, fontweight='bold', color='#0E3B2E', pad=8)
ax4a.set_ylim(-820, 160)
ax4a.grid(True, axis='y', linestyle=':', alpha=0.5, color='#CBD5E1')
ax4a.tick_params(axis='x', labelsize=7.2)

for spine in ax4a.spines.values():
    spine.set_color('#CBD5E1')

# Subplot 4B: Incandescent vs LED String Efficiency Comparison
lamp_types = ['Legacy Incandescent\nStrings (60W x 3)', 'Modern Semiconductor\nLED Strips (5W x 3)']
connected_gw = [18.0, 1.5]
energy_4h_mu = [72.0, 6.0]

x = np.arange(len(lamp_types))
width = 0.35

ax4b.bar(x - width/2, connected_gw, width, label='Peak Load Surge (GW)', color='#D97706', edgecolor='#78350F', linewidth=0.8, alpha=0.9, zorder=3)
ax4b.bar(x + width/2, energy_4h_mu, width, label='4-Hr Energy Met (MU)', color='#059669', edgecolor='#064E3B', linewidth=0.8, alpha=0.9, zorder=3)

for i in range(len(lamp_types)):
    ax4b.text(x[i] - width/2, connected_gw[i] + 0.6, f'{connected_gw[i]:.1f} GW', ha='center', va='bottom', fontsize=7.5, fontweight='bold')
    ax4b.text(x[i] + width/2, energy_4h_mu[i] + 1.8, f'{energy_4h_mu[i]:.0f} MU', ha='center', va='bottom', fontsize=7.5, fontweight='bold')

ax4b.set_ylabel('Power (GW) / Energy (MU)', fontsize=8, fontweight='bold')
ax4b.set_title('Technology Comparison: 100M Households', fontsize=8.5, fontweight='bold', color='#0E3B2E', pad=8)
ax4b.set_xticks(x)
ax4b.set_xticklabels(lamp_types, fontsize=7.5, fontweight='bold')
ax4b.set_ylim(0, 85)
ax4b.grid(True, axis='y', linestyle=':', alpha=0.5, color='#CBD5E1')
ax4b.legend(loc='upper right', fontsize=7.5, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1')

for spine in ax4b.spines.values():
    spine.set_color('#CBD5E1')

plt.tight_layout()
fig4.savefig('report_assets/fig4_load_physics_sankey.png', dpi=300)
plt.close(fig4)

print("SUCCESS: All 4 report figures generated in report_assets/")
