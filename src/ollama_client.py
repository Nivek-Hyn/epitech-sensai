import requests
import json
import yaml


def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


class OllamaClient:
    def __init__(self, config=None):
        config = config or load_config()
        self.model = config["model"]
        self.url = config["ollama_url"]
        self.temperature = config.get("temperature", 0.7)

    def chat(self, messages):
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": self.temperature
            }
        }

        response = requests.post(
            f"{self.url}/api/chat",
            json=payload,
            stream=True
        )

        full_response = ""

        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                token = chunk["message"]["content"]
                print(token, end="", flush=True)
                full_response += token

                if chunk.get("done", False):
                    break

        print()
        return full_response
