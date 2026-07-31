import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)

AI_API_KEY = os.environ.get("AI_API_KEY", "").strip()
AI_MODEL = os.environ.get("AI_MODEL", "").strip()
AI_PROVIDER = os.environ.get("AI_PROVIDER", "").strip()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()

if not AI_API_KEY and OPENAI_API_KEY:
    AI_API_KEY = OPENAI_API_KEY

# Default to OpenAI when an API key is present but provider is unspecified.
if AI_API_KEY and not AI_PROVIDER:
    AI_PROVIDER = "openai"

if not AI_MODEL:
    AI_MODEL = os.environ.get("AI_MODEL", "gpt-3.5-turbo").strip()

AI_ENABLED = bool(AI_API_KEY and AI_PROVIDER)
