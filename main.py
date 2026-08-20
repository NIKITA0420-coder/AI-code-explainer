from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env
load_dotenv()

app = FastAPI(title="AI Code Explainer & Bug Finder")

# Allow the frontend (running from a file or different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MAX_CODE_LENGTH = 6000  # simple guardrail so we don't send huge inputs


class CodeInput(BaseModel):
    code: str
    language: str = "auto"


@app.get("/")
def root():
    return {"status": "AI Code Explainer backend is running"}


@app.post("/analyze")
def analyze_code(input: CodeInput):
    code = input.code.strip()

    if not code:
        raise HTTPException(status_code=400, detail="Code cannot be empty.")

    if len(code) > MAX_CODE_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Code is too long. Please limit to {MAX_CODE_LENGTH} characters.",
        )

    prompt = f"""You are an expert software engineer. Analyze the following {input.language} code.

Respond ONLY with valid JSON in exactly this format, no extra text before or after:
{{
  "explanation": "A clear, line-by-line or block-by-block explanation of what the code does, in plain English.",
  "bugs": ["List each bug, edge case, or bad practice found. If none, return an empty list."],
  "fixed_code": "A corrected version of the code if bugs were found. If no bugs, return the original code unchanged."
}}

Code to analyze:
{code}
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        raw_text = response.choices[0].message.content.strip()

        # Strip markdown code fences if the model wraps the JSON in ```json ... ```
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            if raw_text.startswith("json"):
                raw_text = raw_text[4:].strip()

        result = json.loads(raw_text)
        return result

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail="The AI response could not be parsed. Please try again.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling Groq API: {str(e)}")
