#TODO
#Leftclickdrag to activate several squares or make one larger
#handle images
#nyckelinput

import tkinter as tk

direction = 0   #Setting to horizontal or vertical progression
temp_direction = 0
var = False

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
        if key.isalnum():  # Allow alphanumeric characters
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
        r, c = self.row, self.col
        next_row, next_col = r, c


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
                # Move to the next square in the current direction
                if direction == 0 or direction == 2:
                    next_row -= 1
                elif direction == 1 or direction == 3:
                    next_col -= 1
            else:
                break  # Stop highlighting if a blocked square is encountered




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

    def update_text(self):
        # Create or update the canvas text item with the new value
        text_item = self.canvas.find_withtag(f"text_{self.row}_{self.col}")
        if text_item:
            self.canvas.itemconfig(text_item, text=self.value, state="disabled")
        else:
            text_item = self.canvas.create_text((self.col + 0.5) * self.grid_size, (self.row + 0.5) * self.grid_size, text=self.value, font=('Arial', 20, 'bold'), tags=f"text_{self.row}_{self.col}")


# Initialize Tkinter
root = tk.Tk()
root.title("Crossword Maker")

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
