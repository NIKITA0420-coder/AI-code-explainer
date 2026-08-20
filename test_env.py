from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("GROQ_API_KEY")
print("Key loaded:", key[:8] + "..." if key else "NOT FOUND")
