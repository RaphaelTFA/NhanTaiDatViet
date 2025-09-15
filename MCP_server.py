from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from knowledge_graph.math.graph import math_test, create_kg_math, driver_math, DATABASE as database_math, TOPIC_IDX
from knowledge_graph.math.transfer import transfer as math_transfer
from knowledge_graph.math.upload_canvas import import_qti as math_import_qti
from config import TEST_MODE
import pandas as pd
import os
import subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup") 
def startup_event():
    with driver_math.session(database=database_math) as session:
        create_kg_math(session)
    

@app.post("/math")
async def generate_math(
    course: int = Form(2120114),
    name: str = Form("Test_quiz"),
    grade: int = Form(10),
    file: UploadFile = File(...)
):
    if not file.filename.endswith(".csv"):
        return {"error": "File must be a CSV"}
    df = pd.read_csv(file.file, encoding="utf-8", on_bad_lines="skip")
    required_cols = {"topic", "grade", "difficulty", "question", "n"}
    if not required_cols.issubset(df.columns):
        return {"error": f"CSV must contain columns: {required_cols}"}
    txt_filename = "knowledge_graph/math/llm_return/full_response.txt"
    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write("")
    sum, cnt = 0, 0
    with open(txt_filename, "a", encoding="utf-8") as f:
        for row in df.itertuples(index=False):  
            try:
                result, score = math_test(
                    topic=row.topic,
                    grade=int(row.grade),
                    difficulty=row.difficulty,
                    question=row.question,
                    n=int(row.n)
                )
                sum += score * (row.n)
                cnt += int(row.n)
            except KeyError as e:
                return {"error": f"Invalid topic or grade: {e}"}
            except Exception as e:
                return {"error": f"Unexpected error: {str(e)}"}
            f.write(result + "\n\n")
    if not TEST_MODE:
        qtifile = math_transfer()
        math_import_qti(qtifile = qtifile, course_id = str(course), name = name, score = sum / cnt, grade = str(grade))
    return FileResponse(txt_filename, media_type='text/plain', filename="response.txt")

# cd code\NhanTaiDatViet
# uvicorn MCP_server:app --reload --host 127.0.0.1 --port 8000
# server: 127.0.0.1:8000/docs