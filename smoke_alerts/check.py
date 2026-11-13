import os

import httpx

from . import nsw, store


def decide(site, pm25, threshold, already_alerting):
    """Return (send, now_alerting). Alert once when crossing up, reset when back under."""
    over = pm25 >= threshold
    return (over and not already_alerting), over


def notify(client, site, pm25, threshold):
    topic = os.environ["NTFY_TOPIC"]
    client.post(f"https://ntfy.sh/{topic}", content=f"PM2.5 at {site.title()} is {pm25:.0f} ug/m3 (your limit {threshold:.0f})".encode(),
                headers={"Title": "Smoke alert", "Priority": "high", "Tags": "warning"}, timeout=20)


def run():
    c = store.conn()
    settings = store.get_settings(c)
    with httpx.Client() as client:
        ids = nsw.site_ids(client)
        wanted = {ids[s]: s for s in settings["sites"] if s in ids}
        for sid, r in nsw.latest_pm25(client, wanted).items():
            site = wanted[sid]
            store.save_reading(c, site, r["ts"], r["pm25"])
            send, on = decide(site, r["pm25"], settings["threshold"], store.is_alerting(c, site))
            if send:
                notify(client, site, r["pm25"], settings["threshold"])
            store.set_alerting(c, site, on)


if __name__ == "__main__":
    run()
