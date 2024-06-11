import tkinter as tk
from tkinter import ttk
from generators.signal_processer_generator import SignalProcesser, PROCESSING_OPERATIONS_TYPES, QUANTIZATION_METHOD, RECONSTRUCTION_METHOD, TRANSFORMATION_METHOD
from generators.signal_transformation_generator import SignalTransformationGenerator
from visualizers.signal_transformation import SignalTransformation

def create_processing_widget(notebook_instance):
    notebook_instance.processing_frame = ttk.Frame(notebook_instance)
    notebook_instance.add(notebook_instance.processing_frame, text="Konwersja sygnałów")

    processing_signal_frame = ttk.LabelFrame(notebook_instance.processing_frame, text="Konwersja sygnałów")
    processing_signal_frame.pack(pady=20, padx=20, fill="both", expand=True)

    params_val_dict = {
        'sampling_rate': tk.IntVar(value=10),
        'quantization_level': tk.IntVar(value=1),
        'quantization_method': tk.StringVar(value=""),
        'reconstruction_method': tk.StringVar(value=""),
        'transformation_method': tk.StringVar(value=""),
        'sinc_parameter': tk.IntVar(value=1),
    }

    row_number = 0

    processing_operation_types_keys = list(PROCESSING_OPERATIONS_TYPES.keys())
    processing_operation_types_values = list(PROCESSING_OPERATIONS_TYPES.values())

    notebook_instance.create_label(processing_signal_frame, "Wybierz Operacje", row_number)
    processing_operation = tk.StringVar()
    processing_operation_menu = ttk.OptionMenu(processing_signal_frame, processing_operation, processing_operation_types_values[0], *processing_operation_types_values)
    processing_operation_menu.grid(column=1, row=row_number, padx=10, sticky="w")

    row_number += 1
    notebook_instance.tab_names = [notebook_instance.tab(tab_id, "text") for tab_id in notebook_instance.tabs()[notebook_instance.stable_card_number::]]

    notebook_instance.create_label(processing_signal_frame, "Wybierz Sygnał", row_number)
    notebook_instance.signal_to_process = tk.StringVar(value="")
    notebook_instance.signal_to_process_menu = ttk.Combobox(processing_signal_frame, textvariable=notebook_instance.signal_to_process, values=[])
    notebook_instance.signal_to_process_menu.grid(column=1, row=row_number, padx=10, sticky="w")

    row_number += 1

    quantization_method_keys = list(QUANTIZATION_METHOD.keys())
    quantization_method_values = list(QUANTIZATION_METHOD.values())
    q_operation_label = notebook_instance.create_label(processing_signal_frame, "Wybierz metodę:", row_number)
    q_operation_menu = ttk.OptionMenu(processing_signal_frame, params_val_dict['quantization_method'], quantization_method_values[0], *quantization_method_values)
    q_operation_menu.grid(column=1, row=row_number, padx=10, sticky="w")

    reconstruction_method_keys = list(RECONSTRUCTION_METHOD.keys())
    reconstruction_method_values = list(RECONSTRUCTION_METHOD.values())
    r_operation_label = notebook_instance.create_label(processing_signal_frame, "Wybierz metodę:", row_number)
    r_operation_menu = ttk.OptionMenu(processing_signal_frame, params_val_dict['reconstruction_method'], reconstruction_method_values[0], *reconstruction_method_values)
    r_operation_menu.grid(column=1, row=row_number, padx=10, sticky="w")

    transformation_method_keys = list(TRANSFORMATION_METHOD.keys())
    transformation_method_values = list(TRANSFORMATION_METHOD.values())
    t_operation_label = notebook_instance.create_label(processing_signal_frame, "Wybierz metodę:", row_number)
    t_operation_menu = ttk.OptionMenu(processing_signal_frame, params_val_dict['transformation_method'], transformation_method_values[0], *transformation_method_values)
    t_operation_menu.grid(column=1, row=row_number, padx=10, sticky="w")

    row_number += 1
    sampling_rate_label = notebook_instance.create_label(processing_signal_frame, "Częstotliwość próbkowania:", row_number)
    sampling_rate_entry = notebook_instance.create_entry(processing_signal_frame, params_val_dict['sampling_rate'], row_number)

    quantization_level_label = notebook_instance.create_label(processing_signal_frame, "Poziom kwantyzacji:", row_number)
    quantization_level_entry = notebook_instance.create_entry(processing_signal_frame, params_val_dict['quantization_level'], row_number)

    sinc_parameter_label = notebook_instance.create_label(processing_signal_frame, "paramert sinc:", row_number)
    sinc_parameter_entry = notebook_instance.create_entry(processing_signal_frame, params_val_dict['sinc_parameter'], row_number)

    all_options_dict = {
        'P': [
            sampling_rate_label,
            sampling_rate_entry,
        ],
        'Q': [
            q_operation_label,
            q_operation_menu,
            quantization_level_label,
            quantization_level_entry,
        ],
        'R': [
            r_operation_label,
            r_operation_menu,
            sinc_parameter_label,
            sinc_parameter_entry,
        ],
        'T': [
            t_operation_label,
            t_operation_menu,
        ],
    }

    update_extra_fields(processing_operation.get(), all_options_dict)

    row_number += 1
    generate_button = ttk.Button(
        processing_signal_frame,
        text = "Generuj Wykres",
        command = lambda: generate_and_show_plot_after_processing(
            notebook_instance,
            processing_operation_types_keys[processing_operation_types_values.index(processing_operation.get())],
            notebook_instance.get_tab_by_name(notebook_instance.signal_to_process.get()),
            params_val_dict
        )
    )
    generate_button.grid(column=1, row=row_number)

    processing_operation.trace_add("write", lambda *args: update_extra_fields(processing_operation.get(), all_options_dict))


