from canvasapi import Canvas
from time import sleep
from config import CANVAS_URL, CANVAS_API
import os
import requests

API_URL = CANVAS_URL
API_KEY = CANVAS_API

canvas = Canvas(API_URL, API_KEY)

def import_qti(qtifile, course_id="2120114", score=0, grade=10):
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
    print(f"Quiz '{newquiz.title}' configured & published!")
