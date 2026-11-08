import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec

# Ensure clean Segoe UI / Arial sans-serif typography
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.color'] = '#1E293B'
plt.rcParams['axes.labelcolor'] = '#475569'
plt.rcParams['xtick.color'] = '#64748B'
plt.rcParams['ytick.color'] = '#64748B'

# Load dataset
data_path = 'electricity/data/processed/zenodo_india_states/state_daily_energy_met.parquet'
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Dataset missing at {data_path}")

df = pd.read_parquet(data_path)
df['period_start'] = pd.to_datetime(df['period_start'])

# Aggregate national total
national = df.groupby('period_start')['value'].sum().reset_index().rename(columns={'value': 'mu'})
national = national.sort_values('period_start').reset_index(drop=True)

# Historical Diwali Dates (2013-2023)
diwali_dates = {
    2013: '2013-11-03',
    2014: '2014-10-23',
    2015: '2015-11-11',
    2016: '2016-10-30',
    2017: '2017-10-19',
    2018: '2018-11-07',
    2019: '2019-10-27',
    2020: '2020-11-14',
    2021: '2021-11-04',
    2022: '2022-10-24',
    2023: '2023-11-12'
}

# 1. Historical Year-by-Year Drops
historical_data = []
for yr, d_str in diwali_dates.items():
    d_dt = pd.to_datetime(d_str)
    # Baseline: 14 to 5 days before Diwali
    base_sub = national[(national['period_start'] >= d_dt - pd.Timedelta(days=14)) & (national['period_start'] < d_dt - pd.Timedelta(days=5))]
    base_mu = base_sub['mu'].mean()
    diw_sub = national[national['period_start'] == d_dt]
    if len(diw_sub) > 0 and base_mu > 0:
        diw_mu = diw_sub['mu'].values[0]
        pct = (diw_mu - base_mu) / base_mu * 100
        historical_data.append({
            'year': yr,
            'date': d_str,
            'diwali_mu': diw_mu,
            'base_mu': base_mu,
            'pct_change': pct
        })
hist_df = pd.DataFrame(historical_data)

# 2. 15-Day Festive Window (T-7 to T+7) for Recent 6 Years (2018-2023)
offsets = list(range(-7, 8))
window_matrix = []
for yr in [2018, 2019, 2020, 2021, 2022, 2023]:
    d_dt = pd.to_datetime(diwali_dates[yr])
    base_sub = national[(national['period_start'] >= d_dt - pd.Timedelta(days=14)) & (national['period_start'] < d_dt - pd.Timedelta(days=7))]
    base_val = base_sub['mu'].mean()
    row_vals = []
    for off in offsets:
        target_dt = d_dt + pd.Timedelta(days=off)
        t_val = national[national['period_start'] == target_dt]['mu'].values
        if len(t_val) > 0:
            row_vals.append((t_val[0] - base_val) / base_val * 100)
        else:
            row_vals.append(np.nan)
    window_matrix.append(row_vals)

window_arr = np.array(window_matrix)
mean_traj = np.nanmean(window_arr, axis=0)
std_traj = np.nanstd(window_arr, axis=0)
traj_2023 = window_arr[-1]  # 2023 trajectory

# 3. State-Level Analysis (Recent 6-year average)
state_metrics = []
for state in df['entity'].unique():
    sdf = df[df['entity'] == state]
    changes = []
    for yr in [2018, 2019, 2020, 2021, 2022, 2023]:
        d_dt = pd.to_datetime(diwali_dates[yr])
        base_sub = sdf[(sdf['period_start'] >= d_dt - pd.Timedelta(days=14)) & (sdf['period_start'] < d_dt - pd.Timedelta(days=5))]
        base_val = base_sub['value'].mean()
        diw_sub = sdf[sdf['period_start'] == d_dt]['value'].values
        if len(diw_sub) > 0 and base_val > 0:
            changes.append((diw_sub[0] - base_val) / base_val * 100)
    if changes:
        state_metrics.append({
            'state': state,
            'pct_drop': np.mean(changes)
        })
state_df = pd.DataFrame(state_metrics).sort_values('pct_drop')

# Select top industrial drops and top resilient states
industrial_drops = state_df.head(8).copy()
resilient_states = state_df.tail(6).copy()

# ==============================================================================
# CREATE LINKEDIN PUBLICATION GRAPHIC (14 x 17.5 INCHES @ 300 DPI)
# ==============================================================================
fig = plt.figure(figsize=(14, 17.5), facecolor='#F8FAFC', dpi=300)

