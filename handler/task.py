from handler.llm import call_llm
from config import MODEL

def generate_test(file_dir=""):
    with open(file_dir, "r", encoding="utf-8") as f:
        text_content = f.read()
    sample_prompt = [
            {"role": "user", "content": text_content},
        ]
    response = call_llm(messages=sample_prompt, model = MODEL)
    return response 

def generate_test_2(prompt):
    sample_prompt = [
            {"role": "user", "content": prompt},
        ]
    response = call_llm(messages=sample_prompt, model = MODEL)
    return response 
