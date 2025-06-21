from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests, pandas as pd
from bs4 import BeautifulSoup
import io

# === Config ===
ELECTRICITY_MAPS_TOKEN = 'YOUR_ELECTRICITY_MAPS_API_TOKEN'
WATTTIME_TOKEN = 'YOUR_WATTTIME_API_TOKEN'
ELECTRICITY_MAPS_ZONE = 'IN'
WATTTIME_BA = 'CAISO_NORTH'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['you@example.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'asia_and_api_power_scrapers',
    default_args=default_args,
    description='Scrapes power and carbon data from Asian grid sites and APIs',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

# === API Scrapers ===
def scrape_electricity_maps():
    url = f"https://api.electricitymaps.com/v3/carbon-intensity/latest?zone={ELECTRICITY_MAPS_ZONE}"
    headers = {"Authorization": f"Bearer {ELECTRICITY_MAPS_TOKEN}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame([{
        'zone': ELECTRICITY_MAPS_ZONE,
        'datetime': data['datetime'],
        'carbonIntensity_gCO2eq_per_kWh': data['carbonIntensity'],
        'fossilFuelPercentage': data['fossilFuelPercentage'],
    }])
    df.to_csv(f'/tmp/electricitymaps_{ELECTRICITY_MAPS_ZONE}.csv', index=False)

def scrape_watttime():
    url = f"https://api2.watttime.org/v2/data"
    headers = {"Authorization": f"Bearer {WATTTIME_TOKEN}"}
    params = {"ba": WATTTIME_BA}
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    df = pd.DataFrame(r.json()['results'])
    df.to_csv('/tmp/watttime_data.csv', index=False)

def scrape_uk_carbon_intensity():
    url = "https://api.carbonintensity.org.uk/intensity"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()['data']
    df = pd.DataFrame([{
        'from': d['from'],
        'to': d['to'],
        'forecast': d['intensity']['forecast'],
        'actual': d['intensity']['actual'],
        'index': d['intensity']['index'],
    } for d in data])
    df.to_csv('/tmp/uk_carbon_intensity.csv', index=False)

# === Web/HTML/Excel Scrapers ===
def scrape_ngcp():
    url = 'https://www.ngcp.ph/operations'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = {}
    for section in soup.select('h4'):
        title = section.text.strip()
        table = section.find_next_sibling('table')
        if not table: continue
        df = pd.read_html(str(table))[0]
        data[title] = df
    if 'HOURLY DEMAND' in data:
        data['HOURLY DEMAND'].to_csv('/tmp/ngcp_hourly_demand.csv', index=False)
    if 'GROSS GENERATION PER PLANT TYPE' in data:
        data['GROSS GENERATION PER PLANT TYPE'].to_csv('/tmp/ngcp_generation_monthly.csv', index=False)

def scrape_posoco():
    # NOTE: Placeholder until actual endpoint confirmed
    url = 'https://posoco.in/wp-admin/admin-ajax.php'
    params = {'action': 'gettodayoutput', 'region': 'ALL'}
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame(data['data'])  # Adjust this to match actual structure
    df.to_csv('/tmp/posoco_generation_mix.csv', index=False)

def scrape_pucsl():
    url = 'https://www.pucsl.gov.lk/statistical-data/plant_generation.xlsx'
    r = requests.get(url)
    df = pd.read_excel(io.BytesIO(r.content), sheet_name=0)
    df.to_csv('/tmp/pucsl_generation.csv', index=False)

# === Tasks ===
t1 = PythonOperator(task_id='scrape_electricity_maps', python_callable=scrape_electricity_maps, dag=dag)
t2 = PythonOperator(task_id='scrape_watttime', python_callable=scrape_watttime, dag=dag)
t3 = PythonOperator(task_id='scrape_uk_carbon_intensity', python_callable=scrape_uk_carbon_intensity, dag=dag)
t4 = PythonOperator(task_id='scrape_ngcp', python_callable=scrape_ngcp, dag=dag)
t5 = PythonOperator(task_id='scrape_posoco', python_callable=scrape_posoco, dag=dag)
t6 = PythonOperator(task_id='scrape_pucsl', python_callable=scrape_pucsl, dag=dag)

# Run in parallel or in order as desired
[t1, t2, t3, t4, t5] >> t6  # all run, then PUCSL runs last
