import os
import subprocess

def transfer():
    txt_filename = "knowledge_graph/math/llm_return/full_response.txt"
    os.makedirs("data/math", exist_ok=True)
    test_count = len([f for f in os.listdir("data/math") if f.endswith(".txt")])
    data_name = f"data/math/test_{test_count + 1}"
    with open(f"{data_name}.txt", "w", encoding="utf-8") as f:
        with open(txt_filename, "r", encoding="utf-8") as src:
            f.write(src.read())
    try:
        subprocess.run(["text2qti", f"{data_name}.txt"], check=True)
    except FileNotFoundError:
        print("text2qti not found")
    except subprocess.CalledProcessError as e:
        print(f"text2qti failed: {e}")
    with open(f"{data_name}.txt", "r", encoding="utf-8") as f:
        text = f.read()
    questions = text.split("\n\n")
    no_ans, w_ans = "", ""
    mcq_trig = ['*a)', '*b)', '*c)', '*d)']
    mcq_trig_2 = ['a)', 'b)', 'c)', 'd)']
    mcq_replace = ['\n  A.', '\n  B.', '\n  C.', '\n  D.']
    mcq_replace_2 = ['\n  A. [CA]', '\n  B. [CA]', '\n  C. [CA]', '\n  D. [CA]']

    for ques in questions:
        part = ques.split("\n")
        if not part or not part[0].strip():
            continue  
        try:
            if any(i in ques for i in mcq_trig):
                no_ans += "\n\n Bài " + part[0]
                w_ans += "\n\n Bài " + part[0]
                for i in range(4, 8):
                    if i < len(part):
                        no_ans += part[i].replace(mcq_trig[i-4], mcq_replace[i-4]).replace(mcq_trig_2[i-4], mcq_replace[i-4])
                        w_ans += (
                            "\n" + part[i].replace(mcq_trig[i-4], mcq_replace_2[i-4])
                            if "*" in part[i]
                            else "\n" + part[i].replace(mcq_trig_2[i-4], mcq_replace[i-4])
                        )
            elif "=" in ques and len(part) > 4:
                no_ans += "\n\n Bài " + part[0]
                w_ans += "\n\n Bài " + part[0]
                w_ans += "\n\n" + part[4].replace("=", "    Đáp án")
        except Exception as e:
            print(f"Lỗi khi xử lý câu hỏi: {e}, ques={ques[:50]}...")
    with open(f"{data_name}.txt", "w", encoding="utf-8") as f:
        f.write(no_ans)
    try:
        subprocess.run([
            "pandoc", f"{data_name}.txt", "-o", f"{data_name}_no_ans.docx",
            "--reference-doc=knowledge_graph/math/format/reference.docx"
        ], check=True)
    except Exception as e:
        print(f"Pandoc no_ans failed: {e}")
    with open(f"{data_name}.txt", "w", encoding="utf-8") as f:
        f.write(w_ans)
    try:
        subprocess.run([
            "pandoc", f"{data_name}.txt", "-o", f"{data_name}_wi_ans.docx",
            "--reference-doc=knowledge_graph/math/format/reference.docx"
        ], check=True)
    except Exception as e:
        print(f"Pandoc wi_ans failed: {e}")
    with open(f"{data_name}.txt", "w", encoding="utf-8") as f:
        with open(txt_filename, "r", encoding="utf-8") as src:
            f.write(src.read())
    return f"{data_name}.zip"
