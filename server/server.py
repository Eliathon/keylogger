import socket
import os
import tqdm

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"Listening on {SERVER_HOST}:{SERVER_PORT}")
client_socket, address = s.accept()
print(f"Accepted connection from {address}")
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)
filesize = int(filesize)

progress = tqdm.tqdm(range(filesize), f"Receiving {filesize}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as file:
    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        file.write(data)
        progress.update(len(data))
client_socket.close()
s.close()