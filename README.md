# 🧠 AI Code Explainer & Bug Finder

A simple web app that explains code and flags bugs using an LLM (via the [Groq API](https://groq.com/)). Paste in a code snippet, and it returns a plain-English explanation, a list of potential bugs, and a suggested fixed version.

## Features

- Explains what a block of code does, in plain English
- Detects bugs, edge cases, and bad practices
- Suggests a corrected version of the code
- Supports auto-detect or manual language selection (Python, JavaScript, Java, C, C++)

## Tech Stack

- **Backend:** FastAPI (Python), Groq LLM API (`llama-3.3-70b-versatile`)
- **Frontend:** Single-page HTML/CSS/JS (no framework, no build step)

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
   git clone <your-repo-url>
   cd ai-code-explainer
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

   Open `index.html` directly in your browser (or serve it with any static file server). It's already configured to call `http://127.0.0.1:8000/analyze`.

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

## Deployment

The backend and frontend are deployed separately:

- **Backend:** Deploy `main.py` to a service like [Render](https://render.com) or [Railway](https://railway.app). Set the start command to:
  ```
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```
  Add `GROQ_API_KEY` as an environment variable in the hosting dashboard — never commit your real key.

- **Frontend:** Once the backend has a public URL, update the `API_URL` constant near the top of the `<script>` tag in `index.html` to point at it, then host `index.html` on a static host such as Netlify, Vercel, or GitHub Pages.

## Notes

- `MAX_CODE_LENGTH` is capped at 6000 characters as a simple guardrail against oversized requests.
- CORS is currently open to all origins (`allow_origins=["*"]`) for ease of local development — consider restricting this to your actual frontend domain before going fully public.
- If the Groq API stops responding, check that your key is still active at [console.groq.com/keys](https://console.groq.com/keys) — keys can be revoked, rotated, or rate-limited.

## License

Add a license of your choice here (e.g. MIT).
