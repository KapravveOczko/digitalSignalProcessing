import tkinter as tk
from tkinter import ttk
from visualizers.signal_frame import SignalFrame
from widgets.operation_widget import create_operation_on_signals_widget
from widgets.generate_widget import create_generate_signals_widget
from widgets.processing_widget import create_processing_widget
from widgets.compare_signals_widget import create_compare_signals_widget

class CustomNotebook(ttk.Notebook):
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
        self.stable_card_number = 4

        create_compare_signals_widget(self)
        create_processing_widget(self)
        create_operation_on_signals_widget(self)
        create_generate_signals_widget(self)


    def create_entry(self, parent, default_value, row_number):
        entry = ttk.Entry(parent, textvariable=default_value)
        entry.grid(row=row_number, column=1, padx=10, sticky="w")
        return entry

    def create_label(self, parent, label_text, row_number):
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row_number, column=0, sticky="w")
        return label

    def get_tab_by_name(self, tab_name):
        for tab in self.tabs():
            if self.tab(tab, "text") == tab_name:
                return self.nametowidget(tab)

    def update_tab_list(self):
        self.tab_names = [self.tab(tab_id, "text") for tab_id in self.tabs()][self.stable_card_number::]

        self.first_tab_menu['values'] = self.tab_names
        self.first_compare_tab_menu['values'] = self.tab_names
        self.second_tab_menu['values'] = self.tab_names
        self.second_compare_tab_menu['values'] = self.tab_names
        self.signal_to_process_menu['values'] = self.tab_names

        if self.tab_names:
            self.set_tab_values(self.tab_names[0])
        else:
            self.set_tab_values("")

    def set_tab_values(self, value):
        pass
        # self.first_tab_menu.set(value)
        # self.first_tab_menu.set(value)
        # self.second_compare_tab_menu.set(value)
        # self.second_compare_tab_menu.set(value)
        # self.signal_to_process_menu.set(value)
        # self.first_tab.set(value)
        # self.first_tab.set(value)
        # self.second_compare_tab.set(value)
        # self.second_compare_tab.set(value)
        # self.signal_to_process.set(value)

    def generate_and_show_plot(self, generator, parameters):
        new_tab = SignalFrame(self, generator(*parameters))
        self.add(new_tab, text=f"karta {self.card_number}")
        self.card_number += 1
        self.select(new_tab)
        self.update_tab_list()
        return new_tab


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
        self.update_tab_list()

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
