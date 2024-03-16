import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from signal_generator import SignalGenerator, SIGNAL_TYPES
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

class SignalFrame(ttk.Frame):
    def __init__(self, container, signal_type = None, params_val_dict = None, file_path = None, operation = None, first_signal = None, second_signal = None):
        super().__init__(container)


        if file_path:
            signal_generator = SignalGenerator()
            signal_generator.read_from_file(file_path)
        elif operation:
            signal_generator = SignalGenerator()
            signal_generator.generate_signal_from_two_signals(operation, first_signal, second_signal)
        else:
            app_params = {}
            for k in params_val_dict:
                app_params[k] = params_val_dict[k].get()

            signal_generator = SignalGenerator(signal_type, app_params)
            signal_generator.generate_signal()

        self.signal = signal_generator.signal
        fig = signal_generator.plot_signal()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        save_button = ttk.Button(self, text="Zapisz sygnał", command = lambda: self.choose_file_and_save(signal_generator))
        save_button.pack()

    def choose_file_and_save(self, signal_generator):
        file_path = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Pliki binarne", "*.bin")])
        if file_path:
            signal_generator.save_to_file(file_path)
