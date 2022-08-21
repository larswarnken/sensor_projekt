import gui
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    gui.MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
