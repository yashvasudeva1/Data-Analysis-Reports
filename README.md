# 📊 Data Analysis Reports - Analysis Hub

A centralized, beautifully designed web dashboard for publishing, tracking, and comparing end-to-end data analysis reports. Built with HTML, CSS, and JavaScript.

## 🌟 Executive Overview & Data Volume
This project encompasses massive, real-world data analyses across diverse domains including macroeconomics, meteorology, sports, judicial/law enforcement, aerospace predictive maintenance, and e-commerce retail analytics. 

**Data Volume Processed & Cleaned:**
In total, **over 350,000+ lines of raw dataset records** have been cleaned, engineered, and analyzed across 240+ raw dataset files, complemented by **1.13M+ consumer ratings and reviews**:
* **>50 Million IPC crimes** and judicial records across India (2001–2013).
* **~20,400+ daily weather observations** across Delhi (2018–2025).
* **33,727 aerospace turbofan engine cycles** from NASA simulators.
* **156 continuous months** of macroeconomic inflation data.
* **27,800+ IPL player-match records** across 10 franchises.
* **1,133,234 consumer ratings and 94,432 reviews** across 98 smartphones from 13 brands on Flipkart.

---

## 📈 1. CPI Inflation Analysis (2013–2025)
* **Domain:** Macroeconomics
* **Dataset:** 156 months, 11 sectors (General Index, Food & Bev, Housing, Health, etc.)
* **Model / Methodology:** ARIMA(1,1,1) + Linear Regression

**Key Metrics & Findings:**
* **Total Inflation:** +89.4% cumulative rise in the General Index from 105.2 (2013 Base) to 199.3 (2025). Avg annual growth rate of 5.42%.
* **Predictive Accuracy:** The ARIMA Model achieved an **$R^2$ of 0.883**, a Mean Absolute Error (**MAE**) of **1.35**, and an RMSE of 1.55.
* **Primary Driver:** Food & Beverages (Regression coefficient = 0.436). Spikes in vegetable prices accounted for 44% of total CPI volatility.
* **Volatility (Std Dev):** Vegetables (42.5), Spices (38.2), Oils & Fats (31.4), Fuel & Light (26.5).
* **COVID-19 Impact:** Pre-2020 General Index average was 124.5; Post-2020 surged to 177.2. Peak YoY spike reached 11.2% in 2020.
* **Forecast:** General CPI is projected to maintain a steady 5.1% annualized trend, reaching an index of ~206.4 by Q4 2026.

## 🌧️ 2. Rainfall Analysis in Delhi (2018–2025)
* **Domain:** Climate & Meteorology
* **Dataset:** ~20,400+ daily district observations across 9 districts over 8 years.
* **Model / Methodology:** Two-Stage Hurdle Model (XGBoost Classifier + XGBoost Tweedie Regressor, $p=1.5$)

**Key Metrics & Findings:**
* **Model Accuracy (Regressor):** Test **$R^2$ = 0.820**, Test **MAE = 1.83 mm**, Test **RMSE = 8.62 mm**. Train $R^2$ reached 0.905.
* **Cumulative Volume:** 7,420 mm of total rainfall (Average 927.5 mm/year).
* **Monsoon Concentration:** 68.4% of all rainfall occurs in a narrow 60-day window (July–August).
* **Exceedance Insight:** The top 5% of the wettest days account for >52% of total rainfall volume. Top 1% threshold is 88.5 mm.
* **Highest Rainfall District:** South Delhi (7,842 mm total), followed by East Delhi (7,520 mm).
* **Extreme Spikes:** Max 24h downpour of 93.2 mm occurred on Sept 23, 2022. The peak wettest year was 2021 (1,248 mm total).

## ⚖️ 3. India Crime Analysis (2001–2013)
* **Domain:** Law Enforcement & Judicial
* **Dataset:** 271,321 CSV rows across 19 NCRB categories (Tracking 50 Million+ IPC crimes and 111.1 Million persons under trial in 2013).
* **Methodology:** Spatial Leaflet + Exploratory EDA

**Key Metrics & Findings:**
* **Crime Acceleration:** Total IPC crimes grew from 3.53 Million (2001) to 5.29 Million (2013) — a **+49.6% cumulative increase**.
* **Judicial Backlog:** 85.1% of court trials were pending at the end of 2013 (94.6 Million persons under trial pending out of 111.1M).
* **Conviction Rate:** Only 33.1% national conviction rate (4.74M convicted vs 9.56M acquitted or discharged).
* **Trial Delays:** 37.3% of trials (5.41 Million cases) spanned longer than 3 years; 457,000+ cases delayed for over 10 years.
* **Highest Burden States:** Maharashtra (468,770 IPC crimes in 2013), Madhya Pradesh (454,906), Uttar Pradesh (452,890).
* **Auto Theft Recovery:** Andhra Pradesh had a 73.5% recovery rate, whereas Delhi had a 12.8% recovery rate (30,062 stolen vs 3,848 recovered).
* **Women's Safety:** Uttar Pradesh recorded 62,462 crimes against women. 57% of rape victims nationally were aged 18–30, and 16% were minors (14–18).

## 🏏 4. IPL Performance Analysis (2019–2026)
* **Domain:** Sports Analytics
* **Dataset:** 27,805 statistical player/match rows across 102 players, 10 franchises, and 5 tracked seasons + All-time records.
* **Methodology:** Multi-Season EDA & Trajectory Analysis

