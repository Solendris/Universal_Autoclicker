import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
import keyboard
import mouse
import json
import threading
import time
import datetime
import os

# Global list to hold recorded actions
actions = []
recording = False

# Prepare log file
timestamp_str = datetime.datetime.now().strftime("%d-%m-%Y")
log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(log_dir, f"autoclicker_log_{timestamp_str}.log")
log_file = open(log_filename, "a", encoding="utf-8")

def log_event(message):
    log_file.write(message + "\n")
    log_file.flush()

# === Recording Functions ===
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
                pass
    mouse.hook(on_event)

def record_keyboard():
    def on_key(e):
        if recording and e.event_type in ('down', 'up'):
            record_action("key", {"name": e.name, "event_type": e.event_type})
    keyboard.hook(on_key)

def start_recording():
    global actions, recording
    actions = []
    recording = True
    threading.Thread(target=record_mouse, daemon=True).start()
    threading.Thread(target=record_keyboard, daemon=True).start()
    status_label.config(text="Nagrywanie...")
    log_event("[LOG] Nagrywanie rozpoczęte")

def stop_recording():
    global recording
    recording = False
    status_label.config(text="Zatrzymano")
    log_event("[LOG] Nagrywanie zakończone")

# === Playback Function ===
def play_actions():
    if not actions:
        messagebox.showinfo("Info", "Brak nagranych akcji")
        return

    log_event("[LOG] Rozpoczęto odtwarzanie")
    start_time = actions[0]['time']
    pressed_keys = set()

    for i, action in enumerate(actions):
        if i > 0:
            delay = action['time'] - actions[i - 1]['time']
            time.sleep(delay)

        if action['type'] == 'click':
            d = action['details']
            pyautogui.click(x=d['x'], y=d['y'], button=d['button'])

        elif action['type'] == 'key':
            key_name = action['details']['name']
            event_type = action['details']['event_type']

            if event_type == 'down' and key_name not in pressed_keys:
                keyboard.press(key_name)
                pressed_keys.add(key_name)
            elif event_type == 'up' and key_name in pressed_keys:
                keyboard.release(key_name)
                pressed_keys.remove(key_name)

    log_event("[LOG] Zakończono odtwarzanie")

# === JSON IO ===
def save_to_file():
    if not actions:
        messagebox.showinfo("Info", "Brak danych do zapisania")
        return
    path = filedialog.asksaveasfilename(defaultextension=".json")
    if path:
        with open(path, "w") as f:
            json.dump(actions, f, indent=2)
        log_event(f"[LOG] Zapisano dane w lokalizacji: {path}")
        messagebox.showinfo("Zapisano", f"Zapisano do {path}")

def load_from_file():
    global actions
    path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if path:
        with open(path, "r") as f:
            actions = json.load(f)
        log_event(f"[LOG] Wczytano dane z lokalizacji: {path}")
        messagebox.showinfo("Wczytano", f"Wczytano {len(actions)} akcji z {path}")

# === GUI ===
root = tk.Tk()
root.title("AutoClicker Tester GUI")
root.geometry("300x300")

frame = tk.Frame(root)
frame.pack(pady=20)

btn_start_rec = tk.Button(frame, text="Start nagrywania", command=start_recording, width=20)
btn_start_rec.pack(pady=5)

btn_stop_rec = tk.Button(frame, text="Stop nagrywania", command=stop_recording, width=20)
btn_stop_rec.pack(pady=5)

btn_play = tk.Button(frame, text="Odtwórz akcje", command=lambda: threading.Thread(target=play_actions, daemon=True).start(), width=20)
btn_play.pack(pady=5)

btn_save = tk.Button(frame, text="Zapisz do JSON", command=save_to_file, width=20)
btn_save.pack(pady=5)

btn_load = tk.Button(frame, text="Wczytaj z JSON", command=load_from_file, width=20)
btn_load.pack(pady=5)

status_label = tk.Label(root, text="Status: gotowy")
status_label.pack(pady=10)

root.mainloop()

# Zamknij plik logu po zakończeniu GUI
log_file.close()
