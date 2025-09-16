from __future__ import annotations

import os
import random
import tempfile
import logging
import subprocess
import sys
from pathlib import Path
from typing import Dict, Tuple, List
from datetime import datetime

from config import TEST_MODE, GEN_PROMPT, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, KG_CREATING
from neo4j import GraphDatabase
from handler.task import generate_test
from knowledge_graph.math.eval.eval import evaluate_difficulty, evaluate_concept, evaluate_elo
from knowledge_graph.math.postprocess import postprocess_question
from dotenv import load_dotenv

load_dotenv()

# ======================= CONFIG ===========================
URI = NEO4J_URI
USERNAME = NEO4J_USER
PASSWORD = NEO4J_PASSWORD
DATABASE = "math"
FILE_ROOT = Path(os.getenv("FILE_ROOT", "knowledge_graph/math"))

# Chủ đề chuẩn theo SGK 2025 - Kết nối tri thức
DIFFICULTY = ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"]
QUESTION = ["Multiple choice", "Short answer"]
TOPIC_IDX: Dict[Tuple[int, str], int] = {}
DEFAULT_TOPIC = {
    10: [
        "Mệnh đề - Tập hợp",
        "Bất phương trình và hệ bất phương trình bậc nhất hai ẩn",
        "Hệ thức lượng trong tam giác",
        "Vector",
        "Các số đặc trưng của mẫu số liệu, không ghép nhóm",
        "Hàm số, đồ thị và ứng dụng",
        "Phương pháp tọa độ trong mặt phẳng",
        "Đại số tổ hợp",
        "Tính xác suất theo định nghĩa cổ điển"
    ],
    11: [
        "Hàm số lượng giác - Phương trình lượng giác",
        "Dãy số - Cấp số cộng - Cấp số nhân",
        "Các số đặc trưng đo xu thế trung tâm của mẫu số liệu ghép nhóm",
        "Quan hệ song song trong không gian",
        "Giới hạn - Hàm số liên tục",
        "Hàm số mũ - Hàm số Logarit",
        "Quan hệ vuông góc trong không gian",
        "Các quy tắc tính xác suất",
        "Đạo hàm"
    ],
    12: [
        "Ứng dụng đạo hàm để khảo sát và vẽ đồ thị hàm số",
        "Vector và hệ trục tọa độ trong không gian",
        "Các số đặc trưng đo mức độ phân tán của mẫu số liệu ghép nhóm",
        "Nguyên hàm - Tích phân",
        "Phương pháp tọa độ trong không gian",
        "Xác suất có điều kiện"
    ]
}

SGK_LINK = {
    10: [
        "https://loigiaihay.com/chuong-i-menh-de-va-tap-hop-e24908.html",
        "https://loigiaihay.com/chuong-ii-bat-phuong-trinh-va-he-bat-phuong-trinh-bac-nhat-hai-an-e24954.html",
        "https://loigiaihay.com/chuong-iii-he-thuc-luong-trong-tam-giac-e24955.html",
        "https://loigiaihay.com/chuong-iv-vecto-e24956.html",
        "https://loigiaihay.com/chuong-v-cac-so-dac-trung-cua-mau-so-lieu-khong-ghep-nhom-e24957.html",
        "https://loigiaihay.com/chuong-vi-ham-so-do-thi-va-ung-dung-e26640.html",
        "https://loigiaihay.com/chuong-vii-phuong-phap-toa-do-trong-mat-phang-e27704.html",
        "https://loigiaihay.com/chuong-viii-dai-so-to-hop-e27811.html",
        "https://loigiaihay.com/chuong-ix-tinh-xac-suat-theo-dinh-nghia-co-dien-e27861.html"
    ],
    11: [
        "https://loigiaihay.com/chuong-1-ham-so-luong-giac-va-phuong-trinh-luong-e30703.html",
        "https://loigiaihay.com/chuong-2-day-so-cap-so-cong-va-cap-so-nhan-e31490.html",
        "https://loigiaihay.com/chuong-3-cac-so-dac-trung-do-xu-the-trung-tam-cua-mau-so-lieu-ghep-nhom-cua-mau-so-lieu-e31518.html",
        "https://loigiaihay.com/chuong-4-quan-he-song-song-trong-khong-gian-e31526.html",
        "https://loigiaihay.com/chuong-5-gioi-hanham-so-lien-tuc-e31541.html",
        "https://loigiaihay.com/chuong-vi-ham-so-mu-va-ham-so-logarit-e31934.html",
        "https://loigiaihay.com/chuong-vii-quan-he-vuong-goc-trong-khong-gian-e31958.html",
        "https://loigiaihay.com/chuong-viii-cac-quy-tac-tinh-xac-suat-e31966.html",
        "https://loigiaihay.com/chuong-ix-dao-ham-e31971.html"
    ],
    12: [
        "https://loigiaihay.com/chuong-1-ung-dung-dao-ham-de-khao-sat-va-ve-do-thi-ham-so-e35538.html",
        "https://loigiaihay.com/chuong-2-vecto-va-he-truc-toa-do-trong-khong-gian-e35586.html",
        "https://loigiaihay.com/chuong-3-cac-so-do-dac-trung-do-muc-do-phan-tan-cua-mau-so-lieu-ghep-nhom-e35683.html",
        "https://loigiaihay.com/chuong-4-nguyen-ham-va-tich-phan-toan-12-ket-noi-tri-thuc-e35917.html",
        "https://loigiaihay.com/chuong-5-phuong-phap-toa-do-trong-khong-gian-e35952.html",
        "https://loigiaihay.com/chuong-6-xac-suat-co-dieu-kien-e35963.html"
    ],
}

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