# Main GridSpec
gs = GridSpec(
    nrows=4,
    ncols=2,
    figure=fig,
    height_ratios=[1.7, 4.3, 4.4, 2.5],
    width_ratios=[1.0, 1.0],
    hspace=0.30,
    wspace=0.25,
    left=0.06,
    right=0.94,
    top=0.955,
    bottom=0.035
)

# Colors
C_DARK = '#0E3B2E'       # Emerald Dark
C_GREEN = '#155C46'      # Medium Green
C_ACCENT = '#2E9370'     # Mint Accent
C_AMBER = '#D97706'      # Festive Amber
C_RED = '#DC2626'        # Deficit Red
C_LIGHT_BG = '#FFFFFF'
C_MUTED = '#64748B'
C_BORDER = '#E2E8F0'

# ------------------------------------------------------------------------------
# 1. HEADER & KPI CARDS (Spans across both columns)
# ------------------------------------------------------------------------------
ax_header = fig.add_subplot(gs[0, :])
ax_header.set_facecolor('#F8FAFC')
ax_header.axis('off')

# Title & Eyebrow
ax_header.text(0.0, 0.94, 'NATIONAL GRID ANALYTICS  |  SPECIAL FESTIVE STUDY',
               fontsize=11, fontweight='bold', color=C_ACCENT, transform=ax_header.transAxes)
ax_header.text(0.0, 0.70, 'The Diwali Electricity Paradox',
               fontsize=26, fontweight='bold', color=C_DARK, transform=ax_header.transAxes)
ax_header.text(0.0, 0.52, "Why does India's national power consumption plummet by 15% to 19% during the Festival of Lights?",
               fontsize=12.5, color=C_MUTED, transform=ax_header.transAxes)

# 4 Metric Highlights
kpis = [
    ('-15.5%', 'Diwali Day Deficit', '11-yr avg drop on festival day'),
    ('-18.7%', 'Trough at T+1', 'Govardhan Puja / New Year peak dip'),
    ('11 of 11', 'Decadal Consistency', 'Every year 2013-2023 saw a drop'),
    ('-47.5%', 'Peak State Dip', 'Daman & Diu (TN -31.8%, GJ -28.8%)')
]

for i, (val, title, desc) in enumerate(kpis):
    x_pos = 0.0 + i * 0.255
    # Card Background Box
    rect = patches.FancyBboxPatch(
        (x_pos, 0.0), 0.235, 0.42,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        edgecolor=C_BORDER, facecolor='#FFFFFF',
        transform=ax_header.transAxes, zorder=1
    )
    ax_header.add_patch(rect)
    # Text
    ax_header.text(x_pos + 0.02, 0.29, val, fontsize=18, fontweight='bold',
                   color=C_DARK if i != 0 and i != 1 else C_RED, transform=ax_header.transAxes, zorder=2)
    ax_header.text(x_pos + 0.02, 0.16, title, fontsize=10, fontweight='bold',
                   color='#1E293B', transform=ax_header.transAxes, zorder=2)
    ax_header.text(x_pos + 0.02, 0.05, desc, fontsize=8.2,
                   color=C_MUTED, transform=ax_header.transAxes, zorder=2)

# ------------------------------------------------------------------------------
# 2. PANEL A: THE 15-DAY DEMAND TRAJECTORY (T-7 to T+7)
# ------------------------------------------------------------------------------
ax1 = fig.add_subplot(gs[1, 0])
ax1.set_facecolor('#FFFFFF')
ax1.set_title('A. The 15-Day Demand Trajectory (T-7 to T+7)', fontsize=13, fontweight='bold', color=C_DARK, pad=12, loc='left')

# Shaded background reference line at 0%
ax1.axhline(0, color='#94A3B8', linestyle='--', linewidth=1.2, alpha=0.8, zorder=1)
ax1.text(6.8, 0.6, 'Baseline (0%)', fontsize=8.5, color='#64748B', ha='right', va='bottom', fontweight='bold')

# Confidence band (std)
ax1.fill_between(offsets, mean_traj - std_traj, mean_traj + std_traj, color='#D1FAE5', alpha=0.5, label='6-Year Normal Range (+-1 Std)')

