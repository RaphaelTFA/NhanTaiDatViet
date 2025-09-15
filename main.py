import os
import subprocess

os.chdir(r"C:\Users\hungn\projects\Project_1\code\NhanTaiDatViet") #hoặc cái gì đó tương tự (dẫn đến file NhanTaiDatViet)
subprocess.run([
    "uvicorn", 
    "MCP_server:app", 
    "--reload", 
    "--host", "127.0.0.1", 
    "--port", "8000"
])
