"""
MIT License
Copyright (c) 2026
"""

from tkinter import Tk
from game import KBCGame

def main():
    root = Tk()
    root.title("KBC Quiz Game")
    root.geometry("700x600")
    app = KBCGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()


