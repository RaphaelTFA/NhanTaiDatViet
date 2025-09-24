import os
import subprocess

os.chdir(r"C:\Users\hungn\projects\Project_1\code\NhanTaiDatViet") 
subprocess.run([
    "uvicorn", 
    "MCP_server:app",
    "--host", "127.0.0.1", 
    "--port", "8000",
    "--workers", "4"
])
