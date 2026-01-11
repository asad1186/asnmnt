import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class OpenAIClient:
    def __init__(self, model="gpt-4o-mini"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def chat(self, messages, temperature=0.2, max_tokens=500):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
