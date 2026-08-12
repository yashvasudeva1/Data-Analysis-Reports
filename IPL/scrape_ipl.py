#!/usr/bin/env python3
"""
IPL Official Stats Scraper (iplt20.com backend feeds)
Fully automatic – no configuration required.

Saves CSV files into ./ipl_stats/
"""

import json
import time
from pathlib import Path

import pandas as pd
import requests

# ---------------------------------------------------------------------------
# Configuration (already filled – do not change unless feeds move)
# ---------------------------------------------------------------------------
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
# (discovered by probing the live feeds)
SEASONS = {
    "alltime": "alltime",   # career totals
    2019: 60,               # Jos Buttler 863
    2023: 107,              # Shubman Gill 890
    2024: 148,              # Virat Kohli 741
    2025: 203,              # Sai Sudharsan 759
    2026: 284,              # latest season present on CDN
}

# Stat endpoints that exist for both all-time and season feeds
STAT_ENDPOINTS = [
    "toprunsscorers",
    "mostwickets",
    "mostfours",
    "mostsixes",
    "bestbowlingfigures",
    "mostfifties",
    "mostcenturies",
    "fastestfifties",
    "fastestcenturies",
    "mosthattricks",
    "mostfourwickets",
    "mostfoursinnings",
    "mostsixesinnings",
]

OUTPUT_DIR = Path("ipl_stats")
REQUEST_DELAY = 0.8          # seconds between requests (be polite)
TIMEOUT = 30

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
session = requests.Session()
session.headers.update(HEADERS)


def fetch_jsonp(url: str) -> dict | None:
    """Download a JSONP feed and return the inner JSON object."""
    try:
        r = session.get(url, timeout=TIMEOUT)
        if r.status_code != 200 or len(r.text) < 400:
            return None
        text = r.text
        start = text.find("(")
        end = text.rfind(")")
        if start == -1 or end == -1:
            return None
        return json.loads(text[start + 1 : end])
    except Exception as exc:
        print(f"    [error] {exc}")
        return None


def extract_records(data: dict) -> list:
    """Return the list of player/stat rows from the JSON payload."""
    if not data:
        return []
    # Usually the only key is the endpoint name
    for key, value in data.items():
        if isinstance(value, list):
            return value
    return []


def scrape_one(season_label, competition_id: str | int, endpoint: str) -> pd.DataFrame | None:
    """Fetch one stat table and return a DataFrame (or None)."""
    url = f"{BASE}/{competition_id}-{endpoint}.js?callback=on{endpoint}"
    print(f"  → {season_label} / {endpoint}")
    data = fetch_jsonp(url)
    records = extract_records(data)
    if not records:
        print(f"    (no data)")
        return None

    df = pd.DataFrame(records)
    df.insert(0, "Season", season_label)
    df.insert(1, "StatType", endpoint)
    return df


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output folder: {OUTPUT_DIR.resolve()}\n")

    all_frames = []
    success = 0
    failed = 0

    for season_label, competition_id in SEASONS.items():
        print(f"=== Season: {season_label} (id={competition_id}) ===")
        for endpoint in STAT_ENDPOINTS:
            df = scrape_one(season_label, competition_id, endpoint)
            time.sleep(REQUEST_DELAY)

            if df is None or df.empty:
                failed += 1
                continue

            # Individual file
            safe_season = str(season_label).replace(" ", "_")
            out_file = OUTPUT_DIR / f"{safe_season}_{endpoint}.csv"
            df.to_csv(out_file, index=False)
            print(f"    saved {out_file.name}  ({len(df)} rows)")
            all_frames.append(df)
            success += 1

    # Combined master file (all seasons + all stats)
    if all_frames:
        master = pd.concat(all_frames, ignore_index=True)
        master_path = OUTPUT_DIR / "ALL_IPL_STATS_COMBINED.csv"
        master.to_csv(master_path, index=False)
        print(f"\nMaster file: {master_path}  ({len(master)} total rows)")

    print(f"\nDone.  Success: {success}   Empty/failed: {failed}")
    print(f"Files are in: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()