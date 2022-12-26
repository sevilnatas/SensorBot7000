import re
import time
import math
import datetime
import pyautogui
import tkinter as tk
from tkinter import Tk, Frame, Label, Button, filedialog, ttk
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
testimage = tk.Label()
root.geometry("1200x400")

# Determines if the user is currently traveling. Used to break traveling_loop when Stop Button is clicked
traveling_running = False

# Original survey starting coordinates, read from the Scan Mission file
scan_origin_x = None
scan_origin_y = None 
scan_origin_z = None 

# Coordinates for the survey find location, read from survey image file, file name, supplied by the Analyzer7000.
scan_dest_x = None
scan_dest_y = None
scan_dest_z = None

# Coordinates offset based on difference between 'survey_dest_' and 'survey_origin_' (scan_dest_ - scan_origin_ = 'scan_offset_')
scan_offset_x = None
scan_offset_y = None
scan_offset_z = None

# Travellers seek starting point coordinates, use results of a /showlocation command
seek_start_x = None
seek_start_y = None
seek_start_z = None

# Travellers calculated seek destination coordinates
# Use the 'start_offset_' added to the 'scan_offset_' to calculate the 'seek_dest_'
seek_dest_x = None
seek_dest_y = None
seek_dest_z = None

# Traveller's current coordinates, populated by the /showlocation command, every pass through the loop and used to calculate the
# the arrow image rotatation
seek_current_x = None
seek_current_y = None
seek_current_z = None

# Instantiate the arrow image
arrow_image = Image.open('images\DirectionArrow2.png')

# Rotate the image by the initial angle
rotated_image = arrow_image.rotate(0) # starting with the image rotated 0 degress

# Convert the rotated image to a PhotoImage object
direction_arrow_image = ImageTk.PhotoImage(rotated_image)

# Set up a 2.5 second pause after each PyAutoGUI call
pyautogui.PAUSE = .5

# Get a handle to the Notepad window.
#SC_window = pyautogui.getWindowsWithTitle("Star Citizen")[0]

# Click on the Star Citizen window to make it active.
# pyautogui.click(SC_window.left + 10, SC_window.top + 10)

{ # Psuedo Code for Ground to Ground Seek Missions (Need to add Space to Ground, Space to Space, and Ground to Space)
# ??????? Research what r_displayinfo is. It may be useful
# User finds Scan Mission starting coordinates and positions ship on those coordinates
# User browses for Scan Mission Plan file to get Scan Mission starting coordinates
# User Selects Seek Mission File and loads list of Seek target coordinates they compiled by analyzing the Scan Mission image files
# Locator7000 takes first target and calculates offset between the Scan Mission starting coordinates and the Seek Mission Target coordinates
# Locator7000 gets user's current location using /showlocation command
# Locator7000 uses the Calculated Offset to dirive the Seek Mission Destination coordinates (Might think about calculating all Seek Mission Target   Destinations so the user does not have to worry about being overly percise about their movements, during the Seek mission)
# Locator7000 calculates rotation of arrow and sets image rotation
# Locator7000 calculates Travel Distance and displays it on the screen
# User clicks the Start button and Locator7000 starts to loop through updating users position, distance remaining (x,y), direction
    # Check that the user has not hit the stop button
    # Get users current coordinates with /showlocation
    # Re-calculate distance remaining (x,y) with Seek Mission Target Coordinates - Current Coordinates
    # Re-calculate rotation of arrow image to indicate direction
    # Rinse Repeat until user clicks Stop button
#Old Psuedo Code
# XX User clicks the Start button
# Get destination address from user input textboxes
# App flies user up 5m and forward 5m and forward 
# Set the cordinates in the read-only distance away textboxes
# Calculate if the location cordinates are going up or down (+ or -) for each axis
# Set varible for expected direction for each axis 
# Start loop of getting current location and calculating distances
    # Loop check variable to see if the user has clicked the stop button
    # Get current location using /showlocation command in chat
    # Split the resulting coordinates with the 'splitCoordinates()' function, assigning coordinates to the x,y,z current variable
    # Do the math to calculate distance away in the each axis, using the expected direction variables
    # display distance away in exch axis, to user
    # Update the up/down arrow icon for the z-axis
    # Update the progress bar with amount of distance away for the z-axis
    # Update the left/right arrow icon for the x-axis
    # Update the progress bar with amount of distance away for the y-axis
    # Update the green/red light icon for the y-axis
    # Update the progress bar with amount of distance away for the x-axis
    # Depending upi how fast this loop repeats and the effect on the GUI, might want to add a pause here
# User clicks the Stop button and changes the variable to False so loop will stop
}

