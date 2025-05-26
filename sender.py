import os
import socket
import tqdm

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
host = "127.0.0.1"
port = 5001
filename = "log.txt"
filesize = os.path.getsize(filename)

s = socket.socket()
print(f"Connecting to {host}:{port}")
s.connect((host, port))
print(f"Connected to {host}:{port}")
s.send(f"{filename}{SEPARATOR}{filesize}".encode())

progress = tqdm.tqdm(range(filesize), f"Sending {filesize}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as file:
    while True:
        data = file.read(BUFFER_SIZE)
        if not data:
            break
        s.sendall(data)
        progress.update(len(data))
s.close()