**Key Metrics & Findings:**
* **All-Time Run King:** Virat Kohli (9,336 runs in 283 matches, Avg: 40.42, 9 centuries, 68 fifties, 844 fours).
* **All-Time Wicket Leader:** Bhuvneshwar Kumar (226 wickets in 206 matches, Eco: 7.71).
* **Universe Boss:** Chris Gayle (357 sixes in 142 matches).
* **Best Rates (Minimums Applied):** KL Rahul holds the best batting average (46.15). Sunil Narine holds the best economy (6.79). Jasprit Bumrah holds the best bowling average (23.74). AB de Villiers holds the best boundary frequency rate (SR 151.68).
* **Highest Franchise Dependence:** Jos Buttler (2019 RR) accounted for 31.9% of his team's tracked runs (863 runs) — a 99th percentile peak.
* **Extreme Variance:** Sunil Narine (2024 KKR) jumped 54 percentiles from his baseline to score 488 runs as an opener at the 93rd percentile.

## ✈️ 5. NASA C-MAPSS Turbofan Engine RUL Prediction (FD001)
* **Domain:** Predictive Maintenance & Aerospace
* **Dataset:** 33,727 operational cycle rows (20,631 train, 13,096 test) across 200 turbofan engines.
* **Model / Methodology:** XGBoost Regressor vs Random Forest Baseline

**Key Metrics & Findings:**
* **Model Accuracy:** XGBoost achieved Test **MAE = 10.37 cycles**, Test **RMSE = 14.30 cycles**.
* **NASA PHM Score:** Asymmetric test score of **309.72**, beating the RF validation baseline by 12.1%.
* **Feature Engineering:** 21 raw sensors expanded into **282 temporal features** using rolling means, rolling standard deviations, EWMA, and linear trend slopes.
* **Feature Importance:** Sensor 11 was the strongest predictor (|Pearson| = 0.696, |Spearman| = 0.718), rising consistently as engines degrade.
* **Data Quality:** 0 missing cells, 0 duplicates. 6 zero-variance sensors (sensor_1, sensor_5, sensor_10, etc.) were excluded. Sensor 9 had the highest outlier rate (8.17%, STD=22.08).

## 📱 6. Flipkart Mobile Market & Pricing Analytics (2026)
* **Domain:** E-Commerce & Retail Economics
* **Dataset:** 98 smartphones across 13 brands (Samsung, Ai+, vivo, Motorola, realme, Redmi, HMD, BOLTT, OnePlus, Poco, Infinix, Apple, Nothing), capturing 1,133,234 consumer ratings and 94,432 customer reviews, with extracted hardware specifications (RAM, ROM, battery, cameras, 5G, screen size).
* **Model / Methodology:** Ridge L2-Regularized Regression + Exploratory Econometric Analysis

**Key Metrics & Findings:**
* **Model Accuracy:** 5-Fold Test CV **$R^2$ = 0.806** (Test MAE = ₹3,031); Full dataset **$R^2$ = 0.965** with MAE = ₹1,784 across 19 engineered features.
* **5G Market Penetration:** 68.4% of catalog models (67/98) are 5G-ready, commanding an average price premium of **₹7,655 (+46.2%)** over 4G units.
* **Specification Valuation Weights:** RAM capacity is the single strongest hardware valuation driver (+₹4,100 per normalized unit, $r = +0.775$ with price), followed by Apple brand equity (+₹4,844), Front camera (+₹2,577), and OnePlus/vivo identity (+₹2,200).
* **The "Battery Monster" Inverse Elasticity:** Battery capacity shows a negative correlation with price ($r = -0.233$). Budget devices aggressively pack 6,000–10,001 mAh battery cells (realme P4 Power 5G) to win endurance benchmarks, while flagships prioritize thin ergonomics (3,600–4,000 mAh).
* **Consumer Satisfaction Divergence:** Customer rating correlates positively with retail price ($r = +0.637$); flagships average 4.58/5.0 vs budget devices at 4.17/5.0.
* **Anomaly Detection:** Catalog standardizes a uniform 10% discount across all products, whereas ground-truth MRP comparisons show real discounts averaging 34.6%, reaching 94.5% due to extreme seller MRP inflation (e.g. HMD Vibe2 5G listed at ₹214,999 MRP vs ₹12,999 price).
* **Market Arbitrage:** Identified high-value "undervalued" models like *Ai+ Nova 2 Power 5G* (8GB/128GB/7000mAh at ₹17,999, trading 30% below spec-implied valuation).

---

## 🚀 Getting Started

### 🌐 Live Demo
Open `index.html` in your browser, or serve locally:
```bash
# Using Python
python -m http.server 8080

# Using Node.js (npx)
npx serve .
```
Then visit **http://localhost:8080**

### 🔑 Authentication
- **Admin access**: Use the credentials configured in your `.env` file (excluded from version control).
- **Guest access**: Click *Browse as Guest* for read-only mode (no login required).

## 🛠️ Tech Stack
- **UI:** HTML5 + Vanilla CSS + Vanilla JavaScript (No bundler required)
- **Charts:** Chart.js (CDN)
- **Typography:** Plus Jakarta Sans
- **Machine Learning Pipelines:** Python, scikit-learn, XGBoost, pandas, Statsmodels (ARIMA)
