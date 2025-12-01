# Weather_Prediction_Pipeline

### Project Design, Architecture, and Outcomes

Design:  
  
(1) Build a real-time pipeline that ingests hourly weather JSON from Open-Meteo for chosen locations, stores raw JSON (bronze), cleans and normalizes (silver), produces aggregated features and labels (gold),  
(2) trains and serves ML models to: Forecast temperature for next 24 hours (regression),  
(3) and/or Classify whether it will rain in the next hour (binary classification).  

Objectives: 
  
- Classification (primary portfolio highlight): Predict rain_next_hour (binary) using past N hours features and current conditions. This is intuitive, explainable, and suitable to show both feature engineering and classification metrics.  
- Forecasting (secondary): Multi-output regression forecasting of temperature over next 1/3/6/24 hours. Demonstrate time-series features, cross-validation, and probabilistic metrics.  

Data Source:  Open-Meteo hourly JSON API  

### Repository Structure:  
  
weather-pipeline/  
├── README.md  
├── pyproject.toml OR requirements.txt  
├── docker/  
│   ├── Dockerfile  
│   └── docker-compose.yml  
├── .github/  
│   └── workflows/  
│       └── ci.yml  
├── src/  
│   ├── etl/  
│   │   ├── fetch_open_meteo.py          # fetcher that writes to bronze  
│   │   ├── bronze_to_silver.py          # batch/stream job to build silver  
│   │   ├── silver_to_gold.py            # feature engineering, labels  
│   │   └── schemas.py                   # PySpark schemas  
│   ├── ml/  
│   │   ├── train_classifier.py          # train classification (PySpark ML)  
│   │   ├── train_regressor.py           # train forecasting model  
│   │   ├── predict.py                   # helper to load model and predict  
│   │   └── mlflow_utils.py  
│   ├── api/  
│   │   └── app.py                       # FastAPI serving endpoint  
│   ├── ui/  
│   │   └── streamlit_app.py  
│   ├── orchestrator/  
│   │   └── prefect_flow.py  
│   └── utils/  
│       ├── file_utils.py  
│       ├── dq_checks.py  
│       └── logging_config.py  
├── notebooks/  
│   ├── exploration.ipynb  
│   └── modeling_demo.ipynb  
├── data/  
│   ├── bronze/  
│   ├── silver/  
│   └── gold/  
├── tests/  
│   ├── test_etl.py  
│   └── test_ml.py  
└── docs/  
    └── architecture.png  


### Extract/Transform/Load Pipeline in PySpark

### Machine Learning Pipeline

### Orchestration

### Deployment
- Dockerfile  

### Dashboard  
- Streamlit  

### Testing/Training  

### BEST PRACTICES CHECKLIST  

-- Reproducibility: pin package versions, include requirements.txt and Dockerfile, and seed your randomness in model training.  
-- Data lineage: store source_path and fetch_ts in silver so you can trace back any observation.  
-- Schema evolution: include schema_version metadata and use Parquet/Delta Lake in production to support evolution safely.  
-- Observability: log run times, row counts, and DQ violations to MLflow or another observability tool. Add Prometheus metrics for the API and Prefect.  
-- Tests: unit tests for each transform function + integration test for full flow using small sample JSON files.  
-- Security: if deploying publicly, secure endpoints with authentication, and don't expose your MLflow server without auth.  
