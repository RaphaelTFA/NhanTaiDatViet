from MCP_server import generate_math
import csv
import os

header = "topic,grade,difficulty,question,n\n"

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
    ]
}

def run():
    for grade in DEFAULT_TOPIC: 
        for topic in DEFAULT_TOPIC[grade]:
            for idx, difficulty in enumerate(["Nhận biết", "Thông hiểu", "Vận dụng"], start = 1):
                print(f"Generating for {topic} - Part {idx}")
                rows = [
                    [topic, grade, difficulty, "Multiple choice", 20],
                ]
                with open("code/NhanTaiDatViet/sample/sample.csv", "w", newline="", encoding="utf-8") as f:
                    f.write(header)
                    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
                    writer.writerows(rows)
                make_math = generate_math(
                    course=2120114,
                    name=f"{topic} - Phần {idx}",
                    file=open("sample/sample.csv", "rb")
                )