def update_extra_fields(operation, all_options_dict):
    for symbol in PROCESSING_OPERATIONS_TYPES:
        if operation == PROCESSING_OPERATIONS_TYPES[symbol]:
            for key in all_options_dict:
                if key == symbol:
                    for option in all_options_dict[key]:
                        option.grid()
                else:
                    for option in all_options_dict[key]:
                        option.grid_remove()
            break


def generate_and_show_transformation_plots(notebook_instance, operation, signal):
    signal_transformation_generator = SignalTransformationGenerator(notebook_instance, operation, signal, SignalTransformation)

    return signal_transformation_generator.return_tabs()

def generate_and_show_plot_after_processing(notebook_instance, operation, signal, params_val_dict):
    quantization_method_keys = list(QUANTIZATION_METHOD.keys())
    quantization_method_values = list(QUANTIZATION_METHOD.values())
    reconstruction_method_keys = list(RECONSTRUCTION_METHOD.keys())
    reconstruction_method_values = list(RECONSTRUCTION_METHOD.values())
    transformation_method_keys = list(TRANSFORMATION_METHOD.keys())
    transformation_method_values = list(TRANSFORMATION_METHOD.values())

    transformation_operation = transformation_method_keys[transformation_method_values.index(params_val_dict['transformation_method'].get())]

    params = {
        'sampling_rate': params_val_dict['sampling_rate'].get(),
        'quantization_level': params_val_dict['quantization_level'].get(),
        'quantization_method': quantization_method_keys[quantization_method_values.index(params_val_dict['quantization_method'].get())],
        'reconstruction_method': reconstruction_method_keys[reconstruction_method_values.index(params_val_dict['reconstruction_method'].get())],
        'sinc_parameter': params_val_dict['sinc_parameter'].get(),
        'start_time': signal.parameters['start_time'],
        'duration': signal.parameters['duration'],
        'original_signal': signal.original_signal,
        'original_time': signal.original_time,
        'time': signal.time,
    }

    if operation != 'T':
        new_tab = notebook_instance.generate_and_show_plot(SignalProcesser, [operation, signal.signal, params])
        if new_tab.original_signal is None:
            new_tab.original_signal = signal.signal
            new_tab.original_time = signal.time

    else:
        new_tabs = generate_and_show_transformation_plots(notebook_instance, transformation_operation, signal)
        for tab in new_tabs:
            notebook_instance.add(tab, text=f"karta {notebook_instance.card_number}")
            notebook_instance.card_number += 1
            notebook_instance.select(tab)
            notebook_instance.update_tab_list()
