"""NSW Air Quality API: https://data.airquality.nsw.gov.au/docs/index.html"""
from datetime import date, timedelta

import httpx

BASE = "https://data.airquality.nsw.gov.au/api/Data"


def site_ids(client):
    r = client.get(f"{BASE}/get_SiteDetails", timeout=30)
    r.raise_for_status()
    return {s["SiteName"].upper(): s["Site_Id"] for s in r.json()}


def latest_pm25(client, site_ids_wanted):
    today = date.today()
    body = {
        "Parameters": ["PM2.5"],
        "Sites": list(site_ids_wanted),
        "StartDate": (today - timedelta(days=1)).isoformat(),
        "EndDate": (today + timedelta(days=1)).isoformat(),
        "Categories": ["Averages"],
        "SubCategories": ["Hourly"],
        "Frequency": ["Hourly average"],
    }
    r = client.post(f"{BASE}/get_Observations", json=body, timeout=60)
    r.raise_for_status()
    latest = {}
    for obs in r.json():
        if obs.get("Value") is None:
            continue
        key = (obs["Date"], obs["Hour"])
        sid = obs["Site_Id"]
        if sid not in latest or key > latest[sid][0]:
            latest[sid] = (key, float(obs["Value"]))
    return {sid: {"ts": f"{d} {h:02d}:00", "pm25": v} for sid, ((d, h), v) in latest.items()}
