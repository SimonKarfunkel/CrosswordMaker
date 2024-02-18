import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import globals


class ResizableCanvas(tk.Canvas):
    def __init__(self, master=None, img_path="", **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.image_path = img_path  # Path to your image file
        self.load_image()

        # Bind the canvas resizing event to the method for resizing the image
        self.bind('<Configure>', self.resize_image)
        # Bind the right-click event to show the popup menu
        self.bind("<Button-3>", self.show_popup_menu)

    def load_image(self):
        self.image = Image.open(self.image_path)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.create_image(0, 0, anchor=tk.NW, image=self.image_tk, tags='resizable_image')  # Add tag to the image

    def resize_image(self, event):
        # Resize the image to fit the canvas size
        self.image_resized = self.image.resize((event.width, event.height), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image_resized)
        self.delete('resizable_image')  # Delete previous image item with the tag
        self.create_image(0, 0, anchor=tk.NW, image=self.image_tk, tags='resizable_image')  # Add the resized image with the same tag

    def show_popup_menu(self, event):
        print("The image was right clicked")
        popup_menu = tk.Menu(self, tearoff=0)
        popup_menu.add_command(label="Resize", command=self.resize_image_popup)
        popup_menu.post(event.x_root, event.y_root)

    def resize_image_popup(self):
        # Prompt the user to input the desired width and height of the image
        width = int(input("Enter the desired width (in squares): "))
        height = int(input("Enter the desired height (in squares): "))

        # Resize the image accordingly
        new_width = width * globals.grid_size
        new_height = height * globals.grid_size

        # Update the image on the canvas with the new size
        self.resize_image(tk.Event())



def import_image(canvas, crossword_square):
    # Prompt user to select an image file
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if image_path:
        # Create a resizable image object
        resizable_image = ResizableCanvas(globals.root, img_path=image_path, bg="white", highlightthickness=0)

        # Place the ResizableCanvas widget at the coordinates of the clicked square
        image_x = crossword_square.col * crossword_square.grid_size
        image_y = crossword_square.row * crossword_square.grid_size
        canvas.create_image(image_x, image_y, anchor=tk.NW, image=resizable_image.image_tk, tags='resizable_image')
        resizable_image.focus_set()  # Set focus to the resizable image canvas


    # Adjust stacking order
    adjust_stacking_order(canvas)




def adjust_stacking_order(canvas):
    for row in globals.grid:
        for square in row:
            if square.state == "DISABLED":
                canvas.tag_lower(square.item_id)  # Lower the disabled square
            else:
                canvas.tag_raise(square.item_id)  # Raise the enabled square
