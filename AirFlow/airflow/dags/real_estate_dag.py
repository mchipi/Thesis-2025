from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import requests

from scrape.novel_scrape import scrape_novel
from scrape.square_scrape import scrape_square
from scrape.delta_scrape import scrape_delta

from clean.novel_clean import clean_novel
from clean.square_clean import clean_square
from clean.delta_clean import clean_delta

from push.novel_push import push_novel
from push.square_push import push_square
from push.delta_push import push_delta

from scrape.reklama5_scrape import scrape_reklama5
from clean.reklama5_clean import clean_reklama5
from push.reklama5_push import push_reklama5

from scrape.pazar3_scrape import scrape_pazar3
from clean.pazar3_clean import clean_pazar3
from push.pazar3_push import push_pazar3

dag = DAG(
    'real_estate_pipeline',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 23 * * *',
    description='A pipeline to scrape, clean, transform, and load real estate data',
    catchup=False
)

def pass_data(**kwargs):
    return kwargs['task_instance'].xcom_pull(task_ids=kwargs['downstream_task_id'])


# novel
scrape_novel_task = PythonOperator(
    task_id='scrape_novel',
    python_callable=scrape_novel,
    provide_context=True,
    dag=dag
)

clean_novel_task = PythonOperator(
    task_id='clean_novel',
    python_callable=clean_novel,
    provide_context=True,
    dag=dag
)

push_novel_task = PythonOperator(
    task_id='push_novel',
    python_callable=push_novel,
    provide_context=True,
    dag=dag
)


# square
scrape_square_task = PythonOperator(
    task_id='scrape_square',
    python_callable=scrape_square,
    provide_context=True,
    dag=dag
)

clean_square_task = PythonOperator(
    task_id='clean_square',
    python_callable=clean_square,
    provide_context=True,
    dag=dag
)

push_square_task = PythonOperator(
    task_id='push_square',
    python_callable=push_square,
    provide_context=True,
    dag=dag
)


# delta
scrape_delta_task = PythonOperator(
    task_id='scrape_delta',
    python_callable=scrape_delta,
    provide_context=True,
    dag=dag
)

clean_delta_task = PythonOperator(
    task_id='clean_delta',
    python_callable=clean_delta,
    provide_context=True,
    dag=dag
)

push_delta_task = PythonOperator(
    task_id='push_delta',
    python_callable=push_delta,
    provide_context=True,
    dag=dag
)


# reklama5
scrape_reklama5_task = PythonOperator(
    task_id='scrape_reklama5',
    python_callable=scrape_reklama5,
    provide_context=True,
    dag=dag
)

clean_reklama5_task = PythonOperator(
    task_id='clean_reklama5',
    python_callable=clean_reklama5,
    provide_context=True,
    dag=dag
)

push_reklama5_task = PythonOperator(
    task_id='push_reklama5',
    python_callable=push_reklama5,
    provide_context=True,
    dag=dag
)


# pazar3
scrape_pazar3_task = PythonOperator(
    task_id='scrape_pazar3',
    python_callable=scrape_pazar3,
    provide_context=True,
    dag=dag
)

clean_pazar3_task = PythonOperator(
    task_id='clean_pazar3',
    python_callable=clean_pazar3,
    provide_context=True,
    dag=dag
)

push_pazar3_task = PythonOperator(
    task_id='push_pazar3',
    python_callable=push_pazar3,
    provide_context=True,
    dag=dag
)


scrape_novel_task >> clean_novel_task >> push_novel_task

scrape_square_task >> clean_square_task >> push_square_task

scrape_delta_task >> clean_delta_task >> push_delta_task

scrape_reklama5_task >> clean_reklama5_task >> push_reklama5_task

scrape_pazar3_task >> clean_pazar3_task >> push_pazar3_task