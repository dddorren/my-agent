import sys
import os
import socket

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 查找可用端口
port = 5000
while port < 5020:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', port))
            break
    except OSError:
        port += 1

print("Server starting on port", port)
print("Open browser: http://localhost:" + str(port))

import uvicorn
uvicorn.run("app.main:app", host="0.0.0.0", port=port, log_level="info")