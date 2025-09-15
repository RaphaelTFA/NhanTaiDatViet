import re
import json
from pathlib import Path

# ================== Load SGK syllabus (chương trình hợp lệ) ==================
# Bạn nên tự cập nhật thêm các chủ đề/kiến thức cụ thể cho từng lớp
SYLLABUS_PATH = Path("knowledge_graph/math/syllabus.json")

if SYLLABUS_PATH.exists():
    with open(SYLLABUS_PATH, "r", encoding="utf-8") as f:
        SYLLABUS = json.load(f)
else:
    # fallback: khung cơ bản
    SYLLABUS = {
        "10": ["tập hợp", "hàm số bậc nhất", "hàm số bậc hai", "hệ phương trình", "bất phương trình"],
        "11": ["lượng giác", "dãy số", "giới hạn", "đạo hàm"],
        "12": ["nguyên hàm", "tích phân", "số phức", "logarit", "hàm số mũ"]
    }

# ================== 1. Chuẩn hóa câu dẫn (stem) ==================
def fix_question_stem(question_text: str) -> str:
    """Chuẩn hóa câu dẫn: thêm từ 'Tìm...', 'Họ nguyên hàm...', 'Chọn mệnh đề đúng'."""
    lines = question_text.strip().splitlines()
    fixed_lines = []
    for line in lines:
        l = line.strip()
        if l.startswith("Câu ") or l.startswith("*"):
            fixed_lines.append(l)
            continue
        # nếu chỉ là biểu thức, thêm 'Tìm...'
        if re.match(r"^[\d\w\(\)\+\-\*/=^ ]+$", l):
            fixed_lines.append("Tìm " + l)
        elif "nguyên hàm" in l.lower() and not l.lower().startswith("tìm"):
            fixed_lines.append("Họ nguyên hàm của " + l)
        elif "mệnh đề" in l.lower() and not l.lower().startswith("chọn"):
            fixed_lines.append("Chọn mệnh đề đúng: " + l)
        else:
            fixed_lines.append(l)
    return "\n".join(fixed_lines)

# ================== 2. Validate đáp án ==================
FORBIDDEN_SYMBOLS = {"sec", "cosec", "cotg"}

def validate_answers(question_block: str) -> bool:
    """
    Kiểm tra đáp án:
    - Không chứa ký hiệu lạ (sec, cosec, ...)
    - Có đúng 1 đáp án đúng (giả định đáp án đúng có ký hiệu *)
    """
    if any(sym in question_block for sym in FORBIDDEN_SYMBOLS):
        return False

    # check số lượng đáp án đúng
    correct_count = len(re.findall(r"\*\)", question_block))
    return correct_count == 1

# ================== 3. Check nội dung ngoài SGK ==================
def filter_out_of_scope(question_text: str, grade: int) -> bool:
    """
    Kiểm tra xem câu hỏi có kiến thức ngoài SGK hay không.
    Nếu tìm thấy từ khóa không có trong SYLLABUS -> loại.
    """
    content = question_text.lower()
    valid_keywords = " ".join(SYLLABUS.get(str(grade), [])).lower()
    for word in re.findall(r"[a-zA-Zà-ỹ]+", content):
        if word not in valid_keywords:
            # bỏ qua từ chung chung, chỉ check nếu rõ ràng ngoài chương trình
            if len(word) > 5:  # từ dài
                return False
    return True

# ================== 4. Postprocess tổng hợp ==================
def postprocess_question(raw_text: str, grade: int) -> str | None:
    """
    Sửa lỗi tự động và validate lại.
    Trả về câu hỏi đã sửa nếu hợp lệ, hoặc None nếu không dùng được.
    """
    fixed = fix_question_stem(raw_text)

    # validate đáp án
    if not validate_answers(fixed):
        return None

    # check chương trình
    if not filter_out_of_scope(fixed, grade):
        return None

    return fixed
