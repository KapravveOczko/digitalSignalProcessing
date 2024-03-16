from custom_notebook import CustomNotebook
import tkinter.font

class SignalGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generowanie sygnałów")

        self.root.state('zoomed')

        default_font = tkinter.font.nametofont("TkDefaultFont")
        default_font.configure(size=20)
        self.root.option_add("*Font", default_font)

        notebook = CustomNotebook(self.root)
        notebook.pack(fill="both", expand=True)

    def run(self):
        self.root.mainloop()