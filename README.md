
# 📦 Delivery Time Estimator

A lightweight, interactive web application that predicts food delivery times using a machine learning model deployed as a REST API. This repository contains the frontend interface, which connects to a FastAPI backend hosted on Google Cloud Run. It features a modern card-based UI, one-click random data generation for quick testing, and secure API communication via an API key.

<img width="1672" height="1064" alt="Delivery Time Estimator UI" src="https://github.com/user-attachments/assets/d02d2db2-e3f0-4507-914d-7a18d153ef5d" />

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [API Configuration](#api-configuration)
- [Project Structure](#project-structure)
- [How to Run the Project (End-to-End)](#-how-to-run-the-project-end-to-end)
  - [Step 1: Train the Machine Learning Model](#step-1-train-the-machine-learning-model)
  - [Step 2: Run the Backend API Locally](#step-2-run-the-backend-api-fastapi-locally)
  - [Step 3: Run the Frontend Web Interface](#step-3-run-the-frontend-web-interface)
  - [Step 4: Docker & Cloud Deployment](#step-4-docker--cloud-deployment-production)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [License](#license)

## Features

- **Modern UI** — Built with HTML5, CSS3, and jQuery for a clean, card-based layout.
- **Randomizer** — One-click generation of realistic delivery scenarios for quick testing.
- **Cloud-Connected** — Communicates with a secure backend via REST API over HTTPS.
- **Responsive** — Optimized for both desktop and mobile browsers.
- **Pre-Trained Model Serving** — The backend loads a pre-trained Random Forest model at startup; no training occurs at request time.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript (jQuery) |
| Backend | FastAPI, Uvicorn, Pydantic |
| Machine Learning | Scikit-Learn, Pandas, NumPy, Joblib |
| Containerization | Docker |
| Cloud Platform | Google Cloud Run, Google Cloud Build, Artifact Registry |
| Hosting | GitHub Pages (frontend), Google Cloud Run (backend) |

## API Configuration

This frontend connects to a secure FastAPI backend.

- **Endpoint:** `https://delivery-api-232429281144.us-central1.run.app/predict`
- **Method:** `POST`
- **Security:** Requires an `X-API-Key` header for authentication.
- **Interactive Docs:** Available at `/docs` (Swagger UI) on the deployed API URL.

**Sample request body:**

```json
{
  "Delivery_person_Age": 32.0,
  "Delivery_person_Ratings": 4.9,
  "Vehicle_condition": 2,
  "multiple_deliveries": 0.0,
  "Distance_km": 3.2,
  "Weather": "Sunny",
  "Road_traffic_density": "Low",
  "Type_of_order": "Snack",
  "Type_of_vehicle": "scooter",
  "Festival": "No",
  "City": "Urban"
}
```

**Sample response:**

```json
{
  "estimated_time_minutes": 18.11
}
```

## Project Structure

```
.
├── index.html              # Frontend UI
├── style.css                # Styling for the frontend
├── script.js                 # Frontend logic (API calls, randomizer)
├── main.py                  # FastAPI application (backend)
├── delivery_model.joblib     # Trained model + preprocessing pipeline
├── requirements.txt          # Python dependencies (version-pinned)
├── Dockerfile                # Container build configuration
└── README.md                 # This file
```

> Note: Adjust file names above to match your actual repository layout if they differ.

## 🚀 How to Run the Project (End-to-End)

This project consists of three parts: a machine learning model, a FastAPI backend, and a static HTML/JS frontend. Follow these steps to run the complete pipeline from scratch.

### Step 1: Train the Machine Learning Model

Before running the API, you must generate the trained model artifact.

1. Open the provided Jupyter Notebook or Python training script.
2. Run the data preprocessing and model training cells. This handles missing values, scales numerical features, and encodes categorical variables.
3. Once the Random Forest model is trained, the script serializes it and saves it as `delivery_model.joblib`.
4. Move `delivery_model.joblib` into the root directory of your backend API folder (the same folder as `main.py`).

### Step 2: Run the Backend API (FastAPI) Locally

The backend serves the trained model via a REST API.

1. Ensure you have Python 3.11+ installed.
2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
5. Verify it's running by navigating to `http://localhost:8000/docs` in your browser to view the interactive Swagger documentation.

### Step 3: Run the Frontend Web Interface

1. Clone this repository to your local machine.
2. Open `index.html` in any modern web browser (Chrome, Safari, Edge).
3. **Important — Local Testing:** By default, `index.html` is configured to point to the live Google Cloud Run production URL. To test against your local server instead, temporarily update the `apiUrl` value in `index.html` to `http://localhost:8000/predict`.

### Step 4: Docker & Cloud Deployment (Production)

To deploy the backend to Google Cloud Run, ensure Docker is running and execute the following commands in your terminal.

**1. Build and test locally (optional but recommended):**
```bash
docker build -t delivery-api .
docker run -p 8080:8080 delivery-api
```

**2. Deploy to Google Cloud Run:**
```bash
gcloud run deploy delivery-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi
```

Once deployed, Google Cloud will provide a live URL (e.g., `https://delivery-api-xxxxxxx.run.app`). After deployment:

- Update the `allow_origins` variable in `main.py` to accept traffic from your GitHub Pages URL.
- Update `index.html` to point to this new production endpoint.

## Troubleshooting

Common issues encountered during deployment and their fixes:

| Issue | Cause | Fix |
|---|---|---|
| Container fails to start on Cloud Run | App hardcoded to port 8000, but Cloud Run assigns a dynamic `$PORT` | Update Dockerfile `CMD` to `["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]` |
| `InconsistentVersionWarning` / crash on startup | scikit-learn version mismatch between training and deployment environments | Pin exact versions in `requirements.txt` (e.g., `scikit-learn==1.8.0`) |
| Container crashes due to memory error | Default 512MB Cloud Run memory insufficient for loaded model | Deploy with `--memory 1Gi` |
| Frontend requests blocked by browser (CORS error) | GitHub Pages origin not allowed by backend | Add `CORSMiddleware` in `main.py` and include the GitHub Pages domain and `X-API-Key` header in `allow_origins` / `allow_headers` |
| `403 Forbidden` on `/predict` | Missing or incorrect `X-API-Key` header | Ensure the request includes `X-API-Key: <your-key>` |

## Future Improvements

- Replace the static API key with per-client OAuth2 tokens.
- Integrate a live mapping API (e.g., Google Maps Distance Matrix) for real-time distance and traffic data.
- Add a CI/CD pipeline (GitHub Actions) for automated testing and redeployment on push.
- Experiment with gradient-boosted models (XGBoost/LightGBM) and hyperparameter tuning to improve prediction accuracy.
- Add a `/health` endpoint for uptime monitoring.

## License

This project was built as part of the **Seneca Polytechnic AI (AIGC) Program** for academic purposes.

---

**Author:** Bikash Subedi
