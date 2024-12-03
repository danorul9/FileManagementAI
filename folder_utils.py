import tkinter as tk

def get_color_from_confidence(confidence):
    """Map confidence percentage to color."""
    if confidence >= 80:
        return "green"
    elif confidence >= 50:
        return "yellow"
    else:
        return "red"

def display_suggestions(suggestions, master):
    """Display folder suggestions in a new window."""
    suggestions_window = tk.Toplevel(master)
    suggestions_window.title("Folder Suggestions")
    
    for folder, confidence in suggestions:
        color = get_color_from_confidence(confidence)
        label = tk.Label(suggestions_window, text=folder, foreground=color)
        label.pack(pady=5)
