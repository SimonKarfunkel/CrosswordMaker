#TODO
#Leftclickdrag to activate several squares or make one larger
#handle images

import tkinter as tk
from CrosswordSquare import CrosswordSquare
import globals
import textfiltering



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









# Set up grid dimensions
#grid_size = 50
#rows, cols = 50, 50







# Create a Canvas widget to represent the grid
canvas = tk.Canvas(globals.root, width=globals.cols * globals.grid_size, height=globals.rows * globals.grid_size)
canvas.pack()





def start_drag(event):
    global is_dragging
    is_dragging = True

def stop_drag(event):
    global is_dragging
    is_dragging = False

def on_square_hover(event):
    if is_dragging:
        item_id = canvas.find_closest(event.x, event.y)
        row, col = map(int, canvas.gettags(item_id)[0].split('_'))
        globals.grid[row][col].on_square_click(event)

# Set up drag-and-drop variables
is_dragging = False
canvas.bind("<ButtonPress-1>", start_drag)
canvas.bind("<ButtonRelease-1>", stop_drag)
canvas.bind("<Motion>", on_square_hover)


# Create CrosswordSquare instances for each square in the grid
globals.grid = [[CrosswordSquare(canvas, row, col, globals.grid_size) for col in range(globals.cols)] for row in range(globals.rows)]

# Configure the Tkinter window to be fullscreen
globals.root.attributes("-fullscreen", False)

# Main Tkinter event loop
globals.root.mainloop()