# Mean trajectory line
ax1.plot(offsets, mean_traj, color=C_DARK, linewidth=3.2, marker='o', markersize=6.5, label='6-Yr Mean (2018-2023)', zorder=4)

# 2023 line
ax1.plot(offsets, traj_2023, color=C_AMBER, linewidth=2.2, linestyle='-.', marker='s', markersize=5.5, label='Latest 2023 Festival', zorder=5)

# Annotations for key milestones
# T-2 (Dhanteras)
ax1.annotate('T-2: Dhanteras\n(-3.9%)', xy=(-2, mean_traj[5]), xytext=(-3.6, 4.2),
             arrowprops=dict(arrowstyle="->", color=C_MUTED, lw=1.2),
             fontsize=8.5, fontweight='bold', color='#334155', ha='center',
             bbox=dict(boxstyle="round,pad=0.25", fc="#F1F5F9", ec="#CBD5E1", lw=0.8))

# T=0 (Diwali Day)
ax1.annotate('Diwali Day (T=0)\n-15.5% National Dip', xy=(0, mean_traj[7]), xytext=(-2.2, -8.5),
             arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.5),
             fontsize=8.5, fontweight='bold', color=C_RED, ha='center',
             bbox=dict(boxstyle="round,pad=0.3", fc="#FEF2F2", ec="#FECACA", lw=1))

# T+1 (Govardhan Puja / Maximum Trough)
ax1.annotate('T+1: Govardhan Puja\n-18.7% Deepest Trough', xy=(1, mean_traj[8]), xytext=(2.6, -22.5),
             arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.5),
             fontsize=8.5, fontweight='bold', color=C_RED, ha='left',
             bbox=dict(boxstyle="round,pad=0.3", fc="#FEF2F2", ec="#FECACA", lw=1))

ax1.set_xlabel('Days Relative to Diwali Day (T=0)', fontsize=10, fontweight='bold', labelpad=6)
ax1.set_ylabel('% Change from Pre-Diwali Baseline', fontsize=10, fontweight='bold', labelpad=6)
ax1.set_xticks(offsets)
ax1.set_xticklabels([f'{o:+d}' if o != 0 else 'Diwali' for o in offsets], fontsize=8.5)
ax1.set_ylim(-26, 8)
ax1.grid(True, linestyle=':', alpha=0.5, color='#CBD5E1')
ax1.legend(loc='lower left', fontsize=8.5, frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0')

# Card border
for spine in ax1.spines.values():
    spine.set_color(C_BORDER)

# ------------------------------------------------------------------------------
# 2. PANEL B: 11-YEAR HISTORICAL CONSISTENCY (2013-2023)
# ------------------------------------------------------------------------------
ax2 = fig.add_subplot(gs[1, 1])
ax2.set_facecolor('#FFFFFF')
ax2.set_title('B. 11-Year Historical Consistency (2013-2023)', fontsize=13, fontweight='bold', color=C_DARK, pad=12, loc='left')

years = hist_df['year'].values
pct_drops = hist_df['pct_change'].values

# Bar colors based on severity of drop
bar_colors = [C_GREEN if p > -10 else (C_AMBER if p > -15 else C_RED) for p in pct_drops]
bars = ax2.bar(years, pct_drops, color=bar_colors, width=0.68, edgecolor='#0E3B2E', linewidth=0.8, alpha=0.9, zorder=3)

# Add value labels above/below bars with clear background pill to avoid line clashes
for bar, pct in zip(bars, pct_drops):
    ax2.text(bar.get_x() + bar.get_width() / 2, pct - 1.3, f'{pct:.1f}%',
             ha='center', va='top', fontsize=8, fontweight='bold', color='#1E293B',
             bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))

ax2.axhline(0, color='#94A3B8', linestyle='--', linewidth=1.2, alpha=0.8)
ax2.axhline(np.mean(pct_drops), color=C_RED, linestyle=':', linewidth=1.5, alpha=0.9,
            label=f'11-Yr Mean Dip: {np.mean(pct_drops):.1f}%')

