# Universal AutoClicker

**Smart, Recordable & Cross-platform AutoClicker**

---

## Overview

Universal AutoClicker is a powerful automation tool that lets you **record** and **replay mouse and keyboard actions** with precise timing. Designed for simplicity and flexibility, it's perfect for GUI testing, repetitive tasks, automation, or even gaming.

> Unlike basic auto-clickers, this app captures real-time human interactions and saves them as portable macros (.json files).

---

## Features

- Mouse + Keyboard **input recording** (clicks, key presses/releases)
- **Loopable playback**: once, multiple times, or infinitely
- **Save/Load actions** to/from `.json`
- **Emergency Stop** via **`S` key**
- **User-friendly GUI** with `tkinter`
- **Logging support** with timestamped `.log` files
- **Dist version available**: `dist/UniversalAutoClicker.exe` is a ready-to-use Windows executable

---

## Quick Start

### Option 1: Python source (cross-platform)

1. Clone the repo:
   ```bash
   git clone https://github.com/Solendris/Universal_Autoclicker.git
   cd Universal_Autoclicker

## Option 2: Windows Executable (No Setup Required)

Navigate to the `dist/` folder and run the application: **dist/UniversalAutoClicker.exe**

**No Python installation required** — ready to use instantly on Windows!

---

## How It Works

- Records **mouse clicks** and **keyboard input** (press + release)
- Stores actions with exact timestamps using `mouse`, `keyboard`, and `pyautogui`
- Playback precisely mimics recorded actions including real-time delays
- Optionally, you can **save actions as `.json` macros** and reuse them anytime

---

## Playback Logic

- Repeats recorded actions in order
- Supports:
  - Fixed number of repetitions (e.g., 5x)
  - Infinite loop mode (checkbox)
- Playback can be stopped **immediately** by pressing the **`S` key**

---

## User Interface Overview

| Button / Field      | Function Description                                 |
|---------------------|------------------------------------------------------|
| **Start Recording** | Begins capturing mouse and keyboard input            |
| **Stop Recording**  | Ends the recording session                           |
| **Play Actions**    | Replays the currently recorded (or loaded) actions   |
| **Save to JSON**    | Saves recorded macro to a `.json` file               |
| **Load from JSON**  | Loads a previously saved `.json` macro               |
| **Repetitions**     | Field to define how many times the macro will run    |
| **Infinite Mode**   | Checkbox to run the macro infinitely                 |
| **Status / Cycle**  | Displays current status and current loop count       |

---

## Project Structure
```
Universal_Autoclicker/
├── main.py # GUI + recording + playback logic
├── requirements.txt # Required Python libraries
├── Logs/ # Auto-generated logs folder (by date)
├── dist/ # Contains the compiled .exe application
│ └── UniversalAutoClicker.exe # Ready-to-run Windows executable
└── *.json # Optional: saved user macros
```

---

## Logging

Each session creates a log file in the `Logs/` folder, named using the current date: (example) Logs/19_06_2025.log

---

### Logs include:
- Recording & playback start/stop events  
- Macro saving and loading status  
- Any runtime errors or exceptions

---

## Safety First

- Press **`S`** at any time to **immediately stop** playback
- Playback runs on **background threads**, keeping the GUI responsive
- Ensures you can **always regain control**, even during infinite loops

---

## Example Use Cases

| Scenario        | Description                                        |
|-----------------|----------------------------------------------------|
| **QA Testing**   | Automate click/keyboard sequences for UI testing   |
| **Data Entry**   | Fill repetitive forms or workflows automatically   |
| **Gaming Macros**| Auto-click for grinding or farming tasks           |
| **UX Demos**     | Pre-record keyboard/mouse usage for presentations  |

---

## Roadmap (Ideas)

- [ ] Edit macros visually within the GUI  
- [ ] Timeline view of recorded actions  
- [ ] Adjustable playback speed  
- [ ] CLI mode for headless automation  
- [ ] Add randomness to mouse/key events for realism

---
