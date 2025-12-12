# Credit Risk Model Serving Demo

A simple demo project to teach the basics of **model serving and deployment** using:

- **scikit-learn** - Training a credit risk model
- **MLflow** - Tracking experiments
- **FastAPI** - Serving the model as an API
- **Docker** - Containerizing the application

## Project Structure

```
credit-risk-serving-demo/
├── models/                  # Saved model files
├── mlruns/                  # MLflow tracking data (auto-created)
├── src/
│   ├── train.py            # Train the model + log to MLflow
│   ├── inference.py        # Load model + predict helper
│   └── api/
│       ├── schemas.py      # Pydantic request/response models
│       └── main.py         # FastAPI application
├── tests/
│   └── test_api.py         # API tests
├── requirements.txt
├── Dockerfile              # Container setup (added later)
└── README.md
```

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the model

```bash
python -m src.train
```

This will:
- Load the German Credit dataset
- Train a LogisticRegression model
- Save the model to `models/credit_model.pkl`
- Log the experiment to MLflow

### 3. View MLflow dashboard (optional)

```bash
mlflow ui
```

Open http://localhost:5000 to see your experiment.

### 4. Start the API

```bash
uvicorn src.api.main:app --reload
```

Open http://localhost:8000/docs for the Swagger UI.

### 5. Test the API

```bash
pytest tests/test_api.py -v
```

## API Endpoints

| Method | Endpoint  | Description                          |
|--------|-----------|--------------------------------------|
| GET    | /health   | Check if the service is running      |
| POST   | /predict  | Get credit risk prediction           |

### Example prediction request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "checking_status": "<0",
    "duration": 12,
    "credit_history": "existing paid",
    "purpose": "radio/tv",
    "credit_amount": 1000,
    "savings_status": "<100",
    "employment": "1<=X<4",
    "installment_commitment": 4,
    "personal_status": "male single",
    "other_parties": "none",
    "residence_since": 2,
    "property_magnitude": "car",
    "age": 30,
    "other_payment_plans": "none",
    "housing": "own",
    "existing_credits": 1,
    "job": "skilled",
    "num_dependents": 1,
    "own_telephone": "yes",
    "foreign_worker": "yes"
  }'
```

### Example response

```json
{
  "default_probability": 0.32,
  "risk_label": "low"
}
```

## Dataset

This demo uses the **German Credit dataset** from OpenML (data_id=31).

- 1000 samples, 20 features
- Target: credit risk (good/bad)
- Features include: checking account status, loan duration, credit amount, employment, age, etc.

## Learning Objectives

By the end of this demo, you should understand:

1. **Model Training** - How to train and save an sklearn pipeline
2. **MLflow Tracking** - How to log parameters, metrics, and models
3. **FastAPI Serving** - How to create a REST API for predictions
4. **Pydantic Validation** - How to validate request/response data
5. **Docker** - How to containerize the application (coming next)
