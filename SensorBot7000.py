import time
import datetime
import pyautogui
from tkinter import *

# Coordinates from /showlocation are coordinates of the Solar System, not the moon/planet, so the fact that the moon/planet rotating
# so when starting a scannoing mission, user will be required to capture OM distances, /showlocation coordinates and the compass reading.
# When user uses Locator7000, they must be as accurate as possible to locate themselves on the Scan Mission starting point, OM distance, and then
# the /showlocation coordinates will be used as offsets from the starting point to the desired destination. If the starting point coords are
# x100.00, y100.00, and the first scan finding destination is x200.00, y150.00, then Locator7000 will have the user travel x100.00, y50, from the
# starting point, regardless of the user's current /showlocation coordinates.

# Create the root window.
root = Tk()

# Set up a 2.5 second pause after each PyAutoGUI call
pyautogui.PAUSE = .5

# This variable will be used to track whether the keystroke loop is running or not.
keystrokes_running = False
travel_direction = "w" # Direction of scan pass - forward(w) or backward(s)
hold = 5 # Number of seconds to move left at end of a scan pass

# Get a handle to the Star Citizen window.
SC_window = pyautogui.getWindowsWithTitle("Star Citizen")[0]

# TESTING - Using Notepad to test outside of 
# SC_window = pyautogui.getWindowsWithTitle("Untitled - Notepad")[0]

# Click on the Star Citizen window to make it active.
pyautogui.click(SC_window.left + 10, SC_window.top + 10)

# Send the keystrokes "Hello, world!" to the Notepad window.
#pyautogui.typewrite("Hello, world!", interval=0.1)

# This function will be called when the "Start" button is clicked.
def start_keystrokes():
    global keystrokes_running
    if not keystrokes_running:
        # Start the keystroke loop.
        keystrokes_running = True
        keystroke_loop()

# This function will be called when the "Stop" button is clicked.
def stop_keystrokes():
    global keystrokes_running
    keystrokes_running = "w"

def show_location():
    # paste /showlocation in the chat and have result copied to clipboard
    pyautogui.press("enter")
    pyautogui.typewrite("/showlocation")
    pyautogui.press("enter")
    # Copy the value in the clipboard to a variable.
    coordinates = pyautogui.clipboard.copy()
    return coordinates

# Write the Scan Mission file
def create_scan_mission_file():
    # Get the current date and time
    now = datetime.now()
    # Format the date and time to include only the date and time, not the timezone
    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
    # Use the date and time as the file name
    file_name = "ScanMissionLog_" + date_time
    #  Get the start location from the Show Location function.
    mission_start_location = show_location()
    # Open the file in write mode and write a line of text to it
    with open("C:\\scanImages\\" + file_name + ".txt", "w") as file:
        file.write(mission_start_location)

# Write the /showlocation and ping/screenshot to image file, to mission folder
def create_scan_file():
    # Stub for the /showlocation, ping, screenshot write to file
    # Ping to show boxes
    pyautogui.press("tab")

    # Take a screenshot of the window.
    screenshot = pyautogui.screenshot()

    # Get the coordinates from the Show Location function.
    coordinates = show_location()

    # Save the screenshot to a file on the C drive.
    screenshot.save("C:\\scanImages\\" + travel_direction + "_" + coordinates + "_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".png")

# This is the main keystroke loop. It will run until the keystrokes_running variable is set to False.
def keystroke_loop():
    # Begin Scan Mission by creating a text file with the starting location
    create_scan_mission_file()

    # Do 100 ping forward, move left 5 seconds, do 100 pings backwards, move left 3 seconds, rinse repeat
    for I in range(100):
        # Move in the direction appropriate for this Scan Pass
        pyautogui.keyDown(travel_direction)

        # Perform the operations 100 times.
        for i in range(100):
            # Log the scan
            create_scan_file()

            # Pause for 2 seconds.
            time.sleep(2)

            # Break out of loop if 
            if keystroke_loop == False:
                break

        if  travel_direction == 'w':
            pyautogui.keyUp("w")
            travel_direction = 's'
        else:
            pyautogui.keyUp("s")
            travel_direction = 'w'
        
        # Break out of loop if 
        if keystroke_loop == False:
            break
        
        with pyautogui.hold("a"):
            pyautogui.sleep(hold)
        

# Create the GUI.
frame = Frame(root)
frame.pack()

start_button = Button(frame, text="Start", command=start_keystrokes)
start_button.pack(side=LEFT)

stop_button = Button(frame, text="Stop", command=stop_keystrokes)
stop_button.pack(side=LEFT)

# Start the Tkinter event loop.
root.mainloop()