import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# --- Update with your DB credentials ---
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "your_database"
DB_USER = "your_user"
DB_PASS = "your_password"

# --- Helper function to bulk insert using execute_values ---
def bulk_insert(conn, table_name, df, columns):
    tuples = [tuple(x) for x in df[columns].to_numpy()]
    cols = ','.join(columns)
    query = f"INSERT INTO {table_name} ({cols}) VALUES %s ON CONFLICT DO NOTHING;"
    with conn.cursor() as cur:
        execute_values(cur, query, tuples)
    conn.commit()

def main():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASS
    )

    try:
        # Load CSVs
        regions = pd.read_csv('db_regions.csv')
        sources = pd.read_csv('db_sources.csv')
        generation_mix = pd.read_csv('db_generation_mix.csv')
        carbon_data = pd.read_csv('db_carbon_data.csv')

        # Insert regions
        print("Uploading regions...")
        bulk_insert(conn, 'regions', regions, ['region_id', 'region_code'])

        # Insert sources
        print("Uploading sources...")
        bulk_insert(conn, 'sources', sources, ['source_id', 'name', 'region_id'])

        # Insert generation_mix
        print("Uploading generation_mix...")
        generation_mix['datetime'] = pd.to_datetime(generation_mix['datetime'], errors='coerce')
        bulk_insert(conn, 'generation_mix', generation_mix,
                    ['id', 'region_id', 'source_id', 'datetime', 'fuel_type', 'generation_mwh'])

        # Insert carbon_data
        print("Uploading carbon_data...")
        carbon_data['datetime'] = pd.to_datetime(carbon_data['datetime'], errors='coerce')
        bulk_insert(conn, 'carbon_data', carbon_data,
                    ['id', 'region_id', 'source_id', 'datetime', 'carbon_intensity',
                     'fossil_percent', 'forecast', 'actual', 'intensity_index'])

        print("All data uploaded successfully!")

    except Exception as e:
        print("Error uploading data:", e)

    finally:
        conn.close()

if __name__ == "__main__":
    main()
