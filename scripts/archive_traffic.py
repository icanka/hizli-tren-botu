#!/usr/bin/env python3
"""Archive GitHub repository traffic (views, clones, referrers, paths).

GitHub only exposes the last 14 days of traffic data. This script fetches
that window and merges it into a permanent archive:

  data/traffic.csv                          one row per UTC day
  data/snapshots/referrers/YYYY-MM-DD.json  daily top-10 referrers
  data/snapshots/paths/YYYY-MM-DD.json      daily top-10 paths

Environment variables:
  TRAFFIC_TOKEN  token with access to the repository traffic API (required)
  SOURCE_REPO    "owner/repo" to read traffic from (default: icanka/hizli-tren-botu)
  OUT_DIR        directory to write the archive into (default: .)
"""

import csv
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://api.github.com"
FIELDNAMES = ["date", "views", "unique_views", "clones", "unique_cloners"]
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "traffic-archive-script",
}


def api_get(path, token):
    request = urllib.request.Request(
        API + path, headers={**HEADERS, "Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def load_daily(csv_path):
    rows = {}
    if csv_path.exists():
        with csv_path.open(newline="", encoding="utf-8") as archive:
            for row in csv.DictReader(archive):
                rows[row["date"]] = row
    return rows


def merge_daily(rows, days, field, unique_field):
    for entry in days:
        date = entry["timestamp"][:10]
        row = rows.setdefault(
            date,
            {
                "date": date,
                "views": "",
                "unique_views": "",
                "clones": "",
                "unique_cloners": "",
            },
        )
        row[field] = str(entry["count"])
        row[unique_field] = str(entry["uniques"])
    return rows


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    token = os.environ.get("TRAFFIC_TOKEN")
    if not token:
        sys.exit("TRAFFIC_TOKEN is not set")
    source = os.environ.get("SOURCE_REPO", "icanka/hizli-tren-botu")
    out_dir = Path(os.environ.get("OUT_DIR", ".")).resolve()

    views = api_get(f"/repos/{source}/traffic/views?per=day", token)
    clones = api_get(f"/repos/{source}/traffic/clones?per=day", token)
    referrers = api_get(f"/repos/{source}/traffic/popular/referrers", token)
    paths = api_get(f"/repos/{source}/traffic/popular/paths", token)

    csv_path = out_dir / "data" / "traffic.csv"
    rows = load_daily(csv_path)
    merge_daily(rows, views["views"], "views", "unique_views")
    merge_daily(rows, clones["clones"], "clones", "unique_cloners")

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as archive:
        writer = csv.DictWriter(archive, fieldnames=FIELDNAMES)
        writer.writeheader()
        for date in sorted(rows):
            writer.writerow(rows[date])

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    write_json(out_dir / "data" / "snapshots" / "referrers" / f"{today}.json", referrers)
    write_json(out_dir / "data" / "snapshots" / "paths" / f"{today}.json", paths)

    latest = rows[max(rows)] if rows else {}
    print(
        f"Archived {len(rows)} day(s); latest {latest.get('date')}: "
        f"{latest.get('views')} views / {latest.get('clones')} clones; "
        f"{len(referrers)} referrers, {len(paths)} paths"
    )


if __name__ == "__main__":
    main()
