import tkinter as tk
from signal_generator_app import SignalGeneratorApp

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalGeneratorApp(root)
    app.run()
