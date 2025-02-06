from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 2, 6),
    "retries": 1,
}


dag = DAG(
    "etl_ml_pipeline",
    default_args=default_args,
    schedule_interval="@daily",  # Runs once a day
    catchup=False
)

start = DummyOperator(task_id="start", dag=dag)

etl_task = DockerOperator(
    task_id="run_etl",
    image="ml_model_container",  # Name of the ML model container
    api_version="auto",
    auto_remove=True,
    command=["python", "etl.py"],
    network_mode="bridge",
    dag=dag
)

train_task = DockerOperator(
    task_id="train_model",
    image="ml_model_container",
    api_version="auto",
    auto_remove=True,
    command=["python", "model.py"],
    network_mode="bridge",
    dag=dag
)

end = DummyOperator(task_id="end", dag=dag)

start >> etl_task >> train_task >> end