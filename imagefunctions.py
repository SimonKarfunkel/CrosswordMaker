import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import globals


def import_image(canvas, crossword_square):
    global image_tk  # Define the PhotoImage object as global

    # Prompt user to select an image file
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if image_path:
        # Load the image using PIL
        image = Image.open(image_path)
        # Convert the image to Tkinter-compatible format
        image_tk = ImageTk.PhotoImage(image)
        
        # Create the image item on the canvas with the correct stacking order
        canvas.create_image(crossword_square.col * crossword_square.grid_size, crossword_square.row * crossword_square.grid_size, anchor=tk.NW, image=image_tk, tags="image")  # Adjust coordinates as needed
        
        # Lower the image item to be below the "normal" crossword square items but above the "disabled" ones
        canvas.tag_lower("image")  # Lower the item with the specified tag to the bottom of the display list
    adjust_stacking_order(canvas)


def adjust_stacking_order(canvas):
    for row in globals.grid:
        for square in row:
            if square.state == "DISABLED":
                canvas.tag_lower(square.item_id)  # Lower the disabled square
            else:
                canvas.tag_raise(square.item_id)  # Raise the enabled square