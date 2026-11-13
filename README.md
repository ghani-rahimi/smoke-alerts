smoke-alerts
============

Every hourly reading from the NSW air quality monitors near me, and a phone notification when PM2.5 goes over a level I set.

Started this in the 2019-20 bushfire season after a few nights where the air was bad and I only found out the next
morning. Rewrote it properly in 2024 with Airflow and a small FastAPI app to change settings.

How it works
------------

- An Airflow DAG runs every hour and asks the NSW Air Quality API for the last hour of PM2.5 at the sites in my config
  (Liverpool, Chullora, Bargo, Camden by default)
- If the reading at any site is over the threshold, it sends a push through ntfy.sh to my phone
- It won't send again for the same site until the level drops back under the threshold, otherwise you get an alert
  every hour all night
- The FastAPI app lets me change the threshold and sites from my phone, and shows the last 24 readings

Thresholds: default is 25 ug/m3 (hourly), which is roughly where the NSW air quality category moves from fair to poor.

Setup
-----

    pip install -r requirements.txt
    export NTFY_TOPIC=some-long-random-topic-name
    uvicorn smoke_alerts.api:app --port 8008
    # and point AIRFLOW_HOME at this folder, then: airflow standalone

Tests: `pytest`
