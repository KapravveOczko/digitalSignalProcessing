import tkinter as tk
import struct
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from visualizers.signal_visualizer import SignalVisualizer

class SignalFrame(ttk.Frame):
    def __init__(self, container, generator):
        super().__init__(container)

        self.generator = generator
        self.generator.generate_signal()

        self.signal = self.generator.signal
        if self.generator.original_signal is not None:
            self.original_signal = self.generator.original_signal
            self.original_time = self.generator.original_time
        else:
            self.original_signal = None
            self.original_time = None
        self.parameters = self.generator.parameters
        self.f_multiplier = self.generator.f_multiplier
        self.signal_type = self.generator.signal_type
        self.time = self.generator.time

        self.signal_visualization = SignalVisualizer(*generator.return_params())

        fig = self.signal_visualization.plot_signal()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        save_button = ttk.Button(self, text="Zapisz sygnał", command = lambda: self.choose_file_and_save())
        save_button.pack()

    def choose_file_and_save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Pliki binarne", "*.bin")])
        if file_path:
            self.save_to_file(file_path)

    def save_to_file(self, path):
        with open(path, 'wb') as file:
            file.write(struct.pack('d', self.parameters['start_time']))
            file.write(struct.pack('d', self.parameters['duration']))
            file.write(struct.pack('d', self.f_multiplier))
            file.write(struct.pack('d', int(self.signal_type[1::])))
            for point in self.signal:
                file.write(struct.pack('d', point))