{# Notes:
# Decrease Throttle - F9
# Decrease Throttle to Min - F9 (DOUBLE TAP)
# Increase Throttle - F10
# Increase Throttle to Max - F10 (DOUBLE TAP)
}

# Re-centering HUD/retical "z" or open and close mobiglass

# Get the Mission Plan from the file created by the Analyzer7000 app
def get_mission_list():
    # Open a file selection dialog
    file_path = tk.filedialog.askopenfilename()

    # Read the contents of the file
    with open(file_path, 'r') as f:
        contents = f.read()
    
    # Open the file for reading
    with open('data.txt', 'r') as f:
        # Read all the lines of the file into a list
        lines = f.readlines()

    # Loop through each line in the list
    for line in lines:
        # Split the line on the '|' character to get a list of the fields
        fields = line.split('|')
        # Access the fields using indexing, e.g. fields[0] is the first field, fields[1] is the second, etc.
        field1 = fields[0]
        field2 = fields[1]
        # ...

    # Extract the x and y values from the text using a regular expression
    # Need to expand this from 
    match = re.search(r'x:(\d+\.\d+) y:(\d+\.\d+)', contents)
    if match:
        # scan_origin_x = None
        # scan_origin_y = None 
        # scan_origin_z = None 
        scan_origin_x = float(match.group(1))
        scan_origin_y = float(match.group(2))

# ChatBot code for a collapsible frame, pasted here until ready to use. Probably should go down in the UI section.
def mission_list_frame():
    # Create a root window
    root = tk.Tk()

    # Create a ttk.Notebook widget
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # Create a frame and add it to the notebook
    frame1 = ttk.Frame(notebook)
    notebook.add(frame1, text='Frame 1')

    # Create a second frame and add it to the notebook
    frame2 = ttk.Frame(notebook)
    notebook.add(frame2, text='Frame 2')

    # Run the Tkinter event loop
    root.mainloop()


def get_current_location():
    # paste /showlocation in the chat and have result copied to clipboard
    pyautogui.press("enter")
    pyautogui.typewrite("/showlocation")
    pyautogui.press("enter")

    # Copy the value in the clipboard to a variable.
    coordinates = pyautogui.clipboard.copy()
    return coordinates

# Get the Sensor7000 Scan Mission Plan file
# Use the "C:\Users\sevil\Documents\Scan Mission Files\Scan Mission Plan 1" test file
def get_scan_mission_start():
    # Open a file selection dialog
    file_path = tk.filedialog.askopenfilename()

    # Read the contents of the file
    with open(file_path, 'r') as f:
        contents = f.read()

    # Extract the x and y values from the text using a regular expression
    # Need to expand this from 
    match = re.search(r'x:(\d+\.\d+) y:(\d+\.\d+)', contents)
    if match:
        # scan_origin_x = None
        # scan_origin_y = None 
        # scan_origin_z = None 
        scan_origin_x = float(match.group(1))
        scan_origin_y = float(match.group(2))

# Get the Analyzer7000 Seek Mission Plan file
# Use the "C:\Users\sevil\Documents\Seek Mission Files\Seek Mission Plan 1" test file
def get_seek_mission_dest():
    # Open a file selection dialog
    file_path = tk.filedialog.askopenfilename()

    # Read the contents of the file
    with open(file_path, 'r') as f:
        contents = f.read()

    # Extract the x and y values from the text using a regular expression
    # Need to expand this from 
    match = re.search(r'x:(\d+\.\d+) y:(\d+\.\d+)', contents)
    if match:
        # scan_dest_x = None
        # scan_dest_y = None
        # scan_dest_z = None
        scan_dest_x = float(match.group(1))
        scan_dest_y = float(match.group(2))

