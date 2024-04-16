import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from signal_generator import SIGNAL_TYPES
from signal_frame import SignalFrame

def create_generate_signals_widgets(notebook_instance):
    notebook_instance.generate_frame = ttk.Frame(notebook_instance)
    notebook_instance.add(notebook_instance.generate_frame, text="Generuj Wykres")
    notebook_instance.select(notebook_instance.generate_frame)
    signal_params_frame = ttk.LabelFrame(notebook_instance.generate_frame, text="Parametry sygnału")
    signal_params_frame.pack(pady=20, padx=20, fill="both", expand=True)

    row_number = 0

    params_val_dict = {
        'amplitude': tk.DoubleVar(value=10.0),
        'start_time': tk.DoubleVar(value=0.0),
        'duration': tk.DoubleVar(value=10.0),
        'period': tk.DoubleVar(value=1.0),
        'fill_factor': tk.DoubleVar(value=0.5),
        'probability': tk.DoubleVar(value=0.2),
        'jump_number': tk.IntVar(value=20),
        'time_shift': tk.DoubleVar(value=4.0),
        'frequency': tk.IntVar(value=1000),
        'hist_bins': tk.IntVar(value=10),
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

    signal_type_label = notebook_instance.create_label(signal_params_frame, "Typ sygnału:", row_number)

    signal_types_keys = list(SIGNAL_TYPES.keys())
    signal_types_values = list(SIGNAL_TYPES.values())

    signal_type_var = tk.StringVar(value=signal_types_values[0])

    signal_type_menu = ttk.Combobox(signal_params_frame, textvariable=signal_type_var, values=signal_types_values, width=50)
    signal_type_menu.grid(row=row_number, column=1, padx=5, sticky="w")

    for key in label_text_dict:
        row_number += 1
        render_input(notebook_instance, signal_params_frame, label_text_dict[key], row_number, params_val_dict[key])

    row_number += 1
    hist_bins_label = notebook_instance.create_label(signal_params_frame, "Przedział histogramu:", row_number)

    hist_bins_menu = ttk.Combobox(signal_params_frame, textvariable=params_val_dict['hist_bins'], values=[
        5, 10, 15, 20
    ])
    hist_bins_menu.grid(row=row_number, column=1, padx=5, sticky="w")

    row_number += 1
    generate_button = ttk.Button(
        signal_params_frame,
        text = "Generuj Wykres",
        command = lambda: generate_and_show_plot(
            notebook_instance,
            signal_types_keys[signal_types_values.index(signal_type_var.get())],
            params_val_dict
        )
    )
    generate_button.grid(row=row_number, column=0, pady=10)

    read_button = ttk.Button(
        signal_params_frame,
        text = "Odczytaj Wykres z pliku",
        command = lambda: generate_and_show_plot_from_file(notebook_instance)
    )
    read_button.grid(row=row_number, column=1, pady=10)

def generate_and_show_plot(notebook_instance, signal_type, params_val_dict):
    new_tab = SignalFrame(notebook_instance, signal_type, params_val_dict)
    notebook_instance.add(new_tab, text=f"karta {notebook_instance.card_number}")
    notebook_instance.card_number += 1
    notebook_instance.select(new_tab)

    notebook_instance.update_tab_list()

def generate_and_show_plot_from_file(notebook_instance):
    file_path = filedialog.askopenfilename(defaultextension=".bin", filetypes=[("Pliki binarne", "*.bin")])
    if file_path:
        new_tab = SignalFrame(notebook_instance, file_path=file_path)
        notebook_instance.add(new_tab, text=f"karta {notebook_instance.card_number}")
        notebook_instance.card_number += 1
        notebook_instance.select(new_tab)
        notebook_instance.update_tab_list()

def render_input(notebook_instance, signal_params_frame, label_text, row_number, default_value):
    notebook_instance.create_label(signal_params_frame, label_text, row_number)
    create_entry(notebook_instance, signal_params_frame, default_value, row_number)

def create_entry(notebook_instance, parent, default_value, row_number):
    entry = ttk.Entry(parent, textvariable=default_value)
    entry.grid(row=row_number, column=1, padx=10, sticky="w")
    return entry