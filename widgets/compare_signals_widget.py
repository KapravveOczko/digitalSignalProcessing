import tkinter as tk
from tkinter import ttk
from visualizers.signal_comperator import SignalComperator

def create_compare_signals_widget(notebook_instance):
    notebook_instance.compare_signals_frame = ttk.Frame(notebook_instance)

    notebook_instance.add(notebook_instance.compare_signals_frame, text="Porównaj sygnały")

    compare_signals_frame = ttk.LabelFrame(notebook_instance.compare_signals_frame, text="Porównaj sygnały")
    compare_signals_frame.pack(pady=20, padx=20, fill="both", expand=True)

    row_number = 0

    notebook_instance.tab_names = [notebook_instance.tab(tab_id, "text") for tab_id in notebook_instance.tabs()[3::]]

    notebook_instance.create_label(compare_signals_frame, "Pierwszy Sygnał", row_number)
    notebook_instance.first_compare_tab = tk.StringVar(value="")
    notebook_instance.first_compare_tab_menu = ttk.Combobox(compare_signals_frame, textvariable=notebook_instance.first_compare_tab, values=[])
    notebook_instance.first_compare_tab_menu.grid(column=1, row=row_number)

    row_number += 1
    notebook_instance.create_label(compare_signals_frame, "Drugi Sygnał", row_number)
    notebook_instance.second_compare_tab = tk.StringVar(value="")
    notebook_instance.second_compare_tab_menu = ttk.Combobox(compare_signals_frame, textvariable=notebook_instance.second_compare_tab, values=[])
    notebook_instance.second_compare_tab_menu.grid(column=1, row=row_number)

    row_number += 1
    generate_button = ttk.Button(
        compare_signals_frame,
        text = "Porównaj sygnały",
        command = lambda: generate_and_show_plot_for_compare_two_signals(
            notebook_instance,
            notebook_instance.get_tab_by_name(notebook_instance.first_compare_tab.get()),
            notebook_instance.get_tab_by_name(notebook_instance.second_compare_tab.get())
        )
    )
    generate_button.grid(column=1, row=row_number)

    def generate_and_show_plot_for_compare_two_signals(notebook_instance, first_signal, second_signal):
        new_tab = SignalComperator(notebook_instance, first_signal, second_signal)
        notebook_instance.add(new_tab, text=f"Porównanie {notebook_instance.card_number}")
        notebook_instance.card_number += 1
        notebook_instance.select(new_tab)
        notebook_instance.update_tab_list()
        return new_tab