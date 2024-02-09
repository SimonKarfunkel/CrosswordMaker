import tkinter as tk
from tkinter import Canvas

class CrosswordConstructionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crossword Construction Software")

        # Create and place UI elements
        self.label = tk.Label(root, text="Welcome to Crossword Construction!")
        self.label.pack(pady=10)

        self.create_button = tk.Button(root, text="Create Crossword", command=self.create_crossword)
        self.create_button.pack(pady=10)

        self.load_button = tk.Button(root, text="Load Crossword", command=self.load_crossword)
        self.load_button.pack(pady=10)

        self.quit_button = tk.Button(root, text="Quit", command=root.destroy)
        self.quit_button.pack(pady=10)

        # Initialize crossword grid
        self.grid_size = 10  # Adjust grid size as needed
        self.cell_size = 30  # Adjust cell size as needed
        self.crossword_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.create_crossword_grid()

        # Bind mouse events for panning
        self.canvas.bind("<B2-Motion>", self.pan_canvas)
        self.canvas.bind("<Button-2>", self.start_panning)
        self.canvas.bind("<B3-Motion>", self.pan_canvas)
        self.canvas.bind("<Button-3>", self.start_panning)

        self.panning = False
        self.start_x = 0
        self.start_y = 0

    def create_crossword(self):
        # Add functionality to create crossword grid and enter words
        print("Creating Crossword")

    def load_crossword(self):
        # Add functionality to load an existing crossword
        print("Loading Crossword")

    def create_crossword_grid(self):
        self.canvas = Canvas(self.root, width=self.grid_size * self.cell_size, height=self.grid_size * self.cell_size, bg="white")
        self.canvas.pack()

        # Draw gridlines on the canvas
        for i in range(self.grid_size + 1):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.grid_size * self.cell_size, fill="grey", tags="grid")
            y = i * self.cell_size
            self.canvas.create_line(0, y, self.grid_size * self.cell_size, y, fill="grey", tags="grid")

        # Bind mouse events for adding white squares
        self.canvas.bind("<Button-1>", self.handle_left_click)

    def start_panning(self, event):
        # Start panning when the middle mouse button is pressed
        self.panning = True
        self.start_x = event.x
        self.start_y = event.y

    def pan_canvas(self, event):
        # Pan the canvas based on the movement of the mouse
        if self.panning:
            delta_x = event.x - self.start_x
            delta_y = event.y - self.start_y
            self.canvas.scan_dragto(-delta_x, -delta_y, gain=1)
            self.start_x = event.x
            self.start_y = event.y

    def handle_left_click(self, event):
        # Left-click to add a white square at the clicked position
        x, y = event.x, event.y
        col = x // self.cell_size
        row = y // self.cell_size

        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            self.crossword_grid[row][col] = 1
            x1, y1 = col * self.cell_size, row * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="grey", tags="grid")

if __name__ == "__main__":
    root = tk.Tk()
    app = CrosswordConstructionApp(root)
    root.mainloop()
