import pyautogui
import pydirectinput
import time
import datetime

from PIL import Image, ImageTk


import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

from tktooltip import ToolTip

import threading
import keyboard

clicking = False
hotkey = "ctrl+t"
Xtime = False

# Function to perform clicking at the specified time
def click_at_target_time(target_second, target_millisecond):
    global clicking
    root.bell()
    update_status_label("Waiting to Click")

    while clicking:
        # Get the current time
        current_time = datetime.datetime.now()

        # Extract the current second and millisecond
        current_second = current_time.second
        current_millisecond = current_time.microsecond // 1000  # Convert microseconds to milliseconds

        # Debugging: print the current and target times to check the comparison
        print(f"Current Time: {current_second} sec, {current_millisecond} ms")
        print(f"Target Time: {target_second} sec, {target_millisecond} ms")

        # Check if current time matches the target time (with a tolerance of +/- 10 ms)
        if (current_second == target_second) and (target_millisecond == current_millisecond) and not Xtime:
            pydirectinput.click()  # Perform the click
            current_hour = current_time.hour
            current_minute = current_time.minute
            update_status_label(f"Click Triggered at {current_hour}:{current_minute}:{current_second}:{current_millisecond}")
            clicking = False
            break  # Exit the loop after clicking once
        # Sleep for a small amount to avoid high CPU usage
        time.sleep(0.0005)
    
