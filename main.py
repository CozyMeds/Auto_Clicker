from pyautogui import *
import pyautogui
import time
import keyboard
import sys
import tkinter as tk
from tkinter import ttk
import threading

#Mouse Click & Failsafe
def click(x, y, cps):
    try:
        delay = 1 / cps #Convert CPS to delay time
        while running[0]:
            # FAILSAFE
            if keyboard.is_pressed("F2"):
                status_label.config(text="❌ F2 pressed: Stopping Program", foreground="red")
                root.after(2000, lambda: status_label.config(text=""))
                running[0] = False
                sys.exit()
            
            pyautogui.click(x, y)
            time.sleep(delay)
    except pyautogui.FailSafeException:
        status_label.config(text="Failsafe Triggered: Stopping program", foreground="red")
        root.after(2000, lambda: status_label.config(text=""))
        running[0] = False
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
        status_label.config(text="❌ Please enter a valid number", foreground="red")
        root.after(2000, lambda: status_label.config(text=""))
        return

    status_label.config(text=f"✅ Clicking at ({x}, {y}) with {cps} CPS", foreground="green")
    root.after(4000, lambda: status_label.config(text=""))
    running[0] = True
    
    # Run the autoclicker in a separate thread so it doesn't freeze the GUI
    threading.Thread(target=click, args=(x, y, cps), daemon=True).start()

#Get & display mouse coordinates
def mouse_coords():
    x, y = pyautogui.position()
    
    mouse_label.config(text=f"Mouse: ({x}, {y})", foreground="green")
    root.after(100, mouse_coords)
    

root = tk.Tk()
root.title("Auto Clicker")
root.geometry("300x300")
root.resizable(False, False)

style = ttk.Style(root)
style.configure("TButton", padding=6, relief="flat", font=("Segoe UI", 10))
style.configure("TLabel", font=("Segoe UI", 10))

#Frames
input_frame = ttk.Frame(root, padding=10)
input_frame.pack(fill="x")

status_frame = ttk.Frame(root, padding=10)
status_frame.pack(fill="x")

# CPS input
ttk.Label(input_frame, text="Clicks per second:").grid(row=0, column=0, sticky="w")
click_widget = ttk.Entry(input_frame, width=10)
click_widget.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=3)


# X & Y inputs
ttk.Label(input_frame, text="X Coordinates:").grid(row=1, column=0, sticky="w")
x_widget = ttk.Entry(input_frame, width=10)
x_widget.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=3)

ttk.Label(input_frame, text="Y Coordinates:").grid(row=2, column=0, sticky="w")
y_widget = ttk.Entry(input_frame, width=10)
y_widget.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=3)

# submit Button
ttk.Button(input_frame, text="Submit", command=on_submit).grid(row=3, column=1, pady=15, sticky="ew")

# Status
status_label = ttk.Label(status_frame, text="", font=("Segoe UI", 10))
status_label.pack(pady=5)

# Mouse Coords
mouse_label = ttk.Label(status_frame, text="Mouse: (0, 0)", font=("Segoe UI", 10))
mouse_label.pack(pady=15)

running = [False]
mouse_coords()

root.mainloop()