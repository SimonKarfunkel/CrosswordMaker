#TODO
#Leftclickdrag to activate several squares or make one larger
#handle images
#nyckelinput

import tkinter as tk

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
        canvas.tag_bind(self.item_id, "<B1-Motion>", self.on_square_drag)
        canvas.tag_bind(self.item_id, "<ButtonRelease-1>", self.on_click_release)
        canvas.tag_bind(self.item_id, "<Button-3>", self.on_square_right_click)


    
    def on_square_click(self, event):
        if CrosswordSquare.active_square:
            CrosswordSquare.active_square.set_state("NORMAL")  # Deactivate the current active square

        self.set_state("ACTIVE")  # Activate the clicked square
        self.draw_selection_rect(event)


        # Add more conditions for other states as needed

    def on_square_drag(self, event):
        # Update selection rectangle during drag
        self.draw_selection_rect(event)

        # Add squares within the selection rectangle to selected_squares
        current_selection = self.get_squares_in_selection(event)
        CrosswordSquare.selected_squares = current_selection

        # Print the rows of selected squares (for testing)
        print([sq.row for sq in current_selection])

    def draw_selection_rect(self, event):
    # Draw or update the selection rectangle
        if CrosswordSquare.selection_rect:
            # Use the initial click position for the first point of the rectangle
            x1, y1 = event.x, event.y
            
            # Use the current mouse position for the second point of the rectangle during the drag
            x2, y2 = self.canvas.canvasx(x1), self.canvas.canvasy(y1)
            
            self.canvas.coords(CrosswordSquare.selection_rect, x1, y1, x2, y2)
        else:
            # Create the selection rectangle for the first time
            x1, y1 = event.x, event.y
            x2, y2 = self.canvas.canvasx(x1), self.canvas.canvasy(y1)
            
            CrosswordSquare.selection_rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", dash=(2, 2))
            self.canvas.tag_raise(CrosswordSquare.selection_rect)



    def remove_selection_rect(self):
        # Remove the selection rectangle
        if CrosswordSquare.selection_rect:
            self.canvas.delete(CrosswordSquare.selection_rect)
            CrosswordSquare.selection_rect = None

    def get_squares_in_selection(self, event):
        # Get the squares within the selection rectangle
        x, y = event.x, event.y
        items = self.canvas.find_overlapping(x, y, x + 1, y + 1)

        selected_squares = set()
        for item in items:
            tags = self.canvas.gettags(item)
            for tag in tags:
                if tag.startswith("square_"):
                    row, col = map(int, tag[7:].split("_"))
                    selected_squares.add(grid[row][col])

        return selected_squares

    def on_click_release(self, event):
        self.remove_selection_rect()

        if len(CrosswordSquare.selected_squares) > 1:
            self.show_popup_menu(event)

    def on_square_hover(self, event):
        if event.num == 1:  # Left mouse button            # Left-click-drag, update selection state
            CrosswordSquare.selected_squares.add(self)
            print(self.row)
        elif event.state == 0 and CrosswordSquare.selected_squares:
            # Left mouse button released, display popup menu
            self.show_popup_menu()


    def on_square_enter(self, event):
        # Implement behavior when mouse enters the square
        if event.num == 1:  # Left mouse button            # Left-click-drag, update selection state
            CrosswordSquare.selected_squares.add(self)
            print(self.row)

    def on_square_leave(self, event):
        # Implement behavior when mouse leaves the square
        pass



    def on_square_right_click(self, event):
        # Implement behavior for right-click
        pass

    def set_state(self, new_state):
        # Handle state transitions
        # Update appearance, behavior, etc.
        self.state = new_state
        if new_state == "DISABLED":
            fill_color, outline_color, dash_pattern = "lightgrey", "darkgrey", (5, 1, 2, 1)
        elif new_state == "ACTIVE":
            CrosswordSquare.active_square = self
            self.canvas.focus_set()  # Set focus to the canvas to capture key presses
            self.canvas.bind("<KeyPress>", self.on_key_press)  # Bind key press event
            fill_color, outline_color, dash_pattern = "lightcyan", "blue", ()
        elif new_state == "NORMAL":
            self.canvas.unbind("<KeyPress>")  # Unbind key press event when not in "ACTIVE" state
            fill_color, outline_color, dash_pattern = "white", "black", ()
        # Update the rectangle's appearance
        self.canvas.itemconfig(self.item_id, fill=fill_color, outline=outline_color, dash=dash_pattern)
        # Add more conditions for other states as needed
            
    def on_key_press(self, event):
        # Handle key presses and update the square's value
        key = event.char
        if key.isalnum() or key.isspace():  # Allow alphanumeric characters and spaces
            self.value = key.upper()
        elif key == '\b':  # Handle backspace
            self.value = self.value[:-1]

        # Update the square's appearance with the new value (e.g., display text)
        self.update_text()
        self.goto_next_square()


    def goto_next_square(self):
        #switch to next square
        r, c = self.row, self.col
        
        # Ensure the next square is within the grid boundaries
        if 0 <= r + 1 < len(grid) and 0 <= c < len(grid[0]):
            next_sq = grid[r + 1][c]
            if next_sq.state == "NORMAL":
                self.set_state("NORMAL")
                next_sq.set_state("ACTIVE")


    def show_popup_menu(self, event):
        popup_menu = tk.Menu(self.canvas, tearoff=0)
        popup_menu.add_command(label="Single Squares", command=self.add_multiple_single_squares)
        popup_menu.add_command(label="Join Squares", command=self.join_squares)
        popup_menu.add_command(label="Import Images", command=self.import_images)
        popup_menu.post(event.x_root, event.y_root)

    def add_multiple_single_squares(self):
        # Implement logic for selected squares
        print("Adding Multiple Single Squares")
        

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
            self.canvas.itemconfig(text_item, text=self.value)
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

# Create CrosswordSquare instances for each square in the grid
grid = [[CrosswordSquare(canvas, row, col, grid_size) for col in range(cols)] for row in range(rows)]

# Configure the Tkinter window to be fullscreen
root.attributes("-fullscreen", False)

# Main Tkinter event loop
root.mainloop()
