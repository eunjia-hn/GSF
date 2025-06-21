import requests
import pandas as pd
from datetime import datetime

TOKEN = "YOUR_ELECTRICITY_MAPS_API_TOKEN"  # <- get it from Electricity Maps account
ZONE = "IN"  # India (you can use SG, KR, JP, etc.)

def fetch_electricity_maps(zone=ZONE):
    url = f"https://api.electricitymaps.com/v3/carbon-intensity/latest?zone={zone}"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    df = pd.DataFrame([{
        'zone': zone,
        'datetime': data['datetime'],
        'carbonIntensity_gCO2eq_per_kWh': data['carbonIntensity'],
        'fossilFuelPercentage': data['fossilFuelPercentage'],
    }])
    df.to_csv(f'electricitymaps_{zone}.csv', index=False)
    print(f"Saved electricity maps data for {zone}")

if __name__ == '__main__':
    fetch_electricity_maps()
