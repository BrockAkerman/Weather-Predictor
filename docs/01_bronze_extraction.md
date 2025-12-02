Phase 1 — Bronze Layer (Extract)

The goal of the Bronze layer in this pipeline is to capture immutable, raw JSON data from the Open-Meteo Forecast API. This forms the foundation for all downstream processing and ensures reproducibility of every step in the pipeline.

API Source

I use the Open-Meteo JSON REST API because it provides:

High-frequency, continuously updating weather forecasts

Well-structured JSON responses

A predictable URL pattern suitable for scheduled ingestion

The API endpoint includes hourly variables (temperature, humidity, precipitation, cloud cover, wind metrics) and daily variables (UV index, solar radiation). The latitude, longitude, and timezone parameters configure the request to target my local area.

Bronze Zone Design

Inside data/bronze/, I maintain a directory that stores only raw, unmodified API responses. Each ingestion event generates a new file named using the pattern:

raw_YYYYMMDD_HHMMSS.json

These timestamped snapshots allow me to reconstruct the state of the source system at any point in time.

Initial Ingestion Notebook

To bootstrap the pipeline, I created a notebook:

notebooks/01_fetch_initial_data.ipynb

This notebook performs the first API pull and saves the response as a raw JSON file in the Bronze zone. The notebook also includes safeguards to prevent accidental overwrites, ensuring the integrity of the raw data.

In future steps, a scheduled script or orchestrator will replace this manual notebook process, but the notebook itself documents the initial workflow and demonstrates the extraction logic.