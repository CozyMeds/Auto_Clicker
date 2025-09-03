from pyautogui import *
import pyautogui
import time
import keyboard
import sys
import tkinter as tk
import threading

def click(x, y):
    try:
        while True:
            # FAILSAFE
            if keyboard.is_pressed("F2"):
                status_label.config(text="❌ F2 pressed: Stopping Program", fg="red")
                root.after(2000, lambda: status_label.config(text=""))
                sys.exit()
            
            pyautogui.click(x, y)
            time.sleep(0.1)
    except pyautogui.FailSafeException:
        status_label.config(text="Failsafe Triggered: Stopping program", fg="red")
        root.after(2000, lambda: status_label.config(text=""))
        sys.exit()

def on_submit():
    try:
        x = int(x_widget.get())
        y = int(y_widget.get())
    except ValueError:
        status_label.config(text="❌ Please enter valid numbers!", fg="red")
        root.after(2000, lambda: status_label.config(text=""))
        return

    status_label.config(text=f"✅ Clicking at ({x}, {y})", fg="green")
    root.after(2000, lambda: status_label.config(text=""))

    # Run the autoclicker in a separate thread so it doesn't freeze the GUI
    threading.Thread(target=click, args=(x, y), daemon=True).start()

def mouse_coords():
    x, y = pyautogui.position()
    
    mouse_label.config(text=f"Mouse: ({x}, {y})", fg="green")
    root.after(100, mouse_coords)
    

root = tk.Tk()
root.title("Auto Clicker")
root.geometry("300x300")

tk.Label(root, text="X Coordinates:").pack(pady=5)
x_widget = tk.Entry(root)
x_widget.pack(pady=5)

tk.Label(root, text="Y Coordinates:").pack(pady=5)
y_widget = tk.Entry(root)
y_widget.pack(pady=5)

submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack(pady=10)

mouse_label = tk.Label(root, text="Mouse: (0, 0)")
mouse_label.pack(pady=10)

mouse_coords()

root.mainloop()