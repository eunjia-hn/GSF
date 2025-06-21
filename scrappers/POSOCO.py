import requests
import pandas as pd

API = 'https://posoco.in/wp-admin/admin-ajax.php'
PARAMS = {
    'action': 'gettodayoutput',  # hypothetical endpoint – inspect network requests
    'region': 'ALL'
}

def scrape_posoco():
    res = requests.get(API, params=PARAMS)
    res.raise_for_status()
    payload = res.json()
    # Assume payload['data'] has timestamped rows
    df = pd.DataFrame(payload['data'])
    df.to_csv('posoco_generation_mix.csv', index=False)
    print("Saved POSOCO real-time generation mix.")

if __name__ == '__main__':
    scrape_posoco()