driver_math = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

# ================== Helper functions ======================

def safe_write_file(path: Path | str, content: str):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def safe_create_if_missing(path: Path, placeholder: str = "<PLACEHOLDER>"):
    """Nếu file chưa có thì tạo mới với nội dung mặc định"""
    if not path.exists():
        safe_write_file(path, placeholder)

def make_tempfile_with(content: str) -> str:
    tmp = tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8", suffix=".txt")
    tmp.write(content)
    tmp.flush()
    tmp.close()
    return tmp.name

def open_dir(path: Path):
    """Mở thư mục chứa file để kiểm tra nhanh"""
    if os.name == "nt":  # Windows
        os.startfile(path)
    elif os.name == "posix":  # macOS/Linux
        subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", str(path)])

# ================== Neo4j helpers ==========================

def add_grade(session, grade: int):
    session.run(
        "MERGE (g:Grade {id:$id, name:$name})",
        {"id": f"grade_{grade}", "name": f"Tài liệu lớp {grade}"},
    )

def add_topic(session, grade: int, idx: int, topic: str) -> str:
    tid = f"grade_{grade}_{idx}"
    session.run("MERGE (t:Topic {id:$id, name:$name})", {"id": tid, "name": topic})
    session.run(
        "MATCH (g:Grade {id:$gid}) MATCH (t:Topic {id:$tid}) MERGE (g)-[:HAS_TOPIC]->(t)",
        {"gid": f"grade_{grade}", "tid": tid},
    )
    return tid

# ================== Content generation =====================

def write_or_generate(file_path: Path, template_text: str, generate: bool = True) -> str:
    safe_create_if_missing(file_path, template_text)
    if GEN_PROMPT and generate and not TEST_MODE:
        logger.info("Invoking generate_test for %s", file_path)
        response = generate_test(str(file_path))
        safe_write_file(file_path, response)
    return str(file_path)

def add_concept(session, grade: int, idx: int, topic: str, topic_list: Dict[int, List[str]] = DEFAULT_TOPIC):
    file_dir = FILE_ROOT / str(grade) / str(idx)
    file_path = file_dir / "concept.txt"
    if not file_path.exists() or GEN_PROMPT:
        prompt = f"""
Bạn là giáo viên Toán. Hãy đọc SGK Toán lớp {grade} (Kết nối tri thức).
Chủ đề: {topic_list[grade][idx-1]}.
Url dẫn đến kiến thức: {SGK_LINK[grade][idx-1]}
Nhiệm vụ: Tóm tắt định nghĩa, định lý, công thức, dạng bài tập chính.
"""
        safe_write_file(file_path, prompt)

    node_id = f"grade_{grade}_{idx}_concept"
    session.run(
        "MERGE (c:Concept {id:$id, name:$name, text:$text})",
        {"id": node_id, "name": f"Concept {topic}", "text": str(file_path)},
    )
    session.run(
        "MATCH (t:Topic {id:$tid}) MATCH (c:Concept {id:$cid}) MERGE (t)-[:HAS_CONCEPT]->(c)",
        {"tid": f"grade_{grade}_{idx}", "cid": node_id},
    )

    if not TEST_MODE and GEN_PROMPT:
        prompt = generate_test(str(file_path))
        safe_write_file(file_path, prompt)


def add_format(session, grade: int, idx: int) -> str:
    fid = f"grade_{grade}_{idx}_format"
    file_dir = FILE_ROOT / str(grade) / str(idx)
    file_path = file_dir / "format.txt"

    base_format_path = FILE_ROOT / "format" / "format.txt"
    base_format = base_format_path.read_text(encoding="utf-8") if base_format_path.exists() else "<FORMAT PLACEHOLDER>"
    safe_create_if_missing(file_path, base_format)

    session.run(
        "MERGE (f:Format {id:$id, name:$name, text:$text})",
        {"id": fid, "name": "format", "text": str(file_path)},
    )
    session.run(
        "MATCH (t:Topic {id:$tid}) MATCH (f:Format {id:$fid}) MERGE (t)-[:HAS_FORMAT]->(f)",
        {"tid": f"grade_{grade}_{idx}", "fid": fid},
    )
    return fid

