import re
import time
import math
import datetime
import pyautogui
import tkinter as tk
from tkinter import Tk, Frame, Label, Button, filedialog, ttk, font, PhotoImage
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
#testimage = tk.Label()
root.geometry("1000x100")

# Determines if the user is currently traveling. Used to break traveling_loop when Stop Button is clicked
global traveling_running
traveling_running = False

global counter
counter = 1

# Direction Variables
# Travellers seek starting point coordinates, use results of a /showlocation command
global seek_start_x # = None
global seek_start_y # = None
global seek_start_z # = None

# Travellers calculated seek destination coordinates
# Use the 'start_offset_' added to the 'scan_offset_' to calculate the 'seek_dest_'
global seek_dest_x # = None
global seek_dest_y # = None
global seek_dest_z # = None

# Traveller's current coordinates, populated by the /showlocation command, every pass through the loop and used to calculate the
# the arrow image rotatation
global seek_current_x # = "XXXXXXX.XX"
seek_current_x = "XXXXXXX.XX"
global seek_current_y # = "XXXXXXX.XX"
seek_current_y = "XXXXXXX.XX"
global seek_current_z # = "XXXXXXX.XX"
seek_current_z = "XXXXXXX.XX"

# Remaining distance between current location and destination
global distance_to_dest
distance_to_dest = "XXXXXX.XX"

# Open the image using the Image module from pillow
large_arrow_image = Image.open('images\DirectionArrow2.png')

# Resize arrow image
resized_arrow = large_arrow_image.resize((50, 50), Image.ANTIALIAS)

# Convert resized image to final format
img_direction_arrow = ImageTk.PhotoImage(resized_arrow)



# Rotate the image by 90 degrees
# pil_arrow_image = pil_arrow_image.rotate(90)


# Set up a 2.5 second pause after each PyAutoGUI call
pyautogui.PAUSE = .5

def rotate_arrow(arrow_image):
    rotating_arrow = ImageTk.getimage(arrow_image) # get the incoming arrow image to be rotated

    # Calculate the angle in radians
    angle = math.atan2(seek_dest_y - seek_current_y, seek_dest_x - seek_current_x) # angle = math.atan2(y2 - y1, x2 - x1)

    # Calculate the angle in degrees
    arrow_angle_degrees = angle * 180 / math.pi

    # Rotate the image by the calculated angle
    rotating_arrow = rotating_arrow.rotate(arrow_angle_degrees)

    # Convert the rotated image to a PhotoImage object
    rotated_arrow = ImageTk.PhotoImage(rotating_arrow)

    # Update the image displayed by the label
    direction_arrow_label.configure(image=rotated_arrow)
    direction_arrow_label.image = rotated_arrow

    return rotated_arrow 

def get_current_location():
    # paste /showlocation in the chat and have result copied to clipboard
    pyautogui.press("enter")
    pyautogui.typewrite("/showlocation")
    pyautogui.press("enter")

    # Copy the value in the clipboard to a variable.
    coordinates = pyautogui.clipboard.copy()
    return coordinates

def start_traveling():
    # Check if the
    global traveling_running
    if not traveling_running:
        # Start the keystroke loop.
        traveling_running = True

        # Get a handle to the Notepad window.
        #SC_window = pyautogui.getWindowsWithTitle("Star Citizen")[0]

        # Get a handle to the Notepad window.
        SC_window = pyautogui.getWindowsWithTitle("Untitled - Notepad")[0]

        # Click on the Star Citizen window to make it active.
        # pyautogui.click(SC_window.left + 10, SC_window.top + 10)

        # Click on the Star Citizen window to make it active.
        pyautogui.click(SC_window.left + 10, SC_window.top + 10)

        # Assign values from Start and Dest Coordinates to variables
        # Assign Destination coordinates to variables
        global seek_dest_x
        global seek_dest_y
        global seek_dest_z
        seek_dest_x = tb_dest_cord_x.get()
        seek_dest_y = tb_dest_cord_y.get()
        seek_dest_z = tb_dest_cord_z.get()

        # Assign Current coordinates to variables
        global seek_current_x
        global seek_current_y
        global seek_current_z
        seek_current_x = tb_start_cord_x.get()
        seek_current_y = tb_start_cord_y.get()
        seek_current_z = tb_start_cord_z.get()

        
        traveling_loop()
            
def stop_traveling():
        global traveling_running
        traveling_running = False

        global counter
        str_count = str(counter)
        print("Done, I did " + str_count + " loops!")
        counter = 1

