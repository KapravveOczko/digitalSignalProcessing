import tkinter as tk
from tkinter import ttk
from signal_generator import OPERATION_TYPES
from signal_frame import SignalFrame

def create_operation_on_signals_widgets(notebook_instance):
    notebook_instance.operation_frame = ttk.Frame(notebook_instance)

    notebook_instance.add(notebook_instance.operation_frame, text="Operacje na sygnałach")

    operation_frame = ttk.LabelFrame(notebook_instance.operation_frame, text="Operacje na sygnałach")
    operation_frame.pack(pady=20, padx=20, fill="both", expand=True)

    row_number = 0

    operation_types_keys = list(OPERATION_TYPES.keys())
    operation_types_values = list(OPERATION_TYPES.values())

    operation_label = notebook_instance.create_label(operation_frame, "Wybierz Operacje", row_number)
    operation = tk.StringVar()
    operation_option_menu = ttk.OptionMenu(operation_frame, operation, operation_types_values[0], *operation_types_values)
    operation_option_menu.grid(column=1, row=row_number)

    row_number += 1
    notebook_instance.tab_names = [notebook_instance.tab(tab_id, "text") for tab_id in notebook_instance.tabs()[2::]]

    first_tab_label = notebook_instance.create_label(operation_frame, "Pierwszy Sygnał", row_number)
    notebook_instance.first_tab = tk.StringVar(value="")
    notebook_instance.first_tab_menu = ttk.Combobox(operation_frame, textvariable=notebook_instance.first_tab, values=[])
    notebook_instance.first_tab_menu.grid(column=1, row=row_number)

    row_number += 1
    second_tab_label = notebook_instance.create_label(operation_frame, "Drugi Sygnał", row_number)
    notebook_instance.second_tab = tk.StringVar(value="")
    notebook_instance.second_tab_menu = ttk.Combobox(operation_frame, textvariable=notebook_instance.second_tab, values=[])
    notebook_instance.second_tab_menu.grid(column=1, row=row_number)

    row_number += 1
    generate_button = ttk.Button(
        operation_frame,
        text = "Generuj Wykres",
        command = lambda: generate_and_show_plot_from_two_signals(
            notebook_instance,
            operation_types_keys[operation_types_values.index(operation.get())],
            get_tab_by_name(notebook_instance, notebook_instance.first_tab.get()),
            get_tab_by_name(notebook_instance, notebook_instance.second_tab.get())
        )
    )
    generate_button.grid(column=1, row=row_number)

def get_tab_by_name(notebook_instance, tab_name):
    for tab in notebook_instance.tabs():
        if notebook_instance.tab(tab, "text") == tab_name:
            return notebook_instance.nametowidget(tab)


def generate_and_show_plot_from_two_signals(notebook_instance, operation, first_signal, second_signal):
    first_signal = first_signal.signal
    second_signal = second_signal.signal
    if len(first_signal) == len(second_signal):
        new_tab = SignalFrame(notebook_instance, operation=operation, first_signal=first_signal, second_signal=second_signal)
        notebook_instance.add(new_tab, text=f"karta {notebook_instance.card_number}")
        notebook_instance.card_number += 1
        notebook_instance.select(new_tab)
        notebook_instance.update_tab_list()