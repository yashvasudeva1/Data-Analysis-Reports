# 📊 Data Analysis Reports - Analysis Hub

A centralized, beautifully designed web dashboard for publishing, tracking, and comparing data analysis reports. Built with vanilla HTML, CSS, and JavaScript - no build tools required.

## 🌐 Live Demo

Open `index.html` in your browser, or serve locally:
```bash
# Using Python
python -m http.server 8080

# Using Node.js (npx)
npx serve .
```
Then visit **http://localhost:8080**

---

## 📁 Project Structure

```
Data Analysis Reports/
├── index.html            # Dashboard home page
├── reports.html          # Published reports grid
├── analytics.html        # Cross-report analytics (Chart.js)
├── datasets.html         # Dataset management
├── settings.html         # User settings & preferences
├── help.html             # FAQ & support page
├── hub.css               # Shared design system & component styles
├── hub.js                # Shared JS: nav, search, accordion
│
├── cpi_report.html       # CPI Inflation Analysis - full report
├── rainfall_report.html  # Delhi Rainfall Analysis - full report
│
├── CPI/                  # CPI Inflation Analysis project
│   ├── app.py            # Flask/Dash application
│   ├── data/             # Source datasets
│   ├── model/            # Trained models
│   ├── notebook/         # Jupyter notebooks
│   ├── static/           # Static report output
│   ├── requirements.txt
│   └── README.md
│
└── Rain In Delhi/        # Delhi Rainfall Analysis project
    ├── Plots/            # Generated visualizations
    ├── model/            # Trained XGBoost models
    └── notebook/         # Jupyter notebooks
```

---

## 📈 Published Reports & Datasets

| Report | Domain | Algorithm / Methodology | Dataset Source | Status |
|---|---|---|---|---|
| [India Crime Analysis (2001–2013)](./crime_report.html) | Crime | Leaflet Choropleth + Spatial EDA | [Kaggle Crime in India](https://www.kaggle.com/datasets/rajanand/crime-in-india) | ✅ Completed |
| [CPI Inflation Analysis](./cpi_report.html) | Economics | ARIMA(1,1,1) + Linear Regression | [Data.gov.in CPI-C Resource](https://www.data.gov.in/resource/year-wise-inflation-rate-based-consumer-price-index-combined-cpi-c-2014-15-2021-22) | ✅ Completed |
| [Rainfall Analysis in Delhi](./rainfall_report.html) | Climate & Weather | XGBoost Tweedie Regressor | [Data.gov.in Rainfall Resources](https://www.data.gov.in/search?title=Rainfall&sortby=_score&type=resources) | ✅ Completed |

---

## 🔑 Features

- **Multi-page dashboard** - Dashboard, Reports, Analytics, Datasets, Settings, Help
- **Role-Based Access Control (RBAC)** - Admin and Guest (read-only) roles via `localStorage`
- **Global search** - Filters reports, datasets, and categories in real-time (⌘F / Ctrl+F)
- **Cross-report analytics** - Chart.js powered comparisons across ML models and macro trends
- **Responsive design** - Mobile-first layout, sidebar collapses on small screens
- **No dependencies** - Pure HTML/CSS/JS, no bundler or framework required

---

## 🚀 Getting Started

### Sign In
- **Admin access**: Use the credentials configured in your `.env` file
- **Guest access**: Click *Browse as Guest* for read-only mode (no login required)

> ⚠️ Credentials in `.env` are **excluded from version control** via `.gitignore`. Never commit your `.env` file.

### Local Development
No build step needed. Simply open `index.html` in a browser or use any static file server.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | HTML5 + Vanilla CSS + Vanilla JavaScript |
| Typography | [Plus Jakarta Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans) (Google Fonts) |
| Charts | [Chart.js](https://www.chartjs.org/) (CDN) |
| ML (CPI) | Python, ARIMA, scikit-learn |
| ML (Rain) | Python, XGBoost (Tweedie), pandas |

---

## 📊 Report Highlights

### CPI Inflation Analysis (2013–2025)
- 156-month time-series of India's Consumer Price Index across 11 sectors
- ARIMA(1,1,1) forecasting with **R² = 0.884**, MAE = 1.35 points
- Key finding: General CPI rose ~90% cumulatively; Vegetables & Spices show >35% coefficient of variation

### Rainfall Analysis in Delhi (2018–2025)
- 8-year spatial-temporal study across 9 Delhi districts (~20,000+ daily observations)
- XGBoost Tweedie regression with **R² = 0.82**, MAE = 1.83 mm
- Key finding: South Delhi leads in total rainfall (7,842 mm); peak monsoon window is July–August

---

## 👤 Author

**Yash Vasudeva** - Data Analyst  
[GitHub](https://github.com/yash-vasudeva) · [Email](mailto:vasudevyash@gmail.com)

---

## 📄 License

This project is for portfolio and educational purposes.
