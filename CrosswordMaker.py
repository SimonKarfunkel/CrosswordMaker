#TODO
#possibility to add index numbers in squares
#Leftclickdrag to make one larger square
#Possibility to split key squares


import tkinter as tk
from CrosswordSquare import CrosswordSquare
import globals
import textfiltering
from tkinter import font


def dummy_command():
    print("This is a dummy command")






# Initialize Tkinter
globals.root = tk.Tk()
globals.root.title("Crossword Maker")
textfiltering.create_sidebar()





#MENU BAR------------------------------------------------------------------------------
# Create a Menu Bar
menu_bar = tk.Menu(globals.root)

# Create File Menu and its items
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=dummy_command)
file_menu.add_command(label="Open", command=dummy_command)
file_menu.add_command(label="Save", command=dummy_command)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=globals.root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create Edit Menu and its items
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cut", command=dummy_command)
edit_menu.add_command(label="Copy", command=dummy_command)
edit_menu.add_command(label="Paste", command=dummy_command)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Create View Menu and its items
view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Open Sidebar", command=textfiltering.open_sidebar)
view_menu.add_command(label="Zoom In", command=dummy_command)
view_menu.add_command(label="Zoom Out", command=dummy_command)
menu_bar.add_cascade(label="View", menu=view_menu)

# Configure the menu bar
globals.root.config(menu=menu_bar)
#END MENU BAR--------------------------------------------------------------------------










# Create a Canvas widget to represent the grid
globals.canvas = tk.Canvas(globals.root, width=globals.cols * globals.grid_size, height=globals.rows * globals.grid_size)
globals.canvas.pack()









def start_pan(event):
    # Record the starting position of the mouse
    globals.canvas.scan_mark(event.x, event.y)
    globals.pan_start = (event.x, event.y)

def pan_canvas(event):
    # Compute the distance moved by the mouse
    globals.canvas.scan_dragto(event.x, event.y, gain=1)


    # Compute the distance moved by the mouse
    x_distance = (event.x) - globals.pan_start[0]
    y_distance = (event.y) - globals.pan_start[1]

    # Update the total panned distance
    globals.pan_offset_x -= x_distance
    globals.pan_offset_y -= y_distance

    # Move all labels along with the canvas
    for row in globals.grid:
        for square in row:
            if square.text_label:
                # Get the relative position of the label within its parent CrosswordSquare canvas
                relative_x = square.col * globals.grid_size + globals.grid_size // 2 - globals.pan_offset_x
                relative_y = square.row * globals.grid_size + globals.grid_size // 2 - globals.pan_offset_y
                
                # Move the label by updating its position within its parent CrosswordSquare canvas
                square.text_label.place(x=relative_x, y=relative_y, anchor="center")

    globals.pan_start = (event.x, event.y)


def stop_pan(event):
    print(globals.pan_offset_x, globals.pan_offset_y)  # You can leave this empty if no action is needed when panning stops

# Bind mouse events to canvas for panning
globals.canvas.bind("<ButtonPress-2>", start_pan)  # Mouse wheel click pressed
globals.canvas.bind("<B2-Motion>", pan_canvas)     # Mouse wheel clicked and dragged
globals.canvas.bind("<ButtonRelease-2>", stop_pan)     # Mouse wheel released


# Create CrosswordSquare instances for each square in the grid
globals.grid = [[CrosswordSquare(globals.canvas, row, col, globals.grid_size) for col in range(globals.cols)] for row in range(globals.rows)]

# Configure the Tkinter window to not be fullscreen
globals.root.attributes("-fullscreen", False)
globals.root.geometry("1024x768")


# Main Tkinter event loop
globals.root.mainloop()
