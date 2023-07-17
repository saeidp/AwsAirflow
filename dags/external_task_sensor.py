# This example does not work
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.sensors.external_task import ExternalTaskSensor

# Define default arguments for the DAGs
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 7, 1),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the parent DAG
parent_dag = DAG(
    'parent_dag',
    schedule_interval='@daily',
    default_args=default_args,
    catchup=False
)

# Define a task in the parent DAG
task_parent = DummyOperator(
    task_id='task_parent',
    dag=parent_dag
)

# Create the child DAG
child_dag = DAG(
    'child_dag',
    schedule_interval='@daily',
    default_args=default_args,
    catchup=False
)

# Define a task in the child DAG
task_child = DummyOperator(
    task_id='task_child',
    dag=child_dag
)

# Define an ExternalTaskSensor in the child DAG, waiting for the task in the parent DAG to complete
sensor_task = ExternalTaskSensor(
    task_id='sensor_task',
    external_dag_id='parent_dag',  # The ID of the parent DAG
    external_task_id='task_parent',  # The ID of the task in the parent DAG to wait for
    dag=child_dag,
    mode='reschedule',  # This mode will keep re-scheduling the sensor task until the parent task is successful
)

# Set the dependencies between tasks
task_parent >> sensor_task >> task_child