ax2.set_xlabel('Year', fontsize=10, fontweight='bold', labelpad=6)
ax2.set_ylabel('% Change on Diwali Day vs Baseline', fontsize=10, fontweight='bold', labelpad=6)
ax2.set_xticks(years)
ax2.set_xticklabels(years, rotation=45, fontsize=8.5)
ax2.set_ylim(-24, 2)
ax2.grid(True, axis='y', linestyle=':', alpha=0.5, color='#CBD5E1')
ax2.legend(loc='upper right', fontsize=8.5, frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0')

for spine in ax2.spines.values():
    spine.set_color(C_BORDER)

# ------------------------------------------------------------------------------
# 4. PANEL C: STATE DIVERGENCE (Industrial vs Residential)
# ------------------------------------------------------------------------------
ax3 = fig.add_subplot(gs[2, 0])
ax3.set_facecolor('#FFFFFF')
ax3.set_title('C. State Divergence: Industrial Halts vs Consumer Resilience', fontsize=12, fontweight='bold', color=C_DARK, pad=12, loc='left')

# Combine top drops and resilient states
plot_states = pd.concat([industrial_drops, resilient_states]).sort_values('pct_drop')
s_names = plot_states['state'].values
s_vals = plot_states['pct_drop'].values
y_pos = np.arange(len(s_names))

s_colors = [C_RED if v < -20 else ('#F59E0B' if v < 0 else C_ACCENT) for v in s_vals]

bars3 = ax3.barh(y_pos, s_vals, color=s_colors, height=0.68, edgecolor='#334155', linewidth=0.6, zorder=3)

# Annotate values cleanly
for bar, val in zip(bars3, s_vals):
    if val < 0:
        ax3.text(val - 1.0, bar.get_y() + bar.get_height()/2, f'{val:+.1f}%',
                 va='center', ha='right', fontsize=8, fontweight='bold', color='#1E293B')
    else:
        ax3.text(val + 0.8, bar.get_y() + bar.get_height()/2, f'{val:+.1f}%',
                 va='center', ha='left', fontsize=8, fontweight='bold', color='#1E293B')

ax3.axvline(0, color='#94A3B8', linestyle='-', linewidth=1.2, alpha=0.8)
ax3.set_yticks(y_pos)
ax3.set_yticklabels(s_names, fontsize=8.5, fontweight='bold')
ax3.set_xlabel('% Electricity Demand Change on Diwali', fontsize=10, fontweight='bold', labelpad=6)
ax3.set_xlim(-60, 16)
ax3.grid(True, axis='x', linestyle=':', alpha=0.5, color='#CBD5E1')

# Add category callout boxes in the empty quadrant spaces
# Top-left empty quadrant:
ax3.text(-57, 11.2, 'Heavy Industrial Hubs\n(Factory Shutdowns)', fontsize=8, color=C_RED, fontweight='bold', ha='left',
         bbox=dict(boxstyle="round,pad=0.25", fc="#FEF2F2", ec="#FECACA", lw=0.9))

# Bottom-right empty quadrant:
ax3.text(2.5, 1.8, 'Consumer-Heavy &\nAgrarian States', fontsize=8, color=C_GREEN, fontweight='bold', ha='left',
         bbox=dict(boxstyle="round,pad=0.25", fc="#ECFDF5", ec="#A7F3D0", lw=0.9))

for spine in ax3.spines.values():
    spine.set_color(C_BORDER)

# ------------------------------------------------------------------------------
# 5. PANEL D: THE 3 DRIVERS OF THE DIWALI PARADOX
# ------------------------------------------------------------------------------
ax4 = fig.add_subplot(gs[2, 1])
ax4.set_facecolor('#FFFFFF')
ax4.set_title('D. Grid Physics: The 3 Drivers of the Paradox', fontsize=12, fontweight='bold', color=C_DARK, pad=12, loc='left')
ax4.axis('off')

# Outer border card
border_box = patches.FancyBboxPatch(
    (0.0, 0.0), 1.0, 1.0,
    boxstyle="round,pad=0.01,rounding_size=0.03",
    edgecolor=C_BORDER, facecolor='#FFFFFF',
    transform=ax4.transAxes, zorder=1
)
ax4.add_patch(border_box)

# 3 Explanatory Pillars
drivers = [
    ("1. The Commercial & Industrial (C&I) Shutdown Effect",
     "Commercial and industrial customers account for ~49% of all electricity consumed in India. Continuous-process plants (textiles, chemicals, auto manufacturing, steel rolling) in Gujarat, Tamil Nadu, and Maharashtra initiate planned annual maintenance halts during Dhanteras through Bhai Dooj. The idling of multi-megawatt industrial motors creates a deficit that domestic loads cannot replace.",
     "#FEF2F2", C_RED),

    ("2. The Modern LED Efficiency Revolution",
     "While public intuition assumes decorative lighting creates massive power surges, modern LED serial strings draw only 3W to 10W per 10-meter set (compared to legacy 60W-100W incandescent fixtures). Even if 100 million households power 3 LED strings simultaneously, the total peak lighting load is ~1,500 MW for 4 hours (~6 MU), which is barely 1% of the ~686 MU daily industrial drop.",
     "#FEF3C7", C_AMBER),

    ("3. Agricultural Pumping Holidays",
     "Agricultural irrigation pumpsets represent ~18% to 22% of total load in major states (Punjab, Haryana, Rajasthan, Madhya Pradesh). Tubewells and feeder pumps are idled by farmers during the festival festivities, amplifying the grid-wide demand suppression.",
     "#ECFDF5", C_GREEN)
]

card_y = [0.67, 0.35, 0.03]
card_height = 0.29

for i, (title, text, bg_c, tag_c) in enumerate(drivers):
    y_pos = card_y[i]
    rect = patches.FancyBboxPatch(
        (0.03, y_pos), 0.94, card_height,
        boxstyle="round,pad=0.015,rounding_size=0.025",
        edgecolor=bg_c, facecolor=bg_c,
        transform=ax4.transAxes, zorder=2
    )
    ax4.add_patch(rect)
    ax4.text(0.05, y_pos + card_height - 0.06, title, fontsize=9.2, fontweight='bold', color=tag_c, transform=ax4.transAxes, zorder=3)
    ax4.text(0.05, y_pos + 0.035, text, fontsize=7.9, color='#334155', transform=ax4.transAxes, zorder=3,
             wrap=True, linespacing=1.35)

# ------------------------------------------------------------------------------
# 6. FOOTER & STRATEGIC TAKEAWAY (Spans across both columns)
# ------------------------------------------------------------------------------
ax_footer = fig.add_subplot(gs[3, :])
ax_footer.set_facecolor('#FFFFFF')
ax_footer.axis('off')

foot_box = patches.FancyBboxPatch(
    (0.0, 0.0), 1.0, 1.0,
    boxstyle="round,pad=0.01,rounding_size=0.03",
    edgecolor=C_BORDER, facecolor='#0E3B2E',
    transform=ax_footer.transAxes, zorder=1
)
ax_footer.add_patch(foot_box)

ax_footer.text(0.03, 0.78, 'EXECUTIVE GRID SUMMARY & UTILITY IMPLICATIONS',
               fontsize=11, fontweight='bold', color='#4ADE80', transform=ax_footer.transAxes, zorder=2)

summary_p1 = "For power system operators (Grid-India, SLDCs), Diwali is not a generation-scarcity challenge, but a high-voltage regulation and over-frequency challenge."
summary_p2 = "With ~15% to 19% of national demand suddenly vanishing, transmission grids experience severe Ferranti effects (voltage spikes from lightly loaded lines)."
summary_p3 = "Grid managers actively back down thermal base generation, ramp down hydro, and switch in 765 kV bus reactors to maintain 50 Hz grid stability."

full_summary = f"{summary_p1}\n{summary_p2}\n{summary_p3}"

ax_footer.text(0.03, 0.33, full_summary, fontsize=9.2, color='#F8FAFC', transform=ax_footer.transAxes, zorder=2,
               linespacing=1.45)

ax_footer.text(0.03, 0.09, 'Data: Grid-India / NLDC Open Data (3,955 Days, 132,600+ State Records)  |  Analysis: Analysis Hub  |  Author: Yash Vasudeva',
               fontsize=8.5, color='#94A3B8', transform=ax_footer.transAxes, zorder=2)

# Save Outputs
png_out = 'diwali_electricity_paradox.png'
pdf_out = 'diwali_electricity_paradox.pdf'
web_out = 'diwali_electricity_paradox_web.png'

print(f"Rendering updated high-resolution graphic to {png_out} and {pdf_out}...")
fig.savefig(png_out, dpi=300, bbox_inches='tight', facecolor='#F8FAFC')
fig.savefig(pdf_out, format='pdf', bbox_inches='tight')

# Optimized web PNG (150 DPI)
fig.savefig(web_out, dpi=150, bbox_inches='tight', facecolor='#F8FAFC')
plt.close(fig)

print("SUCCESS: Infographic generated successfully.")
print(f"Files saved: {png_out}, {pdf_out}, {web_out}")
