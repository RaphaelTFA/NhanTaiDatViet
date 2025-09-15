import os

def transfer():
    txt_filename = "knowledge_graph/máth/llm_return/full_response.txt"
    data_name = f"data/math/test_{len(os.listdir('data/math')) // 4 + 1}"
    os.makedirs(os.path.dirname(f"{data_name}.txt"), exist_ok=True)
    with open(f"{data_name}.txt", "w", encoding="utf-8") as f:
        with open(txt_filename, "r", encoding="utf-8") as src:
            f.write(src.read())
    data_name = data_name.replace("/", "\\")
    subprocess.run(["text2qti", f"{data_name}.txt"])
    with open(f"{data_name}.txt", "r", encoding="utf-8") as f:
        text = f.read()
    questions = text.split("\n\n")
    no_ans, w_ans = "", ""
    mcq_trig = ['*a)', '*b)', '*c)', '*d)']
    mcq_trig_2 = ['a)', 'b)', 'c)', 'd)']
    mcq_replace = ['\n  A.', '\n  B.', '\n  C.', '\n  D.']
    mcq_replace_2 = ['\n  A. [CA]', '\n  B. [CA]', '\n  C. [CA]', '\n  D. [CA]']
    for ques in questions:
        if any(i in ques for i in mcq_trig):
            part = ques.split("\n")
            no_ans += "\n\n Bài " + f"{part[0]}"
            w_ans += "\n\n Bài " + f"{part[0]}"
            for i in range(4, 8):
                no_ans += f"{part[i].replace(mcq_trig[i-4], mcq_replace[i-4]).replace(mcq_trig_2[i-4], mcq_replace[i-4])}"
                w_ans += f"\n{part[i].replace(mcq_trig[i-4], mcq_replace_2[i-4])}" if '*' in part[i] else f"\n{part[i].replace(mcq_trig_2[i-4], mcq_replace[i-4])}"
        elif '=' in ques:
            part = ques.split("\n")
            no_ans += "\n\n Bài " + f"{part[0]}"
            w_ans += "\n\n Bài " + f"{part[0]}"
            w_ans += "\n\n" + f"{part[4].replace('=', f'    Đáp án')}"
    with open(f"{data_name}.txt", "w", encoding="utf-8") as f:
        f.write(no_ans)
    subprocess.run(["pandoc", f"{data_name}.txt", "-o", f"{data_name}_no_ans.docx", "--reference-doc=knowledge_graph\math\\format\\reference.docx"])
    with open(f"{data_name}.txt", "w", encoding="utf-8") as f:
        f.write(w_ans)
    subprocess.run(["pandoc", f"{data_name}.txt", "-o", f"{data_name}_wi_ans.docx", "--reference-doc=knowledge_graph\math\\format\\reference.docx"])
    with open(f"{data_name}.txt", "w", encoding="utf-8") as f:
        with open(txt_filename, "r", encoding="utf-8") as src:
            f.write(src.read())