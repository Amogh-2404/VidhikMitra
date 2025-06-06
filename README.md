# Vidhik Mitra

An AI powered assistant for the Indian Judicial System.

## Features
- Fine tuned LLM on Indian law
- Flask backend with chat and upload APIs
- React frontend with ChatGPT style UI
- OCR for PDF/image uploads (supports PDFs via pdf2image)
- Basic user auth (email/password or Google) and chat history with JWT tokens
- Web search augmentation for up-to-date answers
- File upload with automatic redaction of personal data
- Rate limited API to prevent abuse
- Question answering on uploaded documents using transformers

## Setup
1. Clone the repo
2. Install Python deps:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
   pdf2image needs poppler installed. On Ubuntu: `sudo apt-get install poppler-utils`.
3. Install frontend deps (needs Node.js):
   ```bash
   cd ../frontend
   npm install
   ```
4. Create `.env` from `.env.example` and fill secrets.
5. Run backend and frontend in separate terminals.

## Training the Model
Use `model_training/training.ipynb` on Colab to fine tune a base model on `dataset/Indian_Law.jsonl`. Save the resulting `model` directory and set `MODEL_PATH` in `.env`.

## Deployment
The project can be hosted entirely with free tiers:

### Backend (Render)
1. Create a new Web Service on [Render](https://render.com/) and link this repo.
2. Set the build command to:
   ```bash
   pip install -r backend/requirements.txt
   ```
   and the start command to:
   ```bash
   python backend/app.py
   ```
3. Add the environment variables from `.env.example` in the Render dashboard.
4. Deploy. Render will give you a public API URL.

### Google Login
Clients can send a Google `id_token` to `/api/auth/google` to obtain a JWT for the API. Configure the OAuth client ID in the environment variables.

### Frontend (Vercel)
1. Push the repo to GitHub and import the `frontend` folder in [Vercel](https://vercel.com/).
2. Set the build command to `npm run build` and the output directory to `dist`.
3. Configure an environment variable `VITE_API_URL` pointing to your Render API URL if hosting separately.
4. Deploy and Vercel will provide a public URL for the web app.

### Document QA
Use `/api/upload/qa` to submit a file together with a `query` form field and
receive an answer extracted using a transformer QA model.

## Environment Variables
-See `.env.example` for all variables:
- `SECRET_KEY` – Flask secret
- `JWT_SECRET` – token secret
- `DATABASE_URL` – database (defaults to SQLite)
- `MODEL_PATH` – path to fine tuned model
- `GOOGLE_OAUTH_CLIENT_ID` and `GOOGLE_OAUTH_CLIENT_SECRET` – optional Google login
- `RATE_LIMIT` – requests per time window (default `100/minute`)
- `ANALYTICS_ENABLED` – set to `true` to log anonymous usage events
- Passwords are hashed server-side before storage

## Disclaimer
This project provides information for educational purposes and does not constitute legal advice. Always consult a qualified advocate for legal matters.

## Privacy & Safety
- Uploaded files are processed and stored temporarily in `uploads/`.
- Do not upload confidential documents.
- The app redacts Aadhaar, PAN, and phone numbers before storage.
- Abuse is blocked via simple content moderation and rate limiting.
- Usage analytics are disabled by default; enable by setting `ANALYTICS_ENABLED=true`.

## FAQ
- **How do I load a new model?** Place the trained `model` directory path in `MODEL_PATH` and restart the backend.
- **Where are chats stored?** Currently in memory; extend `DATABASE_URL` with a real database for persistence.
- **How do I update the model without downtime?** Replace the files in the directory specified by `MODEL_PATH` and restart the backend service.

## Scaling & Extensions
Run the backend behind a WSGI server like Gunicorn for production and use a managed database (PostgreSQL on Render/Railway). The modular Flask blueprint structure allows adding new legal domains or replacing the model easily.
Logs are written to `app.log` (and `analytics.log` when enabled) for monitoring purposes.

