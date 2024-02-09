#TODO
#Leftclickdrag to activate several squares or make one larger
#handle images
#nyckelinput

import tkinter as tk
from tkinter import filedialog
import textwrap



direction = 0   #Setting to horizontal or vertical progression
temp_direction = 0
var = False
font = "Comic Sans"
sidebar_frame = None  # Initialize sidebar_frame as None
num_of_highlighted_squares = 0
filtering_enabled = False
dictionary_file_path = None
filtered_content = []
content = None
highlighted_string = None

def dummy_command():
    print("This is a dummy command")



#SIDEBAR DICTIONARY FUNCTIONS------------------------------------------------------------------------
    
# Function to open the sidebar window
def open_sidebar():
    global dictionary_file_path
    sidebar_window.deiconify()  # Make the sidebar window visible
    # Read the content of the text file
    dictionary_file_path = filedialog.askopenfilename(parent=sidebar_window, filetypes=[("Text files", "*.txt")])
    if dictionary_file_path:
        with open(dictionary_file_path, "r", encoding='utf-8') as file:
            content = file.read().upper()
            # Clear any existing text in the sidebar text widget
            sidebar_text_widget.delete("1.0", "end")
            # Insert the content of the text file into the sidebar text widget
            sidebar_text_widget.insert("1.0", content)

# Function to close the sidebar window
def close_sidebar():
    sidebar_window.withdraw()  # Withdraw the sidebar window from the screen

def filter_text_by_length(highlighted_string):
    global filtered_content
    global content
    filtered_final = []
    # Get the length of the active direction highlight plus the active square
    length = num_of_highlighted_squares

    # Get the content of the text widget
    if not filtered_content:
        content = sidebar_text_widget.get("1.0", "end").split("\n")

    # Filter lines by length
    filtered_content = [line for line in content if len(line.strip()) == length]


    # Iterate over each line in the content
    for line in filtered_content:
        # Flag to keep track of whether the line matches the highlighted string
        line_matches = True

        # Iterate over each letter in the highlighted string
        for i, letter in enumerate(highlighted_string):
            # If the letter is a wildcard "*", skip comparison
            if letter == "*":
                continue
            
            
            # If the letter in the line doesn't match the highlighted letter and it's not a wildcard "*", the line doesn't match
            elif letter != line[i]:
                line_matches = False
                break
        
        # If the line matches the highlighted string, add it to the filtered lines
        if line_matches:
            filtered_final.append(line)
    
    # Update the text widget with filtered final
    sidebar_text_widget.delete("1.0", "end")
    sidebar_text_widget.insert("1.0", "\n".join(filtered_final))

def toggle_filtering():
    global filtering_enabled
    global content
    filtering_enabled = not filtering_enabled
    if filtering_enabled:
        filter_text_by_length(highlighted_string)
    else:
        # Refresh the content to show all lines
        sidebar_text_widget.delete("1.0", "end")
        sidebar_text_widget.insert("1.0", content)

#END SIDEBAR DICTIONARY FUNCTIONS------------------------------------------------------------------------