# Splits the coordinate string into x,y,x coordinates, that is supplied by the /showlocation command.
def splitCoordinates(coordinateString):

    my_string = coordinateString
    
    parts = re.split(":", my_string)
    del parts[1]
    del parts[0]

    x = parts[0]
    y = parts[1]
    z = parts[2]

    print(x)  # should print '22476400359.992214 y'
    print(y)  # should print '37090941017.974251 z'
    print(z)  # should print '-13606.190188'

    x.strip(" y")
    y.strip(" z")

    coordinateArray = []
    coordinateArray.append(x)
    coordinateArray.append(y)
    coordinateArray.append(z)

    return coordinateArray

def remaining_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def update_arrow_rotation():
    # seek_current_x = x1 => Notes from GPTchat
    # seek_current_y = y1 => Notes from GPTchat
    # seek_current_z = z1 => Notes from GPTchat

    # seek_dest_x = x2 => Notes from GPTchat
    # seek_dest_y = y2 => Notes from GPTchat
    # seek_dest_z = z2 => Notes from GPTchat

    # Calculate the angle in radians
    angle = math.atan2(seek_dest_y - seek_current_y, seek_dest_x - seek_current_x) # angle = math.atan2(y2 - y1, x2 - x1)

    # Calculate the angle in degrees
    arrow_angle_degrees = angle * 180 / math.pi

    # Rotate the image by the calculated angle
    rotated_image = arrow_image.rotate(arrow_angle_degrees)

    # Convert the rotated image to a PhotoImage object
    photo_image = ImageTk.PhotoImage(rotated_image)

    # Update the image displayed by the label
    direction_arrow_label.configure(image=photo_image)
    direction_arrow_label.image = photo_image

# The Loop function that controls the users movement to their destination
def traveling_loop():
    if traveling_running:
        if False: # 
            messagebox.showinfo("Altitude Warning", "Your altitude seems not to have changed since our last warning. We STRONGLY suggest raising your ship to a safe altitude, prior to leaving. If you have gotten this warning in error, we deeply apologize for the incovenience.")
        elif True:
            messagebox.showinfo("Altitude Warning", "Your altitude seems not to have changed since our last warning. We STRONGLY suggest raising your ship to a safe altitude, prior to leaving. If you have gotten this warning in error, we deeply apologize for the incovenience.")
        else:
            messagebox.showinfo("Altitude Warning", "Your altitude seems not to have changed since our last warning. We STRONGLY suggest raising your ship to a safe altitude, prior to leaving. If you have gotten this warning in error, we deeply apologize for the incovenience.")
        distance = distance(125, 50, 350, 75)
        print(distance)  # prints 225.98...



# Start Button Event
def start_traveling():
    if not traveling_running:
        # Start the keystroke loop.
        traveling_running = True
        traveling_loop()

        # Direct user to raise up to a safe altitude, prior to the ship
        messagebox.showinfo("Altitude Warning", "Please use the <SPACEBAR> to raise your ship to a safe altitude, before we depart. Locator7000 does not control the altitude of your ship for you. It is your responsibility fly at a safe altitude.")

        # Click on the Star Citizen window to make it active.
        #pyautogui.click(SC_window.left + 10, SC_window.top + 10)

        x_entry["state"] = "readonly"
        y_entry["state"] = "readonly"
        z_entry["state"] = "readonly"

        # Assign Destination coordinates to variables
        destination_x = x_entry.get()
        destination_y = y_entry.get()
        destination_z = z_entry.get()

# Stop Button Event
def stop_traveling():
    # Click on the Star Citizen window to make it active.
    #pyautogui.click(SC_window.left + 10, SC_window.top + 10)

    x_entry["state"] = "normal"
    y_entry["state"] = "normal"
    z_entry["state"] = "normal"

currentLocal = splitCoordinates("Coordinates: x:22476400359.992214 y:37090941017.974251 z:-13606.190188")

# Create the GUI.
frame = tk.Frame(root)
frame.pack()

# Need to finish this with the Chat code
direction_arrow_label = tk.Label(frame, image=direction_arrow_image)
direction_arrow_label.grid(row=7, column=0, columnspan=6)

# Create the labels
x_label = tk.Label(frame, text="X-Axis")
y_label = tk.Label(frame, text="Y-Axis")
z_label = tk.Label(frame, text="Z-Axis")

