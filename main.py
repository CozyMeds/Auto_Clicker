from customtkinter import *
import pyautogui
import time
import keyboard
import threading
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

json_file_path = resource_path("orange.json")

# Theme settings
set_appearance_mode("System")  # auto-switch based on system setting
set_default_color_theme(json_file_path)  # <- use your custom palette

# Mouse Click & Failsafe
def click(x, y, cps):
    try:
        delay = 1 / cps
        while running[0]:
            # FAILSAFE
            if keyboard.is_pressed("F2"):
                status_label.configure(text="❌ F2 pressed: Stopping Program")
                app.after(2000, lambda: status_label.configure(text=""))
                running[0] = False
                return  # safer than sys.exit()
            
            pyautogui.click(x, y)
            time.sleep(delay)
    except pyautogui.FailSafeException:
        status_label.configure(text="Failsafe Triggered: Stopping program")
        app.after(2000, lambda: status_label.configure(text=""))
        running[0] = False

# Submit button action
def on_submit():
    try:
        cps = int(click_widget.get())
        if cps <= 0:
            raise ValueError("CPS must be greater than 0")
        x = int(x_widget.get())
        y = int(y_widget.get())
    except ValueError:
        status_label.configure(text="❌ Please enter a valid number")
        app.after(2000, lambda: status_label.configure(text=""))
        return

    status_label.configure(text=f"✅ Clicking at ({x}, {y}) with {cps} CPS")
    app.after(4000, lambda: status_label.configure(text=""))
    running[0] = True
    
    # Run in a thread
    threading.Thread(target=click, args=(x, y, cps), daemon=True).start()

# Get & display mouse coordinates
def mouse_coords():
    x, y = pyautogui.position()
    mouse_label.configure(text=f"Mouse: ({x}, {y})")
    app.after(100, mouse_coords)

# Main App Body 
app = CTk()
app.title("Auto Clicker")
app.geometry("320x300")
app.resizable(False, False)

# Frames
input_frame = CTkFrame(master=app)
input_frame.pack(fill="x", padx=10, pady=10)

status_frame = CTkFrame(master=app)
status_frame.pack(fill="x", padx=10, pady=10)

# CPS Input
CTkLabel(input_frame, text="Clicks Per Second:").grid(
    row=0, column=0, sticky="w", padx=(10, 5), pady=5
)
click_widget = CTkEntry(input_frame, width=120)
click_widget.grid(row=0, column=1, padx=(5, 10), pady=5)

# X & Y Inputs
CTkLabel(input_frame, text="X Coordinates:").grid(
    row=1, column=0, sticky="w", padx=(10, 5), pady=5
)
x_widget = CTkEntry(input_frame, width=120)
x_widget.grid(row=1, column=1, padx=(5, 10), pady=5)

CTkLabel(input_frame, text="Y Coordinates:").grid(
    row=2, column=0, sticky="w", padx=(10, 5), pady=5
)
y_widget = CTkEntry(input_frame, width=120)
y_widget.grid(row=2, column=1, padx=(5, 10), pady=5)

# Submit Button
CTkButton(input_frame, text="Submit", command=on_submit).grid(
    row=3, column=1, pady=15, sticky="ew", padx=(5, 10)
)

# Status
status_label = CTkLabel(status_frame, text="", font=("Segoe UI", 12))
status_label.pack(pady=5)

# Mouse Coords
mouse_label = CTkLabel(status_frame, text="Mouse: (0, 0)", font=("Segoe UI", 12))
mouse_label.pack(pady=15)

running = [False]
mouse_coords()

app.mainloop()