class CrosswordSquare:
    active_square = None  # Class variable to store the active square
    selected_squares = set()  # Store selected squares
    selection_rect = None

    def __init__(self, canvas, row, col, grid_size):
        self.canvas = canvas
        self.row = row
        self.col = col
        self.grid_size = grid_size
        self.state = "DISABLED"
        self.value = ""

        x1, y1 = col * grid_size, row * grid_size
        x2, y2 = x1 + grid_size, y1 + grid_size
        self.item_id = canvas.create_rectangle(x1, y1, x2, y2, fill="lightgrey", outline="darkgrey", dash=(7,1,1,1), tags=f"{row}_{col}")
        canvas.tag_bind(self.item_id, "<Button-1>", self.on_square_click)
        canvas.tag_bind(self.item_id, "<ButtonRelease-1>", self.on_click_release)
        canvas.tag_bind(self.item_id, "<Button-3>", self.on_square_right_click)
        

    
    def on_square_click(self, event):
        if self.state == "BLOCK" or self.state == "KEY":
            if self.state == "KEY" and CrosswordSquare.active_square and CrosswordSquare.active_square.state == "ACTIVE":            
                
                CrosswordSquare.active_square.set_state("NORMAL")  # Deactivate the current active square
                CrosswordSquare.active_square.active_direction_highlight("white")
                self.set_state("KEY")

            return  # Do not change the state if the square is in the "BLOCK" or "KEY" state



        if CrosswordSquare.active_square and CrosswordSquare.active_square.state == "ACTIVE":
            
            CrosswordSquare.active_square.set_state("NORMAL")  # Deactivate the current active square
            CrosswordSquare.active_square.active_direction_highlight("white")


        self.set_state("ACTIVE")  # Activate the clicked square
        self.active_direction_highlight("beige")


        # Add more conditions for other states as needed




    def on_click_release(self, event):
        #Release new position for rectangle selection
        print("Hej")


    

    def on_square_right_click(self, event):
        # Implement behavior for right-click
        self.show_popup_menu(event)

        pass

    def set_state(self, new_state):
        # Handle state transitions
        # Update appearance, behavior, etc.
        self.state = new_state
        if new_state == "DISABLED":
            fill_color, outline_color, dash_pattern = "lightgrey", "darkgrey", (5, 1, 2, 1)
            self.canvas.unbind("<KeyPress>")  # Unbind key press event when not in "ACTIVE" state
        elif new_state == "ACTIVE":
            CrosswordSquare.active_square = self
            self.canvas.focus_set()  # Set focus to the canvas to capture key presses
            self.canvas.bind("<KeyPress>", self.on_key_press)  # Bind key press event
            fill_color, outline_color, dash_pattern = "lightcyan", "blue", ()
        elif new_state == "NORMAL":
            fill_color, outline_color, dash_pattern = "white", "black", ()
        elif new_state == "BLOCK":
            fill_color, outline_color, dash_pattern = "black", "black", ()
        elif new_state == "KEY":
            CrosswordSquare.active_square = self
            self.canvas.focus_set()  # Set focus to the canvas to capture key presses
            self.canvas.bind("<KeyPress>", self.on_key_press)  # Bind key press event
            fill_color, outline_color, dash_pattern = "powderblue", "black", ()




        # Update the rectangle's appearance
        self.canvas.itemconfig(self.item_id, fill=fill_color, outline=outline_color, dash=dash_pattern)
        # Add more conditions for other states as needed
            
    def on_key_press(self, event):
        global direction  # Declare direction as global
        global temp_direction
        global var

        key = event.char
        if key.isalnum() or key == '-':  # Allow alphanumeric characters
            if self.state == "KEY":
                self.value += key.upper()
                self.update_text()
                return

            self.value = key.upper()
            self.update_text()
        elif key.isspace():
            if self.state == "KEY":
                self.value += key.upper()
                self.update_text()
                return
            
            self.switch_direction()
            return
        elif key == '\b':  # Handle backspace
            self.value = self.value[:-1]
            self.update_text()
            if self.state == "ACTIVE":
                if direction == 0:
                    self.canvas.event_generate("<KeyPress>", keysym='Up')
                elif direction == 1:
                    self.canvas.event_generate("<KeyPress>", keysym='Left')

            return

        elif event.keysym in {'Up', 'Down', 'Left', 'Right'}:
            # Handle arrow key press
            var = True
            arrow_directions = {'Up': 2, 'Down': 0, 'Left': 3, 'Right': 1}
            self.active_direction_highlight("white")
            #temp_direction = direction
            temp_direction = arrow_directions[event.keysym]
            self.goto_next_square()
            return
        elif event.keysym == 'period':
            # Handle "." key press
            self.active_direction_highlight("white")
            self.set_state("BLOCK")

        


        # Update the square's appearance with the new value
        self.update_text()
        self.goto_next_square()


    def switch_direction(self):
        global direction
        # Toggle between horizontal and vertical progression
        CrosswordSquare.active_square.active_direction_highlight("white")
        direction = 1 - direction  # Toggle between 0 and 1
        CrosswordSquare.active_square.active_direction_highlight("beige")

        return  # Exit the function early
    

    def goto_next_square(self):
        global direction
        global temp_direction
        global var
        # Switch to the next square based on the direction
        r, c = self.row, self.col
        next_row, next_col = r, c

        if var:
            # Calculate the next row and column based on the arrow key direction
            if temp_direction == 0:  # Vertical progression
                next_row += 1
            elif temp_direction == 1:  # Horizontal progression
                next_col += 1
            elif temp_direction == 2:  # Negative vertical progression
                next_row -= 1
            elif temp_direction == 3:  # Negative horizontal progression
                next_col -= 1
        else:
            # Calculate the next row and column based on the direction
            if direction == 0:  # Vertical progression
                next_row += 1
            elif direction == 1:  # Horizontal progression
                next_col += 1
            elif direction == 2:  # Negative vertical progression
                next_row -= 1
            elif direction == 3:  # Negative horizontal progression
                next_col -= 1

        # Ensure the next square is within the grid boundaries
        if 0 <= next_row < len(grid) and 0 <= next_col < len(grid[0]):
            next_sq = grid[next_row][next_col]
            if next_sq.state == "NORMAL":
                if self.state != "BLOCK":  # Check if current square is not "BLOCK"
                    self.set_state("NORMAL")
                    self.active_direction_highlight("white")
                next_sq.set_state("ACTIVE")
                next_sq.active_direction_highlight("beige")

        var = False

        

    def active_direction_highlight(self, highlight_colour):
        global direction
        global num_of_highlighted_squares
        global dictionary_file_path
        global filtering_enabled
        global highlighted_string

        num_of_highlighted_squares = 1
        r, c = self.row, self.col
        next_row, next_col = r, c
        if self.value:
            highlighted_letters = [self.value]  # Initialize list to store highlighted letters
        else:
            highlighted_letters = ["*"]  # Initialize list to store highlighted letters

        # Calculate the next row and column based on the direction
        if direction == 0 or direction == 2:  # Vertical progression
            next_row += 1
        elif direction == 1 or direction == 3:  # Horizontal progression
            next_col += 1

        # Highlight squares in the POSITIVE direction until reaching the edge of the grid or a blocked square
        while 0 <= next_row < len(grid) and 0 <= next_col < len(grid[0]):
            next_sq = grid[next_row][next_col]
            if next_sq.state == "NORMAL":
                next_sq.canvas.itemconfig(next_sq.item_id, fill=highlight_colour)
                if not next_sq.value:
                    highlighted_letters.append("*")  # Append letter to the list
                else:
                    highlighted_letters.append(next_sq.value)  # Append letter to the list
                num_of_highlighted_squares += 1
                # Move to the next square in the current direction
                if direction == 0 or direction == 2:
                    next_row += 1
                elif direction == 1 or direction == 3:
                    next_col += 1
            else:
                break  # Stop highlighting if a blocked square is encountered

        # Reset next_row and next_col to the original values before highlighting in the negative direction
        next_row, next_col = r, c

        # Calculate the next row and column based on the direction
        if direction == 0 or direction == 2:  # Vertical progression
            next_row -= 1
        elif direction == 1 or direction == 3:  # Horizontal progression
            next_col -= 1

        # Highlight squares in the NEGATIVE direction until reaching the edge of the grid or a blocked square
        while 0 <= next_row < len(grid) and 0 <= next_col < len(grid[0]):
            next_sq = grid[next_row][next_col]
            if next_sq.state == "NORMAL":
                next_sq.canvas.itemconfig(next_sq.item_id, fill=highlight_colour)
                if not next_sq.value:
                    highlighted_letters.insert(0, "*")             # Prepend the letter to the beginning of the list
                else:
                    highlighted_letters.insert(0, next_sq.value)             # Prepend the letter to the beginning of the list
                num_of_highlighted_squares += 1
                # Move to the next square in the current direction
                if direction == 0 or direction == 2:
                    next_row -= 1
                elif direction == 1 or direction == 3:
                    next_col -= 1
            else:
                break  # Stop highlighting if a blocked square is encountered
        # Convert the list of highlighted letters to a string
        highlighted_string = "".join(highlighted_letters)
        print("Highlighted Letters:", highlighted_string)

        # Optionally, you can use the highlighted_string for text filtering
        if dictionary_file_path and filtering_enabled:
            filter_text_by_length(highlighted_string)



    def show_popup_menu(self, event):
        popup_menu = tk.Menu(self.canvas, tearoff=0)
        popup_menu.add_command(label="Key Square", command=self.add_key_square)
        popup_menu.add_command(label="Join Squares", command=self.join_squares)
        popup_menu.add_command(label="Import Images", command=self.import_images)
        popup_menu.post(event.x_root, event.y_root)

    def add_key_square(self):
        # Implement logic for selected squares
        self.set_state("KEY")
        print("Adding Key Squares")
        

    def join_squares(self):
        # Implement joining logic for selected squares
        print("Joining squares")

    def import_images(self):
        # Implement image import logic for selected squares
        print("Importing images")

    import textwrap

    def update_text(self):
        # Calculate the position of the text relative to the square
        text_x = self.col * self.grid_size + self.grid_size // 2
        text_y = self.row * self.grid_size + self.grid_size // 2

        # Create or update the canvas text item with the new value
        text_item = self.canvas.find_withtag(f"text_{self.row}_{self.col}")

        # Wrap the text to fit within the square size without breaking long words
        font_size = self.grid_size // 2
        wrapped_text = textwrap.fill(self.value, width=int(self.grid_size / 10), break_long_words=False)

        # Create a font with the current font size
        font = ('Arial', font_size, 'bold')

        # Create or update the canvas text item with the new text and font, center-aligned
        if text_item:
            self.canvas.itemconfig(text_item, text=wrapped_text, font=font, anchor="center", state="normal")
        else:
            text_item = self.canvas.create_text(text_x, text_y, text=wrapped_text, font=font, anchor="center", tags=f"text_{self.row}_{self.col}")

        # Measure the width and height of the text rendered with the current font size
        text_bbox = self.canvas.bbox(text_item)

        # If the text bbox exists and both the width and height fit within the square size, exit
        if text_bbox and (text_bbox[2] - text_bbox[0] <= self.grid_size and text_bbox[3] - text_bbox[1] <= self.grid_size):
            return

        # If the text doesn't fit within the square size, reduce the font size and try again
        while font_size > 0:
            # Decrease the font size by one step
            font_size -= 1

            # Create a font with the new font size
            font = ('Arial', font_size, 'bold')

            # Wrap the text to fit within the square size without breaking long words
            wrapped_text = textwrap.fill(self.value, width=int(self.grid_size / 10), break_long_words=False)

            # Create or update the canvas text item with the new text and font, center-aligned
            if text_item:
                self.canvas.itemconfig(text_item, text=wrapped_text, font=font, anchor="center", state="normal")
            else:
                text_item = self.canvas.create_text(text_x, text_y, text=wrapped_text, font=font, anchor="center", tags=f"text_{self.row}_{self.col}")

            # Measure the width and height of the text rendered with the current font size
            text_bbox = self.canvas.bbox(text_item)

            # If the text bbox exists and both the width and height fit within the square size, exit
            if text_bbox and (text_bbox[2] - text_bbox[0] <= self.grid_size and text_bbox[3] - text_bbox[1] <= self.grid_size):
                break

        # Adjust horizontal center alignment for each line of text
        if text_item:
            for index, line in enumerate(wrapped_text.split('\n')):
                line_tag = f"text_{self.row}_{self.col}.{index + 1}"  # Tag for each line of text
                line_bbox = self.canvas.bbox(line_tag)  # Get the bounding box of the line
                if line_bbox:
                    line_width = line_bbox[2] - line_bbox[0]  # Calculate the width of the line
                    horizontal_offset = (self.grid_size - line_width) // 2  # Calculate horizontal offset
                    self.canvas.move(line_tag, horizontal_offset, 0)  # Move the line to center it horizontally



        # Delete temporary text items
        self.canvas.delete("temp_text")







