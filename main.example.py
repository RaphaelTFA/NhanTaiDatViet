import os
import subprocess

os.chdir(r"...") # direction dẫn tới file NhanTaiDatViet
subprocess.run([
    "uvicorn", 
    "MCP_server:app", 
    "--reload", 
    "--host", "127.0.0.1", 
    "--port", "8000"
])
