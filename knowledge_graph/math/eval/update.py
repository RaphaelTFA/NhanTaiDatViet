from handler.task import generate_test_2

def difficulty_update(difficulty_dir, grade, topic, difficulty, evaluation, feedback, score):
    with open(difficulty_dir, "r", encoding="utf-8") as f:
        prompt = f.read()
    update_prompt = f"""
**1. Mục Tiêu Tổng Quát:**
"Tôi cần bạn phân tích và cải tiến một prompt tạo câu hỏi toán học hiện có. Mục tiêu là để prompt mới khắc phục triệt để các hạn chế đã được nhận xét, đồng thời đảm bảo các câu hỏi tạo ra đáp ứng chính xác về mức độ nhận thức (Nhận biết, Thông hiểu, Vận dụng, Vận dụng cao)"

**2. Thông Tin Chi Tiết Về Yêu Cầu Câu Hỏi:**

*   **Chủ đề toán học:** {topic}
*   **Cấp độ lớp học:** {grade}
*   **Mức độ nhận thức yêu cầu:** {difficulty}

**3. Phân Tích Nhận Xét Từ Đánh Giá (Eval Feedback):**
{evaluation}
{feedback}
*   **Điểm số** {score}/10 

**4. Prompt Cũ Cần Cập Nhật:**

"Dưới đây là phiên bản prompt hiện tại mà tôi muốn bạn phân tích và cập nhật:

```
{prompt}
```"

**5. Hướng Dẫn Chi Tiết Để Cập Nhật Prompt Mới:**

"Dựa trên tất cả các thông tin đã cung cấp (chủ đề, khối học, mức độ, định dạng và các vấn đề từ đánh giá), hãy xây dựng một prompt mới hoàn chỉnh và tối ưu. Prompt mới này phải:
*   **Đảm bảo tính chính xác:** Các câu hỏi tạo ra phải hoàn toàn phù hợp với chủ đề, khối học và đặc biệt là đúng {difficulty} đã chọn.
*   **Khắc phục lỗi:** Giải quyết triệt để tất cả các vấn đề đã nêu trong phần "Phân Tích Nhận Xét Từ Đánh Giá".
*   **Đa dạng và chất lượng đáp án (nếu trắc nghiệm):** Nếu là câu hỏi trắc nghiệm, prompt mới cần chỉ dẫn để tạo ra các đáp án nhiễu hợp lý, có tính đánh lừa cao, không dễ dàng bị loại bỏ.
*   **Rõ ràng và súc tích:** Ngôn ngữ của prompt mới phải rõ ràng, ngắn gọn, dễ hiểu để AI có thể tạo ra câu hỏi một cách hiệu quả nhất, tránh các diễn đạt gây hiểu lầm.
*   **Tính linh hoạt:** Nếu có thể, hãy tích hợp sự linh hoạt để prompt có thể tạo ra các biến thể câu hỏi khác nhau trong cùng một chủ đề và mức độ."

**6. Đầu Ra Mong Muốn:**

"Xin hãy cung cấp prompt mới đã được cập nhật và tối ưu, không cần đưa ra bất kỳ giải thích hay phân tích nào khác ngoài prompt mới này."

"""
    response = generate_test_2(update_prompt)
    with open(difficulty_dir, "w", encoding="utf-8") as f:
        f.write(response)

def concept_update(concept_dir, grade, topic, evaluation, feedback, score):
    with open(concept_dir, "r", encoding="utf-8") as f:
        prompt = f.read()
    update_prompt = f"""
**1. Mục Tiêu Tổng Quát:**
"Tôi muốn bạn phân tích và cập nhật toàn bộ một bộ kiến thức toán học hiện có. Mục tiêu là để bộ kiến thức mới được tối ưu hóa, đảm bảo tính đầy đủ, chính xác, cập nhật theo chương trình **Sách giáo khoa Kết Nối Tri Thức Với Cuộc Sống**, và đặc biệt là khắc phục những hạn chế đã được nhận xét từ các đánh giá trước đó."

**2. Thông Tin Chi Tiết Về Kiến Thức Cần Cập Nhật :**

*   **Chủ đề toán học chính:** {topic}
*   **Cấp độ lớp học:** {grade}
*   **Bộ sách giáo khoa áp dụng:** **Kết Nối Tri Thức Với Cuộc Sống** 

**3. Phân Tích Nhận Xét Từ Đánh Giá (Eval Feedback):**

"Dựa trên các đánh giá và kiểm thử trước đây, bộ kiến thức toán học cũ của tôi thường mắc phải các lỗi hoặc có các điểm yếu sau đây cần được cải thiện:
{evaluation}
{feedback}
*   **Điểm số** {score}/10

**4. Bộ Kiến Thức Toán Học Cũ Cần Cập Nhật (Dán toàn bộ nội dung kiến thức cũ của bạn vào đây):**

Dưới đây là toàn bộ nội dung kiến thức toán học hiện tại về chủ đề {topic} của khối {grade} mà tôi muốn bạn phân tích và cập nhật:
```
{prompt}
```

**5. Hướng Dẫn Chi Tiết Để Cập Nhật Bộ Kiến Thức Mới:**

"Dựa trên tất cả các thông tin đã cung cấp (chủ đề, khối học, bộ sách, và các vấn đề từ đánh giá), hãy xây dựng một bộ kiến thức toán học mới hoàn chỉnh và tối ưu. Bộ kiến thức mới này phải:
*   **Tuân thủ SGK Kết Nối Tri Thức:** Đảm bảo tất cả các định nghĩa, định lý, công thức, ví dụ và bài tập mẫu phải hoàn toàn phù hợp và bám sát với chương trình, phong cách trình bày và triết lý của sách giáo khoa **Kết Nối Tri Thức Với Cuộc Sống** cho khối lớp và chủ đề đã nêu.
*   **Khắc phục lỗi:** Giải quyết triệt để tất cả các vấn đề đã nêu trong phần "Phân Tích Nhận Xét Từ Đánh Giá", đặc biệt là các sai lệch, thiếu sót, hoặc lỗi về cấu trúc.
*   **Đầy đủ và logic:** Nội dung phải đầy đủ các kiến thức cần thiết trong chủ đề, được sắp xếp một cách logic, dễ hiểu, theo trình tự hợp lý cho học sinh.
*   **Rõ ràng và dễ hiểu:** Sử dụng ngôn ngữ rõ ràng, súc tích, cung cấp các giải thích dễ hiểu và các ví dụ minh họa phù hợp với mức độ của học sinh.
*   **Nhấn mạnh ứng dụng:** Tích hợp các ví dụ hoặc phần liên hệ với thực tế nếu chủ đề đó thường được sách Kết Nối Tri Thức trình bày theo hướng ứng dụng."

**6. Đầu Ra Mong Muốn:**

"Xin hãy cung cấp toàn bộ bộ kiến thức toán học mới đã được cập nhật và tối ưu, không cần đưa ra bất kỳ giải thích hay phân tích nào khác ngoài prompt mới này."
"""
    response = generate_test_2(update_prompt)
    with open(concept_dir, "w", encoding="utf-8") as f:
        f.write(response)