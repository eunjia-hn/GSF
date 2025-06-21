import requests, pandas as pd
import io

PUCSL_URL = 'https://www.pucsl.gov.lk/statistical-data/plant_generation.xlsx'

def scrape_pucsl():
    r = requests.get(PUCSL_URL)
    r.raise_for_status()
    df = pd.read_excel(io.BytesIO(r.content), sheet_name=0)
    df.to_csv('pucsl_generation.csv', index=False)
    print("Saved PUCSL plant-level generation data.")

if __name__ == '__main__':
    scrape_pucsl()
