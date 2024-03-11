import tkinter as tk
from tkinter import ttk
from signal_generator import SignalGenerator, SIGNAL_TYPES
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

class SignalGenerationTab(ttk.Frame):
    def __init__(self, tabs):
        super().__init__(tabs)
        self.tabs = tabs
        self.create_widgets()
        self.card_number = 1

    def create_widgets(self):
        signal_params_frame = ttk.LabelFrame(self, text="Parametry sygnału")
        signal_params_frame.pack(pady=20, padx=20, fill="both", expand=True)

        row_number = 0

        params_val_dict = {
            'amplitude': tk.DoubleVar(value=10.0),
            'start_time': tk.DoubleVar(value=0.0),
            'duration': tk.DoubleVar(value=10.0),
            'period': tk.DoubleVar(value=1.0),
            'fill_factor': tk.DoubleVar(value=0.5),
            'probability': tk.DoubleVar(value=0.02),
            'jump_number': tk.IntVar(value=20),
            'time_shift': tk.DoubleVar(value=4.0),
            'frequency': tk.IntVar(value=100),
        }

        label_text_dict = {
            'amplitude': "Amplituda:",
            'start_time': "Czas początkowy:",
            'duration': "Czas trwania:",
            'period': "Okres podstawy:",
            'fill_factor': "Współczynnik wypełnienia:",
            'probability': "Prawdopodobieństwo:",
            'jump_number': "Numer próbki skoku:",
            'time_shift': "Czas skoku:",
            'frequency': "Częstotliwość",
        }

        signal_type_label = ttk.Label(signal_params_frame, text="Typ sygnału:")
        signal_type_label.grid(row=row_number, column=0, sticky="w")

        signal_types_keys = list(SIGNAL_TYPES.keys())
        signal_types_values = list(SIGNAL_TYPES.values())

        signal_type_var = tk.StringVar(value=signal_types_values[0])

        signal_type_menu = ttk.Combobox(signal_params_frame, textvariable=signal_type_var, values=signal_types_values, width=50)
        signal_type_menu.grid(row=row_number, column=1, padx=5, sticky="w")

        for key in label_text_dict:
            row_number += 1
            self.render_input(signal_params_frame, label_text_dict[key], row_number, params_val_dict[key])

        row_number += 1
        generate_button = ttk.Button(
            signal_params_frame,
            text="Generuj Wykres",
            command=lambda: self.generate_and_show_plot(
                signal_types_keys[signal_types_values.index(signal_type_var.get())],
                params_val_dict
            )
        )
        generate_button.grid(row=row_number, columnspan=2, pady=10)

    def generate_and_show_plot(self, signal_type, params_val_dict):
        app_params = {}
        for k in params_val_dict:
            app_params[k] = params_val_dict[k].get()

        signal_generator = SignalGenerator(signal_type, app_params)
        signal_generator.generate_signal()

        new_tab = ttk.Frame(self.tabs)
        self.tabs.add(new_tab, text=f"karta {self.card_number}")
        self.card_number += 1
        self.tabs.select(new_tab)

        fig = signal_generator.plot_signal()

        canvas = FigureCanvasTkAgg(fig, master=new_tab)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, new_tab)
        toolbar.update()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        new_tab.mainloop()

    def render_input(self, signal_params_frame, label_text, row_number, default_value):
        label = ttk.Label(signal_params_frame, text=label_text)
        label.grid(row=row_number, column=0, sticky="w")

        entry = ttk.Entry(signal_params_frame, textvariable=default_value)
        entry.grid(row=row_number, column=1, padx=10, sticky="w")
