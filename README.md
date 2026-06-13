# 📦 Delivery Time Estimator

## Description
A lightweight, interactive web application designed to predict food delivery times. This project serves as the frontend interface for a machine learning model hosted on Google Cloud Run. It features a modern card-based UI, random data generation for quick testing, and secure API communication.

<img width="1672" height="1064" alt="Screenshot 2026-06-13 at 12 13 36 AM" src="https://github.com/user-attachments/assets/d02d2db2-e3f0-4507-914d-7a18d153ef5d" />


## Features
- **Modern UI:** Built with HTML5, CSS3, and jQuery.
- **Randomizer:** One-click generation of realistic delivery scenarios.
- **Cloud-Connected:** Communicates via REST API with a secure backend.
- **Responsive:** Optimized for desktop and mobile browsers.

## API Configuration
This frontend connects to a secure FastAPI backend.
- **Endpoint:** `https://delivery-api-232429281144.us-central1.run.app/predict`
- **Security:** Requires `X-API-Key` authentication.

## How to Run
1. Clone this repository.
2. Open `index.html` directly in any modern web browser.
3. Ensure your backend API is configured to allow CORS requests from your GitHub Pages URL.

---
*Built as part of the Seneca Polytechnic AI (AIGC) Program.*
