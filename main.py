import tkinter as tk
from game_gui import DetectiveGameGUI

def main():
    root = tk.Tk()
    app = DetectiveGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()