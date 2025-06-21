from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests, pandas as pd
from bs4 import BeautifulSoup
import io

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['you@example.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'asia_power_scrapers',
    default_args=default_args,
    description='Scrape NGCP, POSOCO, PUCSL electricity data daily',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

def scrape_ngcp():
    url = 'https://www.ngcp.ph/operations'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    data = {}
    for section in soup.select('h4'):
        title = section.text.strip()
        table = section.find_next_sibling('table')
        if not table: continue
        df = pd.read_html(str(table))[0]
        data[title] = df
    data['HOURLY DEMAND'].to_csv('/tmp/ngcp_hourly_demand.csv', index=False)
    data['GROSS GENERATION PER PLANT TYPE'].to_csv('/tmp/ngcp_generation_monthly.csv', index=False)

def scrape_posoco():
    # Replace with actual XHR endpoint
    api = 'https://posoco.in/wp-admin/admin-ajax.php'
    params = {'action': 'gettodayoutput', 'region': 'ALL'}
    res = requests.get(api, params=params)
    df = pd.DataFrame(res.json()['data'])
    df.to_csv('/tmp/posoco_generation_mix.csv', index=False)

def scrape_pucsl():
    url = 'https://www.pucsl.gov.lk/statistical-data/plant_generation.xlsx'
    r = requests.get(url)
    df = pd.read_excel(io.BytesIO(r.content), sheet_name=0)
    df.to_csv('/tmp/pucsl_generation.csv', index=False)

task_ngcp = PythonOperator(
    task_id='scrape_ngcp',
    python_callable=scrape_ngcp,
    dag=dag,
)

task_posoco = PythonOperator(
    task_id='scrape_posoco',
    python_callable=scrape_posoco,
    dag=dag,
)

task_pucsl = PythonOperator(
    task_id='scrape_pucsl',
    python_callable=scrape_pucsl,
    dag=dag,
)

task_ngcp >> task_posoco >> task_pucsl  # run in sequence
