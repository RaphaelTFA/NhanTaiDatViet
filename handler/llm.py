from openai import OpenAI
from config import LLM_API_KEY, MODEL

import time

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=LLM_API_KEY,
)

default_messages = [
            {"role": "developer", "content": "You are a helpful assistant."},
            {"role": "assistant", "content": "Hello! How can I assist you today?"},
            {"role": "user", "content": "Hello!"}
        ]

async def call_llm(messages=default_messages, model = MODEL):
    time.sleep(2)
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print("[ERROR]", e)
        return None
