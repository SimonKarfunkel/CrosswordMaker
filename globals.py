
root = None
canvas = None
direction = 0   #Setting to horizontal or vertical progression
temp_direction = 0
arrow_key_pressed = False

#font sizes and styles -------------------------------------------------------------------

font_normal = ('Comic Sans MS', 25)
font_key = ('Comic Sans MS', 8)

#FONT END----------------------------------------------------------------------------------

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
grid_size = 60
rows, cols = 50, 50
image_tk = None

pan_start = None


pan_offset_x = 0     #To store the panning offset for moving labels etc.
pan_offset_y = 0