import tkinter as tk

def on_square_click(event):
    global active_square
    canvas_item_id = event.widget.find_closest(event.x, event.y)
    if canvas_item_id:
        item_tags = canvas.gettags(canvas_item_id[0])
        if item_tags:
            row, col = map(int, item_tags[0].split("_"))
            if not grid[row][col]:
                if active_square:
                    canvas.itemconfig(active_square, outline="black", fill="white", width="1", dash=())
                    store_and_display_text(active_square)

                grid[row][col] = True
                canvas.itemconfig(canvas_item_id, fill="white", width="1")
                canvas.itemconfig(canvas_item_id, outline="black", dash=())
                canvas.itemconfig(canvas_item_id, state=tk.NORMAL)  # Enable input

                active_square = canvas_item_id
                canvas.itemconfig(active_square, outline="blue", width="2", fill="lightcyan", dash=())
                canvas.itemconfig(active_square, state=tk.NORMAL)
                canvas.focus_set()
                canvas.focus(active_square)
            else:
                value = canvas.itemcget(canvas_item_id, "text")
                grid_values[row][col] = value
                canvas.itemconfig(canvas_item_id, fill="SystemButtonFace")
                canvas.itemconfig(canvas_item_id, state=tk.DISABLED)  # Disable input

def on_square_right_click(event):
    canvas_item_id = event.widget.find_closest(event.x, event.y)
    if canvas_item_id:
        item_tags = canvas.gettags(canvas_item_id[0])
        if item_tags:
            row, col = map(int, item_tags[0].split("_"))

            context_menu = tk.Menu(root, tearoff=0)
            context_menu.add_command(label="Nyckelruta", command=lambda: set_square_key_square(canvas_item_id))
            context_menu.add_command(label="Block", command=lambda: set_square_block(canvas_item_id))
            context_menu.add_command(label="Avaktivera", command=lambda: deactivate_square(canvas_item_id))

            context_menu.post(event.x_root, event.y_root)

def set_square_key_square(item_id):
    row, col = get_row_col_from_item_id(item_id)
    grid[row][col] = True
    canvas.itemconfig(item_id, fill="white", width="1")
    canvas.itemconfig(item_id, outline="black", dash=())
    canvas.itemconfig(item_id, state=tk.NORMAL)
    set_active_square(item_id)

def set_square_block(item_id):
    row, col = get_row_col_from_item_id(item_id)
    grid[row][col] = False
    canvas.itemconfig(item_id, fill="black", width="1")
    canvas.itemconfig(item_id, outline="black", dash=())
    canvas.itemconfig(item_id, state=tk.NORMAL)
    set_active_square(item_id)

def deactivate_square(item_id):
    row, col = get_row_col_from_item_id(item_id)
    grid[row][col] = False
    canvas.itemconfig(item_id, fill="lightgrey", outline="darkgrey", dash=(7, 1, 1, 1))
    canvas.itemconfig(item_id, state=tk.DISABLED)
    clear_active_square()

def get_row_col_from_item_id(item_id):
    item_tags = canvas.gettags(item_id[0])
    row, col = map(int, item_tags[0].split("_"))
    return row, col

def set_active_square(item_id):
    global active_square
    if active_square:
        canvas.itemconfig(active_square, outline="black", dash=())
    active_square = item_id
    canvas.itemconfig(active_square, outline="blue", width="2", dash=())
    canvas.focus_set()
    canvas.focus(active_square)

def clear_active_square():
    global active_square
    if active_square:
        canvas.itemconfig(active_square, outline="black", dash=())
        active_square = None

def on_square_hover(event):
    if is_dragging:
        on_square_click(event)

def start_drag(event):
    global is_dragging
    is_dragging = True

def stop_drag(event):
    global is_dragging
    is_dragging = False

def store_and_display_text(item_id):
    row, col = get_row_col_from_item_id(item_id)
    value = stored_text.get().upper()  # Get entered text and convert to uppercase
    
    # Clear previous text in the square
    canvas.delete(f"text_{row}_{col}")
    
    canvas.create_text((col + 0.5) * grid_size, (row + 0.5) * grid_size, text=value, font=('Arial', 20, 'bold'))

    canvas.itemconfig(item_id, state=tk.DISABLED)  # Disable input
    stored_text.set("")  # Clear stored text

def on_key_press(event):
    global active_square
    if active_square and event.char and event.char.isalnum():
        stored_text.set(event.char)
        store_and_display_text(active_square)
        set_next_square_active()
        
    
def set_next_square_active():
    global active_square
    if active_square:
        row, col = get_row_col_from_item_id(active_square)
        next_col = (col + 1) % cols  # Calculate the column index of the next square
        next_square_id = canvas.find_withtag(f"{row}_{next_col}")[0]  # Find the canvas item ID of the next square
        if canvas.itemcget(next_square_id, "state") == tk.NORMAL:  # Check if the next square is enabled
            x1, y1, x2, y2 = canvas.coords(next_square_id)
            x, y = (x1 + x2) / 2, (y1 + y2) / 2  # Calculate the center coordinates of the next square
            active_square = None
            on_square_click(tk.Event(widget=canvas, x=x, y=y, x_root=0, y_root=0, num=1, char='', keysym=''))


# Initialize Tkinter
root = tk.Tk()
root.title("Crossword Maker")

# Set up grid dimensions
grid_size = 50
rows, cols = 150, 150

# Create a 2D array to represent the grid
grid = [[False for _ in range(cols)] for _ in range(rows)]
grid_values = [["" for _ in range(cols)] for _ in range(rows)]

# Create a Canvas widget to represent the grid
canvas = tk.Canvas(root, width=cols * grid_size, height=rows * grid_size)
canvas.pack()

# Draw the grid on the Canvas
for row in range(rows):
    for col in range(cols):
        x1, y1 = col * grid_size, row * grid_size
        x2, y2 = x1 + grid_size, y1 + grid_size
        item = canvas.create_rectangle(x1, y1, x2, y2, fill="lightgrey", outline="darkgrey", dash=(7,1,1,1), tags=f"{row}_{col}")
        canvas.tag_bind(item, "<Button-1>", on_square_click)
        canvas.tag_bind(item, "<B1-Motion>", on_square_hover)
        canvas.tag_bind(item, "<Button-3>", on_square_right_click)

# Configure the Tkinter window to be fullscreen
root.attributes("-fullscreen", False)

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Add a "File" menu with an "Exit" option
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.destroy)

# Set up drag-and-drop variables
is_dragging = False
canvas.bind("<ButtonPress-1>", start_drag)
canvas.bind("<ButtonRelease-1>", stop_drag)
active_square = None

# Add the following lines to initialize the Tkinter StringVar
stored_text = tk.StringVar()

# Add the following line to bind the key press event
root.bind("<Key>", on_key_press)

# Main Tkinter event loop
root.mainloop()
