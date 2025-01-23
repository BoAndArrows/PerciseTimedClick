import pyautogui
import time
import datetime
import tkinter as tk
from tkinter import messagebox
import threading
import keyboard

# Global flag to control clicking
clicking = False
hotkey_button = "ctrl+s"

# Function to perform clicking at the specified time
def click_at_target_time(target_second, target_millisecond):
    global clicking
    while clicking:
        # Get the current time
        current_time = datetime.datetime.now()

        # Extract the current second and millisecond
        current_second = current_time.second
        current_millisecond = current_time.microsecond // 1000  # Convert microseconds to milliseconds

        # Check if current time matches the target time
        if current_second == target_second and current_millisecond == target_millisecond:
            print(f"Target time reached! Clicking at {target_second}s:{target_millisecond}ms")
            pyautogui.click()  # Perform the click
            messagebox.showinfo("Click Triggered", f"Clicked at {target_second} seconds and {target_millisecond} milliseconds.")
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
    messagebox.showinfo("Stopped", "Clicking process has been stopped.")

def hotkey_process():
    global clicking
    if not clicking:
        start_clicking()
    else:
        stop_clicking()

# Hotkey listener for start and stop
def listen_for_hotkeys():
    global hotkey_button
    keyboard.add_hotkey(hotkey_button, hotkey_process)]
    keyboard.wait()

def update_hotkey():
    global hotkey_button
    keyboard.clear_all_hotkeys()
    hotkey_button = hotkey_entry.get()


# Set up the main window
root = tk.Tk()
root.title("AutoClicker at Specific Time with Hotkeys")
root.geometry("400x300")

# Get the screen dimensions to set the window size based on display
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.4)  # 50% of the screen width
window_height = int(screen_height * 0.4)  # 30% of the screen height
x_offset = (screen_width - window_width) // 2
y_offset = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

# Create GUI elements
target_time_label = tk.Label(root, text="Set Target Time (Seconds and Milliseconds) or choose from preset timestamps")
target_time_label.pack(pady=10)

# Create radio buttons for predefined timestamps
selected_timestamp = tk.StringVar(value="Custom Time")

time_stamps = [
    ("00:33"),
    ("15:33"),
    ("30:33"),
    ("45:33")
]

for time_stamp in time_stamps:
    time_str = time_stamp
    radio_button = tk.Radiobutton(root, text=f"Time: {time_str}", variable=selected_timestamp, value=time_str)
    radio_button.pack()

# Radio button for "Custom Time" option
radio_button_custom = tk.Radiobutton(root, text="Custom Time", variable=selected_timestamp, value="Custom Time")
radio_button_custom.pack(pady=5)

# Entry fields for custom second and millisecond if "Custom Time" is selected
second_label = tk.Label(root, text="Second (0-59):")
second_label.pack(pady=5)

second_entry = tk.Entry(root)
second_entry.pack(pady=5)

ms_label = tk.Label(root, text="Millisecond (0-999):")
ms_label.pack(pady=5)

ms_entry = tk.Entry(root)
ms_entry.pack(pady=5)

# Start clicking button
start_button = tk.Button(root, text="Start Clicking", command=start_clicking)
start_button.pack(pady=20)

hotkey_entry_label = tk.Label(root, text="Start/Stop Hotkey enter in such format: \"Ctrl+P\", or \"P\"")
hot

# Start a background thread for listening to hotkeys
hotkey_thread = threading.Thread(target=listen_for_hotkeys, daemon=True)
hotkey_thread.start()

# Start the GUI loop
root.mainloop()
