import os
import threading
import time
import logging

import pyautogui
from pynput import keyboard
from pynput.mouse import Button, Controller


class AutoClicker:
    def __init__(self):
        self.mouse = Controller()
        self.running = False
        self.log_folder = "Logs"
        self.setup_logging()

    def setup_logging(self):
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

        logging.basicConfig(
            filename=os.path.join(self.log_folder, f"{time.strftime('%d_%m_%Y')}.log"),
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def on_key_press(self, key):
        try:
            if key == keyboard.Key.f9:
                print("Started searching for images.")
                logging.info("Started searching for images.")
                self.running = True
                threading.Thread(target=self.auto_click).start()
            elif key == keyboard.Key.f10:
                print("Stopped searching for images.")
                logging.info("Stopped searching for images.")
                self.running = False
        except Exception as e:
            logging.error(f"Error during key press: {str(e)}")

    def auto_click(self):
        while self.running:
            try:
                folder_path = r"pictures"
                # logging.info("Przeszukuję folder...")
                for filename in os.listdir(folder_path):
                    # logging.info(f"Sprawdzam plik: {filename}")
                    image_path = os.path.join(folder_path, filename)
                    # logging.info(f"image path: {image_path}")
                    location = pyautogui.locateOnScreen(image_path, minSearchTime=1, confidence=0.9)
                    # logging.info(f"Znalazlem plik w lokacji: {location}")
                    if location is not None:
                        logging.info(f"Clicking on image: {filename}")
                        print(location.left, location.top)
                        mouse = Controller()
                        mouse.position = (int(location.left + location.width/2), int(location.top + location.height/2))
                        self.mouse.click(button=Button.left, count=2)
                        time.sleep(5)
            except Exception as e:
                logging.error(f"Error during auto click: {str(e)}")

    def run(self):
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            listener.join()


auto_clicker = AutoClicker()
auto_clicker.run()
