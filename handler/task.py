from handler.llm import await call_llm
from config import MODEL, CANVAS_URL, CANVAS_API
from canvasapi import Canvas
from time import sleep
import os
import requests

def generate_test(file_dir=""):
    with open(file_dir, "r", encoding="utf-8") as f:
        text_content = f.read()
    sample_prompt = [
            {"role": "user", "content": text_content},
        ]
    response = await call_llm(messages=sample_prompt, model = MODEL)
    return response 

def generate_test_2(prompt):
    sample_prompt = [
            {"role": "user", "content": prompt},
        ]
    response = await call_llm(messages=sample_prompt, model = MODEL)
    return response 

API_URL = CANVAS_URL
API_KEY = CANVAS_API

canvas = Canvas(API_URL, API_KEY)

def import_qti(qtifile, course_id="2120114", name="Quiz", score=0, grade=10):
    course = canvas.get_course(course_id)
    print(f"Uploading {qtifile}...")

    payload = {"migration_type": "qti_converter", "pre_attachment[name]": os.path.basename(qtifile)}
    response = requests.post(
        f"{API_URL}/api/v1/courses/{course_id}/content_migrations/",
        params=payload,
        headers={"Authorization": "Bearer " + API_KEY}
    )
    blob = response.json()

    if "id" not in blob:
        print("Migration error:", blob)
        return

    migration_id = blob["id"]
    upload_url = blob["pre_attachment"]["upload_url"]
    upload_params = blob["pre_attachment"]["upload_params"]

    with open(qtifile, "rb") as f:
        requests.post(upload_url, params=upload_params, files={"file": f})

    quizimport = course.get_content_migration(migration_id)
    progress = quizimport.get_progress()
    while progress.workflow_state != "completed":
        print(f"\rProcessing: {progress.workflow_state} {progress.completion}%", end="")
        sleep(1)
        progress = quizimport.get_progress()

    print("\nImport completed!")

    newquiz = max(course.get_quizzes(), key=lambda q: q.id)

    newquiz.edit(quiz={
        "title": f"[Math] {name} <{score}> ({grade})",
        "shuffle_answers": True,
        "allowed_attempts": 3,
        "show_correct_answers": False,
        "published": True
    })
    quiz_url = f"{API_URL}/courses/{course_id}/quizzes/{newquiz.id}"
    return quiz_url
