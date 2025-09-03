# Auto Clicker

A very basic auto clicker for "clicker" or idle games.

![Overview](./images/overview.png)

## Features

-   Displays real-time mouse coordinates inside the program
-   Allows you to set custom X/Y coordinates for auto-clicking
-   Moves the mouse to the target area and clicks repeatedly
-   Built-in failsafe: press **F2** to stop the program

## Tech Stack

-   Python
-   Tkinter
-   PyAutoGUI

## How It Works

I wanted a simple way to auto-click on specific areas but couldn’t find one I liked.  
Through trial and error, I built this tool to display coordinates, let me set them, and click automatically.

Instead of PyAutoGUI’s built-in failsafe, I implemented a custom **F2 stop key** for reliability.

## Installation & Usage

1. Clone this repository:
    ```bash
    git clone https://github.com/CozyMeds/Auto_Clicker.git
    ```
2. Run the program using:
    ```bash
    ./main.py
    ```