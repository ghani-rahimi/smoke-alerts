import json
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "state.db"

DEFAULTS = {"threshold": 25.0, "sites": ["LIVERPOOL", "CHULLORA", "BARGO", "CAMDEN"]}


def conn(path=DB):
    c = sqlite3.connect(path)
    c.execute("create table if not exists settings (k text primary key, v text)")
    c.execute("create table if not exists readings (site text, ts text, pm25 real, primary key (site, ts))")
    c.execute("create table if not exists alerting (site text primary key)")
    return c


def get_settings(c):
    s = dict(DEFAULTS)
    for k, v in c.execute("select k, v from settings"):
        s[k] = json.loads(v)
    return s


def set_setting(c, k, v):
    c.execute("insert or replace into settings values (?, ?)", (k, json.dumps(v)))
    c.commit()


def save_reading(c, site, ts, pm25):
    c.execute("insert or replace into readings values (?, ?, ?)", (site, ts, pm25))
    c.commit()


def recent(c, n=24):
    rows = c.execute("select site, ts, pm25 from readings order by ts desc limit ?", (n,)).fetchall()
    return [{"site": s, "ts": t, "pm25": v} for s, t, v in rows]


def is_alerting(c, site):
    return c.execute("select 1 from alerting where site = ?", (site,)).fetchone() is not None


def set_alerting(c, site, on):
    if on:
        c.execute("insert or ignore into alerting values (?)", (site,))
    else:
        c.execute("delete from alerting where site = ?", (site,))
    c.commit()
