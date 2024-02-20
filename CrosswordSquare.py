import textwrap
import globals
import textfiltering
import tkinter as tk
import imagefunctions



class CrosswordSquare:
    active_square = None  # Class Variable to store the active square
    selected_squares = set()  # Store selected squares
    selection_rect = None

    def __init__(self, canvas, row, col, grid_size):
        self.canvas = canvas
        self.row = row
        self.col = col
        self.grid_size = grid_size
        self.state = "DISABLED"
        self.value = ""
        self.text_label = None
        self.initial_square = None  # Store the initial square for drag operation
        self.final_square = None  # Store the final square for drag operation 


        x1, y1 = col * grid_size, row * grid_size
        x2, y2 = x1 + grid_size, y1 + grid_size
        self.item_id = canvas.create_rectangle(x1, y1, x2, y2, fill="lightgrey", outline="darkgrey", dash=(7,1,1,1), tags=f"{row}_{col}")
        canvas.tag_bind(self.item_id, "<ButtonPress-1>", self.on_square_click)
        #canvas.tag_bind(self.item_id, "<ButtonRelease-1>", self.on_click_release)
        canvas.tag_bind(self.item_id, "<Button-3>", self.on_square_right_click)
        
        # Set up drag-and-drop variables
        #canvas.tag_bind(self.item_id, "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.item_id, "<ButtonRelease-1>", self.stop_drag)
        canvas.tag_bind(self.item_id, "<Motion>", self.on_square_hover)
        

    
    def on_square_click(self, event):
        self.initial_square = (self.row, self.col)

        if self.state == "BLOCK" or self.state == "KEY":
            if self.state == "KEY" and CrosswordSquare.active_square and CrosswordSquare.active_square.state == "ACTIVE":            
                
                CrosswordSquare.active_square.set_state("NORMAL")  # Deactivate the current active square
                CrosswordSquare.active_square.active_direction_highlight("white")
                self.set_state("KEY")

            return  # Do not change the state if the square is in the "BLOCK" or "KEY" state

        self.on_canvas_click(event)
        
        if CrosswordSquare.active_square and CrosswordSquare.active_square.state == "ACTIVE":
            
            CrosswordSquare.active_square.set_state("NORMAL")  # Deactivate the current active square
            CrosswordSquare.active_square.active_direction_highlight("white")


        self.set_state("ACTIVE")  # Activate the clicked square
        self.active_direction_highlight("beige")


        # Add more conditions for other states as needed


    def on_canvas_click(self, event):
        #cw_square_canvas = self.canvas  # Use the canvas associated with the CrosswordSquare object

        x1, y1 = self.col * globals.grid_size, self.row * globals.grid_size
        x2, y2 = x1 + globals.grid_size, y1 + globals.grid_size
        # Calculate the coordinates of the center of the canvas
        canvas_center = ((self.col * self.grid_size) + (self.grid_size / 2), (self.row * self.grid_size) + (self.grid_size / 2))

        #if-function to define where click happened in square
        if (event.y - canvas_center[1]) < 0 and abs(event.x - canvas_center[0]) < abs(event.y - canvas_center[1]):
            print("Clicked on the top triangle")
        elif (event.y - canvas_center[1]) > 0 and abs(event.x - canvas_center[0]) < abs(event.y - canvas_center[1]):
            print("Clicked on the bottom triangle")
        elif (event.x - canvas_center[0]) > 0 and abs(event.y - canvas_center[1]) < abs(event.x - canvas_center[0]):
            print("Clicked on the right triangle")
        elif (event.x - canvas_center[0]) < 0 and abs(event.y - canvas_center[1]) < abs(event.x - canvas_center[0]):
            print("Clicked on the left triangle")



    def on_click_release(self, event):
        #Release new position for rectangle selection
        return


    

    def on_square_right_click(self, event):
        # Implement behavior for right-click
        self.show_right_click_popup_menu(event)

        pass

    def set_state(self, new_state):
        # Handle state transitions
        # Update appearance, behavior, etc.
        self.state = new_state
        if new_state == "DISABLED":
            fill_color, outline_color, dash_pattern = "lightgrey", "darkgrey", (5, 1, 2, 1)
            self.canvas.unbind("<KeyPress>")  # Unbind key press event when not in "ACTIVE" state
            self.canvas.tag_lower(self.item_id)
        elif new_state == "ACTIVE":
            CrosswordSquare.active_square = self
            self.canvas.focus_set()  # Set focus to the canvas to capture key presses
            self.canvas.bind("<KeyPress>", self.on_key_press)  # Bind key press event
            fill_color, outline_color, dash_pattern = "lightcyan", "blue", ()
            if self.text_label:
                self.text_label.config(bg = "lightcyan")
        elif new_state == "NORMAL":
            fill_color, outline_color, dash_pattern = "white", "black", ()
            if self.text_label:
                self.text_label.config(bg = "white")
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
                if globals.direction == 0:
                    self.canvas.event_generate("<KeyPress>", keysym='Up')
                elif globals.direction == 1:
                    self.canvas.event_generate("<KeyPress>", keysym='Left')

            return

        elif event.keysym in {'Up', 'Down', 'Left', 'Right'}:
            # Handle arrow key press
            globals.arrow_key_pressed = True
            arrow_directions = {'Up': 2, 'Down': 0, 'Left': 3, 'Right': 1}
            globals.temp_direction = arrow_directions[event.keysym]
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
        # Toggle between horizontal and vertical progression
        CrosswordSquare.active_square.active_direction_highlight("white")
        globals.direction = 1 - globals.direction  # Toggle between 0 and 1
        CrosswordSquare.active_square.active_direction_highlight("beige")

        return  # Exit the function early
    

    def goto_next_square(self):
        # Switch to the next square based on the globals.direction
        globals.r, globals.c = self.row, self.col
        next_row, next_col = globals.r, globals.c

        if globals.arrow_key_pressed:
            # Calculate the next row and column based on the arrow key globals.direction
            if globals.temp_direction == 0:  # Vertical progression
                next_row += 1
            elif globals.temp_direction == 1:  # Horizontal progression
                next_col += 1
            elif globals.temp_direction == 2:  # Negative vertical progression
                next_row -= 1
            elif globals.temp_direction == 3:  # Negative horizontal progression
                next_col -= 1
        else:
            # Calculate the next row and column based on the globals.direction
            if globals.direction == 0:  # Vertical progression
                next_row += 1
            elif globals.direction == 1:  # Horizontal progression
                next_col += 1
            elif globals.direction == 2:  # Negative vertical progression
                next_row -= 1
            elif globals.direction == 3:  # Negative horizontal progression
                next_col -= 1

        # Ensure the next square is within the grid boundaries
        if 0 <= next_row < len(globals.grid) and 0 <= next_col < len(globals.grid[0]):
            next_sq = globals.grid[next_row][next_col]
            if next_sq.state == "NORMAL":
                if self.state != "BLOCK":  # Check if current square is not "BLOCK"
                    self.set_state("NORMAL")
                    self.active_direction_highlight("white")
                next_sq.set_state("ACTIVE")
                next_sq.active_direction_highlight("beige")
            else:
                self.active_direction_highlight("beige")

        globals.arrow_key_pressed = False

        

    def active_direction_highlight(self, highlight_colour):
        globals.num_of_highlighted_squares = 1
        globals.r, globals.c = self.row, self.col
        next_row, next_col = globals.r, globals.c
        if self.value:
            highlighted_letters = [self.value]  # Initialize list to store highlighted letters
        else:
            highlighted_letters = ["*"]  # Initialize list to store highlighted letters

        # Calculate the next row and column based on the globals.direction
        if globals.direction == 0 or globals.direction == 2:  # Vertical progression
            next_row += 1
        elif globals.direction == 1 or globals.direction == 3:  # Horizontal progression
            next_col += 1

        # Highlight squares in the POSITIVE globals.direction until reaching the edge of the globals.grid or a blocked square
        while 0 <= next_row < len(globals.grid) and 0 <= next_col < len(globals.grid[0]):
            next_sq = globals.grid[next_row][next_col]
            if next_sq.state == "NORMAL":
                next_sq.canvas.itemconfig(next_sq.item_id, fill=highlight_colour)
                if next_sq.text_label:
                    next_sq.text_label.config(bg = highlight_colour)

                if not next_sq.value:
                    highlighted_letters.append("*")  # Append letter to the list
                else:
                    highlighted_letters.append(next_sq.value)  # Append letter to the list
                # Move to the next square in the current globals.direction
                if globals.direction == 0 or globals.direction == 2:
                    next_row += 1
                elif globals.direction == 1 or globals.direction == 3:
                    next_col += 1
            else:
                break  # Stop highlighting if a blocked square is encountered

        # Reset next_row and next_col to the original values before highlighting in the negative globals.direction
        next_row, next_col = globals.r, globals.c

        # Calculate the next row and column based on the globals.direction
        if globals.direction == 0 or globals.direction == 2:  # Vertical progression
            next_row -= 1
        elif globals.direction == 1 or globals.direction == 3:  # Horizontal progression
            next_col -= 1

        # Highlight squares in the NEGATIVE globals.direction until reaching the edge of the globals.grid or a blocked square
        while 0 <= next_row < len(globals.grid) and 0 <= next_col < len(globals.grid[0]):
            next_sq = globals.grid[next_row][next_col]
            if next_sq.state == "NORMAL":
                next_sq.canvas.itemconfig(next_sq.item_id, fill=highlight_colour)
                if next_sq.text_label:
                    next_sq.text_label.config(bg = highlight_colour)

                if not next_sq.value:
                    highlighted_letters.insert(0, "*")             # Prepend the letter to the beginning of the list
                else:
                    highlighted_letters.insert(0, next_sq.value)             # Prepend the letter to the beginning of the list
                # Move to the next square in the current globals.direction
                if globals.direction == 0 or globals.direction == 2:
                    next_row -= 1
                elif globals.direction == 1 or globals.direction == 3:
                    next_col -= 1
            else:
                break  # Stop highlighting if a blocked square is encountered
        # Convert the list of highlighted letters to a string
        globals.highlighted_string = "".join(highlighted_letters)

        # Optionally, you can use the globals.highlighted_string for text filtering
        if globals.dictionary_file_path and globals.filtering_enabled:
            textfiltering.filter_text_by_length(globals.highlighted_string)



    def show_right_click_popup_menu(self, event):
        popup_menu = tk.Menu(self.canvas, tearoff=0)
        popup_menu.add_command(label="Key Square", command=self.add_key_square)
        popup_menu.add_command(label="Disable Square", command=self.disable_square)
        popup_menu.add_command(label="Join Squares", command=self.join_squares)
        popup_menu.add_command(label="Import Image", command=self.import_image)
        popup_menu.post(event.x_root, event.y_root)

    def show_left_drag_popup_menu(self, x1, y1):
        popup_menu = tk.Menu(self.canvas, tearoff=0)
        popup_menu.add_command(label="Normal Squares", command=self.set_range_of_squares)
        popup_menu.add_command(label="Disable Squares", command=self.disable_square)
        popup_menu.add_command(label="Join Squares", command=self.join_squares)
        popup_menu.add_command(label="Import Image", command=self.import_image)
        popup_menu.post(x1, y1)
        #popup_menu.post((self.final_square[1] * self.grid_size) - globals.pan_offset_x, ((self.final_square[0] -1) * self.grid_size) - globals.pan_offset_y)

    def add_key_square(self):
        # Implement logic for selected squares
        self.set_state("KEY")
        print("Adding Key Squares")
        
    def disable_square(self):
        # Implement joining logic for disabling squares
        self.set_state("DISABLED")
        print("Joining squares")


    def join_squares(self):
        # Implement joining logic for selected squares
        print("Joining squares")

    def import_image(self):
        # Implement image import logic for selected squares
        imagefunctions.import_image(globals.canvas, self)
        print("Importing images")

    def update_text(self):
        # Calculate the position of the text relative to the square
        text_x = self.col * self.grid_size + self.grid_size // 2
        text_y = self.row * self.grid_size + self.grid_size // 2

        # Wrap the text to fit within the square size without breaking long words
        wrapped_text = "\n".join(textwrap.wrap(self.value, width=7, break_long_words=True))

        # Get the fill color of the square on the canvas
        square_fill_color = self.canvas.itemcget(self.item_id, "fill")
           
        # Create or update the Label with the new text and font, center-aligned
        if self.text_label:
            if self.state == "KEY":
                self.text_label.config(text=wrapped_text, bg=square_fill_color, font=globals.font_key)
            else:
                self.text_label.config(text=wrapped_text, bg=square_fill_color, font=globals.font_normal)
        else:
            if self.state == "ACTIVE":
                self.text_label = tk.Label(self.canvas, text=wrapped_text, width=1, font=globals.font_normal, bg=square_fill_color)
                self.text_label.place(x=text_x - globals.pan_offset_x, y=text_y - globals.pan_offset_y, anchor="center")
            elif self.state == "KEY":
                self.text_label = tk.Label(self.canvas, text=wrapped_text, font=globals.font_key, width=7, bg=square_fill_color)
                self.text_label.place(x=text_x - globals.pan_offset_x, y=text_y - globals.pan_offset_y, anchor="center")




    #def start_drag(self, event):
    #    # Record the initial square where the drag operation started
    #    self.initial_square = (self.row, self.col)

    def stop_drag(self, event):
        # Record the final square where the drag operation ended
        item_id = self.canvas.find_closest(event.x + globals.pan_offset_x, event.y + globals.pan_offset_y)
        row, col = map(int, self.canvas.gettags(item_id)[0].split('_'))
        self.final_square = (row, col)

        # Calculate the rectangle of squares encompassed by the drag operation
        if self.initial_square and self.final_square and not self.initial_square == self.final_square:
            self.show_left_drag_popup_menu(event.x, event.y)

        

    def set_range_of_squares(self):
        min_row = min(self.initial_square[0], self.final_square[0])
        max_row = max(self.initial_square[0], self.final_square[0])
        min_col = min(self.initial_square[1], self.final_square[1])
        max_col = max(self.initial_square[1], self.final_square[1])

        # Iterate over the squares in the rectangle
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                # Access the square at (row, col) and perform necessary actions
                square = globals.grid[row][col]
                square.set_state("NORMAL")  

        # Reset initial and final squares
        self.initial_square = None
        self.final_square = None   

    def on_square_hover(self, event):
        #item_id = globals.canvas.find_closest(event.x, event.y)
        #if 'current' in globals.canvas.gettags(item_id):
        #    return  # Ignore hover events over non-grid items
                
        #row, col = map(int, globals.canvas.gettags(item_id)[0].split('_'))
        #globals.grid[row][col].on_square_click(event)
        return