def traveling_loop():
    global traveling_running
    if traveling_running:
        # Get current coords and assign to, using /showlocation:
            # seek_current_x
            # seek_current_y
            # seek_current_z
        # Calculate rotation angle for the arrow image
        # Rotate Arrow Image
        # Calculate the remaining distance using the current coords and the destination coords
        # Assign the calculated distance value to 
        # Calculate Distance 'lbl_distance'

        print(seek_dest_x)
        print(seek_dest_y)
        print(seek_dest_z)

        print(seek_current_x)
        print(seek_current_y)
        print(seek_current_z)

        global counter
        print(counter)
        counter += 1

        # Uses pyautogui to call /showlocation and copy string to clipboard
        str_show_location = get_current_location()

        # Split the /showlocation into coordinates
        array_current_cords = splitCoordinates(str_show_location)

        # Assign coordinates in array to variables
        seek_current_x = array_current_cords[0]
        seek_current_y = array_current_cords[1]
        seek_current_z = array_current_cords[2]

        # Rotate the arrow based on our current location
        rotate_arrow(img_direction_arrow)

        # Calculate the remaining distance between current location and destination
        str_remaining_distance =  remaining_distance(seek_current_x, seek_current_y, seek_dest_x, seek_dest_y)

        # Update the remaining distance label
        lbl_distance.configure(text=str_remaining_distance)

        root.after(50, traveling_loop)

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


# ***********************Font Styles*****************************

# Create a font object with the desired font type, size, and style
# dist_remaining_font = font.Font(family='Arial', size=36, weight='bold', slant='italic')

# Create a font object with the desired font type, size, and style
font_dist_remaining = font.Font(family='Arial', size=24, weight='bold')

# Create a font object with the desired font type, size, and style
font_cords_entry = font.Font(family='Arial', size=10, weight='bold')

# Create a font object with the desired font type, size, and style
font_curr_coords = font.Font(family='Arial', size=8, weight='normal')

# Create a font object with the desired font type, size, and style
font_start_stop_label = font.Font(family='Arial', size=12, weight='bold')

# ***************************************************************

# Create the GUI.
frame = tk.Frame(root)
frame.pack()


# Column O
# Need to finish this with the Chat code
direction_arrow_label = tk.Label(frame, image=img_direction_arrow)
direction_arrow_label.grid(row=0, column=0, rowspan=2)

# Column 1
# Row 0
lbl_current_cords = tk.Label(frame, text="x: " + seek_current_x + " | y: " + seek_current_y + " | z: " + seek_current_z, font=font_curr_coords)
lbl_current_cords.grid(row=0, column=1, columnspan=2)

# Row 1
lbl_distance = tk.Label(frame, text=distance_to_dest, font=font_dist_remaining)
lbl_distance.grid(row=1, column=1, columnspan=2)

# Column 2
# Row 0

# Row 1

# Column 3
# Row 0
lbl_start_cords = tk.Label(frame, text="START Cords:", font=font_cords_entry)
lbl_start_cords.grid(row=0, column=3)
# Row 1
lbl_stop_cords = tk.Label(frame, text="STOP Cords:", font=font_cords_entry)
lbl_stop_cords.grid(row=1, column=3)

# Column 4
# Row 0
tb_start_cord_x = tk.Entry(frame)
tb_start_cord_x.grid(row=0, column=4)
# Row 1
tb_dest_cord_x = tk.Entry(frame)
tb_dest_cord_x.grid(row=1, column=4)

# Column 5
# Row 0
tb_start_cord_y = tk.Entry(frame)
tb_start_cord_y.grid(row=0, column=5)
# Row 1
tb_dest_cord_y = tk.Entry(frame)
tb_dest_cord_y.grid(row=1, column=5)

# Column 6
# Row 0
tb_start_cord_z = tk.Entry(frame)
tb_start_cord_z.grid(row=0, column=6)
# Row 1
tb_dest_cord_z = tk.Entry(frame)
tb_dest_cord_z.grid(row=1, column=6)

# Column 7
# Row 0
btn_start = tk.Button(frame, text="START", width=8, height=2, font=font_start_stop_label, command=start_traveling)
btn_start.grid(row=0, column=7, rowspan=2)
# Row 1

# Column 8
# Row 0
btn_stop = tk.Button(frame, text="STOP", width=8, height=2, font=font_start_stop_label, command=stop_traveling)
btn_stop.grid(row=0, column=8, rowspan=2)
# Row 1


















# Start the Tkinter event loop.
root.mainloop()