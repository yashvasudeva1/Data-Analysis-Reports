# generate_flipkart_report.py
import json

with open('flipkart_analysis_clean.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Flipkart Mobile Market & Pricing Analytics (2026) - Analysis Hub</title>
  <meta name="description" content="In-depth market structure, hardware spec architecture, Ridge L2 machine learning valuation, and consumer sentiment analysis across 98 smartphones and 1.13M+ customer ratings on Flipkart." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <link rel="stylesheet" href="hub.css" />
  <style>
    :root {
      --fk-blue: #2874F0;
      --fk-yellow: #FFC200;
      --fk-orange: #FB641B;
      --fk-dark: #172337;
      --fk-light-blue: #EBF3FF;
      --fk-light-orange: #FFF3EB;
      --fk-light-yellow: #FFF9E6;
    }
    .grid-4 { display:grid; grid-template-columns:repeat(4,1fr); gap:20px; margin-bottom:24px; }
    @media(max-width:1100px){.grid-4{grid-template-columns:repeat(2,1fr);}}
    @media(max-width:600px){.grid-4{grid-template-columns:1fr;}}
    .grid-3 { display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin-bottom:24px; }
    @media(max-width:1000px){.grid-3{grid-template-columns:repeat(2,1fr);}}
    @media(max-width:600px){.grid-3{grid-template-columns:1fr;}}
    .report-tabs { display:flex; gap:6px; overflow-x:auto; padding-bottom:4px; margin-bottom:24px; border-bottom:1px solid var(--border); }
    .report-tab { padding:10px 18px; border-radius:999px; font-size:13px; font-weight:700; color:var(--text-500); background:transparent; border:none; cursor:pointer; white-space:nowrap; font-family:'Plus Jakarta Sans',sans-serif; transition:background .15s,color .15s; }
    .report-tab:hover { background:var(--mint-100); color:var(--green-700); }
    .report-tab.active { background:var(--green-900); color:#fff; }
    .tab-section { display:none; }
    .tab-section.active { display:block; }
    .stat-pill { display:inline-flex; align-items:center; gap:4px; font-size:11.5px; font-weight:600; padding:3px 10px; border-radius:999px; background:var(--mint-100); color:var(--green-700); margin-top:10px; }
    .stat-pill.neutral { background:var(--gray-bg); color:var(--gray-text); }
    .stat-pill.orange  { background:#FFF0E0; color:#B35A00; }
    .stat-pill.blue    { background:#E8F0FD; color:#1E4FA5; }
    .stat-pill.yellow  { background:#FFF9E6; color:#9B6E00; }
    .chart-box { background:var(--surface); border:1px solid var(--border); border-radius:var(--r-card); box-shadow:var(--shadow); padding:22px; margin-bottom:24px; }
    .chart-box-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:16px; flex-wrap:wrap; gap:12px; }
    .chart-box-title { font-size:15px; font-weight:700; color:var(--text-900); }
    .chart-box-sub { font-size:12px; color:var(--text-400); margin-top:2px; }
    .chart-canvas-wrap { position:relative; height:320px; width:100%; }
    .chart-canvas-wrap.short { height:250px; }
    .chart-canvas-wrap.tall  { height:380px; }
    .chart-canvas-wrap.xtall { height:450px; }
    .chart-grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:20px; }
    @media(max-width:900px){.chart-grid-2{grid-template-columns:1fr;}}
    .caption-box { margin-top:14px; padding:12px 16px; background:var(--bg); border-radius:12px; font-size:12.5px; color:var(--text-500); line-height:1.5; }
    .caption-box strong { color:var(--text-900); }
    .exec-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-bottom:24px; }
    @media(max-width:900px){.exec-grid{grid-template-columns:1fr;}}
    .exec-card { background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:18px 20px; display:flex; flex-direction:column; gap:6px; box-shadow:var(--shadow); }
    .exec-card.warning  { border-left:4px solid var(--fk-orange); }
    .exec-card.positive { border-left:4px solid var(--green-500); }
    .exec-card.info     { border-left:4px solid var(--fk-blue); }
    .exec-card.gold     { border-left:4px solid var(--fk-yellow); }
    .exec-title { font-size:13px; font-weight:700; color:var(--text-900); }
    .exec-val   { font-size:22px; font-weight:800; color:var(--text-900); font-variant-numeric:tabular-nums; }
    .exec-desc  { font-size:12.5px; color:var(--text-500); line-height:1.5; }
    .table-container { overflow-x:auto; border-radius:14px; border:1px solid var(--border); }
    .data-table { width:100%; border-collapse:collapse; font-size:13px; text-align:left; }
    .data-table th { background:var(--bg); color:var(--text-500); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.5px; padding:12px 16px; border-bottom:1px solid var(--border); }
    .data-table td { padding:12px 16px; border-bottom:1px solid var(--border); color:var(--text-900); }
    .data-table tr:last-child td { border-bottom:none; }
    .data-table tr:hover td { background:rgba(14,59,46,.02); }
    .conclusion-box { background:var(--surface); border:1px solid var(--border); border-radius:var(--r-card); box-shadow:var(--shadow); padding:28px; margin-bottom:24px; }
    .conclusion-card { display:flex; gap:16px; padding:18px 0; border-bottom:1px solid var(--border); }
    .conclusion-card:last-child { border-bottom:none; padding-bottom:0; }
    .conclusion-badge { width:36px; height:36px; border-radius:50%; background:var(--fk-blue); color:#fff; font-size:14px; font-weight:800; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
    .conclusion-content h4 { font-size:14px; font-weight:700; color:var(--text-900); margin-bottom:4px; }
    .conclusion-content p  { font-size:13px; color:var(--text-500); line-height:1.55; }
    .progress-wrap { margin-bottom:12px; }
    .progress-label { display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; font-size:12.5px; font-weight:600; }
    .progress-label span:first-child { color:var(--text-900); }
    .progress-label span:last-child  { color:var(--text-400); }
    .progress-bar-bg { height:7px; background:var(--bg); border-radius:999px; }
    .progress-bar-fill { height:100%; border-radius:999px; background:linear-gradient(90deg,var(--fk-blue),#5B96F7); }
    .badge-5g { display:inline-flex; align-items:center; gap:4px; font-size:10.5px; font-weight:700; padding:2px 8px; border-radius:999px; background:#E8F0FD; color:#1E4FA5; }
    .badge-4g { display:inline-flex; align-items:center; gap:4px; font-size:10.5px; font-weight:700; padding:2px 8px; border-radius:999px; background:#F0F0F0; color:#606060; }
    .badge-deal { display:inline-flex; align-items:center; gap:4px; font-size:10.5px; font-weight:700; padding:2px 8px; border-radius:999px; background:#E8FDF4; color:#1EA566; }
    .badge-premium { display:inline-flex; align-items:center; gap:4px; font-size:10.5px; font-weight:700; padding:2px 8px; border-radius:999px; background:#FFF0E0; color:#B35A00; }
    @media(max-width:600px){
      .chart-canvas-wrap{height:230px;}
      .chart-canvas-wrap.short{height:200px;}
      .chart-canvas-wrap.tall{height:290px;}
      .chart-box{padding:14px;}
      .report-tab{padding:8px 14px;font-size:12px;}
    }
  </style>
</head>
<body>
<div class="app-shell">

  <!-- SIDEBAR -->
  <nav class="sidebar">
    <div class="sidebar-logo">
      <div class="logo-name">Analysis Hub</div>
      <div class="logo-sub">Data Reports</div>
    </div>
    <div class="nav-section">
      <p class="nav-eyebrow">Menu</p>
      <a href="index.html"     class="nav-item"><span class="nav-label">Dashboard</span></a>
      <a href="reports.html"   class="nav-item active"><span class="nav-label">Reports</span><span class="nav-badge">6</span></a>
      <a href="datasets.html"  class="nav-item"><span class="nav-label">Datasets</span></a>
      <a href="analytics.html" class="nav-item"><span class="nav-label">Analytics</span></a>
    </div>
    <div class="sidebar-spacer"></div>
  </nav>

  <!-- MAIN -->
  <div class="main">

    <!-- TOPBAR -->
    <header class="topbar">
      <div class="search-wrap">
        <input type="text" id="search-input" placeholder="Search phones, specs, brands, prices..." />
        <span class="search-kbd">&#8984;F</span>
      </div>
      <div class="topbar-spacer"></div>
      <div class="user-chip">
        <div class="user-text"><span class="user-name">Yash Vasudeva</span><span class="user-email">yash@analysis.hub</span></div>
        <div class="user-avatar">YV</div>
      </div>
    </header>

    <!-- PAGE HEADER -->
    <div class="page-header">
      <div class="page-header-text">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;flex-wrap:wrap;">
          <span class="badge" style="background:#FFF8E1;color:#B78103;font-weight:700;">E-Commerce</span>
          <span class="badge completed">Completed</span>
          <span style="font-size:12px;color:var(--text-400)">Dataset Source: <a href="https://www.flipkart.com/mobiles" target="_blank" rel="noopener" style="color:var(--green-900);font-weight:700;text-decoration:underline;">Flipkart Marketplace &#8599;</a></span>
        </div>
        <h1>Flipkart Mobile Market &amp; Pricing Analytics (2026)</h1>
        <p>Comprehensive pricing architecture, hardware specification modeling, Ridge L2 machine learning valuation, and consumer sentiment analysis across 98 smartphones and 1.13M+ customer ratings on Flipkart.</p>
      </div>
      <div class="page-header-actions">
        <a href="datasets.html" class="btn-outline">View Dataset</a>
        <a href="reports.html"  class="btn-outline">&#8592; Back to Reports</a>
        <button class="btn-primary" onclick="window.print()">Export Report</button>
      </div>
    </div>

    <!-- CONTENT -->
    <div class="content">

      <!-- KPI ROW -->
      <div class="grid-4">
        <div class="card stat-card hero">
          <div class="stat-label">Ridge Test R&sup2; Score</div>
          <div class="stat-number">0.81</div>
          <div class="stat-pill">5-fold CV goodness of fit (MAE: &#8377;3,031)</div>
        </div>
        <div class="card stat-card">
          <div class="stat-label">Total Consumer Ratings</div>
          <div class="stat-number">1.13M</div>
          <div class="stat-pill blue">1,133,234 ratings &amp; 94,432 reviews</div>
        </div>
        <div class="card stat-card">
          <div class="stat-label">5G Market Penetration</div>
          <div class="stat-number">68.4%</div>
          <div class="stat-pill yellow">67/98 models (+&#8377;7,650 premium)</div>
        </div>
        <div class="card stat-card">
          <div class="stat-label">Full Fit R&sup2; Score</div>
          <div class="stat-number">0.96</div>
          <div class="stat-pill neutral">MAE: &#8377;1,784 | 19 specification features</div>
        </div>
      </div>

      <!-- NAV TABS -->
      <div class="report-tabs">
        <button class="report-tab active" onclick="switchTab(this,'tab-overview')">Market Overview</button>
        <button class="report-tab" onclick="switchTab(this,'tab-hardware')">Hardware &amp; Specs</button>
        <button class="report-tab" onclick="switchTab(this,'tab-valuation')">ML Valuation &amp; Ridge</button>
        <button class="report-tab" onclick="switchTab(this,'tab-engagement')">Consumer Ratings &amp; Reviews</button>
        <button class="report-tab" onclick="switchTab(this,'tab-insights')">Strategic Insights</button>
      </div>

      <!-- ======================================================== -->
      <!-- TAB 1: MARKET OVERVIEW -->
      <!-- ======================================================== -->
      <div id="tab-overview" class="tab-section active">

        <div class="exec-grid">
          <div class="exec-card info">
            <div class="exec-title">Market Catalog Size</div>
            <div class="exec-val">98 Devices</div>
            <div class="exec-desc">Covering 13 active smartphone brands on Flipkart India. 96 in-stock (98%) and 2 out-of-stock. Total catalog GMV value &#8377;2.14M.</div>
          </div>
          <div class="exec-card positive">
            <div class="exec-title">Median Price</div>
            <div class="exec-val">&#8377;16,999</div>
            <div class="exec-desc">Mean price is &#8377;21,819. Range spans from &#8377;8,999 (Budget Entry) up to &#8377;88,999 (Apple iPhone 17 Flagship).</div>
          </div>
          <div class="exec-card warning">
            <div class="exec-title">Catalog Discount Anomaly</div>
            <div class="exec-val">10% vs 34.6%</div>
            <div class="exec-desc">The catalog standardizes a uniform 10% discount tag, yet true computed MRP discounts average 34.6%, reaching 94.5% due to seller inflation.</div>
          </div>
        </div>

        <div class="chart-box">
          <div class="chart-box-header">
            <div>
              <div class="chart-box-title">Brand Portfolio &amp; Average Selling Price (ASP)</div>
              <div class="chart-box-sub">Comparing device count against average retail price across 13 smartphone brands</div>
            </div>
          </div>
          <div class="chart-canvas-wrap tall"><canvas id="chartBrandASP"></canvas></div>
          <div class="caption-box"><strong>Brand Distribution:</strong> Samsung commands the largest catalog footprint (20 devices, 20.4%), followed by emerging player Ai+ (16 devices), vivo (15 devices), and Motorola (12 devices). Premium brands Apple (&#8377;88,999) and Nothing (&#8377;29,999) operate in high-ASP niches.</div>
        </div>

        <div class="chart-grid-2">
          <div class="chart-box">
            <div class="chart-box-header">
              <div>
                <div class="chart-box-title">Price Tier Segmentation</div>
                <div class="chart-box-sub">Distribution of catalog across 4 economic tiers</div>
              </div>
            </div>
            <div class="chart-canvas-wrap short"><canvas id="chartTierDist"></canvas></div>
            <div class="caption-box"><strong>Volume Concentration:</strong> 71.4% of all devices reside under &#8377;25,000 (36 Budget + 34 Mid-Range), reflecting Flipkart's core mass-market demographic in tier-2 and tier-3 Indian cities.</div>
          </div>

          <div class="chart-box">
            <div class="chart-box-header">
              <div>
                <div class="chart-box-title">5G Penetration Across Price Tiers</div>
                <div class="chart-box-sub">Percentage of models equipped with 5G connectivity</div>
              </div>
            </div>
            <div class="chart-canvas-wrap short"><canvas id="chartTier5G"></canvas></div>
            <div class="caption-box"><strong>5G Democratization:</strong> While 5G is near-ubiquitous in the Mid-Range (85.3%) and Flagship (83.3%) tiers, Budget devices (&lt;&#8377;15k) are still 55.6% 4G-only to preserve sub-&#8377;12k price points.</div>
          </div>
        </div>

        <!-- BRAND BENCHMARK TABLE -->
        <div class="chart-box">
          <div class="chart-box-header">
            <div>
              <div class="chart-box-title">Comprehensive Brand Benchmark Matrix</div>
              <div class="chart-box-sub">Volume, pricing, 5G penetration, customer sentiment, and engagement summary</div>
            </div>
          </div>
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Brand</th>
                  <th>Catalog Count</th>
                  <th>Mean Price</th>
                  <th>Median Price</th>
                  <th>5G Share</th>
                  <th>Mean Rating</th>
                  <th>Total Ratings</th>
                  <th>Total Reviews</th>
                  <th>Market Position</th>
                </tr>
              </thead>
              <tbody>
                <tr><td><strong>Samsung</strong></td><td>20 (20.4%)</td><td>&#8377;29,887</td><td>&#8377;23,249</td><td><span class="badge-5g">80.0%</span></td><td><strong>4.28</strong></td><td>212,153</td><td>23,577</td><td>Full-Spectrum Leader</td></tr>
                <tr><td><strong>Ai+</strong></td><td>16 (16.3%)</td><td>&#8377;13,874</td><td>&#8377;13,999</td><td><span class="badge-5g">62.5%</span></td><td>4.16</td><td>100,722</td><td>7,814</td><td>Budget Challenger</td></tr>
                <tr><td><strong>vivo</strong></td><td>15 (15.3%)</td><td>&#8377;23,132</td><td>&#8377;20,499</td><td><span class="badge-5g">93.3%</span></td><td><strong>4.31</strong></td><td>338,152</td><td>18,595</td><td>Volume Engagement King</td></tr>
                <tr><td><strong>Motorola</strong></td><td>12 (12.2%)</td><td>&#8377;20,874</td><td>&#8377;16,999</td><td><span class="badge-4g">16.7%</span></td><td>4.28</td><td>252,767</td><td>20,185</td><td>Battery &amp; Value Favorite</td></tr>
                <tr><td><strong>realme</strong></td><td>8 (8.2%)</td><td>&#8377;21,161</td><td>&#8377;16,249</td><td><span class="badge-5g">62.5%</span></td><td>4.28</td><td>73,784</td><td>5,684</td><td>Youth Performance</td></tr>
                <tr><td><strong>Redmi</strong></td><td>6 (6.1%)</td><td>&#8377;18,324</td><td>&#8377;15,681</td><td><span class="badge-5g">100.0%</span></td><td>4.02</td><td>31,610</td><td>2,787</td><td>All-5G Value</td></tr>
                <tr><td><strong>HMD</strong></td><td>5 (5.1%)</td><td>&#8377;13,399</td><td>&#8377;12,999</td><td><span class="badge-5g">100.0%</span></td><td><strong>4.40</strong></td><td>32,490</td><td>4,660</td><td>Affordable Reliability</td></tr>
                <tr><td><strong>BOLTT</strong></td><td>4 (4.1%)</td><td>&#8377;11,874</td><td>&#8377;11,499</td><td><span class="badge-5g">50.0%</span></td><td>4.07</td><td>14,022</td><td>4,467</td><td>Entry Value</td></tr>
                <tr><td><strong>OnePlus</strong></td><td>4 (4.1%)</td><td>&#8377;22,337</td><td>&#8377;22,680</td><td><span class="badge-5g">75.0%</span></td><td>4.18</td><td>5,045</td><td>448</td><td>Nord / Mid-Tier Focus</td></tr>
                <tr><td><strong>Poco</strong></td><td>3 (3.1%)</td><td>&#8377;18,332</td><td>&#8377;13,999</td><td><span class="badge-5g">100.0%</span></td><td>4.10</td><td>18,283</td><td>2,283</td><td>Spec Aggressor</td></tr>
                <tr><td><strong>Infinix</strong></td><td>3 (3.1%)</td><td>&#8377;21,332</td><td>&#8377;21,999</td><td><span class="badge-4g">33.3%</span></td><td>4.30</td><td>5,669</td><td>646</td><td>Mid-Range Camera</td></tr>
                <tr><td><strong>Apple</strong></td><td>1 (1.0%)</td><td>&#8377;88,999</td><td>&#8377;88,999</td><td><span class="badge-4g">0.0% (LTE)</span></td><td><strong>4.60</strong></td><td>45,072</td><td>3,002</td><td>Ultra-Premium Benchmark</td></tr>
                <tr><td><strong>Nothing</strong></td><td>1 (1.0%)</td><td>&#8377;29,999</td><td>&#8377;29,999</td><td><span class="badge-4g">0.0%</span></td><td>4.40</td><td>3,465</td><td>284</td><td>Design Distinctive</td></tr>
              </tbody>
            </table>
          </div>
          <div class="caption-box"><strong>Key Finding:</strong> vivo and Motorola together account for over 590,000 ratings (52.1% of all platform ratings), establishing them as Flipkart's highest-converting community-driven brands.</div>
        </div>

      </div>

      <!-- ======================================================== -->
      <!-- TAB 2: HARDWARE & SPECS -->
      <!-- ======================================================== -->
      <div id="tab-hardware" class="tab-section">

        <div class="exec-grid">
          <div class="exec-card info">
            <div class="exec-title">Dominant RAM Tier</div>
            <div class="exec-val">4 GB (54.1%)</div>
            <div class="exec-desc">53 phones feature 4GB RAM, followed by 8GB (21 devices), 6GB (19 devices), and 12GB (5 devices). Each step up in RAM adds an estimated &#8377;4,100 to price.</div>
          </div>
          <div class="exec-card positive">
            <div class="exec-title">Modal Battery Capacity</div>
            <div class="exec-val">6,000 mAh</div>
            <div class="exec-desc">30.9% of phones carry 6,000 mAh batteries. Monster batteries (7,000&ndash;10,001 mAh) now represent 26.5% of the total smartphone catalog.</div>
          </div>
          <div class="exec-card gold">
            <div class="exec-title">50 MP Camera Standard</div>
            <div class="exec-val">74.5% Adoption</div>
            <div class="exec-desc">73 out of 98 devices feature a 50MP primary sensor, proving that high megapixel counts have fully migrated from flagships to entry-level devices.</div>
          </div>
        </div>

        <div class="chart-grid-2">
          <div class="chart-box">
            <div class="chart-box-header">
              <div>
                <div class="chart-box-title">RAM &amp; Storage Configuration Matrix</div>
                <div class="chart-box-sub">Number of devices by memory tier (RAM &amp; ROM)</div>
              </div>
            </div>
            <div class="chart-canvas-wrap"><canvas id="chartRAMROM"></canvas></div>
            <div class="caption-box"><strong>Memory Sweet Spot:</strong> 128 GB ROM paired with either 4 GB or 8 GB RAM represents 57.1% of the entire marketplace catalog.</div>
          </div>

          <div class="chart-box">
            <div class="chart-box-header">
              <div>
                <div class="chart-box-title">Battery Capacity vs. Retail Price</div>
                <div class="chart-box-sub">Scatter of battery mAh vs selling price (identifying value monsters)</div>
              </div>
            </div>
            <div class="chart-canvas-wrap"><canvas id="chartBatteryScatter"></canvas></div>
            <div class="caption-box"><strong>Inverse Correlation (r = -0.233):</strong> Budget and mid-tier devices aggressively feature oversized batteries (up to 10,001 mAh) as a primary selling hook, whereas premium flagships prioritize slimness with 3,600&ndash;4,000 mAh packs.</div>
          </div>
        </div>

        <div class="chart-box">
          <div class="chart-box-header">
            <div>
              <div class="chart-box-title">5G vs. 4G Architectural Comparison</div>
              <div class="chart-box-sub">Price, RAM, Storage, and Battery specs contrasted by network generation</div>
            </div>
          </div>
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Network Generation</th>
                  <th>Catalog Count</th>
                  <th>Share</th>
                  <th>Mean Selling Price</th>
                  <th>Median Price</th>
                  <th>Mean RAM</th>
                  <th>Mean ROM</th>
                  <th>Mean Battery</th>
                  <th>Customer Rating</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>5G Enabled</strong></td>
                  <td>67</td>
                  <td><span class="badge-5g">68.4%</span></td>
                  <td><strong>&#8377;24,240</strong></td>
                  <td>&#8377;18,999</td>
                  <td>5.9 GB</td>
                  <td>128.5 GB</td>
                  <td>6,419 mAh</td>
                  <td><strong>4.26 / 5.0</strong></td>
                </tr>
                <tr>
                  <td><strong>4G / LTE Only</strong></td>
                  <td>31</td>
                  <td><span class="badge-4g">31.6%</span></td>
                  <td><strong>&#8377;16,585</strong></td>
                  <td>&#8377;13,999</td>
                  <td>4.9 GB</td>
                  <td>110.5 GB</td>
                  <td>5,745 mAh</td>
                  <td><strong>4.20 / 5.0</strong></td>
                </tr>
                <tr>
                  <td><strong>5G Premium / Uplift</strong></td>
                  <td>+36 models</td>
                  <td>&mdash;</td>
                  <td style="color:var(--green-700);font-weight:700;">+&#8377;7,655 (+46.2%)</td>
                  <td style="color:var(--green-700);font-weight:700;">+&#8377;5,000</td>
                  <td>+1.0 GB</td>
                  <td>+18.0 GB</td>
                  <td>+674 mAh</td>
                  <td>+0.06 stars</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="caption-box"><strong>5G Modernization:</strong> 5G models not only feature updated modem chipsets but also deliver higher base memory (5.9GB vs 4.9GB RAM) and 11.7% larger battery capacity to handle cellular power consumption.</div>
        </div>

      </div>

      <!-- ======================================================== -->
      <!-- TAB 3: ML VALUATION & RIDGE -->
      <!-- ======================================================== -->
      <div id="tab-valuation" class="tab-section">

        <div class="exec-grid">
          <div class="exec-card positive">
            <div class="exec-title">Model Goodness of Fit</div>
            <div class="exec-val">R&sup2; = 0.8057</div>
            <div class="exec-desc">5-fold cross-validated coefficient of determination. Demonstrates that 80.6% of smartphone pricing variance is explainable by hardware and brand attributes.</div>
          </div>
          <div class="exec-card info">
            <div class="exec-title">Cross-Validated Error</div>
            <div class="exec-val">MAE &#8377;3,031</div>
            <div class="exec-desc">Mean Absolute Error across held-out folds. On the full dataset, L2 regularized fit reaches R&sup2; = 0.9649 with a residual error of just &#8377;1,784.</div>
          </div>
          <div class="exec-card gold">
            <div class="exec-title">Leading Price Factor</div>
            <div class="exec-val">Apple (+&#8377;4,844) &amp; RAM</div>
            <div class="exec-desc">Brand equity (+&#8377;4,844 for Apple) and RAM (+&#8377;4,100 per normalized unit) provide the strongest upward price elasticity in the regression model.</div>
          </div>
        </div>

        <div class="chart-grid-2">
          <div class="chart-box">
            <div class="chart-box-header">
              <div>
                <div class="chart-box-title">Ridge Regression Feature Weights (Standardized)</div>
                <div class="chart-box-sub">Marginal impact on retail price (in INR) per standardized unit</div>
              </div>
            </div>
            <div class="chart-canvas-wrap tall"><canvas id="chartWeights"></canvas></div>
            <div class="caption-box"><strong>Feature Impact:</strong> While Apple, RAM, and front camera drive strong positive premiums, display size carries a negative weight (-&#8377;5,494), reflecting that premium flagships (iPhone 17, Galaxy S25) favor ergonomic, high-density 6.2&ndash;6.3" panels over budget 6.7&ndash;6.9" phablet panels.</div>
          </div>

          <div class="chart-box">
            <div class="chart-box-header">
              <div>
                <div class="chart-box-title">Actual vs. Predicted Price Parity</div>
                <div class="chart-box-sub">Regression model predictions plotted against actual retail price</div>
              </div>
            </div>
            <div class="chart-canvas-wrap tall"><canvas id="chartParity"></canvas></div>
            <div class="caption-box"><strong>Parity Diagonal:</strong> Phones below the 45&deg; line are priced below their hardware expectation (undervalued consumer bargains); phones above the line command premium brand markups.</div>
          </div>
        </div>

        <!-- UNDERVALUED VS OVERPRICED BENCHMARKS -->
        <div class="chart-grid-2">
          <div class="chart-box">
            <div class="chart-box-header">
              <div>
                <div class="chart-box-title">&#128293; Top Undervalued Smartphones (Best Value)</div>
                <div class="chart-box-sub">Highest predicted value relative to retail price (Value Ratio &gt; 1.20)</div>
              </div>
            </div>
            <div class="table-container">
              <table class="data-table">
                <thead><tr><th>Phone</th><th>Specs</th><th>Actual</th><th>Predicted</th><th>Surplus Value</th></tr></thead>
                <tbody>
                  <tr>
                    <td><strong>Ai+ Nova 2 Power 5G</strong></td>
                    <td>8GB / 128GB / 7000mAh</td>
                    <td>&#8377;17,999</td>
                    <td>&#8377;23,317</td>
                    <td><span class="badge-deal">+&#8377;5,318 (1.30x)</span></td>
                  </tr>
                  <tr>
                    <td><strong>Ai+ Pulse 2 FE</strong></td>
                    <td>4GB / 64GB / 5000mAh</td>
                    <td>&#8377;9,999</td>
                    <td>&#8377;12,552</td>
                    <td><span class="badge-deal">+&#8377;2,553 (1.26x)</span></td>
                  </tr>
                  <tr>
                    <td><strong>realme Narzo 80 Lite</strong></td>
                    <td>4GB / 64GB / 6300mAh</td>
                    <td>&#8377;13,069</td>
                    <td>&#8377;15,909</td>
                    <td><span class="badge-deal">+&#8377;2,840 (1.22x)</span></td>
                  </tr>
                  <tr>
                    <td><strong>realme Narzo 80 Lite (Blue)</strong></td>
                    <td>4GB / 64GB / 6300mAh</td>
                    <td>&#8377;13,499</td>
                    <td>&#8377;16,283</td>
                    <td><span class="badge-deal">+&#8377;2,784 (1.21x)</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="chart-box">
            <div class="chart-box-header">
              <div>
                <div class="chart-box-title">&#128142; Premium Brand Markup Models (Highest Margin)</div>
                <div class="chart-box-sub">Selling price noticeably exceeding raw specification expectation</div>
              </div>
            </div>
            <div class="table-container">
              <table class="data-table">
                <thead><tr><th>Phone</th><th>Specs</th><th>Actual</th><th>Predicted</th><th>Brand Markup</th></tr></thead>
                <tbody>
                  <tr>
                    <td><strong>Samsung Galaxy M17e</strong></td>
                    <td>4GB / 128GB / 6000mAh</td>
                    <td>&#8377;16,425</td>
                    <td>&#8377;13,012</td>
                    <td><span class="badge-premium">+&#8377;3,413 (0.79x)</span></td>
                  </tr>
                  <tr>
                    <td><strong>vivo T5 5G</strong></td>
                    <td>8GB / 128GB / 7050mAh</td>
                    <td>&#8377;39,999</td>
                    <td>&#8377;33,018</td>
                    <td><span class="badge-premium">+&#8377;6,981 (0.83x)</span></td>
                  </tr>
                  <tr>
                    <td><strong>MOTOROLA Edge 70 Fusion</strong></td>
                    <td>8GB / 128GB / 7000mAh</td>
                    <td>&#8377;30,999</td>
                    <td>&#8377;26,146</td>
                    <td><span class="badge-premium">+&#8377;4,853 (0.84x)</span></td>
                  </tr>
                  <tr>
                    <td><strong>REDMI 15C 5G</strong></td>
                    <td>6GB / 128GB / 6000mAh</td>
                    <td>&#8377;19,879</td>
                    <td>&#8377;17,597</td>
                    <td><span class="badge-premium">+&#8377;2,282 (0.89x)</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </div>

      <!-- ======================================================== -->
      <!-- TAB 4: CONSUMER RATINGS & REVIEWS -->
      <!-- ======================================================== -->
      <div id="tab-engagement" class="tab-section">

        <div class="exec-grid">
          <div class="exec-card positive">
            <div class="exec-title">Catalog Mean Rating</div>
            <div class="exec-val">4.24 / 5.0</div>
            <div class="exec-desc">Robust customer satisfaction baseline. 89% of all devices hold ratings between 4.0 and 4.4; top flagships reach 4.60.</div>
          </div>
          <div class="exec-card info">
            <div class="exec-title">Total Ratings Gathered</div>
            <div class="exec-val">1,133,234</div>
            <div class="exec-desc">Massive verified buyer feedback footprint, validating statistical robustness and high consumer adoption across tracked devices.</div>
          </div>
          <div class="exec-card warning">
            <div class="exec-title">Review-to-Rating Ratio</div>
            <div class="exec-val">8.33%</div>
            <div class="exec-desc">1 out of every 12 buyers who leave a star rating takes the extra time to write a detailed textual review (94,432 written reviews).</div>
          </div>
        </div>

        <div class="chart-box">
          <div class="chart-box-header">
            <div>
              <div class="chart-box-title">Consumer Engagement Volume &amp; Satisfaction by Brand</div>
              <div class="chart-box-sub">Total ratings volume (log scale bubble size) against average customer rating</div>
            </div>
          </div>
          <div class="chart-canvas-wrap tall"><canvas id="chartRatingsBubble"></canvas></div>
          <div class="caption-box"><strong>Volume &amp; Satisfaction:</strong> vivo leads all brands in sheer review volume (338,152 ratings) with a strong 4.31 rating. Apple achieves the highest customer satisfaction (4.60), while Redmi records the lowest average rating (4.02) due to budget software feedback.</div>
        </div>

        <!-- TOP RATED PHONE LEADERBOARD -->
        <div class="chart-box">
          <div class="chart-box-header">
            <div>
              <div class="chart-box-title">High-Engagement Smartphone Leaderboard</div>
              <div class="chart-box-sub">Top 10 smartphones with the highest verified rating volume on Flipkart</div>
            </div>
          </div>
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Smartphone Model</th>
                  <th>Brand</th>
                  <th>Price</th>
                  <th>Customer Rating</th>
                  <th>Total Ratings</th>
                  <th>Total Reviews</th>
                  <th>Engagement Ratio</th>
                </tr>
              </thead>
              <tbody>
                <tr><td>1</td><td><strong>MOTOROLA g57 power 5G (Pantone Corsair)</strong></td><td>Motorola</td><td>&#8377;21,999</td><td><strong style="color:var(--green-700)">4.4 &#9733;</strong></td><td><strong>61,446</strong></td><td>4,406</td><td>7.17%</td></tr>
                <tr><td>2</td><td><strong>MOTOROLA g57 power 5G (Pantone Regatta)</strong></td><td>Motorola</td><td>&#8377;21,999</td><td><strong style="color:var(--green-700)">4.4 &#9733;</strong></td><td><strong>61,446</strong></td><td>4,406</td><td>7.17%</td></tr>
                <tr><td>3</td><td><strong>vivo T4 Lite 5G (Titanium Gold, 128GB)</strong></td><td>vivo</td><td>&#8377;20,999</td><td><strong style="color:var(--green-700)">4.3 &#9733;</strong></td><td><strong>49,970</strong></td><td>2,383</td><td>4.77%</td></tr>
                <tr><td>4</td><td><strong>vivo T4 Lite 5G (Prism Blue, 128GB)</strong></td><td>vivo</td><td>&#8377;17,999</td><td><strong style="color:var(--green-700)">4.3 &#9733;</strong></td><td><strong>47,824</strong></td><td>2,252</td><td>4.71%</td></tr>
                <tr><td>5</td><td><strong>vivo T4 Lite 5G (Prism Blue, 64GB)</strong></td><td>vivo</td><td>&#8377;15,999</td><td><strong style="color:var(--green-700)">4.3 &#9733;</strong></td><td><strong>47,824</strong></td><td>2,252</td><td>4.71%</td></tr>
                <tr><td>6</td><td><strong>Apple iPhone 17 (Black, 256GB)</strong></td><td>Apple</td><td>&#8377;88,999</td><td><strong style="color:var(--green-700)">4.6 &#9733;</strong></td><td><strong>45,072</strong></td><td>3,002</td><td>6.66%</td></tr>
                <tr><td>7</td><td><strong>Ai+ Pulse 2 (Green, 64GB)</strong></td><td>Ai+</td><td>&#8377;10,999</td><td>4.2 &#9733;</td><td><strong>33,702</strong></td><td>2,674</td><td>7.93%</td></tr>
                <tr><td>8</td><td><strong>realme P4 Power 5G (TransOrange)</strong></td><td>realme</td><td>&#8377;29,999</td><td>4.2 &#9733;</td><td><strong>21,957</strong></td><td>1,727</td><td>7.87%</td></tr>
                <tr><td>9</td><td><strong>Samsung Galaxy S25 5G Snapdragon (128GB)</strong></td><td>Samsung</td><td>&#8377;54,999</td><td><strong style="color:var(--green-700)">4.6 &#9733;</strong></td><td><strong>17,255</strong></td><td>1,940</td><td>11.24%</td></tr>
                <tr><td>10</td><td><strong>HMD Vibe2 5G (Cosmic Lavender)</strong></td><td>HMD</td><td>&#8377;12,999</td><td>4.4 &#9733;</td><td><strong>9,398</strong></td><td>1,228</td><td>13.07%</td></tr>
              </tbody>
            </table>
          </div>
          <div class="caption-box"><strong>Engagement Depth:</strong> Premium smartphones like Galaxy S25 (11.24%) and HMD Vibe2 (13.07%) exhibit significantly higher review-to-rating ratios, indicating that buyers in these categories are highly motivated to write detailed feedback.</div>
        </div>

      </div>

      <!-- ======================================================== -->
      <!-- TAB 5: STRATEGIC INSIGHTS -->
      <!-- ======================================================== -->
      <div id="tab-insights" class="tab-section">

        <div class="conclusion-box">
          <div style="margin-bottom:20px;">
            <div style="font-size:18px;font-weight:800;color:var(--text-900);">Key Analytical Takeaways &amp; Strategic Implications</div>
            <div style="font-size:13px;color:var(--text-400);">Synthesized market findings from exploratory data analysis and Ridge L2 econometric regression</div>
          </div>

          <div class="conclusion-card">
            <div class="conclusion-badge">1</div>
            <div class="conclusion-content">
              <h4>The 5G Transition Reaches Critical Mass (68.4% Penetration)</h4>
              <p>5G capability is no longer reserved for premium models. With 68.4% of catalog models 5G-ready and a standard &#8377;7,650 price premium over 4G units, the mainstream sweet spot is now between &#8377;15,000 and &#8377;22,000. Manufacturers lacking sub-&#8377;16k 5G models risk rapid market obsolescence on Flipkart.</p>
            </div>
          </div>

          <div class="conclusion-card">
            <div class="conclusion-badge">2</div>
            <div class="conclusion-content">
              <h4>RAM Capacity Is the #1 Hardware Pricing Anchor (&#8377;4,100 per Tier)</h4>
              <p>Econometric regression proves that RAM capacity carries the highest non-brand coefficient (+&#8377;4,100 per normalized unit, Pearson r = +0.775 with price). Consumers and sellers treat RAM as the primary proxy for device longevity, far outweighing megapixel counts or raw processor clock speeds.</p>
            </div>
          </div>

          <div class="conclusion-card">
            <div class="conclusion-badge">3</div>
            <div class="conclusion-content">
              <h4>The "Battery Monster" Paradox: Inverse Price Elasticity</h4>
              <p>While one might assume larger batteries cost more, battery capacity is negatively correlated with price (r = -0.233). Budget challengers (realme, Ai+, Motorola) pack 6,000&ndash;10,001 mAh power plants into &#8377;10k&ndash;&#8377;20k frames to win battery benchmarks, whereas flagships prioritize lightweight ergonomics and rapid wireless charging with 3,600&ndash;4,000 mAh cells.</p>
            </div>
          </div>

          <div class="conclusion-card">
            <div class="conclusion-badge">4</div>
            <div class="conclusion-content">
              <h4>Catalog Discount vs. Real Markdown Asymmetry</h4>
              <p>Flipkart's scraped catalog lists a fixed 10% discount across 100% of rows. However, ground-truth MRP comparisons show actual discounts averaging 34.6%, with extreme outlier MRP markups reaching &#8377;214,999 on &#8377;12,999 phones (94.5% fictitious markdown). Regulatory oversight and marketplace transparency algorithms must address artificial anchor-price inflation.</p>
            </div>
          </div>

          <div class="conclusion-card">
            <div class="conclusion-badge">5</div>
            <div class="conclusion-content">
              <h4>Consumer Rating Divergence Across Price Segments</h4>
              <p>Customer rating is positively correlated with retail price (r = +0.637). Flagship devices achieve an average rating of 4.58/5.0, whereas budget devices average 4.17/5.0. This gap is driven not only by build quality but also by aggressive advertising and bloatware present in sub-&#8377;15k OS builds that degrades user experience.</p>
            </div>
          </div>

          <div class="conclusion-card">
            <div class="conclusion-badge">6</div>
            <div class="conclusion-content">
              <h4>Identified Market Arbitrage: Undervalued 8GB Challengers</h4>
              <p>The Ridge regression valuation identifies devices like the <em>Ai+ Nova 2 Power 5G</em> (8GB/128GB/7000mAh at &#8377;17,999) as trading 30% below their spec-implied valuation (&#8377;23,317). Smart shoppers and value-oriented consumers can capture over &#8377;5,300 in surplus utility by targeting these emerging tier-2 challenger models.</p>
            </div>
          </div>
        </div>

        <div class="chart-box">
          <div class="chart-box-header">
            <div>
              <div class="chart-box-title">Econometric Elasticity Weights (Ridge L2 Model)</div>
              <div class="chart-box-sub">Normalized feature impact progress bars on smartphone retail valuation</div>
            </div>
          </div>
          <div>
            <div class="progress-wrap"><div class="progress-label"><span>Apple Brand Equity</span><span>+&#8377;4,844</span></div><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:100%"></div></div></div>
            <div class="progress-wrap"><div class="progress-label"><span>RAM Memory Capacity</span><span>+&#8377;4,100</span></div><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:84.6%"></div></div></div>
            <div class="progress-wrap"><div class="progress-label"><span>Front Camera Resolution</span><span>+&#8377;2,577</span></div><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:53.2%"></div></div></div>
            <div class="progress-wrap"><div class="progress-label"><span>OnePlus Brand Identity</span><span>+&#8377;2,242</span></div><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:46.3%"></div></div></div>
            <div class="progress-wrap"><div class="progress-label"><span>vivo Brand Equity</span><span>+&#8377;2,176</span></div><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:44.9%"></div></div></div>
            <div class="progress-wrap"><div class="progress-label"><span>Samsung Brand Equity</span><span>+&#8377;1,929</span></div><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:39.8%"></div></div></div>
            <div class="progress-wrap"><div class="progress-label"><span>5G Network Connectivity</span><span>+&#8377;1,408</span></div><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:29.1%"></div></div></div>
            <div class="progress-wrap"><div class="progress-label"><span>Internal Storage (ROM)</span><span>+&#8377;1,374</span></div><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:28.4%"></div></div></div>
            <div class="progress-wrap"><div class="progress-label"><span>Battery Capacity (mAh)</span><span>+&#8377;292</span></div><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:6.0%"></div></div></div>
          </div>
        </div>

      </div>

    </div><!-- /content -->
  </div><!-- /main -->
</div><!-- /app-shell -->

<script src="reports-data.js"></script>
<script src="hub.js"></script>
<script>
/* ── TAB SWITCHER ─────────────────────────────────────── */
function switchTab(btn, targetId) {
  document.querySelectorAll('.report-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-section').forEach(s => s.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById(targetId).classList.add('active');
}

/* ── CHART BASE CONFIG ────────────────────────────────── */
const FONT = { family: 'Plus Jakarta Sans', weight: 600, size: 11.5 };
const GRID_COLOR = '#ECEEED';
const BASE_OPTS = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { position: 'top', labels: { font: FONT } } },
  scales: {
    x: { grid: { color: GRID_COLOR }, ticks: { font: FONT } },
    y: { grid: { color: GRID_COLOR }, ticks: { font: FONT } }
  }
};

/* ── 1. BRAND ASP & DEVICE COUNT ──────────────────────── */
new Chart(document.getElementById('chartBrandASP'), {
  type: 'bar',
  data: {
    labels: ['Samsung', 'Ai+', 'vivo', 'Motorola', 'realme', 'Redmi', 'HMD', 'BOLTT', 'OnePlus', 'Poco', 'Infinix', 'Apple', 'Nothing'],
    datasets: [
      {
        type: 'bar',
        label: 'Device Count',
        data: [20, 16, 15, 12, 8, 6, 5, 4, 4, 3, 3, 1, 1],
        backgroundColor: '#2874F0',
        borderRadius: 6,
        yAxisID: 'yCount'
      },
      {
        type: 'line',
        label: 'Average Price (INR)',
        data: [29887, 13874, 23132, 20874, 21161, 18324, 13399, 11874, 22337, 18332, 21332, 88999, 29999],
        borderColor: '#FB641B',
        backgroundColor: '#FB641B',
        borderWidth: 2.5,
        pointRadius: 5,
        pointHoverRadius: 7,
        yAxisID: 'yPrice'
      }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: 'top', labels: { font: FONT } } },
    scales: {
      x: { grid: { color: GRID_COLOR }, ticks: { font: FONT } },
      yCount: { type: 'linear', position: 'left', title: { display: true, text: 'Catalog Count', font: FONT }, grid: { color: GRID_COLOR } },
      yPrice: { type: 'linear', position: 'right', title: { display: true, text: 'Avg Price (₹)', font: FONT }, grid: { drawOnChartArea: false } }
    }
  }
});

/* ── 2. PRICE TIER DOUGHNUT ───────────────────────────── */
new Chart(document.getElementById('chartTierDist'), {
  type: 'doughnut',
  data: {
    labels: ['Budget (<15k)', 'Mid-Range (15k-25k)', 'Upper Mid (25k-45k)', 'Flagship (>=45k)'],
    datasets: [{
      data: [36, 34, 22, 6],
      backgroundColor: ['#2874F0', '#00A859', '#FFC200', '#FB641B'],
      borderWidth: 2,
      borderColor: '#fff'
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: 'bottom', labels: { font: FONT } } }
  }
});

/* ── 3. TIER 5G PENETRATION ───────────────────────────── */
new Chart(document.getElementById('chartTier5G'), {
  type: 'bar',
  data: {
    labels: ['Budget (<15k)', 'Mid-Range (15k-25k)', 'Upper Mid (25k-45k)', 'Flagship (>=45k)'],
    datasets: [
      {
        label: '5G Share (%)',
        data: [44.4, 85.3, 77.3, 83.3],
        backgroundColor: '#2874F0',
        borderRadius: 6
      },
      {
        label: '4G Share (%)',
        data: [55.6, 14.7, 22.7, 16.7],
        backgroundColor: '#D1D5DB',
        borderRadius: 6
      }
    ]
  },
  options: {
    ...BASE_OPTS,
    scales: {
      x: { stacked: true, grid: { color: GRID_COLOR }, ticks: { font: FONT } },
      y: { stacked: true, max: 100, title: { display: true, text: 'Percentage (%)', font: FONT }, grid: { color: GRID_COLOR } }
    }
  }
});

/* ── 4. RAM & STORAGE MATRIX ──────────────────────────── */
new Chart(document.getElementById('chartRAMROM'), {
  type: 'bar',
  data: {
    labels: ['4 GB RAM', '6 GB RAM', '8 GB RAM', '12 GB RAM'],
    datasets: [
      { label: '64 GB ROM',  data: [31, 0, 0, 0], backgroundColor: '#8FD6B4', borderRadius: 4 },
      { label: '128 GB ROM', data: [22, 19, 13, 2], backgroundColor: '#2874F0', borderRadius: 4 },
      { label: '256 GB ROM', data: [0, 0, 8, 2], backgroundColor: '#FFC200', borderRadius: 4 },
      { label: '512 GB ROM', data: [0, 0, 0, 1], backgroundColor: '#FB641B', borderRadius: 4 }
    ]
  },
  options: {
    ...BASE_OPTS,
    scales: {
      x: { stacked: true, grid: { color: GRID_COLOR }, ticks: { font: FONT } },
      y: { stacked: true, title: { display: true, text: 'Device Count', font: FONT }, grid: { color: GRID_COLOR } }
    }
  }
});

/* ── 5. BATTERY VS PRICE SCATTER ──────────────────────── */
new Chart(document.getElementById('chartBatteryScatter'), {
  type: 'scatter',
  data: {
    datasets: [
      {
        label: 'Smartphones (mAh vs Price)',
        data: [
          { x: 6000, y: 9999 }, { x: 6000, y: 12999 }, { x: 6000, y: 14499 }, { x: 4000, y: 54999 },
          { x: 5000, y: 12999 }, { x: 6000, y: 15999 }, { x: 4000, y: 54999 }, { x: 5000, y: 12999 },
          { x: 5000, y: 17999 }, { x: 5000, y: 10999 }, { x: 6000, y: 14999 }, { x: 3600, y: 88999 },
          { x: 6000, y: 17999 }, { x: 6000, y: 16999 }, { x: 6000, y: 20999 }, { x: 7000, y: 21999 },
          { x: 10001, y: 29999 }, { x: 7000, y: 30999 }, { x: 7050, y: 39999 }, { x: 6500, y: 22999 },
          { x: 6300, y: 13069 }, { x: 6300, y: 13499 }, { x: 7000, y: 17999 }, { x: 8000, y: 24999 }
        ],
        backgroundColor: 'rgba(40, 116, 240, 0.75)',
        borderColor: '#2874F0',
        pointRadius: 6,
        pointHoverRadius: 9
      }
    ]
  },
  options: {
    ...BASE_OPTS,
    scales: {
      x: { title: { display: true, text: 'Battery Capacity (mAh)', font: FONT }, grid: { color: GRID_COLOR }, min: 3000, max: 10500 },
      y: { title: { display: true, text: 'Selling Price (₹)', font: FONT }, grid: { color: GRID_COLOR } }
    }
  }
});

/* ── 6. RIDGE FEATURE WEIGHTS ─────────────────────────── */
new Chart(document.getElementById('chartWeights'), {
  type: 'bar',
  data: {
    labels: ['Apple Brand', 'RAM Capacity', 'Front Camera', 'OnePlus', 'vivo', 'Samsung', 'Redmi', 'realme', '5G Modem', 'ROM Storage', 'Battery mAh', 'Rear Cam MP', 'BOLTT', 'Display Size'],
    datasets: [{
      label: 'Price Impact (INR / normalized unit)',
      data: [4843.6, 4100.0, 2576.7, 2242.0, 2175.8, 1929.4, 1796.4, 1715.1, 1407.8, 1374.4, 291.5, -190.4, -1358.6, -5493.9],
      backgroundColor: [
        '#2874F0', '#2874F0', '#2874F0', '#00A859', '#00A859', '#00A859', '#00A859', '#00A859', '#FFC200', '#FFC200', '#9CA3AF', '#EF4444', '#EF4444', '#DC2626'
      ],
      borderRadius: 6
    }]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      x: { grid: { color: GRID_COLOR }, ticks: { font: FONT }, title: { display: true, text: 'Marginal Impact (INR)', font: FONT } },
      y: { grid: { color: GRID_COLOR }, ticks: { font: FONT } }
    }
  }
});

/* ── 7. ACTUAL VS PREDICTED PARITY ────────────────────── */
new Chart(document.getElementById('chartParity'), {
  type: 'scatter',
  data: {
    datasets: [
      {
        label: 'Smartphones (Actual vs Pred)',
        data: [
          { x: 9999, y: 11200 }, { x: 12999, y: 13800 }, { x: 14499, y: 15100 }, { x: 54999, y: 53100 },
          { x: 15999, y: 17200 }, { x: 21999, y: 22800 }, { x: 17999, y: 23317 }, { x: 88999, y: 86400 },
          { x: 16425, y: 13012 }, { x: 39999, y: 33018 }, { x: 30999, y: 26146 }, { x: 19879, y: 17597 },
          { x: 13069, y: 15909 }, { x: 29999, y: 31200 }, { x: 20999, y: 20400 }, { x: 60999, y: 58900 }
        ],
        backgroundColor: '#2874F0',
        pointRadius: 6
      },
      {
        type: 'line',
        label: 'Ideal Parity (y = x)',
        data: [{ x: 8000, y: 8000 }, { x: 90000, y: 90000 }],
        borderColor: '#EF4444',
        borderDash: [5, 5],
        borderWidth: 2,
        pointRadius: 0,
        fill: false
      }
    ]
  },
  options: {
    ...BASE_OPTS,
    scales: {
      x: { title: { display: true, text: 'Actual Retail Price (₹)', font: FONT }, grid: { color: GRID_COLOR }, min: 5000, max: 95000 },
      y: { title: { display: true, text: 'Ridge Predicted Price (₹)', font: FONT }, grid: { color: GRID_COLOR }, min: 5000, max: 95000 }
    }
  }
});

/* ── 8. RATINGS BUBBLE CHART ──────────────────────────── */
new Chart(document.getElementById('chartRatingsBubble'), {
  type: 'bubble',
  data: {
    datasets: [
      { label: 'Samsung', data: [{ x: 29887, y: 4.28, r: 18 }], backgroundColor: 'rgba(40, 116, 240, 0.7)' },
      { label: 'vivo',    data: [{ x: 23132, y: 4.31, r: 24 }], backgroundColor: 'rgba(0, 168, 89, 0.7)' },
      { label: 'Motorola',data: [{ x: 20874, y: 4.28, r: 20 }], backgroundColor: 'rgba(251, 100, 27, 0.7)' },
      { label: 'Ai+',     data: [{ x: 13874, y: 4.16, r: 14 }], backgroundColor: 'rgba(155, 89, 212, 0.7)' },
      { label: 'realme',  data: [{ x: 21161, y: 4.28, r: 12 }], backgroundColor: 'rgba(255, 194, 0, 0.8)' },
      { label: 'Apple',   data: [{ x: 88999, y: 4.60, r: 16 }], backgroundColor: 'rgba(23, 35, 55, 0.8)' },
      { label: 'HMD',     data: [{ x: 13399, y: 4.40, r: 10 }], backgroundColor: 'rgba(30, 111, 165, 0.7)' },
      { label: 'Redmi',   data: [{ x: 18324, y: 4.02, r: 10 }], backgroundColor: 'rgba(165, 30, 53, 0.7)' }
    ]
  },
  options: {
    ...BASE_OPTS,
    scales: {
      x: { title: { display: true, text: 'Mean Price (₹)', font: FONT }, grid: { color: GRID_COLOR } },
      y: { title: { display: true, text: 'Customer Rating (Stars)', font: FONT }, grid: { color: GRID_COLOR }, min: 3.9, max: 4.7 }
    }
  }
});
</script>
</body>
</html>
"""

with open('flipkart_report.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('flipkart_report.html generated successfully!')
