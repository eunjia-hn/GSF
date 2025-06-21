import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = 'https://www.ngcp.ph/operations'

def scrape_ngcp():
    res = requests.get(BASE_URL)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')

    data = {}
    for section in soup.select('h4'):
        title = section.text.strip()
        table = section.find_next_sibling('table')
        if not table: continue
        df = pd.read_html(str(table))[0]
        data[title] = df
        print(f"Scraped section: {title}")
    return data

if __name__ == '__main__':
    ngcp_data = scrape_ngcp()
    ngcp_data['HOURLY DEMAND'].to_csv('ngcp_hourly_demand.csv', index=False)
    ngcp_data['GROSS GENERATION PER PLANT TYPE'].to_csv('ngcp_generation_monthly.csv', index=False)
