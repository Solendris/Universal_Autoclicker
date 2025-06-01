import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
import keyboard
import mouse
import json
import threading
import time
import logging
import os

# Global list to hold recorded actions
actions = []
recording = False
stop_signal = False


def setup_logging():
    log_folder = "Logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    logging.basicConfig(
        filename=os.path.join(log_folder, f"{time.strftime('%d_%m_%Y')}.log"),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def record_action(event_type, details):
    timestamp = time.time()
    action = {"time": timestamp, "type": event_type, "details": details}
    actions.append(action)


def record_mouse():
    def on_event(event):
        if not recording:
            return
        if isinstance(event, mouse.ButtonEvent) and event.event_type == 'down':
            try:
                pos = pyautogui.position()
                record_action("click", {"x": pos.x, "y": pos.y, "button": event.button})
            except Exception as e:
                logging.error(f"Error during mouse recording: {str(e)}")
    mouse.hook(on_event)


def record_keyboard():
    def on_key(e):
        try:
            if recording and e.event_type in ('down', 'up'):
                record_action("key", {"name": e.name, "event_type": e.event_type})
        except Exception as e:
            logging.error(f"Error during key recording: {str(e)}")
    keyboard.hook(on_key)


def start_recording():
    global actions, recording
    actions = []
    recording = True
    threading.Thread(target=record_mouse, daemon=True).start()
    threading.Thread(target=record_keyboard, daemon=True).start()
    logging.info("Recording started")
    status_label.config(text="Nagrywanie...")


def stop_recording():
    global recording
    recording = False
    status_label.config(text="Zatrzymano")
    logging.info("Recording stopped")


def play_actions_loop():
    global stop_signal
    stop_signal = False

    def play():
        if not actions:
            messagebox.showinfo("Info", "Brak nagranych akcji")
            return

        repeat_count = entry_count.get()
        infinite = infinite_var.get()

        try:
            count = int(repeat_count) if not infinite else float('inf')
        except ValueError:
            messagebox.showerror("Błąd", "Wprowadź poprawną liczbę powtórzeń.")
            return

        status_label.config(text="Odtwarzanie...")
        logging.info("Replay started")

        pressed_keys = set()
        i = 0
        while i < count and not stop_signal:
            cycle_label.config(text=f"Cykl: {i + 1}")
            for j, action in enumerate(actions):
                if stop_signal:
                    break

                if j > 0:
                    delay = action['time'] - actions[j - 1]['time']
                    time.sleep(delay)

                if action['type'] == 'click':
                    d = action['details']
                    pyautogui.mouseDown(x=d['x'], y=d['y'], button=d['button'])
                    time.sleep(0.05)
                    pyautogui.mouseUp(x=d['x'], y=d['y'], button=d['button'])

                elif action['type'] == 'key':
                    key_name = action['details']['name']
                    event_type = action['details']['event_type']
                    if event_type == 'down' and key_name not in pressed_keys:
                        keyboard.press(key_name)
                        pressed_keys.add(key_name)
                    elif event_type == 'up' and key_name in pressed_keys:
                        keyboard.release(key_name)
                        pressed_keys.remove(key_name)

            i += 1

        status_label.config(text="Zatrzymano")
        logging.info("Replay finished")

    threading.Thread(target=play, daemon=True).start()


def monitor_stop():
    def check_stop():
        global stop_signal
        while True:
            if keyboard.is_pressed('s'):
                stop_signal = True
                break
            time.sleep(0.1)
    threading.Thread(target=check_stop, daemon=True).start()


def save_to_file():
    if not actions:
        messagebox.showinfo("Info", "Brak danych do zapisania")
        return
    path = filedialog.asksaveasfilename(defaultextension=".json")
    if path:
        with open(path, "w") as f:
            json.dump(actions, f, indent=2)
        logging.info(f"Data saved to location: {path}")
        messagebox.showinfo("Zapisano", f"Zapisano do {path}")


def load_from_file():
    global actions
    path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if path:
        with open(path, "r") as f:
            actions = json.load(f)
        logging.info(f"Data loaded from location: {path}")
        messagebox.showinfo("Wczytano", f"Wczytano {len(actions)} akcji z {path}")


# === GUI ===
root = tk.Tk()
root.title("Universal AutoClicker")
root.geometry("350x420")

frame = tk.Frame(root)
frame.pack(pady=10)

btn_start_rec = tk.Button(frame, text="Start nagrywania", command=start_recording, width=25)
btn_start_rec.pack(pady=5)

btn_stop_rec = tk.Button(frame, text="Stop nagrywania", command=stop_recording, width=25)
btn_stop_rec.pack(pady=5)

btn_play = tk.Button(frame, text="Odtwórz akcje", command=lambda: [monitor_stop(), play_actions_loop()], width=25)
btn_play.pack(pady=5)

btn_save = tk.Button(frame, text="Zapisz do JSON", command=save_to_file, width=25)
btn_save.pack(pady=5)

btn_load = tk.Button(frame, text="Wczytaj z JSON", command=load_from_file, width=25)
btn_load.pack(pady=5)

count_frame = tk.Frame(root)
count_frame.pack(pady=5)

entry_label = tk.Label(count_frame, text="Liczba powtórzeń:")
entry_label.pack(side=tk.LEFT)

entry_count = tk.Entry(count_frame, width=5)
entry_count.insert(0, "1")
entry_count.pack(side=tk.LEFT, padx=5)


def validate_digits(p):
    return p.isdigit() or p == ""


vcmd = (root.register(validate_digits), '%P')
entry_count.config(validate="key", validatecommand=vcmd)

infinite_var = tk.BooleanVar()
chk_infinite = tk.Checkbutton(count_frame, text="Infinite", variable=infinite_var)
chk_infinite.pack(side=tk.LEFT)

status_label = tk.Label(root, text="Status: gotowy")
status_label.pack(pady=10)

cycle_label = tk.Label(root, text="Cykl: 0")
cycle_label.pack(pady=2)

hint_label = tk.Label(root, text="Naciśnij 's', aby zatrzymać odtwarzanie.", fg="gray")
hint_label.pack(pady=2)

setup_logging()
root.mainloop()
