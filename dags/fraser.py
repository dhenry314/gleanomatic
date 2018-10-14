from airflow import DAG
from airflow.operators import BashOperator
from MOHUB.configure import default_args
from datetime import datetime, timedelta

dag = DAG('frbstl.fraser', default_args=default_args)

ingest = BashOperator(
        task_id='fraserIngest',
        bash_command='python /usr/local/airflow/dags/MOHUB/oaiIngest.py frbstl.fraser',
        dag=dag
     )

