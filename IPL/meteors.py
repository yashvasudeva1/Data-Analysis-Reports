#!/usr/bin/env python3
"""
IPL Meteors & Ghosts
--------------------
Finds one-season explosions, high-volume never-elites, and franchise
dependence patterns from official iplt20.com aggregate stats feeds.

Run:
    pip install requests pandas
    python meteors.py

Outputs land in ./output/
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pandas as pd
import requests

# =============================================================================
# Config
# =============================================================================
BASE = "https://ipl-stats-sports-mechanic.s3.ap-south-1.amazonaws.com/ipl/feeds/stats"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "*/*",
    "Referer": "https://www.iplt20.com/",
}

# Competition IDs that currently return real data on the official CDN
SEASONS = {
    2019: 60,
    2023: 107,
    2024: 148,
    2025: 203,
    2026: 284,
}

BATTING_ENDPOINT = "toprunsscorers"
BOWLING_ENDPOINT = "mostwickets"

OUT = Path(__file__).resolve().parent / "output"
REQUEST_DELAY = 0.6
TIMEOUT = 30
MIN_SEASONS_FOR_CAREER = 2
MIN_MATCHES_IN_SEASON = 5

session = requests.Session()
session.headers.update(HEADERS)


# =============================================================================
# Scrape
# =============================================================================
def fetch_jsonp(url: str) -> dict | None:
    try:
        r = session.get(url, timeout=TIMEOUT)
        if r.status_code != 200 or len(r.text) < 400:
            return None
        text = r.text
        start, end = text.find("("), text.rfind(")")
        if start < 0 or end < 0:
            return None
        return json.loads(text[start + 1 : end])
    except Exception as exc:
        print(f"  [fetch error] {exc}")
        return None


def extract_records(data: dict | None) -> list:
    if not data:
        return []
    for value in data.values():
        if isinstance(value, list):
            return value
    return []


def scrape_endpoint(competition_id: int | str, endpoint: str) -> list[dict]:
    url = f"{BASE}/{competition_id}-{endpoint}.js?callback=on{endpoint}"
    data = fetch_jsonp(url)
    return extract_records(data)


def load_all_season_stats() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Download batting + bowling season tables. Returns (batting_df, bowling_df)."""
    bat_rows, bowl_rows = [], []

    print("Downloading official season stats…")
    for year, cid in SEASONS.items():
        print(f"  Season {year} (id={cid})")
        for endpoint, bucket in (
            (BATTING_ENDPOINT, bat_rows),
            (BOWLING_ENDPOINT, bowl_rows),
        ):
            records = scrape_endpoint(cid, endpoint)
            time.sleep(REQUEST_DELAY)
            for rec in records:
                rec = dict(rec)
                rec["Season"] = year
                bucket.append(rec)
            print(f"    {endpoint}: {len(records)} rows")

    batting = pd.DataFrame(bat_rows)
    bowling = pd.DataFrame(bowl_rows)
    return batting, bowling


