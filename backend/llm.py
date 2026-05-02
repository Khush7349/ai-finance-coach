import requests
import time
from backend.config import OLLAMA_URL, MODEL, TIMEOUT, RETRIES
def call(prompt, temperature=0.2):
    for attempt in range(RETRIES + 1):
        try:
            res = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature
                    }
                },
                timeout=TIMEOUT
            )
            res.raise_for_status()
            data = res.json()
            if "response" not in data:
                return "LLM Error: Invalid response format"
            return data["response"].strip()
        except requests.exceptions.Timeout:
            error = "LLM Error: Timeout"
        except requests.exceptions.ConnectionError:
            error = "LLM Error: Cannot connect to Ollama"
        except requests.exceptions.HTTPError:
            error = f"LLM Error: HTTP {res.status_code}"
        except Exception as e:
            error = f"LLM Error: {str(e)}"
        if attempt < RETRIES:
            time.sleep(1)
        else:
            return error