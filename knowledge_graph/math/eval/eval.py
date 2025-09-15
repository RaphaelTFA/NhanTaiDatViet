from handler.task import generate_test_2
from knowledge_graph.math.eval.update import difficulty_update, concept_update
import re

def evaluate_difficulty(difficulty_dir: str, content_dir: str, grade: int, topic: str, difficulty: str) -> None:
    with open(content_dir, "r", encoding="utf-8") as f:
        content = f.read()
    with open("knowledge_graph/math/eval/difficulty.txt", "r", encoding="utf-8") as f:
        eval_prompt = f.read()

    prompt = f"""
{eval_prompt} 

***THÔNG TIN VĂN BẢN CẦN ĐƯỢC CHẤM:***
*   **Khối học**: {grade}
*   **Chủ đề**: {topic}
*   **Mức độ khó cần thiết**: {difficulty}
*   **Văn bản**: {content}
"""
    response = generate_test_2(prompt)
    lines = response.split("\n")

    # Lấy điểm
    score_line = next((line for line in lines if "Tổng điểm" in line), None)
    score = None
    if score_line:
        match = re.search(r"(\d+(\.\d+)?)/10", score_line)
        if match:
            score = float(match.group(1))

    # Nếu điểm thấp hơn 8, update đánh giá
    if score is not None and score < 8:
        evaluation = next((line for line in lines if "Đánh giá" in line), "")
        feedback = next((line for line in lines if "Nhận xét" in line), "")
        difficulty_update(difficulty_dir, grade, topic, difficulty, evaluation, feedback, score)


def evaluate_concept(concept_dir: str, content_dir: str, grade: int, topic: str) -> None:
    with open(content_dir, "r", encoding="utf-8") as f:
        content = f.read()
    with open("knowledge_graph/math/eval/concept.txt", "r", encoding="utf-8") as f:
        eval_prompt = f.read()

    prompt = f"""
{eval_prompt} 

***THÔNG TIN VĂN BẢN CẦN ĐƯỢC CHẤM:***
*   **Khối học**: {grade}
*   **Chủ đề**: {topic}
*   **Văn bản**: {content}
"""
    response = generate_test_2(prompt)
    lines = response.split("\n")

    # Lấy điểm
    score_line = next((line for line in lines if "Tổng điểm" in line), None)
    score = None
    if score_line:
        match = re.search(r"(\d+(\.\d+)?)/10", score_line)
        if match:
            score = float(match.group(1))

    # Nếu điểm thấp hơn 8, update đánh giá
    if score is not None and score < 8:
        evaluation = next((line for line in lines if "Đánh giá" in line), "")
        feedback = next((line for line in lines if "Nhận xét" in line), "")
        concept_update(concept_dir, grade, topic, evaluation, feedback, score)

def evaluate_elo(content_dir: str, grade: int, topic: str, difficulty: str) -> None:
    with open(content_dir, "r", encoding="utf-8") as f:
        content = f.read()
    with open("knowledge_graph/math/eval/elo.txt", "r", encoding="utf-8") as f:
        eval_prompt = f.read()

    prompt = f"""
{eval_prompt} 

***THÔNG TIN VĂN BẢN CẦN ĐƯỢC CHẤM:***
*   **Khối học**: {grade}
*   **Chủ đề**: {topic}
*   **Mức độ khó cần thiết**: {difficulty}
*   **Văn bản**: {content}
"""
    response = generate_test_2(prompt)
    lines = response.split("\n")

    # Lấy điểm
    score_line = next((line for line in lines if "Tổng điểm" in line), None)
    score = None
    if score_line:
        match = re.search(r"(\d+(\.\d+)?)/10", score_line)
        if match:
            score = float(match.group(1))
    return score

