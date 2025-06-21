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
| US (optional)| WattTime API          | REST API   | `watttime_data.csv` |
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
