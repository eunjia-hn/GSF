import pandas as pd
import uuid

# === Utility ===
def generate_id():
    return str(uuid.uuid4())

# === Step 1: Define Source Metadata ===
sources = pd.DataFrame([
    {'source_id': 'NGCP', 'name': 'Philippines NGCP', 'region_code': 'PH'},
    {'source_id': 'POSOCO', 'name': 'India POSOCO', 'region_code': 'IN'},
    {'source_id': 'PUCSL', 'name': 'Sri Lanka PUCSL', 'region_code': 'LK'},
    {'source_id': 'EM', 'name': 'Electricity Maps API', 'region_code': 'IN'},
    {'source_id': 'WT', 'name': 'WattTime API', 'region_code': 'US'},
    {'source_id': 'UKCI', 'name': 'UK Carbon Intensity API', 'region_code': 'UK'}
])

regions = sources[['region_code']].drop_duplicates().reset_index(drop=True)
regions['region_id'] = regions['region_code'].apply(lambda x: generate_id())
regions = regions[['region_id', 'region_code']]

# Map region codes to IDs
region_id_map = dict(zip(regions['region_code'], regions['region_id']))
sources['region_id'] = sources['region_code'].map(region_id_map)

# === Step 2: Load and Normalize Each Dataset ===

generation_mix = []
carbon_data = []

# 1. NGCP (PH)
try:
    ngcp_df = pd.read_csv('/tmp/ngcp_generation_monthly.csv')
    for _, row in ngcp_df.iterrows():
        generation_mix.append({
            'id': generate_id(),
            'region_id': region_id_map['PH'],
            'source_id': 'NGCP',
            'datetime': pd.Timestamp.now().isoformat(),
            'fuel_type': row.get('PLANT TYPE', None),
            'generation_mwh': row.get('GROSS GENERATION (MWH)', None)
        })
except Exception as e:
    print("NGCP data not found:", e)

# 2. POSOCO (IN)
try:
    posoco_df = pd.read_csv('/tmp/posoco_generation_mix.csv')
    for _, row in posoco_df.iterrows():
        generation_mix.append({
            'id': generate_id(),
            'region_id': region_id_map['IN'],
            'source_id': 'POSOCO',
            'datetime': row.get('timestamp', pd.Timestamp.now().isoformat()),
            'fuel_type': row.get('fuel_type', 'UNKNOWN'),
            'generation_mwh': row.get('generation', None)
        })
except Exception as e:
    print("POSOCO data not found:", e)

# 3. PUCSL (LK)
try:
    pucsl_df = pd.read_csv('/tmp/pucsl_generation.csv')
    for _, row in pucsl_df.iterrows():
        generation_mix.append({
            'id': generate_id(),
            'region_id': region_id_map['LK'],
            'source_id': 'PUCSL',
            'datetime': row.get('Date', pd.Timestamp.now().isoformat()),
            'fuel_type': row.get('Fuel Type', 'UNKNOWN'),
            'generation_mwh': row.get('Energy Generated (MWh)', None)
        })
except Exception as e:
    print("PUCSL data not found:", e)

# 4. Electricity Maps (EM - IN)
try:
    em_df = pd.read_csv(f'/tmp/electricitymaps_IN.csv')
    for _, row in em_df.iterrows():
        carbon_data.append({
            'id': generate_id(),
            'region_id': region_id_map['IN'],
            'source_id': 'EM',
            'datetime': row['datetime'],
            'carbon_intensity': row['carbonIntensity_gCO2eq_per_kWh'],
            'fossil_percent': row['fossilFuelPercentage'],
            'actual': None,
            'forecast': None,
            'intensity_index': None
        })
except Exception as e:
    print("EM data not found:", e)

# 5. WattTime (US)
try:
    wt_df = pd.read_csv('/tmp/watttime_data.csv')
    for _, row in wt_df.iterrows():
        carbon_data.append({
            'id': generate_id(),
            'region_id': region_id_map['US'],
            'source_id': 'WT',
            'datetime': row['timestamp'],
            'carbon_intensity': row.get('value', None),
            'fossil_percent': None,
            'actual': None,
            'forecast': None,
            'intensity_index': None
        })
except Exception as e:
    print("WattTime data not found:", e)

# 6. UK Carbon Intensity
try:
    uk_df = pd.read_csv('/tmp/uk_carbon_intensity.csv')
    for _, row in uk_df.iterrows():
        carbon_data.append({
            'id': generate_id(),
            'region_id': region_id_map['UK'],
            'source_id': 'UKCI',
            'datetime': row['from'],
            'carbon_intensity': None,
            'fossil_percent': None,
            'forecast': row.get('forecast'),
            'actual': row.get('actual'),
            'intensity_index': row.get('index')
        })
except Exception as e:
    print("UK CI data not found:", e)

# === Step 3: Save to CSV ===
sources.to_csv('db_sources.csv', index=False)
regions.to_csv('db_regions.csv', index=False)
pd.DataFrame(generation_mix).to_csv('db_generation_mix.csv', index=False)
pd.DataFrame(carbon_data).to_csv('db_carbon_data.csv', index=False)

print("All relational-ready data exported as CSV.")
