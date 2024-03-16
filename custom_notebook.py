import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from signal_generator import SignalGenerator, SIGNAL_TYPES, OPERATION_TYPES
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from signal_frame import SignalFrame

class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

        self.card_number = 1

        self.create_operatin_on_signals_widgets()
        self.create_generate_signals_widgets()

    def create_operatin_on_signals_widgets(self):
        self.operation_frame = ttk.Frame(self)
        self.add(self.operation_frame, text="Operacje na sygnałach")

        operation_frame = ttk.LabelFrame(self.operation_frame, text="Operacje na sygnałach")
        operation_frame.pack(pady=20, padx=20, fill="both", expand=True)

        row_number = 0

        operation_types_keys = list(OPERATION_TYPES.keys())
        operation_types_values = list(OPERATION_TYPES.values())

        operation_label = self.create_label(operation_frame, "Wybierz Operacje", row_number)
        operation = tk.StringVar()
        operation_option_menu = ttk.OptionMenu(operation_frame, operation, operation_types_values[0], *operation_types_values)
        operation_option_menu.grid(column=1, row=row_number)

        row_number += 1
        self.tab_names = [self.tab(tab_id, "text") for tab_id in self.tabs()[2::]]

        first_tab_label = self.create_label(operation_frame, "Pierwszy Sygnał", row_number)
        self.first_tab = tk.StringVar(value="")
        self.first_tab_menu = ttk.Combobox(operation_frame, textvariable=self.first_tab, values=[])
        self.first_tab_menu.grid(column=1, row=row_number)

        row_number += 1
        second_tab_label = self.create_label(operation_frame, "Drugi Sygnał", row_number)
        self.second_tab = tk.StringVar(value="")
        self.second_tab_menu = ttk.Combobox(operation_frame, textvariable=self.second_tab, values=[])
        self.second_tab_menu.grid(column=1, row=row_number)

        row_number += 1
        generate_button = ttk.Button(
            operation_frame,
            text = "Generuj Wykres",
            command = lambda: self.generate_and_show_plot_from_two_signals(
                operation_types_keys[operation_types_values.index(operation.get())],
                self.get_tab_by_name(self.first_tab.get()),
                self.get_tab_by_name(self.second_tab.get())
            )
        )
        generate_button.grid(column=1, row=row_number)

    def get_tab_by_name(self, tab_name):
        for tab in self.tabs():
            if self.tab(tab, "text") == tab_name:
                return self.nametowidget(tab)


    def generate_and_show_plot_from_two_signals(self, operation, first_signal, second_signal):
        first_signal = first_signal.signal
        second_signal = second_signal.signal
        if len(first_signal) == len(second_signal):
            new_tab = SignalFrame(self, operation=operation, first_signal=first_signal, second_signal=second_signal)
            self.add(new_tab, text=f"karta {self.card_number}")
            self.card_number += 1
            self.select(new_tab)
            self.update_tab_list()


    def create_generate_signals_widgets(self):
        self.generate_frame = ttk.Frame(self)
        self.add(self.generate_frame, text="Generuj Wykres")
        self.select(self.generate_frame)
        signal_params_frame = ttk.LabelFrame(self.generate_frame, text="Parametry sygnału")
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

        signal_type_label = self.create_label(signal_params_frame, "Typ sygnału:", row_number)

        signal_types_keys = list(SIGNAL_TYPES.keys())
        signal_types_values = list(SIGNAL_TYPES.values())

        signal_type_var = tk.StringVar(value=signal_types_values[0])

        signal_type_menu = ttk.Combobox(signal_params_frame, textvariable=signal_type_var, values=signal_types_values, width=50)
        signal_type_menu.grid(row=row_number, column=1, padx=5, sticky="w")

        for key in label_text_dict:
            row_number += 1
            self.render_input(signal_params_frame, label_text_dict[key], row_number, params_val_dict[key])

        row_number += 1
        hist_bins_label = self.create_label(signal_params_frame, "Przedział histogramu:", row_number)

        hist_bins_menu = ttk.Combobox(signal_params_frame, textvariable=params_val_dict['hist_bins'], values=[
            5, 10, 15, 20
        ])
        hist_bins_menu.grid(row=row_number, column=1, padx=5, sticky="w")

        row_number += 1
        generate_button = ttk.Button(
            signal_params_frame,
            text = "Generuj Wykres",
            command = lambda: self.generate_and_show_plot(
                signal_types_keys[signal_types_values.index(signal_type_var.get())],
                params_val_dict
            )
        )
        generate_button.grid(row=row_number, column=0, pady=10)

        read_button = ttk.Button(
            signal_params_frame,
            text = "Odczytaj Wykres z pliku",
            command = self.generate_and_show_plot_from_file
        )
        read_button.grid(row=row_number, column=1, pady=10)

    def generate_and_show_plot(self, signal_type, params_val_dict):
        new_tab = SignalFrame(self, signal_type, params_val_dict)
        self.add(new_tab, text=f"karta {self.card_number}")
        self.card_number += 1
        self.select(new_tab)

        self.update_tab_list()

    def generate_and_show_plot_from_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".bin", filetypes=[("Pliki binarne", "*.bin")])
        if file_path:
            new_tab = SignalFrame(self, file_path=file_path)
            self.add(new_tab, text=f"karta {self.card_number}")
            self.card_number += 1
            self.select(new_tab)
            self.update_tab_list()

    def render_input(self, signal_params_frame, label_text, row_number, default_value):
        self.create_label(signal_params_frame, label_text, row_number)
        self.create_entry(signal_params_frame, default_value, row_number)

    def create_label(self, paren, label_text, row_number):
        label = ttk.Label(paren, text=label_text)
        label.grid(row=row_number, column=0, sticky="w")
        return label

    def create_entry(self, parent, default_value, row_number):
        entry = ttk.Entry(parent, textvariable=default_value)
        entry.grid(row=row_number, column=1, padx=10, sticky="w")
        return entry

    def update_tab_list(self):
        self.tab_names = [self.tab(tab_id, "text") for tab_id in self.tabs()][2::]

        self.first_tab_menu['values'] = self.tab_names
        self.second_tab_menu['values'] = self.tab_names

        if self.tab_names:
            self.set_tab_values(self.tab_names[0])

    def set_tab_values(self, value):
        self.first_tab_menu.set(value)
        self.second_tab_menu.set(value)
        self.first_tab.set(value)
        self.second_tab.set(value)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index(f"@{event.x},{event.y}")
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        if "close" not in element:
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])
