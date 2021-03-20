from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta, date
from airflow.utils.dates import days_ago
from pathlib import Path

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'loganalyzer',
    default_args=default_args,
    description='Log Analyzer',
    schedule_interval='0 18 * * 1-5',
    start_date=days_ago(1)
)

def analyze_file(**kwargs):

    file_list = Path('/usr/local/airflow/logs/marketvol/{}'.format(kwargs['file'])).rglob('*.log')

    error_count = 0
    error_lines = []

    for file in file_list:

        with open(file, 'r') as log_file:
        
            for line in log_file:
                if 'ERROR' in line:
                    error_count += 1
                    error_lines.append(line)

    return error_count, error_lines

t1 = PythonOperator(
    task_id='create_directory',
    python_callable=analyze_file,
    provide_context=True,
    op_kwargs={'file': 'create_directory'},
    dag=dag
)

t2 = PythonOperator(
    task_id='get_apple_data',
    python_callable=analyze_file,
    provide_context=True,
    op_kwargs={'file': 'get_apple_data'},
    dag=dag
)

t3 = PythonOperator(
    task_id='get_tesla_data',
    python_callable=analyze_file,
    provide_context=True,
    op_kwargs={'file': 'get_tesla_data'},
    dag=dag
)

t4 = PythonOperator(
    task_id='move_apple',
    python_callable=analyze_file,
    provide_context=True,
    op_kwargs={'file': 'move_apple'},
    dag=dag
)

t5 = PythonOperator(
    task_id='move_tesla',
    python_callable=analyze_file,
    provide_context=True,
    op_kwargs={'file': 'move_tesla'},
    dag=dag
)

t6 = PythonOperator(
    task_id='query_data',
    python_callable=analyze_file,
    provide_context=True,
    op_kwargs={'file': 'query_data'},
    dag=dag
)

def print_results(**kwargs):
    ti = kwargs['ti']
    
    t1_count, t1_lines = ti.xcom_pull(task_ids='create_directory')
    t2_count, t2_lines = ti.xcom_pull(task_ids='get_apple_data')
    t3_count, t3_lines = ti.xcom_pull(task_ids='get_tesla_data')
    t4_count, t4_lines = ti.xcom_pull(task_ids='move_apple')
    t5_count, t5_lines = ti.xcom_pull(task_ids='move_tesla')
    t6_count, t6_lines = ti.xcom_pull(task_ids='query_data')
    error_count = t1_count + t2_count + t3_count + t4_count + t5_count + t6_count
    error_lines = t1_lines + t2_lines + t3_lines + t4_lines + t5_lines + t6_lines
    print('ERROR COUNT is {}'.format(error_count))
    for line in error_lines:
        print(line)

t7 = PythonOperator(
    task_id='print_results',
    python_callable=print_results,
    provide_context=True,
    dag=dag
)

t1 >> t2 >> t3 >> t4 >> t5 >> t6 >> t7