# Initialize Tkinter
root = tk.Tk()
root.title("Crossword Maker")





#MENU BAR------------------------------------------------------------------------------
# Create a Menu Bar
menu_bar = tk.Menu(root)

# Create File Menu and its items
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=dummy_command)
file_menu.add_command(label="Open", command=dummy_command)
file_menu.add_command(label="Save", command=dummy_command)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create Edit Menu and its items
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cut", command=dummy_command)
edit_menu.add_command(label="Copy", command=dummy_command)
edit_menu.add_command(label="Paste", command=dummy_command)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Create View Menu and its items
view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Open Sidebar", command=open_sidebar)
view_menu.add_command(label="Zoom In", command=dummy_command)
view_menu.add_command(label="Zoom Out", command=dummy_command)
menu_bar.add_cascade(label="View", menu=view_menu)

# Configure the menu bar
root.config(menu=menu_bar)
#END MENU BAR--------------------------------------------------------------------------





#DICTIONARY SIDEBAR------------------------------------------------------------------------------
# Create the sidebar window
sidebar_window = tk.Toplevel(root)
sidebar_window.title("Sidebar")
sidebar_window.attributes("-topmost", True)  # Set the sidebar window to be always on top
sidebar_window.withdraw()  # Hide the sidebar window initially

# Create a top bar frame
top_bar_frame = tk.Frame(sidebar_window)
top_bar_frame.pack(fill="x")

