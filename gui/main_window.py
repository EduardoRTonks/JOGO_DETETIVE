import tkinter as tk
from tkinter import ttk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        self.root.title("Detetive")
        self.root.geometry("800x600")
        self.root.minsize(400, 300)
        
        self.center_window()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Create and place all widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Welcome label
        welcome_label = ttk.Label(main_frame, text="Welcome to Detetive", 
                                font=('Arial', 16, 'bold'))
        welcome_label.grid(row=0, column=0, pady=20)
        
        # Sample button
        sample_button = ttk.Button(main_frame, text="Click Me!", 
                                 command=self.on_button_click)
        sample_button.grid(row=1, column=0, pady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.grid(row=2, column=0, pady=20)
    
    def on_button_click(self):
        """Handle button click event"""
        self.status_label.config(text="Button was clicked!")