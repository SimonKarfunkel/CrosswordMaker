root = None
direction = 0   #Setting to horizontal or vertical progression
temp_direction = 0
arrow_key_pressed = False
font = ('Arial', 25, 'bold')
sidebar_frame = None  # Initialize sidebar_frame as None
filtering_enabled = False
dictionary_file_path = "svenska-ord.txt"
filtered_content = []
content = None
highlighted_string = None
grid = []
line_word = None
r = None    #row of active square
c = None    #column of active square

# Set up grid dimensions
grid_size = 50
rows, cols = 50, 50