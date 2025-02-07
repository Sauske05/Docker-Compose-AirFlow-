from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

# default_args = {
#     "owner": "airflow",
#     "start_date": datetime(2025, 2, 7),
#     "retries": 1,
# }


# dag = DAG(
#     "etl_ml_pipeline",
#     default_args=default_args,
#     schedule="@daily",  # Runs once a day
#     catchup=False
# )

# start = EmptyOperator(task_id="start", dag=dag)

# etl_task = DockerOperator(
#     task_id="run_etl",
#     image="etl_image",  # Name of the ML model container
#     #api_version="auto",
#     network_mode = "host",
#     #auto_remove=True,
#     #command=["python", "etl.py"],
#     #network_mode="backend_network",
#     dag=dag,
#     docker_url="unix://var/run/docker.sock",  # Ensure access to Docker daemon
#     environment={
#         "DB_HOST": "my-mysql",
#         "DB_USER": "arun",
#         "DB_PASSWORD": "root",
#         "DB_NAME": "yfinance"
#     }
# )

# train_task = DockerOperator(
#     task_id="train_model",
#     image="model_image",
#     #api_version="auto",
#     network_mode = "host",
#     #auto_remove=True,
#     #command=["python", "model.py"],
#     #network_mode="backend_network",
#     dag=dag,
#     docker_url="unix://var/run/docker.sock",  # Ensure access to Docker daemon
#     environment={
#         "DB_HOST": "my-mysql",
#         "DB_USER": "arun",
#         "DB_PASSWORD": "root",
#         "DB_NAME": "yfinance"
#     }
# )

# end = EmptyOperator(task_id="end", dag=dag)

# start >> etl_task >> train_task >> end

#import pendulum
from airflow.decorators import dag, task

# Default arguments
default_args = {
    "start_date": datetime(2025, 2, 7),
    "retries": 1,
}

@dag(
    default_args=default_args,
    schedule_interval="@daily",  # Runs once a day
    catchup=False,
)
def etl_ml_pipeline():
    """
    ### ETL and ML Pipeline
    This DAG performs an ETL process followed by a machine learning model training,
    utilizing Docker containers for task isolation.
    """

    t1 = DockerOperator(
        image="etl_image",  # Name of the ETL Docker image
        network_mode="host",
        docker_url="unix://var/run/docker.sock", # Ensure access to Docker daemon
        command = 'echo "command running in docker container"',
        environment={
            "DB_HOST": "my-mysql",
            "DB_USER": "arun",
            "DB_PASSWORD": "root",
            "DB_NAME": "yfinance",
        },
    )

    t2 = DockerOperator(
        image="model_image",  # Name of the ML model Docker image
        network_mode="host",
        docker_url="unix://var/run/docker.sock",  # Ensure access to Docker daemon
        command = 'echo "command running in docker container"',
        environment={
            "DB_HOST": "my-mysql",
            "DB_USER": "arun",
            "DB_PASSWORD": "root",
            "DB_NAME": "yfinance",
        },
    )
    t1 >> t2
# Instantiate the DAG
dag = etl_ml_pipeline()