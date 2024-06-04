import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from generators.signal_generator import SignalGenerator, SIGNAL_TYPES, WINDOW_TYPES
from generators.signal_from_file_generator import SignalFromFileGenerator

def create_generate_signals_widget(notebook_instance):
    notebook_instance.generate_frame = ttk.Frame(notebook_instance)
    notebook_instance.add(notebook_instance.generate_frame, text="Generuj Wykres")
    notebook_instance.select(notebook_instance.generate_frame)
    signal_params_frame = ttk.LabelFrame(notebook_instance.generate_frame, text="Parametry sygnału")
    signal_params_frame.pack(pady=20, padx=20, fill="both", expand=True)


    all_options_for_signal = []
    all_options_for_filter = []
    row_number = 0
    row_number_for_filter = 1

    params_val_for_filter_dict = {
        'sampling_rate': tk.IntVar(value=10000),
        'order': tk.IntVar(value=125),
        'cut_off_frequency': tk.IntVar(value=50),
    }

    label_text_for_filter_dict = {
        'sampling_rate': "Częstotliwość próbkowania (fd):",
        'order': "Rząd filtru (M):",
        'cut_off_frequency': "Częstotliwość odcięcia (f0):",
    }

    params_val_dict = {
        'amplitude': tk.DoubleVar(value=1.0),
        'start_time': tk.DoubleVar(value=0.0),
        'duration': tk.DoubleVar(value=0.1),
        'period': tk.DoubleVar(value=0.01),
        'fill_factor': tk.DoubleVar(value=0.5),
        'probability': tk.DoubleVar(value=0.2),
        'jump_number': tk.IntVar(value=20),
        'time_shift': tk.DoubleVar(value=4.0),
        'frequency': tk.IntVar(value=10000),
        'hist_bins': tk.IntVar(value=10),
    }

    label_text_dict = {
        'amplitude': "Amplituda:",
        'start_time': "Czas początkowy:",
        'duration': "Czas trwania:",
        'period': "Okres podstawowy:",
        'fill_factor': "Współczynnik wypełnienia:",
        'probability': "Prawdopodobieństwo:",
        'jump_number': "Numer próbki skoku:",
        'time_shift': "Czas skoku:",
        'frequency': "Częstotliwość",
    }

    notebook_instance.create_label(signal_params_frame, "Typ sygnału:", row_number)

    signal_types_keys = list(SIGNAL_TYPES.keys())
    signal_types_values = list(SIGNAL_TYPES.values())

    signal_type_var = tk.StringVar(value=signal_types_values[2])

    signal_type_menu = ttk.Combobox(signal_params_frame, textvariable=signal_type_var, values=signal_types_values, width=42)
    signal_type_menu.grid(row=row_number, column=1, padx=5, sticky="w")

    for key in label_text_dict:
        row_number += 1
        elements = render_input(notebook_instance, signal_params_frame, label_text_dict[key], row_number, params_val_dict[key])
        for element in elements:
            all_options_for_signal.append(element)

    for key in label_text_for_filter_dict:
        params_val_dict[key] = params_val_for_filter_dict[key]
        row_number_for_filter += 1
        elements = render_input(notebook_instance, signal_params_frame, label_text_for_filter_dict[key], row_number_for_filter, params_val_for_filter_dict[key])
        for element in elements:
            all_options_for_filter.append(element)


    row_number_for_filter += 1
    signal_for_filter_label = notebook_instance.create_label(signal_params_frame, "Sygnał", row_number_for_filter)
    signal_for_filter_var = tk.StringVar(value="")
    params_val_dict['card'] = signal_for_filter_var
    notebook_instance.signal_for_filter_menu = ttk.Combobox(signal_params_frame, textvariable=signal_for_filter_var, values=[], width=25)
    notebook_instance.signal_for_filter_menu.grid(column=1, row=row_number_for_filter, padx=5, sticky="w")

    window_types_values = list(WINDOW_TYPES.values())

    window_type_var = tk.StringVar(value=window_types_values[0])
    params_val_dict['window_type'] = window_type_var

    row_number_for_filter += 1
    window_type_label = notebook_instance.create_label(signal_params_frame, "typ okna:", row_number_for_filter)

    window_type_menu = ttk.Combobox(signal_params_frame, textvariable=window_type_var, values=window_types_values, width=25)
    window_type_menu.grid(row=row_number_for_filter, column=1, padx=5, sticky="w")

    all_options_for_filter.append(window_type_label)
    all_options_for_filter.append(window_type_menu)
    all_options_for_filter.append(signal_for_filter_label)
    all_options_for_filter.append(notebook_instance.signal_for_filter_menu)

    row_number += 1
    hist_bins_label = notebook_instance.create_label(signal_params_frame, "Przedział histogramu:", row_number)

    hist_bins_menu = ttk.Combobox(signal_params_frame, textvariable=params_val_dict['hist_bins'], values=[
        5, 10, 15, 20
    ])
    hist_bins_menu.grid(row=row_number, column=1, padx=5, sticky="w")

    update_extra_fields(signal_type_var.get(), all_options_for_signal, all_options_for_filter)

    row_number += 1
    generate_button = ttk.Button(
        signal_params_frame,
        text = "Generuj Wykres",
        command = lambda: generate_and_show_plot_from_form(
            notebook_instance,
            signal_types_keys[signal_types_values.index(signal_type_var.get())],
            params_val_dict
        )
    )
    generate_button.grid(row=row_number, column=0, pady=10)

    signal_type_var.trace_add("write", lambda *args: update_extra_fields(signal_type_var.get(), all_options_for_signal, all_options_for_filter))

    read_button = ttk.Button(
        signal_params_frame,
        text = "Odczytaj Wykres z pliku",
        command = lambda: generate_and_show_plot_from_file(notebook_instance)
    )
    read_button.grid(row=row_number, column=1, pady=10)

def generate_and_show_plot_from_form(notebook_instance, signal_type, params_val_dict):
    params_val_dict['card_to_filter'] = notebook_instance.get_tab_by_name(params_val_dict['card'].get())
    notebook_instance.generate_and_show_plot(SignalGenerator, [signal_type, params_val_dict])

def generate_and_show_plot_from_file(notebook_instance):
    file_path = filedialog.askopenfilename(defaultextension=".bin", filetypes=[("Pliki binarne", "*.bin")])
    if file_path:
        notebook_instance.generate_and_show_plot(SignalFromFileGenerator, [file_path])

def render_input(notebook_instance, signal_params_frame, label_text, row_number, default_value):
    label = notebook_instance.create_label(signal_params_frame, label_text, row_number)
    entry = notebook_instance.create_entry(signal_params_frame, default_value, row_number)
    return [label, entry]


def update_extra_fields(operation, all_options_for_signal_dict, all_options_for_filter_dict):
    all_options_to_render = None
    all_options_to_remove = None

    if operation[0] == 's':
        all_options_to_render = all_options_for_signal_dict
        all_options_to_remove = all_options_for_filter_dict
    else:
        all_options_to_render = all_options_for_filter_dict
        all_options_to_remove = all_options_for_signal_dict

    for element in all_options_to_render:
        element.grid()

    for element in all_options_to_remove:
        element.grid_remove()