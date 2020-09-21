from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

default_args = {
    'owner': 'chrolss',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'retries': 2,
    'retry_delay': timedelta(minutes=60)
}
dag = DAG(dag_id='polisen_etl',
          default_args=default_args,
          description='ETL workflow for polisen API',
          schedule_interval='0 6 * * *')

startTask = DummyOperator(
    task_id='Start',
    dag=dag
)

downloadTask = BashOperator(
    task_id='Download',
    bash_command='python3 ~/PycharmProjects/polisen_api/main.py'
)

etlTask = BashOperator(
    task_id='Transform',
    bash_command='python3 ~/PycharmProjects/polisen_api/data_model.py'
)

startTask >> downloadTask >> etlTask
