from openai import OpenAI
from config import LLM_API_KEY, MODEL_PROMPTING, MODEL_REPHRASE, MODEL_CALCULATE

import time

client = OpenAI(
    base_url="https://openrouter.ai/api/v1/", # Mention! Openrouter is the best option for now
    api_key=LLM_API_KEY,
)

default_messages = [
            {"role": "developer", "content": "You are a helpful assistant."},
            {"role": "assistant", "content": "Hello! How can I assist you today?"},
            {"role": "user", "content": "Hello!"}
        ]

def call_llm(messages=default_messages, model=MODEL_PROMPTING):
    time.sleep(5)
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False,
        )
        if not completion or not completion.choices:
            print("[ERROR] Empty response:", completion)
            return None
        with open("handler/llm_history.txt", "a", encoding="utf-8") as f:
            #real time logging
            f.write(f"\n\n----------------------------------\n{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n")
            f.write(f"[REQUEST - {model}]\n")
            f.write(f"[RESPONSE]: {completion.choices[0].message.content}\n")
        return completion.choices[0].message.content
    except Exception as e:
        print("[ERROR] Bad return:", e)
        return None
