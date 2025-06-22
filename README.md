# GSF
### A small step to build a green software.

API-based scrapers:

🌍 Electricity Maps (e.g., India, Japan, Korea)

🌍 WattTime (optional, mostly US-based)

🇬🇧 UK Carbon Intensity

Scraper-based (HTML / Excel):

🇵🇭 Philippines NGCP

🇮🇳 India POSOCO

🇱🇰 Sri Lanka PUCSL


# 🌱 Green Software Grid Data Pipeline

This project collects, transforms, and prepares real-time electricity grid and carbon intensity data from Asian and global sources. It supports the mission of the [Green Software Foundation](https://greensoftware.foundation) by making energy-aware software development more accessible and data-driven.

---

## 🌍 Overview

Every app we build runs on electricity — and not all electricity is created equal. This project enables developers, data scientists, and researchers to:

- Measure the carbon intensity of electricity powering software
- Analyze generation mixes by country or grid
- Support the development of carbon-aware applications

---

## 📦 What This Project Includes

### ✅ Web/API Scrapers
Collect real-time and historical grid data from:

| Region       | Source                | Method     | Output |
|--------------|-----------------------|------------|--------|
| Philippines  | NGCP                  | HTML Table | `ngcp_hourly_demand.csv`, `ngcp_generation_monthly.csv` |
| India        | POSOCO                | API        | `posoco_generation_mix.csv` |
| Sri Lanka    | PUCSL                 | Excel File | `pucsl_generation.csv` |
| India/Asia   | Electricity Maps API  | REST API   | `electricitymaps_IN.csv` |
| US           | WattTime API          | REST API   | `watttime_data.csv` |
| UK           | UK Carbon Intensity   | Open API   | `uk_carbon_intensity.csv` |

---

### ⚙️ Airflow DAG

An Airflow DAG automates daily data collection across all sources.

- File: `asia_and_api_power_scrapers.py`
- Schedule: `@daily`
- Output: All files saved to `/tmp/` or designated storage

---

### 🧱 Relational Database Model (ERD)

The `transform_to_db.py` script normalizes and maps all collected datasets into a relational database structure:

| Table              | Description                          |
|--------------------|--------------------------------------|
| `regions`          | Unique countries or grid zones       |
| `sources`          | Metadata on where data came from     |
| `generation_mix`   | Generation by fuel type              |
| `carbon_data`      | Carbon intensity data (actual/forecast) |

Output files:

- `db_regions.csv`
- `db_sources.csv`
- `db_generation_mix.csv`
- `db_carbon_data.csv`


Attributes

🗃️ regions Table
Attribute	Description
region_id	Unique UUID for each region
region_code	ISO country or grid code (e.g. IN, PH, UK)

🗃️ sources Table
Attribute	Description
source_id	Short ID for each data source (e.g. NGCP)
name	Full name of the source
region_id	Foreign key to the regions table

⚡ generation_mix Table
Attribute	Description
id	Unique UUID for each record
region_id	Foreign key to the region where data is from
source_id	Foreign key to the source providing the data
datetime	Timestamp of the data (actual or recorded)
fuel_type	Name of the fuel (e.g. Coal, Solar, Hydro)
generation_mwh	Amount of electricity generated in MWh

🌿 carbon_data Table
Attribute	Description
id	Unique UUID for each record
region_id	Foreign key to region
source_id	Foreign key to data source
datetime	Timestamp of measurement
carbon_intensity	Grams of CO₂ emitted per kWh (gCO2eq/kWh)
fossil_percent	% of electricity from fossil fuels (from EM API)
forecast	Forecasted carbon intensity (UK Carbon Intensity API)
actual	Actual carbon intensity (UK Carbon Intensity API)
intensity_index	Qualitative intensity (e.g., low, moderate, high)