# =============================================================================
# Cleaning
# =============================================================================
def _num(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def clean_batting(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    out = pd.DataFrame(
        {
            "player": df.get("StrikerName", pd.Series(dtype=str)).astype(str).str.strip(),
            "player_id": df.get("PlayerId", pd.Series(dtype=str)).astype(str),
            "team": df.get("TeamName", pd.Series(dtype=str)).astype(str).str.strip(),
            "team_code": df.get("TeamCode", pd.Series(dtype=str)).astype(str),
            "season": _num(df["Season"]).astype(int),
            "matches": _num(df.get("Matches", 0)),
            "innings": _num(df.get("Innings", 0)),
            "runs": _num(df.get("TotalRuns", 0)),
            "balls": _num(df.get("Balls", 0)),
            "average": _num(df.get("BattingAverage", 0)),
            "strike_rate": _num(df.get("StrikeRate", 0)),
            "fours": _num(df.get("Fours", 0)),
            "sixes": _num(df.get("Sixes", 0)),
            "fifties": _num(df.get("FiftyPlusRuns", 0)),
            "hundreds": _num(df.get("Centuries", 0)),
            "highest": df.get("HighestScore", pd.Series(dtype=str)).astype(str),
        }
    )
    out = out[out["player"].str.len() > 0]
    out = out[out["matches"] >= MIN_MATCHES_IN_SEASON]
    out = out.dropna(subset=["runs"])
    return out.reset_index(drop=True)


def clean_bowling(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    name_col = "BowlerName" if "BowlerName" in df.columns else (
        "PlayerName" if "PlayerName" in df.columns else "StrikerName"
    )
    wickets_col = "Wickets" if "Wickets" in df.columns else "TotalWickets"
    matches_col = "Matches" if "Matches" in df.columns else "Mat"

    out = pd.DataFrame(
        {
            "player": df.get(name_col, pd.Series(dtype=str)).astype(str).str.strip(),
            "player_id": df.get("PlayerId", pd.Series(dtype=str)).astype(str),
            "team": df.get("TeamName", pd.Series(dtype=str)).astype(str).str.strip(),
            "season": _num(df["Season"]).astype(int),
            "matches": _num(df.get(matches_col, 0)),
            "wickets": _num(df.get(wickets_col, 0)),
            "economy": _num(df.get("Economy", df.get("EconomyRate", 0))),
            "average": _num(df.get("BowlingAverage", df.get("Average", 0))),
            "strike_rate": _num(df.get("BowlingStrikeRate", df.get("StrikeRate", 0))),
        }
    )
    out = out[out["player"].str.len() > 0]
    out = out[out["matches"] >= MIN_MATCHES_IN_SEASON]
    out = out.dropna(subset=["wickets"])
    return out.reset_index(drop=True)


# =============================================================================
# Meteor engine
# =============================================================================
def season_ranks(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    """Add dense rank within each season (1 = best)."""
    d = df.copy()
    d["season_rank"] = (
        d.groupby("season")[value_col]
        .rank(method="min", ascending=False)
        .astype(int)
    )
    d["season_n"] = d.groupby("season")[value_col].transform("count")
    d["season_pct"] = (1 - (d["season_rank"] - 1) / d["season_n"].clip(lower=1)) * 100
    return d


def build_player_careers(ranked: pd.DataFrame, value_col: str) -> pd.DataFrame:
    """One row per player with career summary + best season."""
    rows = []
    for player, g in ranked.groupby("player"):
        g = g.sort_values("season")
        n_seasons = len(g)
        best_idx = g[value_col].idxmax()
        best = g.loc[best_idx]

        other = g.drop(index=best_idx)
        if len(other):
            other_mean_pct = other["season_pct"].mean()
            other_mean_val = other[value_col].mean()
            other_best_rank = other["season_rank"].min()
        else:
            other_mean_pct = float("nan")
            other_mean_val = float("nan")
            other_best_rank = float("nan")

        peak_pct = float(best["season_pct"])
        gap = peak_pct - (other_mean_pct if pd.notna(other_mean_pct) else peak_pct)

        if n_seasons < MIN_SEASONS_FOR_CAREER:
            meteor_score = peak_pct * 0.35
            category = "single-season snapshot"
        else:
            meteor_score = peak_pct * 0.55 + max(gap, 0) * 0.45
            if peak_pct >= 90 and (other_mean_pct is not None and other_mean_pct < 55):
                category = "meteor"
            elif peak_pct >= 85 and gap >= 25:
                category = "meteor"
            elif peak_pct < 70 and g[value_col].sum() >= g[value_col].quantile(0.7) * n_seasons:
                category = "volume ghost"
            else:
                category = "normal"

        rows.append(
            {
                "player": player,
                "seasons_played": n_seasons,
                "career_total": g[value_col].sum(),
                "career_mean": g[value_col].mean(),
                "best_season": int(best["season"]),
                "best_value": float(best[value_col]),
                "best_rank": int(best["season_rank"]),
                "best_pct": peak_pct,
                "best_team": best.get("team", ""),
                "best_matches": float(best.get("matches", 0)),
                "other_mean_value": other_mean_val,
                "other_mean_pct": other_mean_pct,
                "other_best_rank": other_best_rank,
                "pct_gap": gap if n_seasons >= MIN_SEASONS_FOR_CAREER else float("nan"),
                "meteor_score": meteor_score,
                "category": category,
                "season_values": " | ".join(
                    f"{int(r.season)}:{r[value_col]:.0f}(#{int(r.season_rank)})"
                    for _, r in g.iterrows()
                ),
            }
        )
    return pd.DataFrame(rows).sort_values("meteor_score", ascending=False)


def franchise_dependence(batting: pd.DataFrame) -> pd.DataFrame:
    """Share of team runs coming from the top scorer each season."""
    rows = []
    for (season, team), g in batting.groupby(["season", "team"]):
        if team in ("", "nan", "None") or g.empty:
            continue
        total = g["runs"].sum()
        if total <= 0:
            continue
        top = g.loc[g["runs"].idxmax()]
        rows.append(
            {
                "season": int(season),
                "team": team,
                "team_runs": total,
                "top_player": top["player"],
                "top_runs": float(top["runs"]),
                "dependence_pct": 100.0 * float(top["runs"]) / total,
                "n_batsmen": len(g),
            }
        )
    return pd.DataFrame(rows).sort_values("dependence_pct", ascending=False)


def volume_ghosts(careers: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """High career total, never cracked the true elite in any season."""
    g = careers[
        (careers["seasons_played"] >= MIN_SEASONS_FOR_CAREER)
        & (careers["best_rank"] > 10)
    ].copy()
    return g.sort_values("career_total", ascending=False).head(top_n)


def pure_meteors(careers: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    m = careers[careers["category"] == "meteor"].copy()
    if m.empty:
        m = careers[careers["seasons_played"] >= MIN_SEASONS_FOR_CAREER].copy()
    return m.sort_values("meteor_score", ascending=False).head(top_n)


# =============================================================================
# Narratives
# =============================================================================
def narrate_meteor(row: pd.Series) -> str:
    other = row["other_mean_value"]
    other_s = f"{other:.0f}" if pd.notna(other) else "-"
    gap = row["pct_gap"]
    gap_s = f"{gap:.0f}" if pd.notna(gap) else "-"

    return (
        f"In {int(row['best_season'])}, {row['player']} ({row['best_team']}) "
        f"posted {row['best_value']:.0f} - rank #{int(row['best_rank'])} that season "
        f"({row['best_pct']:.0f}th percentile). "
        f"Across their other {int(row['seasons_played']) - 1} season(s) in this sample "
        f"they averaged {other_s}. "
        f"Peak-to-baseline gap: {gap_s} percentile points. "
        f"Career line in sample: {row['season_values']}."
    )


def narrate_ghost(row: pd.Series) -> str:
    return (
        f"{row['player']} stacked {row['career_total']:.0f} across "
        f"{int(row['seasons_played'])} seasons, yet never finished higher than "
        f"#{int(row['best_rank'])} in any single year (best: {row['best_value']:.0f} "
        f"in {int(row['best_season'])}). High volume, low headlines."
    )


def narrate_dependence(row: pd.Series) -> str:
    return (
        f"{int(row['season'])} {row['team']}: {row['top_player']} scored "
        f"{row['top_runs']:.0f} of the team's {row['team_runs']:.0f} recorded runs "
        f"in this feed ({row['dependence_pct']:.1f}%). "
        f"One bat, heavy load."
    )


# =============================================================================
# HTML report
# =============================================================================
def html_escape(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_html(
    meteors: pd.DataFrame,
    ghosts: pd.DataFrame,
    dependence: pd.DataFrame,
    batting_careers: pd.DataFrame,
    seasons: list[int],
) -> str:
    def table(df: pd.DataFrame, cols: list[str], n: int = 12) -> str:
        if df.empty:
            return "<p><em>No rows matched the filters.</em></p>"
        view = df[cols].head(n)
        headers = "".join(f"<th>{html_escape(c)}</th>" for c in cols)
        body = []
        for _, r in view.iterrows():
            tds = "".join(f"<td>{html_escape(r[c])}</td>" for c in cols)
            body.append(f"<tr>{tds}</tr>")
        return f"<table><thead><tr>{headers}</tr></thead><tbody>{''.join(body)}</tbody></table>"

    meteor_stories = "\n".join(
        f"<li>{html_escape(narrate_meteor(r))}</li>"
        for _, r in meteors.head(5).iterrows()
    )
    ghost_stories = "\n".join(
        f"<li>{html_escape(narrate_ghost(r))}</li>"
        for _, r in ghosts.head(5).iterrows()
    )
    dep_stories = "\n".join(
        f"<li>{html_escape(narrate_dependence(r))}</li>"
        for _, r in dependence.head(5).iterrows()
    )

    season_list = ", ".join(str(s) for s in seasons)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>IPL Meteors &amp; Ghosts</title>
<style>
  :root {{
    --bg: #0b0f14;
    --panel: #141b24;
    --text: #e7eef7;
    --muted: #8b9bb0;
    --accent: #ff6b35;
    --accent2: #3dccc7;
    --line: #243041;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
    background: radial-gradient(1200px 600px at 10% -10%, #1a2330, var(--bg));
    color: var(--text);
    line-height: 1.55;
  }}
  main {{ max-width: 980px; margin: 0 auto; padding: 40px 20px 80px; }}
  h1 {{
    font-size: clamp(1.8rem, 4vw, 2.6rem);
    margin: 0 0 8px;
    letter-spacing: -0.02em;
  }}
  h2 {{
    margin-top: 48px;
    font-size: 1.35rem;
    color: var(--accent2);
    border-bottom: 1px solid var(--line);
    padding-bottom: 8px;
  }}
  .lede {{ color: var(--muted); font-size: 1.05rem; max-width: 62ch; }}
  .tag {{
    display: inline-block;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent);
    border: 1px solid var(--accent);
    padding: 3px 8px;
    border-radius: 999px;
    margin-bottom: 16px;
  }}
  .card {{
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 18px 20px;
    margin: 16px 0;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.92rem;
  }}
  th, td {{
    text-align: left;
    padding: 8px 10px;
    border-bottom: 1px solid var(--line);
    vertical-align: top;
  }}
  th {{ color: var(--muted); font-weight: 600; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.04em; }}
  tr:hover td {{ background: rgba(255,255,255,0.02); }}
  ul {{ padding-left: 1.15rem; }}
  li {{ margin: 10px 0; color: #d5deea; }}
  footer {{
    margin-top: 56px;
    color: var(--muted);
    font-size: 0.85rem;
  }}
  code {{ background: #0e141c; padding: 1px 6px; border-radius: 4px; }}
</style>
</head>
<body>
<main>
  <div class="tag">Uncommon IPL analytics</div>
  <h1>Meteors &amp; Ghosts</h1>
  <p class="lede">
    Most IPL stats pages rank who scored the most. This one ranks who
    <strong>exploded once and faded</strong>, who quietly piled runs without
    ever looking elite, and which franchises leaned hardest on a single bat.
  </p>
  <p class="lede">
    Sample seasons in this build: <strong>{html_escape(season_list)}</strong>
    (official aggregate feeds still published by iplt20.com).
  </p>

  <h2>1. Meteors - one season that doesn’t match the rest</h2>
  <div class="card">
    <p style="color:var(--muted);margin-top:0">
      Peak season percentile vs the player’s other seasons in this sample.
      High score = elite peak + ordinary baseline.
    </p>
    {table(
        meteors,
        ["player", "best_season", "best_value", "best_rank", "best_pct",
         "other_mean_value", "pct_gap", "meteor_score", "best_team"],
        12,
    )}
  </div>
  <div class="card">
    <strong>Short stories</strong>
    <ul>{meteor_stories or "<li>No meteor stories available.</li>"}</ul>
  </div>

  <h2>2. Volume ghosts - lots of runs, never the headline</h2>
  <div class="card">
    <p style="color:var(--muted);margin-top:0">
      Highest career totals among players who never finished top-10 in a season.
    </p>
    {table(
        ghosts,
        ["player", "seasons_played", "career_total", "best_season",
         "best_value", "best_rank", "season_values"],
        12,
    )}
  </div>
  <div class="card">
    <strong>Short stories</strong>
    <ul>{ghost_stories or "<li>No ghost stories available.</li>"}</ul>
  </div>

  <h2>3. Franchise dependence - one bat carrying the load</h2>
  <div class="card">
    <p style="color:var(--muted);margin-top:0">
      Share of a team’s recorded runs (in this feed) from its top scorer that season.
    </p>
    {table(
        dependence,
        ["season", "team", "top_player", "top_runs", "team_runs", "dependence_pct"],
        12,
    )}
  </div>
  <div class="card">
    <strong>Short stories</strong>
    <ul>{dep_stories or "<li>No dependence stories available.</li>"}</ul>
  </div>

  <footer>
    Built from public official stats feeds used by iplt20.com.
    This is not ball-by-ball data - ranks are within the published aggregate tables
    for the seasons above. Method: season percentile of runs, gap vs the same
    player’s other seasons, plus franchise top-scorer share.
    Generated by <code>meteors.py</code>.
  </footer>
</main>
</body>
</html>
"""


# =============================================================================
# Main
# =============================================================================
def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    batting_raw, bowling_raw = load_all_season_stats()
    batting = clean_batting(batting_raw)
    bowling = clean_bowling(bowling_raw)

    if batting.empty:
        raise SystemExit(
            "No batting data returned. The official feeds may have moved - "
            "re-check competition IDs in SEASONS."
        )

    batting.to_csv(OUT / "batting_seasons_clean.csv", index=False)
    if not bowling.empty:
        bowling.to_csv(OUT / "bowling_seasons_clean.csv", index=False)

    ranked = season_ranks(batting, "runs")
    careers = build_player_careers(ranked, "runs")
    meteors = pure_meteors(careers, 25)
    ghosts = volume_ghosts(careers, 15)
    dependence = franchise_dependence(batting)

    careers.to_csv(OUT / "player_careers.csv", index=False)
    meteors.to_csv(OUT / "meteors.csv", index=False)
    ghosts.to_csv(OUT / "volume_ghosts.csv", index=False)
    dependence.to_csv(OUT / "franchise_dependence.csv", index=False)

    lines = ["=== METEORS ===", ""]
    for _, r in meteors.head(8).iterrows():
        lines.append(narrate_meteor(r))
        lines.append("")
    lines += ["=== VOLUME GHOSTS ===", ""]
    for _, r in ghosts.head(8).iterrows():
        lines.append(narrate_ghost(r))
        lines.append("")
    lines += ["=== FRANCHISE DEPENDENCE ===", ""]
    for _, r in dependence.head(8).iterrows():
        lines.append(narrate_dependence(r))
        lines.append("")
    (OUT / "narratives.txt").write_text("\n".join(lines), encoding="utf-8")

    seasons = sorted(batting["season"].unique().tolist())
    html = render_html(meteors, ghosts, dependence, careers, seasons)
    html_path = OUT / "meteors_report.html"
    html_path.write_text(html, encoding="utf-8")

    print("\n======= TOP METEORS =======")
    cols = ["player", "best_season", "best_value", "best_rank", "other_mean_value", "meteor_score"]
    if not meteors.empty:
        print(meteors[cols].head(10).to_string(index=False))
    else:
        print("(none)")

    print("\n======= VOLUME GHOSTS =======")
    gcols = ["player", "seasons_played", "career_total", "best_rank", "best_season"]
    if not ghosts.empty:
        print(ghosts[gcols].head(8).to_string(index=False))
    else:
        print("(none - need multi-season overlap)")

    print("\n======= MOST DEPENDENT FRANCHISES =======")
    dcols = ["season", "team", "top_player", "dependence_pct"]
    if not dependence.empty:
        print(dependence[dcols].head(8).to_string(index=False))

    print(f"\nDone. Open: {html_path}")
    print(f"All files: {OUT}")


if __name__ == "__main__":
    main()