CREATE TABLE regions (
    region_id UUID PRIMARY KEY,
    region_code VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE sources (
    source_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255),
    region_id UUID REFERENCES regions(region_id)
);

CREATE TABLE generation_mix (
    id UUID PRIMARY KEY,
    region_id UUID REFERENCES regions(region_id),
    source_id VARCHAR(10) REFERENCES sources(source_id),
    datetime TIMESTAMP,
    fuel_type VARCHAR(100),
    generation_mwh NUMERIC
);

CREATE TABLE carbon_data (
    id UUID PRIMARY KEY,
    region_id UUID REFERENCES regions(region_id),
    source_id VARCHAR(10) REFERENCES sources(source_id),
    datetime TIMESTAMP,
    carbon_intensity NUMERIC,
    fossil_percent NUMERIC,
    forecast NUMERIC,
    actual NUMERIC,
    intensity_index VARCHAR(50)
);