# Create the OM Distance labels
OM1_label = tk.Label(frame, text="OM-1 Distance")
OM2_label = tk.Label(frame, text="OM-2 Distance")
OM3_label = tk.Label(frame, text="OM-3 Distance")
OM4_label = tk.Label(frame, text="OM-4 Distance")
OM5_label = tk.Label(frame, text="OM-5 Distance")
OM6_label = tk.Label(frame, text="OM-6 Distance")

# Create the Compass Heading label
compass_heading_label = tk.Label(frame, text="Compass Heading")

# Add Destination Coordinates label to the UI
x_label.grid(row=1, column=1, columnspan=2)
y_label.grid(row=1, column=2, columnspan=2)
z_label.grid(row=1, column=3, columnspan=2)

# Add OM Distance label to the UI
OM1_label.grid(row=3, column=0)
OM2_label.grid(row=3, column=1)
OM3_label.grid(row=3, column=2)
OM4_label.grid(row=3, column=3)
OM5_label.grid(row=3, column=4)
OM6_label.grid(row=3, column=5)

# Add Compass Heading label to the UI
compass_heading_label.grid(row=5, column=0, columnspan=6)

# Add the OM Distances textboxes to the UI

# Create the Destination Coordinates textboxes
# The scan location you want to go mine
x_entry = tk.Entry(frame)
y_entry = tk.Entry(frame)
z_entry = tk.Entry(frame)

# Create the Compass Heading textbox
compass_heading_entry = tk.Entry(frame)

# Create the OM Distance textboxes
# The distances from the 6 OM (Orbital Markers)
OM1_entry = tk.Entry(frame)
OM2_entry = tk.Entry(frame)
OM3_entry = tk.Entry(frame)
OM4_entry = tk.Entry(frame)
OM5_entry = tk.Entry(frame)
OM6_entry = tk.Entry(frame)

# Add the Destination Coordinate textboxes to the UI
x_entry.grid(row=2, column=1, padx=4, columnspan=2)
y_entry.grid(row=2, column=2, padx=4, columnspan=2)
z_entry.grid(row=2, column=3, padx=4, columnspan=2)

# Add the OM Distances textboxes to the UI
OM1_entry.grid(row=4, column=0, padx=4)
OM2_entry.grid(row=4, column=1, padx=4)
OM3_entry.grid(row=4, column=2, padx=4)
OM4_entry.grid(row=4, column=3, padx=4)
OM5_entry.grid(row=4, column=4, padx=4)
OM6_entry.grid(row=4, column=5, padx=4)

# Add the Destination Coordinate textboxes to the UI
compass_heading_entry.grid(row=6, column=0, columnspan=6)

# Create the read-only textbox
# current_location_textbox = tk.Text(frame)
# current_location_textbox.pack()

location_label = tk.Label(frame, text="Distance Yet to Travel")
location_label.grid(row=8, column=0, columnspan=6, pady=10)

current_location_x = tk.Label(frame, text="x: " + currentLocal[0].strip(" yz"))
current_location_x.grid(row=9, column=1, pady=2, columnspan=2)

current_location_y = tk.Label(frame, text="y: " + currentLocal[1].strip(" yz"))
current_location_y.grid(row=9, column=2, pady=2, columnspan=2)

current_location_z = tk.Label(frame, text="z: " + currentLocal[2].strip(" yz"))
current_location_z.grid(row=9, column=3, pady=2, columnspan=2)


start_button = tk.Button(frame, text="Start", width=10, command=start_traveling) # tk.Button(frame, text="Start", command=start_keystrokes)
start_button.grid(row=10, column=5, pady=3)

stop_button = tk.Button(frame, text="Stop", width=10) # tk.Button(frame, text="Stop", command=stop_keystrokes)
stop_button.grid(row=10, column=4, pady=3)

load_scan_start = tk.Button(frame, text="Load Scan Start", width=10, command=get_scan_mission_start) # 
load_scan_start.grid(row=10, column=1, pady=3)

load_seek_destination = tk.Button(frame, text="Load Seek Destination", width=10, command=get_seek_mission_dest) # 
load_seek_destination.grid(row=10, column=0, pady=3)

# Start the Tkinter event loop.
root.mainloop()