def add_questions(session, grade: int, idx: int, fid: str):
    file_dir = FILE_ROOT / str(grade) / str(idx)
    for qn, question in enumerate(QUESTION, start=1):
        file_path = file_dir / f"question_{qn}.txt"
        template_path = FILE_ROOT / "format" / ("multiple_choice.txt" if qn == 1 else "short_answer.txt")
        template = template_path.read_text(encoding="utf-8") if template_path.exists() else f"<QUESTION TEMPLATE {question}>"
        safe_create_if_missing(file_path, template)

        qid = f"grade_{grade}_{idx}_question_{question.replace(' ', '_')}"
        session.run(
            "MERGE (q:Question {id:$id, name:$name, text:$text})",
            {"id": qid, "name": question, "text": str(file_path)},
        )
        session.run(
            "MATCH (f:Format {id:$fid}) MATCH (q:Question {id:$qid}) MERGE (f)-[:HAS_QUESTION]->(q)",
            {"fid": fid, "qid": qid},
        )

def add_difficulties(session, grade: int, idx: int, tid: str):
    file_dir = FILE_ROOT / str(grade) / str(idx)
    for dif, difficulty in enumerate(DIFFICULTY, start=1):
        file_path = file_dir / f"difficulty_{dif}.txt"
        cond_path = FILE_ROOT / "difficulty_cond" / f"difficulty_{dif}.txt"
        cond = cond_path.read_text(encoding="utf-8") if cond_path.exists() else ""
        if not file_path.exists() or GEN_PROMPT:
            prompt = f"""
Bạn là giáo viên Toán. Hãy tạo hướng dẫn sinh đề ở mức {difficulty}.
Chủ đề: {DEFAULT_TOPIC[grade][idx-1]}, lớp {grade}.
Điều kiện bổ sung:
{cond}
"""
            safe_write_file(file_path, prompt)

        did = f"grade_{grade}_{idx}_difficulty_{difficulty.replace(' ', '_')}"
        session.run(
            "MERGE (d:Difficulty {id:$id, name:$name, text:$text})",
            {"id": did, "name": difficulty, "text": str(file_path)},
        )
        session.run(
            "MATCH (t:Topic {id:$tid}) MATCH (d:Difficulty {id:$did}) MERGE (t)-[:HAS_DIFFICULTY]->(d)",
            {"tid": tid, "did": did},
        )
        if not TEST_MODE and GEN_PROMPT:
            prompt = generate_test(str(file_path))
            safe_write_file(file_path, prompt)
# ================== KG Builder ===============================

def create_kg_math(session, topic_map: Dict[int, List[str]] = DEFAULT_TOPIC):
    logger.info("Start creating KG math")
    for grade in sorted(topic_map.keys()):
        if KG_CREATING:
            add_grade(session, grade)   
        for idx, topic in enumerate(topic_map[grade], start=1):
            TOPIC_IDX[(grade, topic)] = idx
            if KG_CREATING:
                tid = add_topic(session, grade, idx, topic)
                add_concept(session, grade, idx, topic, topic_map)
                fid = add_format(session, grade, idx)
                add_questions(session, grade, idx, fid)
                add_difficulties(session, grade, idx, tid)
    logger.info("Finished KG creation")

# ================== Prompt Builder ==========================

def ask_question(session, grade: int, topic: str, difficulty: str, question: str):
    tid = f"grade_{grade}_{TOPIC_IDX[(grade, topic)]}"
    fid = f"grade_{grade}_{TOPIC_IDX[(grade, topic)]}_format"
    cid = f"grade_{grade}_{TOPIC_IDX[(grade, topic)]}_concept"
    qid = f"grade_{grade}_{TOPIC_IDX[(grade, topic)]}_question_{question.replace(' ', '_')}"
    did = f"grade_{grade}_{TOPIC_IDX[(grade, topic)]}_difficulty_{difficulty.replace(' ', '_')}"

    result = session.run(
        "MATCH (t:Topic {id:$tid})-[:HAS_FORMAT]->(f:Format {id:$fid})"
        "-[:HAS_QUESTION]->(q:Question {id:$qid}) "
        "MATCH (t)-[:HAS_CONCEPT]->(c:Concept {id:$cid}) "
        "MATCH (t)-[:HAS_DIFFICULTY]->(d:Difficulty {id:$did}) "
        "RETURN t.name AS topic, f.text AS format, "
        "q.name AS question, q.text AS question_text, "
        "d.name AS difficulty, d.text AS difficulty_text, "
        "c.name AS concept, c.text AS concept_text",
        {"tid": tid, "fid": fid, "qid": qid, "did": did, "cid": cid},
    )
    data = result.data()
    if not data:
        raise ValueError("Không tìm thấy dữ liệu KG cho topic/difficulty/question đã chọn")
    return data[0]

