from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class LLMWrapper:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def complete(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    def show_models(self):
        models = self.client.models.list()

        for model in models.data:
            print(model.id)