def click_at_X_target(target_second, target_millisecond):
    global clicking
    global Xtime
    root.bell()
    update_status_label("Waiting to Click")

    while(clicking):
        current_time = datetime.datetime.now()
        current_second = str(current_time.second)
        current_millisecond = str((current_time.microsecond)//1000)

        print(f"Current Time: {current_second} sec, {current_millisecond} ms")
        print(f"Target Time: {target_second} sec, {target_millisecond} ms")

        if current_second.endswith(str(target_second)) and current_millisecond.endswith(str(target_millisecond)):
            pydirectinput.click()
            current_hour = current_time.hour
            current_minute = current_time.minute
            update_status_label(f"Click Triggered at {current_hour}:{current_minute}:{current_second}:{current_millisecond}")
            clicking = False
            break  # Exit the loop after clicking once
        # Sleep for a small amount to avoid high CPU usage
        time.sleep(0.0005)
    


# Function to start the clicker process from GUI inputs
def start_clicking():
    global clicking
    global Xtime
    try:
        # Get user input from the entry fields or radio button selection
        timeValue = selected_timestamp.get()
        if timeValue == "Custom Time":
            target_second = int(second_entry.get())
            target_millisecond = int(ms_entry.get())
        elif timeValue == "X Custom Time":
            Xtime = True
            target_second = int(second_entry.get())
            target_millisecond = int(ms_entry.get())
        else:
            # Extract the second and millisecond from the selected timestamp
            target_second, target_millisecond = map(int, timeValue.split(":"))
        
        if target_second < 0 or target_second > 59:
            raise ValueError("Second must be between 0 and 59.")
        if target_millisecond < 0 or target_millisecond > 999:
            raise ValueError("Millisecond must be between 0 and 999.")
        
        clicking = True  # Set the clicking flag to True

        # Start the clicking process in a separate thread to not block the GUI
        click_thread = threading.Thread(target=click_at_X_target, args=(target_second, target_millisecond)) if Xtime else threading.Thread(target=click_at_target_time, args=(target_second, target_millisecond))
        click_thread.daemon = True
        click_thread.start()

    except ValueError as e:
        messagebox.showerror("Something Went Wrong, Invalid Input", f"Error: {e}")

# Function to stop the clicking process
def stop_clicking():
    global clicking
    clicking = False
    update_status_label("Stopped by User")

# Function to update the status label
def update_status_label(new_status):
    current_status_label.config(text=f"Status: {new_status}")
    root.update_idletasks()  # Ensure the UI gets updated immediately

# Function to unfocus entry boxes when clicking elsewhere (outside entry boxes)
def unfocus_entry(event):
    # Check if the click was inside the entry box
    if event.widget not in [second_entry, ms_entry]:
        # If the click was outside the Entry widgets, unfocus the Entry widgets
        root.focus_set()  # Move the focus to the root window

def record_hotkey(event):
    global hotkey_input
    key = event.keysym

    # Stop recording after two keys
    if len(hotkey_input) < 2:
        if key not in hotkey_input:  # Avoid adding duplicates
            hotkey_input.append(key)
            hotkey_label.config(text=f"Hotkey: {' + '.join(hotkey_input)}")

def hotkey_process():
    global clicking
    if not clicking:
        start_clicking()
    else:
        stop_clicking()

def listen_for_hotkeys():
    global hotkey_button
    keyboard.add_hotkey(hotkey, hotkey_process)
    keyboard.wait()



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

#importing assets
info_badge_image_PIL = Image.open("Assets/info_badge_image.png")
#info_badge_image = ImageTk.PhotoImage(info_badge_image_PIL)
small_info_badge_image = info_badge_image_PIL.resize((20, 20), Image.LANCZOS)
info_badge_image = ImageTk.PhotoImage(small_info_badge_image)
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

#Click on every XX Second and XXX Milisecond
radio_button_everyX = tk.Radiobutton(root, text="Click Every XX:XXX", variable=selected_timestamp, value="X Custom Time")
radio_button_everyX.grid(row=row, column=0, sticky="w", pady=5)

everyX_tooltip_icon = tk.Canvas(root, width=20, height=20)
everyX_tooltip_icon.create_image(0, 0, anchor=tk.NW, image=info_badge_image)
everyX_tooltip_icon.grid(row=row, column=0, sticky="e")
ToolTip(everyX_tooltip_icon, msg="This option will click whenever the target second and target millisecond is found, for example\n" \
                                "when you enter 5:21, whenever 5 is seen in the ones place for the second it will click \n" \
                                "i.e 05, 15, 25, 35, etc. same with milliseconds.\n" \
                                "NOTE: if you specify 10 it will only look for 10 or X10, if u want it to click on 0, simply put 0", delay=0.5)
row += 1

# Radio button for "Custom Time" option
radio_button_custom = tk.Radiobutton(root, text="Custom Time", variable=selected_timestamp, value="Custom Time")
radio_button_custom.grid(row=row, column=0, sticky="w")

custom_tooltip_icon = tk.Canvas(root, width=20, height=20)
custom_tooltip_icon.create_image(0, 0, anchor=tk.NW, image=info_badge_image)
custom_tooltip_icon.grid(row=row, column=0, sticky="e")
ToolTip(custom_tooltip_icon, msg="This option will click whenever a specific target second and target millisecond is found\n" \
                                "for example entering 01:330 will click when the second and millisecond on the clock\n" \
                                " matches regardless of minute hour etc", delay=0.5)
row += 1

# Entry fields for custom second and millisecond if "Custom Time" is selected
seconds_tooltip_icon = tk.Canvas(root, width=20, height=20)
seconds_tooltip_icon.create_image(0, 0, anchor=tk.NW, image=info_badge_image)
ToolTip(seconds_tooltip_icon, msg="Enter any reachable second from 0 - 59. \n" \
                                  "IMPORTANT: When selecting custom time make sure the \n" \
                                  "entry is 0 padded. EX. \"05\"")
seconds_tooltip_icon.grid(row=row, column=0, sticky="e")
second_label = tk.Label(root, text="Seconds:")
second_label.grid(row=row, column=0, sticky="w", padx=5)
second_entry = tk.Entry(root)
second_entry.grid(row=row, column=1,sticky="w", padx=5)
row += 1


milli_tooltip_icon = tk.Canvas(root, width=20, height=20)
milli_tooltip_icon.create_image(0, 0, anchor=tk.NW, image=info_badge_image)
ToolTip(milli_tooltip_icon, msg="Enter any reachable second from 0 - 999. \n" \
                                  "IMPORTANT: When selecting custom time make sure the \n" \
                                  "entry is 0 padded. EX. \"003\" or \"023\"")
milli_tooltip_icon.grid(row=row, column=0, sticky="e")
ms_label = tk.Label(root, text="Millisecond:")
ms_label.grid(row=row, column=0, sticky="w", padx=5)
ms_entry = tk.Entry(root)
ms_entry.grid(row=row, column=1, sticky="w", padx=5)
row += 1

# Bind the mouse click event to unfocus the entry widgets if clicked outside
root.bind("<Button-1>", unfocus_entry)

hotkey_label = tk.Label(root, text= f"Current Hotkey: {hotkey}")
hotkey_label.grid(row=row, column=0, pady=5)

set_hotkey_button = tk.Button(root, text="Set Hotkey", command=record_hotkey)
set_hotkey_button.grid(row=row, column=1, pady=5)

row+=1
# Start clicking button
start_button = tk.Button(root, text="Start Clicking", command=start_clicking)
start_button.grid(row=row, column=0, columnspan=2, pady=20)

stop_button = tk.Button(root, text="Stop Clicking", command=stop_clicking)
stop_button.grid(row=row, column=1, columnspan=2, pady=20)
row += 1

# Current status label
current_status_label = tk.Label(root, text="NOT Clicking")
current_status_label.grid(row=row, column=0, columnspan=2, pady=10)

hotkey_thread = threading.Thread(target=listen_for_hotkeys, daemon=True)
hotkey_thread.start()

# Start the GUI loop
root.mainloop()
