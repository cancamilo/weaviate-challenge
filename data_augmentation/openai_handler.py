from openai import OpenAI
import os
import logging
import json
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

MAX_LENGTH = 16384
SYSTEM_PROMPT = "You are an asistant whose job is crypto traders make informed decisions based on market sentiment"

class OpenAIHandler:
    def __init__(self, gpt_model: str = "gpt-3.5-turbo"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.gpt_model = gpt_model

    def request(self, prompt: str) -> list:
            try:
                client = OpenAI(api_key=self.api_key)
                logging.info("Sending batch to LLM")
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt[:MAX_LENGTH]},
                    ],
                    model=self.gpt_model,
                )
                response = chat_completion.choices[0].message.content
                return json.loads(self.clean_response(response))
            except Exception as e:
                logging.error(f"Skipping batch! An error occurred while communicating with API: {e}")
                return []

    @staticmethod
    def clean_response(response: str) -> str:
        start_index = response.find("[")
        end_index = response.rfind("]")
        return response[start_index : end_index + 1]