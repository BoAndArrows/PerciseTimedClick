import pyautogui
import time
import datetime
import tkinter as tk
from tkinter import messagebox
import threading
import keyboard

# Global flag to control clicking
clicking = False
hotkey_button = "ctrl+~"

# Function to perform clicking at the specified time
def click_at_target_time(target_second, target_millisecond):
    global clicking
    update_status_label("Waiting to Click")

    while clicking:
        # Get the current time
        current_time = datetime.datetime.now()

        # Extract the current second and millisecond
        current_second = current_time.second
        current_millisecond = current_time.microsecond // 1000  # Convert microseconds to milliseconds

        # Check if current time matches the target time
        if current_second == target_second and current_millisecond == target_millisecond:
            print(f"Target time reached! Clicked at {current_second}s:{round(current_time.microsecond//1000, 1)}ms")
            pyautogui.click()  # Perform the click
            update_status_label("Click Triggered")
            break  # Exit the loop after clicking once

        # Sleep for a small amount to avoid high CPU usage
        time.sleep(0.01)

# Function to start the clicker process from GUI inputs
def start_clicking():
    global clicking
    try:
        # Get user input from the entry fields or radio button selection
        if selected_timestamp.get() == "Custom Time":
            target_second = int(second_entry.get())
            target_millisecond = int(ms_entry.get())
        else:
            # Extract the second and millisecond from the selected timestamp
            selected_time = selected_timestamp.get()
            target_second, target_millisecond = map(int, selected_time.split(":"))
        
        if target_second < 0 or target_second > 59:
            raise ValueError("Second must be between 0 and 59.")
        if target_millisecond < 0 or target_millisecond > 999:
            raise ValueError("Millisecond must be between 0 and 999.")
        
        clicking = True  # Set the clicking flag to True

        # Start the clicking process in a separate thread to not block the GUI
        click_thread = threading.Thread(target=click_at_target_time, args=(target_second, target_millisecond))
        click_thread.daemon = True
        click_thread.start()

    except ValueError as e:
        messagebox.showerror("Invalid Input", f"Error: {e}")

# Function to stop the clicking process
def stop_clicking():
    global clicking
    clicking = False
    update_status_label("Stopped Waiting")


def hotkey_process():
    global clicking
    if not clicking:
        start_clicking()
    else:
        stop_clicking()

# Hotkey listener for start and stop
def listen_for_hotkeys():
    global hotkey_button
    keyboard.add_hotkey(hotkey_button, hotkey_process)
    keyboard.wait()

def update_hotkey():
    global hotkey_button
    keyboard.clear_all_hotkeys()
    hotkey_button = hotkey_entry.get()

def update_status_label(new_status):
    current_status_label.config(text=f"Status: {new_status}")
    root.update_idletasks()  # Ensure the UI gets updated immediately

# Function to unfocus entry boxes when clicking elsewhere (outside entry boxes)
def unfocus_entry(event):
    # Check if the click was inside the entry box
    if event.widget not in [second_entry, ms_entry, hotkey_entry]:
        # If the click was outside the Entry widgets, unfocus the Entry widgets
        root.focus_set()  # Move the focus to the root window


# Set up the main window
root = tk.Tk()
root.title("Time Precise Clicker")
root.geometry("400x300")

# Get the screen dimensions to set the window size based on display
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.3)  # 50% of the screen width
window_height = int(screen_height * 0.5)  # 30% of the screen height
x_offset = (screen_width - window_width) // 2
y_offset = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

# Create GUI elements using grid layout

# Target time label
target_time_label = tk.Label(root, text="Set Target Time (Seconds and Milliseconds) or choose from preset timestamps")
target_time_label.grid(row=0, column=0, columnspan=2, pady=10)

# Create radio buttons for predefined timestamps
selected_timestamp = tk.StringVar(value="Custom Time")

time_stamps = [
    ("00:33"),
    ("15:33"),
    ("30:33"),
    ("45:33")
]

row = 1  # Start from row 1 for radio buttons
for time_stamp in time_stamps:
    time_str = time_stamp
    radio_button = tk.Radiobutton(root, text=f"Time: {time_str}", variable=selected_timestamp, value=time_str)
    radio_button.grid(row=row, column=0, sticky="w")
    row += 1

# Radio button for "Custom Time" option
radio_button_custom = tk.Radiobutton(root, text="Custom Time", variable=selected_timestamp, value="Custom Time")
radio_button_custom.grid(row=row, column=0, sticky="w", pady=5)
row += 1

# Entry fields for custom second and millisecond if "Custom Time" is selected
second_label = tk.Label(root, text="Second (0-59):")
second_label.grid(row=row, column=0, sticky="e", padx=5)
second_entry = tk.Entry(root)
second_entry.grid(row=row, column=1, padx=5)
row += 1

ms_label = tk.Label(root, text="Millisecond (0-999):")
ms_label.grid(row=row, column=0, sticky="e", padx=5)
ms_entry = tk.Entry(root)
ms_entry.grid(row=row, column=1, padx=5)
row += 1

# Bind the mouse click event to unfocus the entry widgets if clicked outside
root.bind("<Button-1>", unfocus_entry)

hotkey_entry_label = tk.Label(root, text="Start/Stop Hotkey (e.g., 'ctrl+p' or 'p'):")
hotkey_entry_label.grid(row=row, column=0, padx = 5, pady=5)

hotkey_entry = tk.Entry(root)
hotkey_entry.grid(row=row, column=1, padx = 5, pady=5)

hotkey_set_button = tk.Button(root, text="Set Hotkey", command = update_hotkey)
hotkey_set_button.grid(row=row, column=2, padx = 5, pady = 5)

row += 1

# Start clicking button
start_button = tk.Button(root, text="Start Clicking", command=start_clicking)
start_button.grid(row=row, column=0, columnspan=2, pady=20)
row += 1

current_status_label = tk.Label(root, text="NOT Clicking")
current_status_label.grid(row=row, column= 0, columnspan=2, pady=10)

# Start a background thread for listening to hotkeys
hotkey_thread = threading.Thread(target=listen_for_hotkeys, daemon=True)
hotkey_thread.start()

# Start the GUI loop
root.mainloop()
