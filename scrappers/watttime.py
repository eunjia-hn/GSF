import requests
import pandas as pd

# Replace with your WattTime token
TOKEN = "YOUR_WATTTIME_API_TOKEN"
GRID = "IN-CENTRAL"  # Regional grid identifier if available (most are US-based)

def fetch_watttime():
    url = f"https://api2.watttime.org/v2/data"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    params = {"ba": GRID}
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    data = r.json()

    df = pd.DataFrame(data['results'])
    df.to_csv("watttime_data.csv", index=False)
    print("Saved WattTime data")

if __name__ == '__main__':
    fetch_watttime()
