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

def pan_canvas(event):
    # Compute the distance moved by the mouse
    globals.canvas.scan_dragto(event.x, event.y, gain=1)


# Bind mouse events to canvas for panning
globals.canvas.bind("<ButtonPress-2>", start_pan)  # Mouse wheel click pressed
globals.canvas.bind("<B2-Motion>", pan_canvas)     # Mouse wheel clicked and dragged


# Create CrosswordSquare instances for each square in the grid
globals.grid = [[CrosswordSquare(globals.canvas, row, col, globals.grid_size) for col in range(globals.cols)] for row in range(globals.rows)]

# Configure the Tkinter window to be fullscreen
globals.root.attributes("-fullscreen", False)

# Main Tkinter event loop
globals.root.mainloop()
