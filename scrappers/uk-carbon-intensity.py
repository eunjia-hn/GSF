import requests
import pandas as pd

def fetch_uk_carbon_intensity():
    url = "https://api.carbonintensity.org.uk/intensity"
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()['data']

    df = pd.DataFrame([{
        'from': item['from'],
        'to': item['to'],
        'forecast': item['intensity']['forecast'],
        'actual': item['intensity']['actual'],
        'index': item['intensity']['index'],
    } for item in data])
    df.to_csv('uk_carbon_intensity.csv', index=False)
    print("Saved UK Carbon Intensity")

if __name__ == '__main__':
    fetch_uk_carbon_intensity()
