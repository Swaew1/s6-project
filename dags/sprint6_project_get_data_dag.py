import os
import boto3
import pendulum
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def fetch_s3_file(bucket: str, key: str) -> None:
    os.makedirs('/data', exist_ok=True)

    aws_access_key_id = Variable.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = Variable.get('AWS_SECRET_ACCESS_KEY')

    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    destination_path = f'/data/{key}'
    s3_client.download_file(
        Bucket=bucket,
        Key=key,
        Filename=destination_path,
    )
    print(f'Файл {key} успешно скачан в {destination_path}')


bash_command_tmpl = """
{% for file in params.files %}
  echo "=== {{ file }} ==="
  head -n 10 {{ file }}
{% endfor %}
"""

bucket_files = ['group_log.csv']

with DAG(
    dag_id='sprint6_project_get_data',
    schedule_interval=None,
    start_date=pendulum.parse('2022-02-22'),
    catchup=False,
    tags=['sprint6', 'project'],
) as dag:
    fetch_tasks = []

    for file_name in bucket_files:
        task = PythonOperator(
            task_id=f'fetch_{file_name}',
            python_callable=fetch_s3_file,
            op_kwargs={
                'bucket': 'sprint6',
                'key': file_name,
            },
        )
        fetch_tasks.append(task)

    print_10_lines_of_each = BashOperator(
        task_id='print_10_lines_of_each',
        bash_command=bash_command_tmpl,
        params={'files': [f'/data/{f}' for f in bucket_files]},
    )

    fetch_tasks >> print_10_lines_of_each