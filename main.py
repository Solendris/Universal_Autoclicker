import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
import keyboard
import mouse
import json
import threading
import time

# Global list to hold recorded actions
actions = []
recording = False


# === Recording Functions ===
def record_action(event_type, details):
    timestamp = time.time()
    actions.append({"time": timestamp, "type": event_type, "details": details})


def record_mouse():
    def on_event(event):
        if not recording:
            return
        if isinstance(event, mouse.ButtonEvent) and event.event_type == 'down':
            try:
                pos = pyautogui.position()
                record_action("click", {"x": pos.x, "y": pos.y, "button": event.button})
            except Exception as e:
                print("Błąd przy odczycie pozycji:", e)
    mouse.hook(on_event)


def record_keyboard():
    def on_key(e):
        if recording:
            record_action("key", {"name": e.name, "event_type": e.event_type})
    keyboard.hook(on_key)


def start_recording():
    global actions, recording
    actions = []
    recording = True
    threading.Thread(target=record_mouse, daemon=True).start()
    threading.Thread(target=record_keyboard, daemon=True).start()
    status_label.config(text="Nagrywanie...")


def stop_recording():
    global recording
    recording = False
    status_label.config(text="Zatrzymano")


# === Playback Function ===
def play_actions():
    if not actions:
        messagebox.showinfo("Info", "Brak nagranych akcji")
        return

    # start_time = actions[0]['time']
    for i, action in enumerate(actions):
        if i > 0:
            delay = action['time'] - actions[i - 1]['time']
            time.sleep(delay)

        if action['type'] == 'click':
            d = action['details']
            pyautogui.click(x=d['x'], y=d['y'], button=d['button'])
        elif action['type'] == 'key' and action['details']['event_type'] == 'down':
            keyboard.write(action['details']['name'])


# === JSON IO ===
def save_to_file():
    if not actions:
        messagebox.showinfo("Info", "Brak danych do zapisania")
        return
    path = filedialog.asksaveasfilename(defaultextension=".json")
    if path:
        with open(path, "w") as f:
            json.dump(actions, f, indent=2)
        messagebox.showinfo("Zapisano", f"Zapisano do {path}")


def load_from_file():
    global actions
    path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if path:
        with open(path, "r") as f:
            actions = json.load(f)
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

btn_play = tk.Button(frame, text="Odtwórz akcje",
                     command=lambda: threading.Thread(target=play_actions, daemon=True).start(), width=20)
btn_play.pack(pady=5)

btn_save = tk.Button(frame, text="Zapisz do JSON", command=save_to_file, width=20)
btn_save.pack(pady=5)

btn_load = tk.Button(frame, text="Wczytaj z JSON", command=load_from_file, width=20)
btn_load.pack(pady=5)

status_label = tk.Label(root, text="Status: gotowy")
status_label.pack(pady=10)

root.mainloop()
