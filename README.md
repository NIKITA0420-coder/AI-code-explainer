# 🧠 AI Code Explainer & Bug Finder

A simple web app that explains code and flags bugs using an LLM (via the [Groq API](https://groq.com/)). Paste in a code snippet, and it returns a plain-English explanation, a list of potential bugs, and a suggested fixed version.

## 🌐 Live Demo

- **Frontend:** [ai-code-explainer-6178.netlify.app](https://ai-code-explainer-6178.netlify.app/)
- **Backend API:** [ai-code-explainer-wbed.onrender.com](https://ai-code-explainer-wbed.onrender.com/)

> Note: the backend is hosted on Render's free tier, so it spins down after inactivity. The first request after idle time may take 30-60 seconds to respond while it wakes up.

## Features

- Explains what a block of code does, in plain English
- Detects bugs, edge cases, and bad practices
- Suggests a corrected version of the code
- Supports auto-detect or manual language selection (Python, JavaScript, Java, C, C++)

## Tech Stack

- **Backend:** FastAPI (Python), Groq LLM API (`llama-3.3-70b-versatile`), deployed on [Render](https://render.com)
- **Frontend:** Single-page HTML/CSS/JS (no framework, no build step), deployed on [Netlify](https://netlify.com)

## Project Structure

```
ai-code-explainer/
├── main.py            # FastAPI backend — /analyze endpoint
├── index.html          # Frontend UI
├── requirements.txt    # Python dependencies
├── test_env.py         # Quick script to check .env is loading correctly
├── .env                # Your GROQ_API_KEY (not committed to git)
└── .gitignore
```

## Setup (Local Development)

1. **Clone the repo and enter the project folder**
   ```bash
   git clone https://github.com/NIKITA0420-coder/AI-code-explainer.git
   cd AI-code-explainer
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Add your Groq API key**
   Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_real_groq_api_key_here
   ```
   Get a key from [console.groq.com/keys](https://console.groq.com/keys).
4. **Run the backend**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be live at `http://127.0.0.1:8000`.
5. **Open the frontend**
   Open `index.html` directly in your browser (or serve it with any static file server). By default it's configured to call the live Render backend — if you want to test fully locally, change the `API_URL` constant near the top of the `<script>` tag in `index.html` to `http://127.0.0.1:8000`.

## API

### `POST /analyze`

**Request body:**
```json
{
  "code": "your code here",
  "language": "python"
}
```

**Response:**
```json
{
  "explanation": "...",
  "bugs": ["..."],
  "fixed_code": "..."
}
```

**Example (against the live backend):**
```bash
curl -X POST https://ai-code-explainer-wbed.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "print(1/0)", "language": "python"}'
```

## Deployment

The backend and frontend are deployed separately:

- **Backend:** Deployed on [Render](https://render.com) at [ai-code-explainer-wbed.onrender.com](https://ai-code-explainer-wbed.onrender.com/). Start command:
  ```
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```
  `GROQ_API_KEY` is set as an environment variable in the Render dashboard — never commit your real key.

- **Frontend:** Deployed on [Netlify](https://netlify.com) at [ai-code-explainer-6178.netlify.app](https://ai-code-explainer-6178.netlify.app/). The `API_URL` constant in `index.html` points to the live Render backend above.

To redeploy your own copy:
1. Fork/clone this repo and deploy `main.py` to Render or [Railway](https://railway.app) with the start command above, plus your own `GROQ_API_KEY`.
2. Update the `API_URL` constant in `index.html` to point to your new backend URL.
3. Deploy `index.html` to Netlify, Vercel, or GitHub Pages.

## Notes

- `MAX_CODE_LENGTH` is capped at 6000 characters as a simple guardrail against oversized requests.
- CORS is currently open to all origins (`allow_origins=["*"]`) for ease of local development — consider restricting this to `https://ai-code-explainer-6178.netlify.app` before going fully public.
- If the Groq API stops responding, check that your key is still active at [console.groq.com/keys](https://console.groq.com/keys) — keys can be revoked, rotated, or rate-limited.

## License

Add a license of your choice here (e.g. MIT).
