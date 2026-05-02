import os
from dotenv import load_dotenv
load_dotenv()
def get_env(key: str, default=None, required=False):
    value = os.getenv(key, default)
    if required and value is None:
        raise ValueError(f"Missing required env variable: {key}")
    return value
OLLAMA_URL = get_env(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)
MODEL = get_env(
    "OLLAMA_MODEL",
    "mistral"
)
TEMPERATURE = float(get_env("OLLAMA_TEMPERATURE", 0.2))
TIMEOUT = int(get_env("OLLAMA_TIMEOUT", 30))
RETRIES = int(get_env("OLLAMA_RETRIES", 2))
ENV = get_env("ENV", "dev")
DEBUG = ENV == "dev"