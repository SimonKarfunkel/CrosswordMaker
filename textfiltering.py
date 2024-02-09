import globals
import tkinter as tk
from tkinter import filedialog


sidebar_window = None
sidebar_text_widget = None

#SIDEBAR DICTIONARY FUNCTIONS------------------------------------------------------------------------
    
# Function to open the sidebar window
def open_sidebar():
    sidebar_window.deiconify()  # Make the sidebar window visible
    # Read the globals.content of the text file
    globals.dictionary_file_path = filedialog.askopenfilename(parent=sidebar_window, filetypes=[("Text files", "*.txt")])
    if globals.dictionary_file_path:
        with open(globals.dictionary_file_path, "r", encoding='utf-8') as file:
            globals.content = file.read().upper()
            # Clear any existing text in the sidebar text widget
            sidebar_text_widget.delete("1.0", "end")
            # Insert the globals.content of the text file into the sidebar text widget
            sidebar_text_widget.insert("1.0", globals.content)

# Function to close the sidebar window
def close_sidebar():
    sidebar_window.withdraw()  # Withdraw the sidebar window from the screen



def toggle_filtering():
    globals.filtering_enabled = not globals.filtering_enabled
    if globals.filtering_enabled:
        filter_text_by_length(globals.highlighted_string)
    else:
        # Refresh the globals.content to show all lines
        sidebar_text_widget.delete("1.0", "end")
        sidebar_text_widget.insert("1.0", globals.content)



def filter_text_by_length(highlighted_string):
    filtered_final = []
    # Get the length of the active direction highlight plus the active square
    length = len(globals.highlighted_string)

    # Get the globals.content of the text widget
    if not globals.filtered_content:
        globals.content = sidebar_text_widget.get("1.0", "end").split("\n")

    # Filter lines by length
    globals.filtered_content = [line for line in globals.content if len(line.strip()) == length]


    # Iterate over each line in the globals.content
    for line in globals.filtered_content:
        # Flag to keep track of whether the line matches the highlighted string
        line_matches = True

        # Iterate over each letter in the highlighted string
        for i, letter in enumerate(globals.highlighted_string):
            # If the letter is a wildcard "*", skip comparison
            if letter == "*":
                continue
            
            
            # If the letter in the line doesn't match the highlighted letter and it's not a wildcard "*", the line doesn't match
            elif letter != line[i]:
                line_matches = False
                break
        
        # If the line matches the highlighted string, add it to the filtered lines
        if line_matches:
            filtered_final.append(line)
    
    # Update the text widget with filtered final
    sidebar_text_widget.delete("1.0", "end")
    sidebar_text_widget.insert("1.0", "\n".join(filtered_final))


#END SIDEBAR DICTIONARY FUNCTIONS------------------------------------------------------------------------





#DICTIONARY SIDEBAR------------------------------------------------------------------------------
# Create the sidebar window
def create_sidebar():
    global sidebar_window
    global sidebar_text_widget
    
    sidebar_window = tk.Toplevel(globals.root)
    print(globals.root)
    sidebar_window.title("Sidebar")
    sidebar_window.attributes("-topmost", True)  # Set the sidebar window to be always on top
    sidebar_window.withdraw()  # Hide the sidebar window initially

    # Create a top bar frame
    top_bar_frame = tk.Frame(sidebar_window)
    top_bar_frame.pack(fill="x")

    # Add a Toggle Filtering button to the top bar
    globals.filtering_enabled = False
    filter_button = tk.Button(top_bar_frame, text="Toggle Filtering", command=toggle_filtering)
    filter_button.pack(side="left")

    # Create a text widget inside the sidebar window
    sidebar_text_widget = tk.Text(sidebar_window, wrap="word", font=("Arial", 12))
    sidebar_text_widget.pack(fill="both", expand=True)

    # Bind closing of sidebar window to close_sidebar function
    sidebar_window.protocol("WM_DELETE_WINDOW", close_sidebar)
#END DICTIONARY SIDEBAR--------------------------------------------------------------------------