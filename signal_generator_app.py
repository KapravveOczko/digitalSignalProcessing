from custom_notebook import CustomNotebook
from signal_generator_tab import SignalGenerationTab
import tkinter.font

class SignalGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generowanie sygnałów")

        self.root.state('zoomed')

        default_font = tkinter.font.nametofont("TkDefaultFont")
        default_font.configure(size=20)
        self.root.option_add("*Font", default_font)

        self.tabs = CustomNotebook(self.root)
        self.tabs.pack(fill="both", expand=True)

        signal_generation_tab = SignalGenerationTab(self.tabs)
        self.tabs.add(signal_generation_tab, text="Generuj Wykres")

    def run(self):
        self.root.mainloop()
