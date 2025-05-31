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
                logging.error(f"Error occures during recording mouse movement: {str(e)}")
    mouse.hook(on_event)


def record_keyboard():
    def on_key(e):
        try:
            if recording and e.event_type in ('down', 'up'):
                record_action("key", {"name": e.name, "event_type": e.event_type})
        except Exception as e:
            logging.error(f"Error occures during recording key click: {str(e)}")
    keyboard.hook(on_key)


def start_recording():
    global actions, recording
    actions = []
    recording = True
    threading.Thread(target=record_mouse, daemon=True).start()
    threading.Thread(target=record_keyboard, daemon=True).start()
    logging.info("Recording started")


def stop_recording():
    global recording
    recording = False
    status_label.config(text="Zatrzymano")
    logging.info("Recording stopped")


# === Playback Function ===
def play_actions():
    if not actions:
        messagebox.showinfo("Info", "Brak nagranych akcji")
        return

    logging.info("Replay started")
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

    logging.info("Reply finished")


# === JSON IO ===
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
        logging.info(f"Data readed from location: {path}")
        messagebox.showinfo("Wczytano", f"Wczytano {len(actions)} akcji z {path}")


# === GUI ===
root = tk.Tk()
root.title("Universal AutoClicker")
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

setup_logging()
root.mainloop()
