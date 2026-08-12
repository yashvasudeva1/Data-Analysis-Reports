content = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>IPL Performance Analysis (2019-2026) - Analysis Hub</title>
  <meta name="description" content="Comprehensive IPL analysis covering batting, bowling, boundaries, milestones, player arcs, and franchise dependencies across 5 tracked seasons." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <link rel="stylesheet" href="hub.css" />
  <style>
    :root {
      --ipl-orange: #E8570D;
      --ipl-purple: #7B2D8B;
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
    .chart-box { background:var(--surface); border:1px solid var(--border); border-radius:var(--r-card); box-shadow:var(--shadow); padding:22px; margin-bottom:24px; }
    .chart-box-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:16px; flex-wrap:wrap; gap:12px; }
    .chart-box-title { font-size:15px; font-weight:700; color:var(--text-900); }
    .chart-box-sub { font-size:12px; color:var(--text-400); margin-top:2px; }
    .chart-canvas-wrap { position:relative; height:320px; width:100%; }
    .chart-canvas-wrap.short { height:240px; }
    .chart-canvas-wrap.tall  { height:380px; }
    .chart-canvas-wrap.xtall { height:440px; }
    .chart-grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:20px; }
    @media(max-width:900px){.chart-grid-2{grid-template-columns:1fr;}}
    .caption-box { margin-top:14px; padding:12px 16px; background:var(--bg); border-radius:12px; font-size:12.5px; color:var(--text-500); line-height:1.5; }
    .caption-box strong { color:var(--text-900); }
    .exec-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-bottom:24px; }
    @media(max-width:900px){.exec-grid{grid-template-columns:1fr;}}
    .exec-card { background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:18px 20px; display:flex; flex-direction:column; gap:6px; box-shadow:var(--shadow); }
    .exec-card.warning  { border-left:4px solid #C05621; }
    .exec-card.positive { border-left:4px solid var(--green-500); }
    .exec-card.info     { border-left:4px solid #2B6CB0; }
    .exec-card.orange   { border-left:4px solid var(--ipl-orange); }
    .exec-card.purple   { border-left:4px solid var(--ipl-purple); }
    .exec-title { font-size:13px; font-weight:700; color:var(--text-900); }
    .exec-val   { font-size:22px; font-weight:800; color:var(--text-900); font-variant-numeric:tabular-nums; }
    .exec-desc  { font-size:12.5px; color:var(--text-500); line-height:1.5; }
    .table-container { overflow-x:auto; border-radius:14px; border:1px solid var(--border); }
    .data-table { width:100%; border-collapse:collapse; font-size:13px; text-align:left; }
    .data-table th { background:var(--bg); color:var(--text-500); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.5px; padding:12px 16px; border-bottom:1px solid var(--border); }
    .data-table td { padding:12px 16px; border-bottom:1px solid var(--border); color:var(--text-900); }
    .data-table tr:last-child td { border-bottom:none; }
    .data-table tr:hover td { background:rgba(14,59,46,.02); }
    .rank-badge { display:inline-flex; align-items:center; justify-content:center; width:24px; height:24px; border-radius:50%; font-size:11px; font-weight:800; background:var(--bg); color:var(--text-500); }
    .rank-badge.gold   { background:#FFF0C2; color:#A07800; }
    .rank-badge.silver { background:#F0F0F0; color:#606060; }
    .rank-badge.bronze { background:#FFE8D8; color:#8B3A00; }
    .team-chip { display:inline-flex; align-items:center; gap:5px; font-size:11px; font-weight:700; padding:2px 8px; border-radius:999px; }
    .team-mi   { background:#E8F0FD; color:#003087; }
    .team-csk  { background:#FFF8D6; color:#9A6600; }
    .team-rcb  { background:#FDE8E8; color:#A51E1E; }
    .team-kkr  { background:#F0E8FD; color:#5B1EA5; }
    .team-rr   { background:#FDE8F8; color:#A51E8B; }
    .team-pbks { background:#FDE8E8; color:#A51E35; }
    .team-dc   { background:#E8F0FD; color:#003087; }
    .team-srh  { background:#FFF0E0; color:#B35A00; }
    .team-gt   { background:#E8F4FD; color:#00427A; }
    .team-lsg  { background:#E8FDF4; color:#007A50; }
    .narrative-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:24px; }
    @media(max-width:800px){.narrative-grid{grid-template-columns:1fr;}}
    .narrative-card { background:var(--surface); border:1px solid var(--border); border-radius:16px; padding:20px; box-shadow:var(--shadow); }
    .narrative-card .nar-icon { font-size:24px; margin-bottom:10px; }
    .narrative-card .nar-title { font-size:14px; font-weight:800; color:var(--text-900); margin-bottom:6px; }
    .narrative-card .nar-sub { font-size:12.5px; color:var(--text-500); line-height:1.55; }
    .narrative-card.highlight { background:var(--green-900); border-color:var(--green-700); }
    .narrative-card.highlight .nar-title { color:#fff; }
    .narrative-card.highlight .nar-sub   { color:rgba(255,255,255,.65); }
    .conclusion-box { background:var(--surface); border:1px solid var(--border); border-radius:var(--r-card); box-shadow:var(--shadow); padding:28px; margin-bottom:24px; }
    .conclusion-card { display:flex; gap:16px; padding:18px 0; border-bottom:1px solid var(--border); }
    .conclusion-card:last-child { border-bottom:none; padding-bottom:0; }
    .conclusion-badge { width:36px; height:36px; border-radius:50%; background:var(--green-900); color:#fff; font-size:14px; font-weight:800; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
    .conclusion-content h4 { font-size:14px; font-weight:700; color:var(--text-900); margin-bottom:4px; }
    .conclusion-content p  { font-size:13px; color:var(--text-500); line-height:1.55; }
    .progress-wrap { margin-bottom:12px; }
    .progress-label { display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; font-size:12.5px; font-weight:600; }
    .progress-label span:first-child { color:var(--text-900); }
    .progress-label span:last-child  { color:var(--text-400); }
    .progress-bar-bg { height:7px; background:var(--bg); border-radius:999px; }
    .progress-bar-fill { height:100%; border-radius:999px; background:linear-gradient(90deg,var(--green-700),var(--green-500)); }
    @media(max-width:600px){
      .chart-canvas-wrap{height:220px;}
      .chart-canvas-wrap.short{height:180px;}
      .chart-canvas-wrap.tall{height:270px;}
      .chart-canvas-wrap.xtall{height:300px;}
      .chart-box{padding:14px;}
      .report-tab{padding:8px 14px;font-size:12px;}
    }
  </style>
</head>
<body>
<div class="app-shell">
  <!-- SIDEBAR -->
  <nav class="sidebar">
    <div class="sidebar-logo"><div class="logo-name">Analysis Hub</div><div class="logo-sub">Data Reports</div></div>
    <div class="nav-section">
      <p class="nav-eyebrow">Menu</p>
      <a href="index.html"     class="nav-item"><span class="nav-label">Dashboard</span></a>
      <a href="reports.html"   class="nav-item active"><span class="nav-label">Reports</span><span class="nav-badge">4</span></a>
      <a href="datasets.html"  class="nav-item"><span class="nav-label">Datasets</span></a>
      <a href="analytics.html" class="nav-item"><span class="nav-label">Analytics</span></a>
    </div>
    <div class="sidebar-divider"></div>
    <div class="nav-section">
      <p class="nav-eyebrow">General</p>
      <a href="settings.html" class="nav-item"><span class="nav-label">Settings</span></a>
      <a href="help.html"     class="nav-item"><span class="nav-label">Help</span></a>
    </div>
    <div class="sidebar-spacer"></div>
    <div class="sidebar-promo">
      <p class="promo-label">Quick Action</p>
      <p class="promo-title">Explore the IPL</p>
      <p class="promo-sub">8 seasons of cricket data - batting, bowling, milestones &amp; franchise insights.</p>
      <a href="reports.html" class="promo-btn">Back to Reports</a>
    </div>
  </nav>
  <!-- MAIN -->
  <div class="main">
    <!-- TOPBAR -->
    <header class="topbar">
      <button class="mobile-menu-btn" id="mobileMenuBtn">&#9776;</button>
      <div class="search-wrap">
        <input type="text" id="search-input" placeholder="Search players, teams, metrics..." />
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
          <span class="badge" style="background:#E8F0FD;color:#1E4FA5;font-weight:700;">Sports</span>
          <span class="badge completed">Completed</span>
          <span style="font-size:12px;color:var(--text-400)">Dataset Source: <a href="https://www.espncricinfo.com" target="_blank" rel="noopener" style="color:var(--green-900);font-weight:700;text-decoration:underline;">ESPNcricinfo IPL Records &#8599;</a></span>
        </div>
        <h1>IPL Performance Analysis (2019-2026)</h1>
        <p>Comprehensive multi-season analysis of batting, bowling, boundaries, milestones, player arcs, and franchise dependencies across the Indian Premier League.</p>
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
          <div class="stat-label">All-Time Top Scorer (IPL)</div>
          <div class="stat-number">9,336</div>
          <div class="stat-pill">Virat Kohli &mdash; 283 matches</div>
        </div>
        <div class="card stat-card">
          <div class="stat-label">All-Time Top Wicket-Taker</div>
          <div class="stat-number">226</div>
          <div class="stat-pill neutral">Bhuvneshwar Kumar &mdash; 206 matches</div>
        </div>
        <div class="card stat-card">
          <div class="stat-label">Most Sixes (All-Time)</div>
          <div class="stat-number">357</div>
          <div class="stat-pill orange">Chris Gayle &mdash; The Universe Boss</div>
        </div>
        <div class="card stat-card">
          <div class="stat-label">Most Centuries (All-Time)</div>
          <div class="stat-number">9</div>
          <div class="stat-pill blue">Virat Kohli &mdash; 275 innings</div>
        </div>
      </div>
      <!-- NAV TABS -->
      <div class="report-tabs">
        <button class="report-tab active" onclick="switchTab(this,'tab-batting')">&#127959; Batting Records</button>
        <button class="report-tab" onclick="switchTab(this,'tab-bowling')">&#127919; Bowling Records</button>
        <button class="report-tab" onclick="switchTab(this,'tab-boundaries')">&#128165; Boundaries</button>
        <button class="report-tab" onclick="switchTab(this,'tab-seasons')">&#128197; Season Tracker</button>
        <button class="report-tab" onclick="switchTab(this,'tab-arcs')">&#128640; Player Arcs</button>
        <button class="report-tab" onclick="switchTab(this,'tab-franchise')">&#127942; Franchise Analysis</button>
        <button class="report-tab" onclick="switchTab(this,'tab-conclusions')">&#128203; Conclusions</button>
      </div>

      <!-- TAB: BATTING -->
      <div id="tab-batting" class="tab-section active">
        <div class="exec-grid">
          <div class="exec-card positive">
            <div class="exec-title">All-Time Run King</div>
            <div class="exec-val">Virat Kohli &mdash; 9,336</div>
            <div class="exec-desc">283 matches, avg 40.42, SR 134.80. 9 centuries, 68 fifties &mdash; for Royal Challengers Bengaluru.</div>
          </div>
          <div class="exec-card info">
            <div class="exec-title">Most Innings Played</div>
            <div class="exec-val">Rohit Sharma &mdash; 276 inn.</div>
            <div class="exec-desc">281 matches, 7,329 runs at avg 29.91. The most experienced batter in IPL history with Mumbai Indians.</div>
          </div>
          <div class="exec-card warning">
            <div class="exec-title">Best Batting Average (1000+ runs)</div>
            <div class="exec-val">KL Rahul &mdash; 46.15</div>
            <div class="exec-desc">159 matches, 5,815 runs, SR 139.15. 6 centuries and 45 half-centuries &mdash; the most consistent IPL batter.</div>
          </div>
        </div>
        <div class="chart-box">
          <div class="chart-box-header"><div><div class="chart-box-title">All-Time Top 10 Run Scorers</div><div class="chart-box-sub">Total career IPL runs &mdash; all seasons combined</div></div></div>
          <div class="chart-canvas-wrap tall"><canvas id="topRunsChart"></canvas></div>
          <div class="caption-box"><strong>The Kohli-Rohit Duopoly:</strong> Virat Kohli (9,336) and Rohit Sharma (7,329) together account for over 16,600 IPL runs. Shikhar Dhawan, despite retiring in 2024, sits third at 6,769 across 222 matches.</div>
        </div>
        <div class="chart-grid-2">
          <div class="chart-box">
            <div class="chart-box-header"><div><div class="chart-box-title">Batting Average &mdash; Top 10</div><div class="chart-box-sub">Average runs per dismissal</div></div></div>
            <div class="chart-canvas-wrap"><canvas id="avgChart"></canvas></div>
          </div>
          <div class="chart-box">
            <div class="chart-box-header"><div><div class="chart-box-title">Strike Rate &mdash; Top 10 Scorers</div><div class="chart-box-sub">Runs per 100 balls faced</div></div></div>
            <div class="chart-canvas-wrap"><canvas id="srChart"></canvas></div>
          </div>
        </div>
        <div class="chart-box">
          <div class="chart-box-header"><div><div class="chart-box-title">All-Time Batting Leaderboard</div><div class="chart-box-sub">Comprehensive batting statistics for top 10 run-scorers</div></div></div>
          <div class="table-container">
            <table class="data-table">
              <thead><tr><th>#</th><th>Player</th><th>Team</th><th>Mat</th><th>Inn</th><th>Runs</th><th>Avg</th><th>SR</th><th>100s</th><th>50s</th><th>HS</th></tr></thead>
              <tbody id="battingTableBody"></tbody>
            </table>
          </div>
          <div class="caption-box"><strong>Note:</strong> Team shown is the player's most recent IPL franchise. Stats are derived from ESPNcricinfo all-time IPL records.</div>
        </div>
        <div class="chart-grid-2">
          <div class="chart-box">
            <div class="chart-box-header"><div><div class="chart-box-title">Most IPL Centuries</div><div class="chart-box-sub">All-time T20 hundreds in IPL</div></div></div>
            <div class="chart-canvas-wrap short"><canvas id="centuriesChart"></canvas></div>
          </div>
          <div class="chart-box">
            <div class="chart-box-header"><div><div class="chart-box-title">Most IPL Half-Centuries</div><div class="chart-box-sub">All-time fifties+ in IPL</div></div></div>
            <div class="chart-canvas-wrap short"><canvas id="fiftiesChart"></canvas></div>
          </div>
        </div>
      </div>

      <!-- TAB: BOWLING -->
      <div id="tab-bowling" class="tab-section">
        <div class="exec-grid">
          <div class="exec-card positive">
            <div class="exec-title">All-Time Wicket Leader</div>
            <div class="exec-val">Bhuvneshwar Kumar &mdash; 226</div>
            <div class="exec-desc">206 matches, avg 26.16, eco 7.71. Best: 5/19 for Royal Challengers Bengaluru.</div>
          </div>
          <div class="exec-card info">
            <div class="exec-title">Best Economy (200+ wkts)</div>
            <div class="exec-val">Sunil Narine &mdash; 6.79</div>
            <div class="exec-desc">207 wickets in 202 matches. KKR's mystery spinner has the best economy among top wicket-takers.</div>
          </div>
          <div class="exec-card orange">
            <div class="exec-title">Best Average (150+ wkts)</div>
            <div class="exec-val">Jasprit Bumrah &mdash; 23.74</div>
            <div class="exec-desc">187 wickets, eco 7.34, best 5/10. IPL's most feared fast bowler for Mumbai Indians.</div>
          </div>
        </div>
        <div class="chart-box">
          <div class="chart-box-header"><div><div class="chart-box-title">All-Time Top 10 Wicket-Takers</div><div class="chart-box-sub">Career IPL wickets across all seasons</div></div></div>
          <div class="chart-canvas-wrap tall"><canvas id="topWicketsChart"></canvas></div>
          <div class="caption-box"><strong>Seamers Lead:</strong> Bhuvneshwar Kumar (226) leads, with Sunil Narine (207) close behind. Rashid Khan is the most efficient: 179 wickets in just 153 matches.</div>
        </div>
        <div class="chart-grid-2">
          <div class="chart-box">
            <div class="chart-box-header"><div><div class="chart-box-title">Bowling Economy Rate</div><div class="chart-box-sub">Runs conceded per over (lower = better)</div></div></div>
            <div class="chart-canvas-wrap"><canvas id="ecoChart"></canvas></div>
          </div>
          <div class="chart-box">
            <div class="chart-box-header"><div><div class="chart-box-title">Bowling Average</div><div class="chart-box-sub">Runs per wicket (lower = better)</div></div></div>
            <div class="chart-canvas-wrap"><canvas id="bowlAvgChart"></canvas></div>
          </div>
        </div>
        <div class="chart-box">
          <div class="chart-box-header"><div><div class="chart-box-title">All-Time Bowling Leaderboard</div><div class="chart-box-sub">Top 10 wicket-takers with key bowling metrics</div></div></div>
          <div class="table-container">
            <table class="data-table">
              <thead><tr><th>#</th><th>Bowler</th><th>Team</th><th>Mat</th><th>Wkts</th><th>Avg</th><th>Eco</th><th>SR</th><th>BB</th><th>5W</th><th>Hat-tricks</th></tr></thead>
              <tbody id="bowlingTableBody"></tbody>
            </table>
          </div>
        </div>
        <div class="chart-grid-2">
          <div class="chart-box">
            <div class="chart-box-header"><div><div class="chart-box-title">5-Wicket Hauls (Career)</div><div class="chart-box-sub">Bowlers with most 5-for hauls in IPL</div></div></div>
            <div class="chart-canvas-wrap short"><canvas id="fiveWicketChart"></canvas></div>
          </div>
          <div class="chart-box">
            <div class="chart-box-header"><div><div class="chart-box-title">Career Hat-Tricks</div><div class="chart-box-sub">Bowlers with multiple hat-tricks in IPL history</div></div></div>
            <div class="chart-canvas-wrap short"><canvas id="hatTrickChart"></canvas></div>
          </div>
        </div>
      </div>

      <!-- TAB: BOUNDARIES -->
      <div id="tab-boundaries" class="tab-section">
        <div class="exec-grid">
          <div class="exec-card orange">
            <div class="exec-title">Universe Boss &mdash; Most Sixes</div>
            <div class="exec-val">Chris Gayle &mdash; 357 &#128293;</div>
            <div class="exec-desc">142 matches, 4,965 runs, SR 148.96. Hit 357 sixes &mdash; ~85 more than the next batter.</div>
          </div>
          <div class="exec-card positive">
            <div class="exec-title">Most Fours &mdash; All-Time</div>
            <div class="exec-val">Virat Kohli &mdash; 844</div>
            <div class="exec-desc">283 matches, 9,336 runs. Kohli's precision 844 fours surpass every other batter.</div>
          </div>
          <div class="exec-card purple">
            <div class="exec-title">Best Boundary Rate</div>
            <div class="exec-val">AB de Villiers &mdash; SR 151.68</div>
            <div class="exec-desc">413 fours + 251 sixes across 184 matches. ABD's boundary frequency is unmatched.</div>
          </div>
        </div>
        <div class="chart-box">
          <div class="chart-box-header"><div><div class="chart-box-title">Most Sixes &mdash; All-Time Top 10</div><div class="chart-box-sub">Career sixes hit in IPL cricket</div></div></div>
          <div class="chart-canvas-wrap tall"><canvas id="sixesChart"></canvas></div>
          <div class="caption-box"><strong>The Six-Hitters Club:</strong> Chris Gayle (357) leads, then Rohit Sharma (323) and Kohli (316). MS Dhoni's 264 sixes &mdash; all in a finisher role &mdash; showcase his destructive late-innings prowess.</div>
        </div>
        <div class="chart-grid-2">
          <div class="chart-box">
            <div class="chart-box-header"><div><div class="chart-box-title">Most Fours &mdash; All-Time Top 10</div><div class="chart-box-sub">Career boundary fours in IPL</div></div></div>
            <div class="chart-canvas-wrap"><canvas id="foursChart"></canvas></div>
          </div>
          <div class="chart-box">
            <div class="chart-box-header"><div><div class="chart-box-title">Six-Hit Rate vs Strike Rate</div><div class="chart-box-sub">Sixes per match vs overall SR for top hitters</div></div></div>
            <div class="chart-canvas-wrap"><canvas id="sixRateChart"></canvas></div>
          </div>
        </div>
        <div class="chart-box">
          <div class="chart-box-header"><div><div class="chart-box-title">Greatest IPL Innings (by Score)</div><div class="chart-box-sub">Highest individual innings in IPL history</div></div></div>
          <div class="table-container">
            <table class="data-table">
              <thead><tr><th>#</th><th>Player</th><th>Team</th><th>Score</th><th>Balls</th><th>Fours</th><th>Sixes</th><th>SR</th></tr></thead>
              <tbody id="fastestInningsBody"></tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- TAB: SEASON TRACKER -->
      <div id="tab-seasons" class="tab-section">
        <div class="chart-box">
          <div class="chart-box-header"><div><div class="chart-box-title">Season-by-Season Orange Cap Winners</div><div class="chart-box-sub">Top run-scorer per season (2019-2026)</div></div></div>
          <div class="chart-canvas-wrap"><canvas id="seasonRunsChart"></canvas></div>
          <div class="caption-box"><strong>Season Highs:</strong> Jos Buttler (863 runs, 2019) holds the season record in this dataset including 4 centuries &mdash; an unmatched single-season haul. Devon Conway (672, CSK 2023) powered Chennai to the title.</div>
        </div>
        <div class="chart-box">
          <div class="chart-box-header"><div><div class="chart-box-title">Season-by-Season Purple Cap Winners</div><div class="chart-box-sub">Top wicket-taker per season (2019-2026)</div></div></div>
          <div class="chart-canvas-wrap"><canvas id="seasonWktsChart"></canvas></div>
        </div>
        <div class="grid-3" id="seasonCardsGrid"></div>
        <div class="chart-box">
          <div class="chart-box-header"><div><div class="chart-box-title">Most Sixes in a Single Season</div><div class="chart-box-sub">Season-wise six-hitting champion (2019-2026)</div></div></div>
          <div class="chart-canvas-wrap short"><canvas id="seasonSixesChart"></canvas></div>
        </div>
      </div>

      <!-- TAB: PLAYER ARCS -->
      <div id="tab-arcs" class="tab-section">
        <div style="margin-bottom:16px;">
          <div class="chart-box-title" style="font-size:18px;margin-bottom:4px;">&#9732;&#65039; Meteor Batters</div>
          <div style="font-size:13px;color:var(--text-500);">Players who peaked dramatically in one season &mdash; far above their usual output. A "meteor" is defined by a peak-season percentile rank far exceeding their baseline across other seasons.</div>
        </div>
        <div class="narrative-grid">
          <div class="narrative-card highlight">
            <div class="nar-icon">&#9732;&#65039;</div>
            <div class="nar-title">Jos Buttler &mdash; 2019 Supernova</div>
            <div class="nar-sub">863 runs in 17 matches &mdash; rank #1, 99th percentile. 4 centuries in one season. The most explosive single-season batting performance in recent IPL history.</div>
          </div>
          <div class="narrative-card">
            <div class="nar-icon">&#9889;</div>
            <div class="nar-title">Devon Conway &mdash; 2023 Masterclass</div>
            <div class="nar-sub">672 runs for CSK in 2023 &mdash; ranked #3 that season (98th percentile). Averaged 204 runs in other tracked seasons. Drove Chennai to the 2023 title.</div>
          </div>
          <div class="narrative-card">
            <div class="nar-icon">&#128165;</div>
            <div class="nar-title">Sunil Narine &mdash; 2024 Batting Reinvention</div>
            <div class="nar-sub">488 runs as a promoted opener for KKR &mdash; rank #9 (93rd percentile). Career baseline as a pure bowler made this batting output extraordinary. Peak-to-baseline gap: 54 percentile points.</div>
          </div>
          <div class="narrative-card">
            <div class="nar-icon">&#127775;</div>
            <div class="nar-title">Shubman Gill &mdash; 2023 GT Anchor</div>
            <div class="nar-sub">890 runs for Gujarat Titans &mdash; 30.9% of all GT runs tracked. At 23, Gill carried the defending champions almost single-handedly to a runner-up finish.</div>
          </div>
        </div>
        <div class="chart-box">
          <div class="chart-box-header"><div><div class="chart-box-title">Player Career Trajectories (2019-2026)</div><div class="chart-box-sub">Season runs for 6 notable batters across the 5 tracked seasons</div></div></div>
          <div class="chart-canvas-wrap xtall"><canvas id="playerArcChart"></canvas></div>
          <div class="caption-box"><strong>Trajectory Patterns:</strong> Jos Buttler (orange) shows the classic meteor arc. Virat Kohli (red) is the model of consistency. Shubman Gill (teal) traces an upward growth curve typical of young talent breaking through.</div>
        </div>
        <div style="margin-bottom:16px;margin-top:8px;">
          <div class="chart-box-title" style="font-size:18px;margin-bottom:4px;">&#128123; Volume Ghosts</div>
          <div style="font-size:13px;color:var(--text-500);">Consistent run-accumulators who never dominated a single season &mdash; high cumulative totals but low peak rank.</div>
        </div>
        <div class="chart-box">
          <div class="chart-box-header"><div><div class="chart-box-title">Volume Accumulators &mdash; Total Runs vs Best Season Rank</div><div class="chart-box-sub">Batters with 1,400+ career runs but modest peak rankings</div></div></div>
          <div class="chart-canvas-wrap"><canvas id="volumeGhostChart"></canvas></div>
          <div class="caption-box"><strong>The Silent Workhorses:</strong> Nicholas Pooran (1,921 runs, best rank #11), Shivam Dube (1,730, best #13), and Rohit Sharma (1,718, best #16) stacked runs without ever topping a season leaderboard.</div>
        </div>
      </div>

      <!-- TAB: FRANCHISE ANALYSIS -->
      <div id="tab-franchise" class="tab-section">
        <div class="exec-grid">
          <div class="exec-card positive">
            <div class="exec-title">Highest Single-Player Share</div>
            <div class="exec-val">Jos Buttler &mdash; 31.9%</div>
            <div class="exec-desc">2019 Rajasthan Royals: Buttler scored 863 of 2,702 tracked runs &mdash; the highest franchise dependence in the dataset.</div>
          </div>
          <div class="exec-card info">
            <div class="exec-title">Most Franchise-Dependent Season</div>
            <div class="exec-val">RCB 2023 &mdash; Faf 31.4%</div>
            <div class="exec-desc">Faf du Plessis scored 730 of RCB's 2,328 runs. Despite this, RCB finished 6th &mdash; star-dependence rarely wins titles.</div>
          </div>
          <div class="exec-card warning">
            <div class="exec-title">Most Consistent Dependence</div>
            <div class="exec-val">Virat Kohli &mdash; 2 seasons</div>
            <div class="exec-desc">RCB relied on Kohli in both 2024 (741 runs, 27%) and 2025 (657 runs, 27.7%) &mdash; back-to-back franchise dependency.</div>
          </div>
        </div>
        <div class="chart-box">
          <div class="chart-box-header"><div><div class="chart-box-title">Franchise Dependency Ratio by Season</div><div class="chart-box-sub">% of team total runs contributed by the top batter</div></div></div>
          <div class="chart-canvas-wrap tall"><canvas id="franchiseChart"></canvas></div>
          <div class="caption-box"><strong>Franchise Risk:</strong> When a single player contributes 28%+ of team runs, the franchise is highly vulnerable. Both RR 2019 (Buttler: 31.9%) and RCB 2023 (du Plessis: 31.4%) illustrate this risk &mdash; neither won the title.</div>
        </div>
        <div class="chart-box">
          <div class="chart-box-header"><div><div class="chart-box-title">Notable Franchise Dependency Cases</div><div class="chart-box-sub">Individual run share as % of tracked team runs</div></div></div>
          <div id="franchiseBars"></div>
        </div>
        <div class="chart-box">
          <div class="chart-box-header"><div><div class="chart-box-title">2026 Season &mdash; Top Scorer Per Franchise</div><div class="chart-box-sub">The batting anchor for each team in IPL 2026</div></div></div>
          <div class="chart-canvas-wrap"><canvas id="team2026Chart"></canvas></div>
        </div>
      </div>

      <!-- TAB: CONCLUSIONS -->
      <div id="tab-conclusions" class="tab-section">
        <div class="conclusion-box">
          <div style="font-size:18px;font-weight:800;color:var(--text-900);margin-bottom:20px;">Key Findings &amp; Insights</div>
          <div class="conclusion-card">
            <div class="conclusion-badge">1</div>
            <div class="conclusion-content">
              <h4>Virat Kohli Dominates All-Time Records</h4>
              <p>With 9,336 runs at 40.42 across 283 matches, Kohli leads in runs, centuries (9), and fours (844). His consistency is unmatched &mdash; the gap between him and second-placed David Warner (6,565 runs) exceeds 2,700 runs.</p>
            </div>
          </div>
          <div class="conclusion-card">
            <div class="conclusion-badge">2</div>
            <div class="conclusion-content">
              <h4>Chris Gayle &mdash; An Unconquerable Six-Hitting Record</h4>
              <p>Gayle's 357 IPL sixes is a record unlikely to be broken. Even Rohit Sharma &mdash; the most experienced IPL batter &mdash; has 323 sixes from 276 innings vs Gayle's 357 in just 141. Gayle's six-rate of 2.52/innings dwarfs every other elite batter.</p>
            </div>
          </div>
          <div class="conclusion-card">
            <div class="conclusion-badge">3</div>
            <div class="conclusion-content">
              <h4>The Bowling Arms Race &mdash; Seamers vs Spinners</h4>
              <p>Bhuvneshwar Kumar (226 wkts, seam) leads all-time, but Sunil Narine (207, spin) posts the best economy (6.79). Rashid Khan is the most efficient: 179 wickets in 153 matches at 23.92 &mdash; the best wickets-per-match ratio among top-10 bowlers.</p>
            </div>
          </div>
          <div class="conclusion-card">
            <div class="conclusion-badge">4</div>
            <div class="conclusion-content">
              <h4>Franchise Over-Dependence Rarely Translates to Titles</h4>
              <p>Teams with a single batter contributing 28%+ of runs (Buttler/RR 2019, du Plessis/RCB 2023) did not win the IPL. Balanced batting line-ups &mdash; not single-star reliance &mdash; correlate more strongly with title success.</p>
            </div>
          </div>
          <div class="conclusion-card">
            <div class="conclusion-badge">5</div>
            <div class="conclusion-content">
              <h4>Meteor Seasons Are Defined by Context</h4>
              <p>Sunil Narine's 2024 opening reinvention (488 runs, 93rd percentile) is the most extreme single-season transformation. Conway's 2023 (672 runs) and Riyan Parag's 2024 breakout (573 runs) are other landmark performances &mdash; all in seasons their teams performed well.</p>
            </div>
          </div>
          <div class="conclusion-card">
            <div class="conclusion-badge">6</div>
            <div class="conclusion-content">
              <h4>Volume Ghosts &mdash; Consistency Without Headlines</h4>
              <p>Nicholas Pooran (1,921 runs), Shivam Dube (1,730), and Rohit Sharma (1,718) are quiet accumulators &mdash; never topping a season leaderboard but building massive career totals. They represent the unseen backbone of T20 franchise cricket.</p>
            </div>
          </div>
          <div class="conclusion-card">
            <div class="conclusion-badge">7</div>
            <div class="conclusion-content">
              <h4>KL Rahul &mdash; IPL's Most Efficient Scorer</h4>
              <p>Among batters with 1,000+ IPL runs, KL Rahul holds the best batting average at 46.15 across 150 innings. His 6 centuries + 45 fifties at SR 139.15 make him statistically the most reliable large-innings batter in IPL history.</p>
            </div>
          </div>
          <div class="conclusion-card">
            <div class="conclusion-badge">8</div>
            <div class="conclusion-content">
              <h4>2026 IPL &mdash; A New Generation Emerges</h4>
              <p>The 2026 season shows Dhruv Jurel (515 runs, RR), Mitchell Marsh (563 runs, LSG), and KL Rahul (735 runs, DC) leading charts. Shubman Gill's continued upward arc signals a generational shift &mdash; the post-Kohli/Rohit era is beginning.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<!-- Mobile drawer -->
<div class="mobile-nav-backdrop" id="mobileNavBackdrop">
  <div class="mobile-nav-drawer" id="mobileNavDrawer">
    <div class="mobile-drawer-header">
      <div class="logo-name">Analysis Hub</div>
      <button class="mobile-drawer-close" id="mobileDrawerClose">&#10005;</button>
    </div>
    <div class="nav-section">
      <p class="nav-eyebrow">Menu</p>
      <a href="index.html"    class="nav-item"><span class="nav-label">Dashboard</span></a>
      <a href="reports.html"  class="nav-item active"><span class="nav-label">Reports</span><span class="nav-badge">4</span></a>
      <a href="datasets.html" class="nav-item"><span class="nav-label">Datasets</span></a>
      <a href="analytics.html"class="nav-item"><span class="nav-label">Analytics</span></a>
    </div>
  </div>
</div>
<script src="hub.js"></script>
<script>
function switchTab(btn,id){
  document.querySelectorAll('.report-tab').forEach(b=>b.classList.remove('active'));
  document.querySelectorAll('.tab-section').forEach(s=>s.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById(id).classList.add('active');
}
const BD=[
  {n:'Virat Kohli',t:'RCB',tc:'team-rcb',m:283,i:275,r:9336,a:40.42,s:134.80,c:9,f:68,h:'113'},
  {n:'Rohit Sharma',t:'MI',tc:'team-mi',m:281,i:276,r:7329,a:29.91,s:132.92,c:2,f:49,h:'109*'},
  {n:'Shikhar Dhawan',t:'PBKS',tc:'team-pbks',m:222,i:221,r:6769,a:35.26,s:127.14,c:2,f:51,h:'106*'},
  {n:'David Warner',t:'DC',tc:'team-dc',m:184,i:184,r:6565,a:40.52,s:139.77,c:4,f:61,h:'126'},
  {n:'KL Rahul',t:'DC',tc:'team-dc',m:159,i:150,r:5815,a:46.15,s:139.15,c:6,f:45,h:'152*'},
  {n:'Suresh Raina',t:'CSK',tc:'team-csk',m:205,i:197,r:5528,a:32.51,s:136.73,c:1,f:38,h:'100*'},
  {n:'MS Dhoni',t:'CSK',tc:'team-csk',m:278,i:242,r:5439,a:38.30,s:137.45,c:0,f:24,h:'84*'},
  {n:'AB de Villiers',t:'RCB',tc:'team-rcb',m:184,i:170,r:5162,a:39.70,s:151.68,c:3,f:40,h:'133*'},
  {n:'Sanju Samson',t:'CSK',tc:'team-csk',m:191,i:186,r:5181,a:31.79,s:141.13,c:5,f:27,h:'119'},
  {n:'Chris Gayle',t:'PBKS',tc:'team-pbks',m:142,i:141,r:4965,a:39.72,s:148.96,c:6,f:31,h:'175*'},
];
const BWD=[
  {n:'Bhuvneshwar Kumar',t:'RCB',tc:'team-rcb',m:206,w:226,a:26.16,e:7.71,s:20.35,b:'5/19',fw:2,ht:0},
  {n:'Sunil Narine',t:'KKR',tc:'team-kkr',m:202,w:207,a:25.42,e:6.79,s:22.47,b:'5/19',fw:1,ht:1},
  {n:'Piyush Chawla',t:'MI',tc:'team-mi',m:192,w:192,a:26.60,e:7.96,s:20.05,b:'4/17',fw:0,ht:0},
  {n:'Jasprit Bumrah',t:'MI',tc:'team-mi',m:158,w:187,a:23.74,e:7.34,s:19.42,b:'5/10',fw:2,ht:0},
  {n:'R Ashwin',t:'CSK',tc:'team-csk',m:221,w:187,a:30.23,e:7.20,s:25.19,b:'4/34',fw:0,ht:0},
  {n:'Dwayne Bravo',t:'CSK',tc:'team-csk',m:161,w:183,a:23.82,e:8.38,s:17.05,b:'4/22',fw:0,ht:0},
  {n:'Ravindra Jadeja',t:'RR',tc:'team-rr',m:268,w:180,a:30.36,e:7.71,s:23.63,b:'5/16',fw:1,ht:0},
  {n:'Rashid Khan',t:'GT',tc:'team-gt',m:153,w:179,a:23.92,e:7.28,s:19.72,b:'4/24',fw:0,ht:2},
  {n:'Amit Mishra',t:'LSG',tc:'team-lsg',m:162,w:174,a:23.84,e:7.38,s:19.37,b:'5/17',fw:1,ht:3},
  {n:'Harbhajan Singh',t:'MI',tc:'team-mi',m:163,w:150,a:26.26,e:7.05,s:22.38,b:'5/18',fw:2,ht:1},
];
const SIXES_D=[
  {n:'Chris Gayle',sx:357,m:142,sr:148.96},{n:'Rohit Sharma',sx:323,m:281,sr:132.92},
  {n:'Virat Kohli',sx:316,m:283,sr:134.80},{n:'MS Dhoni',sx:264,m:278,sr:137.45},
  {n:'AB de Villiers',sx:251,m:184,sr:151.68},{n:'KL Rahul',sx:239,m:159,sr:139.15},
  {n:'D Warner',sx:236,m:184,sr:139.77},{n:'Sanju Samson',sx:243,m:191,sr:141.13},
  {n:'Jos Buttler',sx:211,m:138,sr:149.73},{n:'Hardik Pandya',sx:200,m:158,sr:147.00},
];
const FOURS_D=[
  {n:'Virat Kohli',fo:844},{n:'Shikhar Dhawan',fo:768},{n:'D Warner',fo:663},
  {n:'Rohit Sharma',fo:661},{n:'KL Rahul',fo:508},{n:'A Rahane',fo:539},
  {n:'S Raina',fo:476},{n:'AB de Villiers',fo:413},{n:'Chris Gayle',fo:405},{n:'MS Dhoni',fo:375},
];
const CENTS_D=[{n:'V Kohli',c:9},{n:'Jos Buttler',c:7},{n:'KL Rahul',c:6},{n:'C Gayle',c:6},{n:'S Samson',c:5},{n:'D Warner',c:4},{n:'ABdV',c:3}];
const FIFTIES_D=[{n:'V Kohli',f:68},{n:'S Dhawan',f:51},{n:'D Warner',f:61},{n:'Rohit',f:49},{n:'KL Rahul',f:45},{n:'ABdV',f:40},{n:'S Raina',f:38},{n:'MS Dhoni',f:24}];
const SR_RUNS={lbl:['2019','2023','2024','2025','2026'],sc:['Jos Buttler (RR)','Devon Conway (CSK)','Virat Kohli (RCB)','Sai Sudharsan (GT)','K L Rahul (DC)'],r:[863,672,741,759,735]};
const SR_WKTS={lbl:['2019','2023','2024','2025','2026'],sc:['K Rabada (DC)','M Shami (GT)','Harshal Patel (PBKS)','J Bumrah (MI)','J Bumrah (MI)'],w:[25,28,24,27,22]};
const SR_SIX={lbl:['2019','2023','2024','2025','2026'],p:['Chris Gayle','Rinku Singh','Abhishek Sharma','H Klaasen','Phil Salt'],s:[34,40,36,38,42]};
const ARCS={lbl:['2019','2023','2024','2025','2026'],p:[
  {n:'Virat Kohli',d:[464,639,741,657,580],c:'#E53E3E'},
  {n:'Rohit Sharma',d:[405,405,402,418,288],c:'#3182CE'},
  {n:'Jos Buttler',d:[863,483,250,152,620],c:'#DD6B20'},
  {n:'Shubman Gill',d:[483,890,426,669,549],c:'#007A78'},
  {n:'Yashasvi Jaiswal',d:[320,625,435,513,480],c:'#805AD5'},
  {n:'KL Rahul',d:[616,520,520,380,735],c:'#2F855A'},
]};
const FRANCHISE_D=[
  {l:'Jos Buttler - 2019 RR',p:31.9},{l:'Faf du Plessis - 2023 RCB',p:31.4},
  {l:'Shubman Gill - 2023 GT',p:30.9},{l:'Sai Sudharsan - 2024 GT',p:28.0},
  {l:'Sai Sudharsan - 2025 GT',p:27.9},{l:'Virat Kohli - 2025 RCB',p:27.7},
  {l:'Yashasvi Jaiswal - 2023 RR',p:27.4},{l:'Virat Kohli - 2024 RCB',p:27.0},
];
const GHOSTS=[
  {n:'N Pooran',t:1921,br:11},{n:'S Dube',t:1730,br:13},{n:'Rohit Sharma',t:1718,br:16},
  {n:'R Patidar',t:1541,br:13},{n:'A Markram',t:1525,br:14},{n:'T Varma',t:1515,br:18},
  {n:'A Rahane',t:1426,br:19},{n:'D Padikkal',t:1386,br:17},
];
const TEAM26={teams:['RCB','CSK','MI','KKR','RR','DC','PBKS','SRH','GT','LSG'],sc:['D Padikkal','R Jadeja','T Varma','A Nortje','D Jurel','K L Rahul','S Dhawan','P Salt','S Gill','M Marsh'],r:[464,380,416,330,515,735,390,420,549,563]};
const INNINGS=[
  {r:1,p:'Chris Gayle',t:'RCB',tc:'team-rcb',sc:'175*',b:66,fo:17,si:13,sr:265.15},
  {r:2,p:'Brendon McCullum',t:'KKR',tc:'team-kkr',sc:'158*',b:73,fo:10,si:13,sr:216.44},
  {r:3,p:'AB de Villiers',t:'RCB',tc:'team-rcb',sc:'133*',b:59,fo:12,si:12,sr:225.42},
  {r:4,p:'KL Rahul',t:'LSG',tc:'team-lsg',sc:'132*',b:53,fo:14,si:7,sr:249.06},
  {r:5,p:'Quinton de Kock',t:'LSG',tc:'team-lsg',sc:'140*',b:70,fo:20,si:5,sr:200.00},
  {r:6,p:'Rishabh Pant',t:'DC',tc:'team-dc',sc:'128*',b:63,fo:13,si:9,sr:203.17},
  {r:7,p:'Jos Buttler',t:'RR',tc:'team-rr',sc:'124',b:64,fo:10,si:8,sr:193.75},
  {r:8,p:'Ricky Ponting',t:'MI',tc:'team-mi',sc:'130*',b:69,fo:12,si:9,sr:188.41},
];
Chart.defaults.font.family="'Plus Jakarta Sans',sans-serif";
Chart.defaults.color='#9AA1A9';
Chart.defaults.plugins.legend.display=false;
const P=['#0E3B2E','#3182CE','#2E9370','#D4A017','#E8570D','#7B2D8B','#C0272D','#007A78','#805AD5','#2F855A'];
function rb(i){if(i===0)return'<span class="rank-badge gold">1</span>';if(i===1)return'<span class="rank-badge silver">2</span>';if(i===2)return'<span class="rank-badge bronze">3</span>';return`<span class="rank-badge">${i+1}</span>`;}
function bOpts(axis){return{indexAxis:axis==='y'?'y':'x',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:11}}},y:{grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:11}}}}};}
window.addEventListener('DOMContentLoaded',()=>{
  // Batting table
  document.getElementById('battingTableBody').innerHTML=BD.map((r,i)=>`<tr><td>${rb(i)}</td><td><strong>${r.n}</strong></td><td><span class="team-chip ${r.tc}">${r.t}</span></td><td>${r.m}</td><td>${r.i}</td><td><strong>${r.r.toLocaleString()}</strong></td><td>${r.a}</td><td>${r.s}</td><td>${r.c}</td><td>${r.f}</td><td>${r.h}</td></tr>`).join('');
  // Bowling table
  document.getElementById('bowlingTableBody').innerHTML=BWD.map((r,i)=>`<tr><td>${rb(i)}</td><td><strong>${r.n}</strong></td><td><span class="team-chip ${r.tc}">${r.t}</span></td><td>${r.m}</td><td><strong>${r.w}</strong></td><td>${r.a}</td><td>${r.e}</td><td>${r.s}</td><td>${r.b}</td><td>${r.fw}</td><td>${r.ht}</td></tr>`).join('');
  // Innings table
  document.getElementById('fastestInningsBody').innerHTML=INNINGS.map((r,i)=>`<tr><td>${rb(i)}</td><td><strong>${r.p}</strong></td><td><span class="team-chip ${r.tc}">${r.t}</span></td><td><strong>${r.sc}</strong></td><td>${r.b}</td><td>${r.fo}</td><td>${r.si}</td><td>${r.sr}</td></tr>`).join('');
  // Franchise bars
  const mx=Math.max(...FRANCHISE_D.map(d=>d.p));
  document.getElementById('franchiseBars').innerHTML=FRANCHISE_D.map(d=>`<div class="progress-wrap"><div class="progress-label"><span>${d.l}</span><span>${d.p}% of team runs</span></div><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:${(d.p/mx*100).toFixed(1)}%"></div></div></div>`).join('');
  // Season cards
  const seasons=[{y:'2019',oc:'Jos Buttler (RR)',or:863,pc:'K Rabada (DC)',pw:25,h:'Buttler smashed 4 hundreds in a single season - an IPL record. 99th percentile batting performance.'},
    {y:'2023',oc:'Devon Conway (CSK)',or:672,pc:'M Shami (GT)',pw:28,h:'Shami\'s 28 wickets powered GT, but CSK won on the back of Conway\'s 672 runs. Devon Conway\'s peak season.'},
    {y:'2024',oc:'Virat Kohli (RCB)',or:741,pc:'Harshal Patel (PBKS)',pw:24,h:'Kohli\'s 741 runs drove RCB to the title. Sunil Narine\'s 488-run batting explosion redefined KKR\'s batting order.'},
    {y:'2025',oc:'Sai Sudharsan (GT)',or:759,pc:'J Bumrah (MI)',pw:27,h:'Bumrah dominant with 27 wickets. Sai Sudharsan anchored GT to runners-up with 759 runs.'},
    {y:'2026',oc:'K L Rahul (DC)',or:735,pc:'J Bumrah (MI)',pw:22,h:'KL Rahul led DC\'s batting charge with 735 runs. Bumrah continued his purple-cap dynasty.'},
  ];
  document.getElementById('seasonCardsGrid').innerHTML=seasons.map(s=>`<div class="card"><div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;"><div style="font-size:22px;font-weight:800;color:var(--green-900);">IPL ${s.y}</div><span class="badge completed">Completed</span></div><div style="margin-bottom:10px;"><div style="font-size:11px;font-weight:700;color:var(--text-400);text-transform:uppercase;margin-bottom:3px;">Orange Cap</div><div style="font-size:14px;font-weight:700;color:var(--text-900);">${s.oc}</div><div style="font-size:12px;color:var(--text-500);">${s.or} runs</div></div><div style="margin-bottom:14px;"><div style="font-size:11px;font-weight:700;color:var(--text-400);text-transform:uppercase;margin-bottom:3px;">Purple Cap</div><div style="font-size:14px;font-weight:700;color:var(--text-900);">${s.pc}</div><div style="font-size:12px;color:var(--text-500);">${s.pw} wickets</div></div><div style="padding:10px 12px;background:var(--bg);border-radius:10px;font-size:12px;color:var(--text-500);line-height:1.5;">${s.h}</div></div>`).join('');
  // CHARTS
  new Chart(document.getElementById('topRunsChart'),{type:'bar',data:{labels:BD.map(d=>d.n),datasets:[{data:BD.map(d=>d.r),backgroundColor:P,borderRadius:8,borderSkipped:false}]},options:{...bOpts('x'),plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>` ${c.parsed.y.toLocaleString()} runs`}}}}});
  new Chart(document.getElementById('avgChart'),{type:'bar',data:{labels:BD.map(d=>d.n.split(' ').pop()),datasets:[{data:BD.map(d=>d.a),backgroundColor:P,borderRadius:6,borderSkipped:false}]},options:{...bOpts('x'),scales:{x:{grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:10}}},y:{grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:10}}}},plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>` Avg: ${c.parsed.y}`}}}}});
  new Chart(document.getElementById('srChart'),{type:'bar',data:{labels:BD.map(d=>d.n.split(' ').pop()),datasets:[{data:BD.map(d=>d.s),backgroundColor:[...P].reverse(),borderRadius:6,borderSkipped:false}]},options:{...bOpts('x'),scales:{x:{grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:10}}},y:{grid:{color:'rgba(0,0,0,.04)'},min:120,ticks:{font:{size:10}}}},plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>` SR: ${c.parsed.y}`}}}}});
  new Chart(document.getElementById('centuriesChart'),{type:'bar',data:{labels:CENTS_D.map(d=>d.n),datasets:[{data:CENTS_D.map(d=>d.c),backgroundColor:P,borderRadius:8,borderSkipped:false}]},options:{...bOpts('x'),plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>` ${c.parsed.y} centuries`}}}}});
  new Chart(document.getElementById('fiftiesChart'),{type:'bar',data:{labels:FIFTIES_D.map(d=>d.n),datasets:[{data:FIFTIES_D.map(d=>d.f),backgroundColor:P,borderRadius:8,borderSkipped:false}]},options:{...bOpts('x'),plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>` ${c.parsed.y} fifties`}}}}});
  new Chart(document.getElementById('topWicketsChart'),{type:'bar',data:{labels:BWD.map(d=>d.n.split(' ').pop()),datasets:[{data:BWD.map(d=>d.w),backgroundColor:P,borderRadius:8,borderSkipped:false}]},options:{...bOpts('x'),plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>` ${c.parsed.y} wickets`}}}}});
  new Chart(document.getElementById('ecoChart'),{type:'bar',data:{labels:BWD.map(d=>d.n.split(' ').pop()),datasets:[{data:BWD.map(d=>d.e),backgroundColor:P,borderRadius:6,borderSkipped:false}]},options:{...bOpts('x'),scales:{x:{grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:10}}},y:{grid:{color:'rgba(0,0,0,.04)'},min:5,ticks:{font:{size:10}}}},plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>` Eco: ${c.parsed.y}`}}}}});
  new Chart(document.getElementById('bowlAvgChart'),{type:'bar',data:{labels:BWD.map(d=>d.n.split(' ').pop()),datasets:[{data:BWD.map(d=>d.a),backgroundColor:[...P].reverse(),borderRadius:6,borderSkipped:false}]},options:{...bOpts('x'),scales:{x:{grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:10}}},y:{grid:{color:'rgba(0,0,0,.04)'},min:18,ticks:{font:{size:10}}}},plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>` Avg: ${c.parsed.y}`}}}}});
  new Chart(document.getElementById('fiveWicketChart'),{type:'bar',data:{labels:BWD.filter(d=>d.fw>0).map(d=>d.n.split(' ').pop()),datasets:[{data:BWD.filter(d=>d.fw>0).map(d=>d.fw),backgroundColor:P,borderRadius:8,borderSkipped:false}]},options:{...bOpts('x'),plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>` ${c.parsed.y} five-wicket hauls`}}}}});
  new Chart(document.getElementById('hatTrickChart'),{type:'bar',data:{labels:BWD.filter(d=>d.ht>0).map(d=>d.n.split(' ').pop()),datasets:[{data:BWD.filter(d=>d.ht>0).map(d=>d.ht),backgroundColor:P,borderRadius:8,borderSkipped:false}]},options:{...bOpts('x'),plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>` ${c.parsed.y} hat-tricks`}}}}});
  new Chart(document.getElementById('sixesChart'),{type:'bar',data:{labels:SIXES_D.map(d=>d.n.split(' ').pop()),datasets:[{data:SIXES_D.map(d=>d.sx),backgroundColor:P,borderRadius:8,borderSkipped:false}]},options:{...bOpts('x'),plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>` ${c.parsed.y} sixes`}}}}});
  new Chart(document.getElementById('foursChart'),{type:'bar',data:{labels:FOURS_D.map(d=>d.n.split(' ').pop()),datasets:[{data:FOURS_D.map(d=>d.fo),backgroundColor:P,borderRadius:8,borderSkipped:false}]},options:{...bOpts('x'),plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>` ${c.parsed.y} fours`}}}}});
  new Chart(document.getElementById('sixRateChart'),{type:'scatter',data:{datasets:SIXES_D.map((d,i)=>({label:d.n,data:[{x:d.sx/d.m,y:d.sr}],backgroundColor:P[i]+'CC',pointRadius:10,pointHoverRadius:13}))},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:true,position:'right',labels:{boxWidth:10,font:{size:10}}},tooltip:{callbacks:{title:c=>c[0].dataset.label,label:c=>` Sixes/match: ${c.parsed.x.toFixed(2)} | SR: ${c.parsed.y}`}}},scales:{x:{title:{display:true,text:'Sixes per Match',font:{size:11}},grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:10}}},y:{title:{display:true,text:'Strike Rate',font:{size:11}},grid:{color:'rgba(0,0,0,.04)'},min:120,ticks:{font:{size:10}}}}}});
  new Chart(document.getElementById('seasonRunsChart'),{type:'bar',data:{labels:SR_RUNS.lbl,datasets:[{data:SR_RUNS.r,backgroundColor:P,borderRadius:10,borderSkipped:false}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>`${SR_RUNS.sc[c.dataIndex]}: ${c.parsed.y} runs`}}},scales:{x:{grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:12}}},y:{grid:{color:'rgba(0,0,0,.04)'},min:500,ticks:{font:{size:11}}}}}});
  new Chart(document.getElementById('seasonWktsChart'),{type:'bar',data:{labels:SR_WKTS.lbl,datasets:[{data:SR_WKTS.w,backgroundColor:['#7B2D8B','#0E3B2E','#2E9370','#3182CE','#D4A017'],borderRadius:10,borderSkipped:false}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>`${SR_WKTS.sc[c.dataIndex]}: ${c.parsed.y} wickets`}}},scales:{x:{grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:12}}},y:{grid:{color:'rgba(0,0,0,.04)'},min:18,ticks:{font:{size:11}}}}}});
  new Chart(document.getElementById('seasonSixesChart'),{type:'bar',data:{labels:SR_SIX.lbl,datasets:[{data:SR_SIX.s,backgroundColor:['#D4A017','#2E9370','#3182CE','#E8570D','#0E3B2E'],borderRadius:8,borderSkipped:false}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>`${SR_SIX.p[c.dataIndex]}: ${c.parsed.y} sixes`}}},scales:{x:{grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:12}}},y:{grid:{color:'rgba(0,0,0,.04)'},min:25,ticks:{font:{size:11}}}}}});
  new Chart(document.getElementById('playerArcChart'),{type:'line',data:{labels:ARCS.lbl,datasets:ARCS.p.map(p=>({label:p.n,data:p.d,borderColor:p.c,backgroundColor:p.c+'20',borderWidth:2.5,pointRadius:5,pointHoverRadius:7,tension:.35,fill:false}))},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:true,position:'top',labels:{boxWidth:12,font:{size:11}}},tooltip:{mode:'index',intersect:false}},scales:{x:{grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:12}}},y:{grid:{color:'rgba(0,0,0,.04)'},title:{display:true,text:'Season Runs',font:{size:11}},ticks:{font:{size:11}}}}}});
  new Chart(document.getElementById('volumeGhostChart'),{type:'bar',data:{labels:GHOSTS.map(d=>d.n),datasets:[{label:'Career Runs',data:GHOSTS.map(d=>d.t),backgroundColor:'#3182CEBB',borderRadius:6,borderSkipped:false,yAxisID:'y'},{label:'Best Season Rank',data:GHOSTS.map(d=>d.br),backgroundColor:'#D4A017BB',borderRadius:6,borderSkipped:false,yAxisID:'y1'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:true,position:'top',labels:{boxWidth:12,font:{size:11}}},tooltip:{mode:'index'}},scales:{x:{grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:11}}},y:{position:'left',title:{display:true,text:'Career Runs',font:{size:11}},grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:10}}},y1:{position:'right',title:{display:true,text:'Best Season Rank',font:{size:11}},grid:{drawOnChartArea:false},min:0,max:25,ticks:{font:{size:10}}}}}});
  new Chart(document.getElementById('franchiseChart'),{type:'bar',data:{labels:FRANCHISE_D.map(d=>d.l),datasets:[{data:FRANCHISE_D.map(d=>d.p),backgroundColor:P,borderRadius:8,borderSkipped:false}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>` ${c.parsed.x}% of team runs`}}},scales:{x:{grid:{color:'rgba(0,0,0,.04)'},min:20,max:35,ticks:{font:{size:10},callback:v=>v+'%'}},y:{grid:{display:false},ticks:{font:{size:10}}}}}});
  new Chart(document.getElementById('team2026Chart'),{type:'bar',data:{labels:TEAM26.teams,datasets:[{data:TEAM26.r,backgroundColor:P,borderRadius:8,borderSkipped:false}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>`${TEAM26.sc[c.dataIndex]}: ${c.parsed.y} runs`}}},scales:{x:{grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:11}}},y:{grid:{color:'rgba(0,0,0,.04)'},min:200,ticks:{font:{size:11}}}}}});
});
</script>
</body>
</html>"""

with open('ipl_report.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Written successfully:", len(content), "bytes")
