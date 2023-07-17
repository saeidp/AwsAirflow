import os
from datetime import timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.models.baseoperator import chain
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

DAG_ID = os.path.basename(__file__).replace(".py", "")
DEFAULT_ARGS = {
    "owner": "saeid",
    "depends_on_past": False,
    "retries": 0,
    "email_on_failure": False,
    "email_on_retry": False,
}

with DAG(
    dag_id=DAG_ID,
    description="Prepare Data Lake Demonstration using BashOperator and AWS CLI vs. AWS Operators",
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(minutes=5),
    start_date=days_ago(1),
    schedule_interval=None,
    tags=["data lake demo"],
) as dag:
    
   begin = DummyOperator(task_id="begin")

   end = DummyOperator(task_id="end")
   
   create_demo_catalog = BashOperator(
            task_id="create_demo_catalog",
            bash_command="""aws glue create-database --database-input \
                '{"Name": "tickit_demo", "Description": "Datasets from AWS E-commerce TICKIT relational database"}'""",
        )

   chain(
        begin,
        create_demo_catalog,
        end,
    )