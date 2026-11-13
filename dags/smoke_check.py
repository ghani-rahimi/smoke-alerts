from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from smoke_alerts.check import run

with DAG(
    "smoke_check",
    schedule="5 * * * *",  # readings land a few minutes after the hour
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={"retries": 3, "retry_delay": timedelta(minutes=4)},
) as dag:
    PythonOperator(task_id="check_pm25", python_callable=run)