def build_prompt(topic: str = "", grade: int = 0,
                 difficulty: str = "Vận dụng", question: str = "Short answer", n: int = 1):
    if topic == "":
        topic = random.choice(DEFAULT_TOPIC[grade])
    elif grade == 0:
        grade = next(g for g, topics in DEFAULT_TOPIC.items() if topic in topics)

    with driver_math.session(database=DATABASE) as session:
        row = ask_question(session, grade, topic, difficulty, question)

    concept_text = Path(row["concept_text"]).read_text(encoding="utf-8")
    difficulty_text = Path(row["difficulty_text"]).read_text(encoding="utf-8")
    format_text = Path(row["format"]).read_text(encoding="utf-8")
    question_text = Path(row["question_text"]).read_text(encoding="utf-8")

    prompt = f"""
**** Role: Bạn là giáo viên Toán. Hãy tạo {n} câu hỏi cho học sinh. ****
**** Chủ đề: **** {topic}
**** Khái niệm và kiến thức (Concept): ****
{concept_text}
**** Hình thức (Format): ****
{format_text}
**** Kiểu câu hỏi (Question - {row['question']}): ****
{question_text}
**** Mức độ khó (Difficulty - {row['difficulty']}): ****
{difficulty_text}
**** Yêu cầu: Sinh {n} câu hỏi đúng theo các ràng buộc trên. ****
"""

    return prompt, row["concept_text"], row["difficulty_text"], row["format"], row["question_text"]

# ================== Main Test ===============================

def reform(file_dir : str, format_path, question_path):
    with open(file_dir, "r", encoding="utf-8") as f:
        prompt = f.read()
    with open(format_path, "r", encoding="utf-8") as f:
        format_text = f.read()
    with open(question_path, "r", encoding="utf-8") as f:
        question_text = f.read()
    reform_prompt = f"""
**** Role: Bạn là một nhân vật có khả năng điều chỉnh đề bài rất tốt. ****
**** Task: Tôi có một file đề Toán khá là tốt có độ khó vừa phải, tuy nhiên về mặt điều chỉnh format, đề trên còn gặp rất nhiều vấn đề khi tôi muốn chuyển chúng từ file txt sang file qti (text2qti). Vì vậy, tôi muốn bạn hỗ trợ tôi điều này.
**** Lưu ý: **** Không thêm bất kì một yếu tố nào ngoài lề vào prompt mới, kể cả bình luận và tiêu đề, và cả những đánh dấu của tôi
**** Hình thức yêu cầu (Format): ****
{format_text}
**** Kiểu câu hỏi: ****
{question_text}
**** Prompt cần chỉnh sửa: ****
-------
{prompt}
-------
""" 
    with open(file_dir, "w", encoding="utf-8") as f:
        f.write(reform_prompt)
    response = generate_test(file_dir)
    with open(file_dir, "w", encoding="utf-8") as f:
        f.write(response)


def math_test(topic: str = "", grade: int = 11, difficulty: str = "Vận dụng",
              question: str = "Short answer", n: int = 1):
    logger.info("Building prompt...")
    prompt, concept_path, difficulty_path, format_path, question_path = build_prompt(
        topic, grade, difficulty, question, n
    )
    if TEST_MODE:
        logger.info("TEST_MODE active: return prompt only.")
        return prompt, 0
    tmp_prompt_path = make_tempfile_with(prompt)
    response_text = generate_test(tmp_prompt_path)
    reform(tmp_prompt_path, format_path, question_path)
    evaluate_difficulty(difficulty_path, make_tempfile_with(response_text), grade, topic, difficulty)
    evaluate_concept(concept_path, make_tempfile_with(response_text), grade, topic)
    score = evaluate_elo(make_tempfile_with(response_text), grade, topic)
    with open("knowledge_graph/math/llm_return/response.txt", "w", encoding="utf-8") as f:
        f.write(str(response_text))
    return response_text, score

# ================== Example run ============================

if __name__ == "__main__":
    with driver_math.session(database=DATABASE) as session:
        create_kg_math(session)
    sample = math_test(topic="Hệ thức lượng trong tam giác", grade=10,
                       difficulty="Nhận biết", question="Short answer", n=1)
    print(sample)
