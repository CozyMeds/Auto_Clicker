from pyautogui import *
import pyautogui
import time
import keyboard
import sys
import tkinter as tk
import threading

#Mouse Click & Failsafe
def click(x, y, cps):
    try:
        delay = 1 / cps #Convert CPS to delay time
        while True:
            # FAILSAFE
            if keyboard.is_pressed("F2"):
                status_label.config(text="❌ F2 pressed: Stopping Program", fg="red")
                root.after(2000, lambda: status_label.config(text=""))
                sys.exit()
            
            pyautogui.click(x, y)
            time.sleep(delay)
    except pyautogui.FailSafeException:
        status_label.config(text="Failsafe Triggered: Stopping program", fg="red")
        root.after(2000, lambda: status_label.config(text=""))
        sys.exit()

#Submit button action
def on_submit():
    try:
        cps = int(click_widget.get())
        if cps <= 0:
            raise ValueError("CPS must be greater than 0")
        x = int(x_widget.get())
        y = int(y_widget.get())
    except ValueError:
        status_label.config(text="❌ Please enter valid numbers!", fg="red")
        root.after(2000, lambda: status_label.config(text=""))
        return

    status_label.config(text=f"✅ Clicking at ({x}, {y})", fg="green")
    root.after(2000, lambda: status_label.config(text=""))

    # Run the autoclicker in a separate thread so it doesn't freeze the GUI
    threading.Thread(target=click, args=(x, y, cps), daemon=True).start()

#Get & display mouse coordinates
def mouse_coords():
    x, y = pyautogui.position()
    
    mouse_label.config(text=f"Mouse: ({x}, {y})", fg="green")
    root.after(100, mouse_coords)
    

root = tk.Tk()
root.title("Auto Clicker")
root.geometry("300x300")

tk.Label(root, text="Clicks per second:").pack(pady=5)
click_widget = tk.Entry(root)
click_widget.pack(pady=5)

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