import tkinter as tk
from tkinter import ttk
import time

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.first_click = True  # Flag to track first click
        self.start_time = None   # Store when timer started
        self.timer_running = False
        
        self.setup_window()
        self.create_widgets()
        self.update_timer()  # Start the timer update loop
    
    def setup_window(self):
        self.root.title("Timer Game")
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
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Timer display
        self.timer_label = ttk.Label(main_frame, text="Timer: 00:00", 
                                   font=('Arial', 14, 'bold'))
        self.timer_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Status display
        self.status_label = ttk.Label(main_frame, text="Click any button to start timer")
        self.status_label.grid(row=1, column=0, columnspan=3, pady=5)
        
        # Multiple buttons to test
        self.button1 = ttk.Button(main_frame, text="Button 1", 
                                command=lambda: self.on_any_button_click("Button 1"))
        self.button1.grid(row=2, column=0, padx=5, pady=10)
        
        self.button2 = ttk.Button(main_frame, text="Button 2", 
                                command=lambda: self.on_any_button_click("Button 2"))
        self.button2.grid(row=2, column=1, padx=5, pady=10)
        
        self.button3 = ttk.Button(main_frame, text="Button 3", 
                                command=lambda: self.on_any_button_click("Button 3"))
        self.button3.grid(row=2, column=2, padx=5, pady=10)
        
        # Reset button
        self.reset_button = ttk.Button(main_frame, text="Reset Timer", 
                                     command=self.reset_timer)
        self.reset_button.grid(row=3, column=1, pady=20)
    
    def on_any_button_click(self, button_name):
        """Handle any button click"""
        if self.first_click:
            self.start_timer()
            self.first_click = False
            self.status_label.config(text=f"Timer started! First click: {button_name}")
        else:
            # Timer already running, just show which button was clicked
            elapsed = time.time() - self.start_time
            self.status_label.config(text=f"Clicked {button_name} at {elapsed:.1f}s")
    
    def start_timer(self):
        """Start the timer"""
        self.start_time = time.time()
        self.timer_running = True
        print(f"Timer started at: {time.strftime('%H:%M:%S')}")
    
    def update_timer(self):
        """Update timer display every 100ms"""
        if self.timer_running and self.start_time:
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            self.timer_label.config(text=f"Timer: {minutes:02d}:{seconds:02d}")
        
        # Schedule next update
        self.root.after(100, self.update_timer)
    
    def reset_timer(self):
        """Reset the timer and first click flag"""
        self.first_click = True
        self.start_time = None
        self.timer_running = False
        self.timer_label.config(text="Timer: 00:00")
        self.status_label.config(text="Click any button to start timer")
        print("Timer reset")