import os
import pandas as pd
import pendulum
import vertica_python
from airflow import DAG
from airflow.hooks.base import BaseHook
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

SCHEMA = 'VT2610287BD414__STAGING'


def load_group_log_to_vertica(table_name: str, csv_path: str, copy_sql: str) -> None:
    df_group_log = pd.read_csv(csv_path)
    df_group_log['user_id_from'] = pd.array(df_group_log['user_id_from'], dtype='Int64')

    tmp_csv_path = '/data/group_log_prepared.csv'
    df_group_log.to_csv(tmp_csv_path, index=False)

    conn = BaseHook.get_connection('vertica_conn')
    conn_info = {
        'host': conn.host,
        'port': conn.port,
        'user': conn.login,
        'password': conn.password,
        'database': conn.schema or 'dwh',
        'autocommit': True,
    }

    try:
        with vertica_python.connect(**conn_info) as connection:
            cur = connection.cursor()
            cur.execute(f'TRUNCATE TABLE {SCHEMA}.{table_name};')
            with open(tmp_csv_path, 'rb') as f:
                cur.copy(copy_sql, f)
            cur.execute(f'SELECT COUNT(*) FROM {SCHEMA}.{table_name};')
            count = cur.fetchone()[0]
            print(f'Успешно загружено строк в {SCHEMA}.{table_name}: {count}')
    finally:
        if os.path.exists(tmp_csv_path):
            os.remove(tmp_csv_path)


with DAG(
    dag_id='sprint6_project_load_staging',
    schedule_interval=None,
    start_date=pendulum.parse('2022-02-22'),
    catchup=False,
    tags=['sprint6', 'project', 'staging'],
) as dag:

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    load_group_log = PythonOperator(
        task_id='load_group_log',
        python_callable=load_group_log_to_vertica,
        op_kwargs={
            'table_name': 'group_log',
            'csv_path': '/data/group_log.csv',
            'copy_sql': f'''
                COPY {SCHEMA}.group_log (group_id, user_id, user_id_from, event, datetime)
                FROM STDIN
                DELIMITER ','
                NULL ''
                ENCLOSED BY '"'
                SKIP 1
                REJECTED DATA AS TABLE {SCHEMA}.group_log_rej;
            ''',
        },
    )

    start >> load_group_log >> end