# MLOps: Wine Quality Prediction with Deployment

End‑to‑end **MLOps** project that predicts wine quality from physicochemical features. Production‑minded structure with modular code, tracked experiments, and CI/CD.

**Live app (Azure):** *coming soon →* **\[ADD YOUR LINK HERE]**

---

## Why this project

* 🧱 **Modular pipeline** with clear stages (ingest → validate → transform → train → evaluate → serve).
* 🧪 **Experiment tracking** with MLflow (compatible with DagsHub remote).
* 🐳 **Dockerized** for reproducibility and cloud deploys.
* ⚙️ **Config‑driven** (YAML) so runs are parameterized and repeatable.

> Repo highlights include `config/`, `datasets/`, `src/MLOPS/`, `app.py`, `main.py`, `params.yaml`, `schema.yaml`, `Dockerfile`, and `requirements.txt`. See the repo for the full layout.

---

## Architecture


<img width="1536" height="1024" alt="ChatGPT Image Mar 9, 2026 at 05_18_29 PM" src="https://github.com/user-attachments/assets/24551af9-732c-430e-8011-2567f595d186" />

---

## Project structure

```
.
├── config/                # config.yaml, stage configs
├── datasets/              # raw/processed data
├── logs/                  # pipeline & app logs
├── research/              # notebooks / scratch
├── src/MLOPS/             # package with components & pipelines
├── templates/             # index.html
├── app.py                 # inference service (FastAPI/Streamlit/Flask)
├── main.py                # pipeline runner / orchestrator
├── params.yaml            # hyperparams & run settings
├── schema.yaml            # data schema for validation
├── Dockerfile             # container image
├── requirements.txt       # Python deps
└── README.md
```

---

## Datasets

* **Source**: UCI Wine Quality (red/white) physicochemical dataset.
* **Target**: `quality` (regression or ordinal classification depending on params).

Place raw CSVs under `datasets/` or update the path in `config.yaml` and `params.yaml`.

---

## Module‑by‑module

**1) Data Ingestion**

* Reads raw CSVs, handles train/test split, writes to `datasets/processed/`.

**2) Data Validation**

* Enforces `schema.yaml` (dtypes, ranges, required cols). Fails fast on drift/missing columns.

**3) Data Transformation**

* Feature engineering, imputation, scaling; persists transformers for inference parity.

**4) Model Trainer**

* Trains baseline + tuned model (e.g., ElasticNet/RandomForest/XGBoost as configured). Saves model artifacts.

**5) Model Evaluation**

* Computes metrics (RMSE/MAE/R²), logs params/metrics/artifacts to **MLflow**; supports DagsHub tracking URI.

**6) Inference Service (`app.py`)**

* Loads the latest model + transformer bundle; exposes `predict` endpoint or Streamlit UI.

**7) Orchestration (`main.py`)**

* Runs stages sequentially/individually; controlled by `params.yaml` and `config.yaml`.

---

## Getting started

### 1) Setup

```bash
# clone & create env
git clone https://github.com/Vatsal-Founder/MLOPS_project.git
cd MLOPS_project
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Configure

Edit **`config/config.yaml`**, **`params.yaml`**, and **`schema.yaml`** for paths, splits, hyperparams, and schema rules. For MLflow remote (e.g., DagsHub):

```bash
export MLFLOW_TRACKING_URI=https://dagshub.com/<user>/<repo>.mlflow
export MLFLOW_TRACKING_USERNAME=<user>
export MLFLOW_TRACKING_PASSWORD=<token>
```

### 3) Run the pipeline

```bash
# end‑to‑end
python main.py

# OR run stage‑wise (examples)
python main.py --stage ingest
python main.py --stage validate
python main.py --stage transform
python main.py --stage train
python main.py --stage evaluate
```

Artifacts (models/transformers) are saved to the configured `artifacts/` path; runs and metrics appear in MLflow.

### 4) Serve predictions

```bash
# option A: FastAPI/Flask style
python app.py
# option B: Streamlit UI (if implemented)
streamlit run app.py
```

Visit `http://localhost:8000` or `http://localhost:8501` depending on your entrypoint.

---

## Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# pipeline
# CMD ["python", "main.py"]
# inference (FastAPI)
# CMD ["python", "app.py"]
```

Build & run:

```bash
docker build -t wine-mlops .
# run pipeline
# docker run --rm wine-mlops python main.py
# run API (map a port)
docker run -p 8000:8000 wine-mlops python app.py
```

---

## CI/CD (GitHub Actions)

Typical workflow:

1. Lint & unit checks
2. Build Docker image
3. Run pipeline on push to `main` (optional)
4. Push image to registry
5. Deploy to Azure (see below)

> This repo includes a workflows folder. Adapt it with your Azure credentials and environment secrets.

---

## Azure deployment (placeholder)

* **Option A — Azure App Service (inference):**

  * Build image → push to **Azure Container Registry (ACR)**.
  * Create Web App for Containers → set env vars (MLflow URI, data paths, keys).
  * Configure startup command: `python app.py` (or `gunicorn` if applicable).
  * Public URL: **\[ADD YOUR AZURE APP LINK HERE]**

* **Option B — Azure ML (batch/online endpoints):**

  * Register model artifact; create env from `requirements.txt`.
  * Define inference entry (`app.py` or `score.py`), deploy endpoint.

*(Keep this section updated with your exact steps & URLs.)*

---

## Configuration files

* **`config/config.yaml`** – paths and stage toggles
* **`params.yaml`** – hyperparameters (splits, model params)
* **`schema.yaml`** – column names, dtypes, ranges

---

## License

GPL‑3.0 © Vatsal Founder
