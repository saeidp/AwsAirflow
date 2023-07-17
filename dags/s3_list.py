from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.operators.athena import AthenaOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.operators.glue_crawler import GlueCrawlerOperator
from airflow.providers.amazon.aws.operators.s3 import (
    S3CreateBucketOperator,
    S3CreateObjectOperator,
    S3DeleteBucketOperator,
)
from airflow.providers.amazon.aws.sensors.glue import GlueJobSensor
from airflow.providers.amazon.aws.sensors.glue_crawler import GlueCrawlerSensor

import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'retries': 1,
    'retry_delay': datetime. timedelta(hours=1),
}

dag = DAG(
    's3_list',
    default_args=default_args,
    description='A simple DAG to demonstrate Airflow with PyTorch and Kubernetes',
    schedule_interval='@daily',
    catchup=False
)

def read_images_from_s3(**kwargs):
    s3_conn = S3Hook(aws_conn_id='aws_default')
    # images = []
    for obj in s3_conn.get_bucket('saeid-test').objects.all():
        print(obj)
    #     images.append(obj.key)
    # kwargs['ti'].xcom_push(key='images', value=images)

read_images = PythonOperator(
    task_id='read_images',
    python_callable=read_images_from_s3,
    provide_context=True,
    dag=dag
)

read_images