# Add a Toggle Filtering button to the top bar
filtering_enabled = False
filter_button = tk.Button(top_bar_frame, text="Toggle Filtering", command=toggle_filtering)
filter_button.pack(side="left")

# Create a text widget inside the sidebar window
sidebar_text_widget = tk.Text(sidebar_window, wrap="word", font=("Arial", 12))
sidebar_text_widget.pack(fill="both", expand=True)

# Bind closing of sidebar window to close_sidebar function
sidebar_window.protocol("WM_DELETE_WINDOW", close_sidebar)
#END DICTIONARY SIDEBAR--------------------------------------------------------------------------



# Set up grid dimensions
grid_size = 50
rows, cols = 50, 50







# Create a Canvas widget to represent the grid
canvas = tk.Canvas(root, width=cols * grid_size, height=rows * grid_size)
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
        grid[row][col].on_square_click(event)

# Set up drag-and-drop variables
is_dragging = False
canvas.bind("<ButtonPress-1>", start_drag)
canvas.bind("<ButtonRelease-1>", stop_drag)
canvas.bind("<Motion>", on_square_hover)


# Create CrosswordSquare instances for each square in the grid
grid = [[CrosswordSquare(canvas, row, col, grid_size) for col in range(cols)] for row in range(rows)]

# Configure the Tkinter window to be fullscreen
root.attributes("-fullscreen", False)

# Main Tkinter event loop
root.mainloop()
