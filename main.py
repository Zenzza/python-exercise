import gui
import customtkinter as ctk

if __name__ == "__main__":
    root = ctk.CTk()
    app = gui.DiffApp(root)
    root.mainloop()