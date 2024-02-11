import textwrap
import globals
import textfiltering
import tkinter as tk
import imagefunctions



class CrosswordSquare:
    active_square = None  # Class globals.arrow_key_pressediable to store the active square
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
            arrow_globals.directions = {'Up': 2, 'Down': 0, 'Left': 3, 'Right': 1}
            self.active_direction_highlight("white")
            #globals.temp_direction = globals.direction
            globals.temp_direction = arrow_globals.directions[event.keysym]
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
        print(globals.direction)
        print(globals.temp_direction)
        print(globals.arrow_key_pressed)
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
        print("Highlighted Letters:", globals.highlighted_string)

        # Optionally, you can use the globals.highlighted_string for text filtering
        if globals.dictionary_file_path and globals.filtering_enabled:
            textfiltering.filter_text_by_length(globals.highlighted_string)



    def show_popup_menu(self, event):
        popup_menu = tk.Menu(self.canvas, tearoff=0)
        popup_menu.add_command(label="Key Square", command=self.add_key_square)
        popup_menu.add_command(label="Join Squares", command=self.join_squares)
        popup_menu.add_command(label="Import Image", command=self.import_image)
        popup_menu.post(event.x_root, event.y_root)

    def add_key_square(self):
        # Implement logic for selected squares
        self.set_state("KEY")
        print("Adding Key Squares")
        

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

        # Create or update the canvas text item with the new value
        text_item = self.canvas.find_withtag(f"text_{self.row}_{self.col}")

        # Wrap the text to fit within the square size without breaking long words
        font_size = self.grid_size // 2
        wrapped_text = textwrap.fill(self.value, width=int(self.grid_size / 10), break_long_words=False)

        # Create a font with the current font size
        font = ('Arial', font_size, 'bold')

        # Create or update the canvas text item with the new text and font, center-aligned
        if text_item:
            self.canvas.itemconfig(text_item, text=wrapped_text, font=font, anchor="center", state="disabled")
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

