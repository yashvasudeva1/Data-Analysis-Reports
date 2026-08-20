// reports-data.js
// Single source of truth for all report and dataset metadata.
// To add a new report: append one object to the REPORTS array below.
// All pages (index, reports, datasets, analytics) read from this file automatically.

const REPORTS = [
  {
    id: 'crime-analysis-india',
    title: 'India Crime Analysis (2001\u20132013)',
    category: 'crime',
    categoryLabel: 'Crime',
    categoryColors: { bg: '#FDE8ED', text: '#A51E35' },
    desc: 'Comprehensive analysis of NCRB crime datasets across 36 states/UTs covering 5.3M+ IPC crimes, crimes against women, auto theft & custodial deaths.',
    status: 'completed',
    updated: 'Jul 28, 2026',
    color: '#0E3B2E',
    url: './crime_report.html',
    kpis: [
      { label: 'IPC Crimes', value: '5.3M' },
      { label: 'Datasets',   value: '19'   },
      { label: 'Years',      value: '13'   }
    ],
    insights: [
      'Total IPC crimes grew 49.6% from 2001 to 2013',
      'UP, AP & West Bengal report highest crimes against women'
    ],
    dataset: {
      name:        'Crime in India (NCRB 2001\u20132014)',
      format:      'CSV / Archive',
      size:        '145.2 MB',
      sizeMB:      145.2,
      sourceLabel: 'Kaggle Dataset',
      sourceUrl:   'https://www.kaggle.com/datasets/rajanand/crime-in-india',
      portal:      'Kaggle'
    },
    analytics: {
      domain:        'Crime',
      badgeBg:       '#FDE8ED',
      badgeText:     '#A51E35',
      methodology:   'Spatial Leaflet + Exploratory EDA',
      sampleSize:    '19 Datasets (36 States)',
      modelMetrics:  null,
      primaryMetric: '85.1% Judicial Backlog (94.6M)'
    }
  },
  {
    id: 'cpi-inflation-2025',
    title: 'CPI Inflation Analysis',
    category: 'economics',
    categoryLabel: 'Economics',
    categoryColors: { bg: '#E8F4FD', text: '#1E6FA5' },
    desc: "Time-series analysis of India's Consumer Price Index from 2013 to 2025, with sector-level decomposition and ML forecasting.",
    status: 'completed',
    updated: 'Nov 26, 2025',
    color: '#2E9370',
    url: './cpi_report.html',
    kpis: [
      { label: 'R\u00b2 Score', value: '0.88'  },
      { label: 'MAE',      value: '1.35'  },
      { label: 'Sectors',  value: '11'    }
    ],
    insights: [
      'General CPI rose ~90% cumulatively, 2013\u20132025',
      'Vegetables/spices show >35% coefficient of variation'
    ],
    dataset: {
      name:        'Year-wise CPI Inflation Rate (Combined CPI-C)',
      format:      'CSV',
      size:        '1.2 MB',
      sizeMB:      1.2,
      sourceLabel: 'Data.gov.in Resource',
      sourceUrl:   'https://www.data.gov.in/resource/year-wise-inflation-rate-based-consumer-price-index-combined-cpi-c-2014-15-2021-22',
      portal:      'Data.gov.in'
    },
    analytics: {
      domain:        'Economics',
      badgeBg:       '#E8F4FD',
      badgeText:     '#1E6FA5',
      methodology:   'ARIMA(1,1,1) + Linear Reg',
      sampleSize:    '156 Months (2013-2025)',
      modelMetrics:  { r2: 0.884, mae: 0.135, label: 'R\u00b2 = 0.8840 | MAE = 1.35' },
      primaryMetric: '90% Cumulative CPI Rise'
    }
  },
  {
    id: 'rainfall-delhi-2025',
    title: 'Rainfall Analysis in Delhi',
    category: 'climate',
    categoryLabel: 'Climate & Weather',
    categoryColors: { bg: '#E8FDF4', text: '#1EA566' },
    desc: '8-year spatial-temporal study of precipitation across 9 Delhi districts, monsoon anomaly heatmaps, and XGBoost Tweedie regression model.',
    status: 'completed',
    updated: 'Dec 1, 2025',
    color: '#1EA566',
    url: './rainfall_report.html',
    kpis: [
      { label: 'R\u00b2 (Test)', value: '0.82'    },
      { label: 'MAE',       value: '1.83 mm' },
      { label: 'Years',     value: '8'       }
    ],
    insights: [
      'South Delhi leads in total rainfall (7,842 mm)',
      'XGBoost Tweedie model achieves 0.82 Test R\u00b2'
    ],
    dataset: {
      name:        'India Rainfall & Precipitation Data (District-wise)',
      format:      'CSV',
      size:        '4.8 MB',
      sizeMB:      4.8,
      sourceLabel: 'Data.gov.in Search',
      sourceUrl:   'https://www.data.gov.in/search?title=Rainfall&sortby=_score&type=resources',
      portal:      'Data.gov.in'
    },
    analytics: {
      domain:        'Climate & Weather',
      badgeBg:       '#E8FDF4',
      badgeText:     '#1EA566',
      methodology:   'XGBoost Regressor (tweedie)',
      sampleSize:    '20,000+ Days (2018-2025)',
      modelMetrics:  { r2: 0.820, mae: 0.183, label: 'R\u00b2 = 0.8200 | MAE = 1.83 mm' },
      primaryMetric: '7,842 mm Max Rainfall'
    }
  },
  {
    id: 'ipl-performance-analysis',
    title: 'IPL Performance Analysis (2019\u20132026)',
    category: 'sports',
    categoryLabel: 'Sports',
    categoryColors: { bg: '#E8F0FD', text: '#1E4FA5' },
    desc: 'Comprehensive multi-season analysis of batting, bowling, boundaries, player arcs, and franchise dependencies across the Indian Premier League.',
    status: 'completed',
    updated: 'Aug 9, 2026',
    color: '#1E4FA5',
    url: './ipl_report.html',
    kpis: [
      { label: 'Top Scorer',  value: '9,336' },
      { label: 'Top Wickets', value: '226'   },
      { label: 'Seasons',     value: '5'     }
    ],
    insights: [
      'Virat Kohli leads all-time with 9,336 runs and 9 centuries',
      "Chris Gayle's 357 sixes record remains uncontested"
    ],
    dataset: {
      name:        'IPL Official Stats & Career Records (2019\u20132026)',
      format:      'CSV (scraped)',
      size:        '6.2 MB',
      sizeMB:      6.2,
      sourceLabel: 'iplt20.com Stats',
      sourceUrl:   'https://www.iplt20.com/stats',
      portal:      'iplt20.com'
    },
    analytics: {
      domain:        'Sports',
      badgeBg:       '#E8F0FD',
      badgeText:     '#1E4FA5',
      methodology:   'Multi-Season EDA & Trajectory Analysis',
      sampleSize:    '25+ Datasets (102 Players)',
      modelMetrics:  null,
      primaryMetric: '31.9% Max Franchise Dependence (Buttler)'
    }
  },
  {
    id: 'nasa-cmapss-rul',
    title: 'NASA C-MAPSS RUL Prediction (FD001)',
    category: 'ml',
    categoryLabel: 'ML',
    categoryColors: { bg: '#F0E8FD', text: '#6A1EA5' },
    desc: 'End-to-end predictive maintenance pipeline for NASA C-MAPSS turbofan engines. XGBoost regression with 282 temporal features, engine-level leakage-safe validation, asymmetric PHM scoring, and FastAPI + Streamlit inference.',
    status: 'completed',
    updated: 'Aug 20, 2026',
    color: '#6A1EA5',
    url: './nasa_rul_report.html',
    kpis: [
      { label: 'Test MAE',  value: '10.37 cy' },
      { label: 'PHM Score', value: '309.72'   },
      { label: 'Features',  value: '282'      }
    ],
    insights: [
      'sensor_11 is the strongest RUL predictor (|Pearson|=0.696)',
      'XGBoost outperforms RF baseline across all 3 metrics'
    ],
    dataset: {
      name:        'NASA C-MAPSS Aircraft Engine Simulator Data (FD001\u2013FD004)',
      format:      'TXT / CSV',
      size:        '2.1 MB',
      sizeMB:      2.1,
      sourceLabel: 'NASA Data Portal',
      sourceUrl:   'https://data.nasa.gov/dataset/C-MAPSS-Aircraft-Engine-Simulator-Data/xaut-bemq',
      portal:      'NASA Data'
    },
    analytics: {
      domain:        'Machine Learning',
      badgeBg:       '#F0E8FD',
      badgeText:     '#6A1EA5',
      methodology:   'XGBoost Regressor + Random Forest Baseline',
      sampleSize:    '33,727 Rows (200 Engines)',
      modelMetrics:  { r2: 0, mae: 0.104, label: 'MAE = 10.37 cy | PHM = 309.72' },
      primaryMetric: '282 Temporal Features'
    }
  }
];

// Computed aggregates — consumed by all pages
const HUB_STATS = (() => {
  const total       = REPORTS.length;
  const completed   = REPORTS.filter(r => r.status === 'completed').length;
  const inProgress  = REPORTS.filter(r => r.status === 'in_progress').length;
  const pending     = REPORTS.filter(r => r.status === 'pending').length;
  const totalSizeMB = REPORTS.reduce((s, r) => s + (r.dataset.sizeMB || 0), 0);

  // Format size: show in GB if >= 1000 MB
  const fmtSize = mb => mb >= 1000 ? (mb / 1024).toFixed(1) + ' GB' : mb.toFixed(1) + ' MB';

  const portals = [...new Set(REPORTS.map(r => r.dataset.portal))];

  return { total, completed, inProgress, pending, totalSizeMB, totalSizeLabel: fmtSize(totalSizeMB), portals };
})();
