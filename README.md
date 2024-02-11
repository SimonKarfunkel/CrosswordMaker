Crossword Maker
Crossword Maker is a Python application designed to facilitate the creation of custom crossword puzzles. With an intuitive user interface and powerful features, it allows users to construct crossword grids, input text, and manipulate grid elements efficiently.

Features
Grid Construction: Easily create crossword grids of customizable dimensions.
Text Input: Input letters and words into grid squares with intuitive click-and-type functionality.
Navigation: Navigate through the grid using arrow keys or mouse clicks.
Sidebar Dictionary: Access a sidebar dictionary to assist in constructing the puzzle by providing word suggestions and definitions.
Text Filtering: Toggle text filtering to narrow down word suggestions based on highlighted letters in the grid.

Installation
Ensure you have Python installed on your system.
Clone this repository to your local machine.
Install the required dependencies using pip:
pip install -r requirements.txt

Usage
Run the program by executing the main.py file.
Use the mouse to interact with the grid:
Left-click to input letters into grid squares.
Right-click to access additional options such as marking squares as key squares or importing images.
Use the arrow keys to navigate through the grid:
Up and Down arrows switch between vertical and horizontal progression.
Left and Right arrows move the active square in the corresponding direction.
Utilize the sidebar dictionary:
Open the sidebar to view word suggestions and definitions.
Toggle text filtering to narrow down word suggestions based on highlighted letters in the grid.
Development
The program is written in Python using the Tkinter library for the graphical user interface. It is structured into multiple modules, each responsible for specific functionalities:

CrosswordMaker.py: Entry point of the application.
CrosswordSquare.py: Defines the CrosswordSquare class for managing individual grid squares.
textfiltering.py: Handles text filtering and dictionary functionality.
globals.py: Contains global variables and settings used throughout the program.
README.md: Documentation explaining the program and its usage.

Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository, make your changes, and submit a pull request.

License
TBD