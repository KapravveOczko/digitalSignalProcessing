import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import  QTableWidgetItem, QMessageBox

from Ui_MainWindowUI import Ui_MainWindow
from MplCanvas import MplCanvas
from transmitter import Transmitter


class TransmitterMainAppWindow(Ui_MainWindow):
    def __init__(self):
        self.plot_original = None
        self.plot_reflected = None
        self.plot_correlation = None
        self.antenna = None
        self.timer = QTimer()
        self.timeout: int = 100
        self.plots_time: float = 0


    def setupUi(self, MainWindow):
        Ui_MainWindow.setupUi(self, MainWindow)

        self.connections()

        self.plot_original = MplCanvas(parent=self.vl_plot_original, width=5, height=4, dpi=100)
        self.vl_plot_original.addWidget(self.plot_original)

        self.plot_reflected = MplCanvas(parent=self.plot_original, width=5, height=4, dpi=100)
        self.vl_plot_original.addWidget(self.plot_reflected)

        self.plot_correlation = MplCanvas(parent=self.plot_original, width=5, height=4, dpi=100)
        self.vl_plot_original.addWidget(self.plot_correlation)

        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Czas [s]", "Prawdziwa wartość", "Wartość z czujnika", "Różnica pomiaru"])
        self.tableWidget.setColumnWidth(0, 80)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 150)
        self.set_antenna_parameters()

        self.animationButton.setEnabled(False)
        self.stopButton.setEnabled(False)

    def set_antenna_parameters(self):
        self.Parameter_amount_of_measures.setValue(50)
        self.Parameter_time_unit.setValue(0.5)
        self.Parameter_real_object_speed.setValue(0.5),
        self.Parameter_signal_speed.setValue(100)
        self.Parameter_signal_period.setValue(1)
        self.Parameter_sampling_frequency.setValue(20),
        self.Parameter_buffers_length.setValue(60)
        self.Parameter_reporting_period.setValue(0.5)

    def correlation_analysis(self):
        self.antenna = Transmitter(int(self.Parameter_amount_of_measures.value()), self.Parameter_time_unit.value(),
                             self.Parameter_real_object_speed.value(),
                             self.Parameter_signal_speed.value(), self.Parameter_signal_period.value(),
                             self.Parameter_sampling_frequency.value(),
                             self.Parameter_buffers_length.value(), self.Parameter_reporting_period.value())

        if self.antenna.real_object_speed > self.antenna.signal_speed:
            return

        original_vales, received_values, diff = self.antenna.calculate_all()
        self.antenna.create_plots()

        self.tableWidget.setRowCount(len(original_vales))
        for i in range(len(original_vales)):
            item0 = QTableWidgetItem(f'{self.antenna.time_values[i]:.2f}')
            item0.setTextAlignment(Qt.AlignHCenter)
            item1 = QTableWidgetItem(f'{original_vales[i]}')
            item1.setTextAlignment(Qt.AlignHCenter)
            item2 = QTableWidgetItem(f'{received_values[i]}')
            item2.setTextAlignment(Qt.AlignHCenter)
            item3 = QTableWidgetItem(f'{diff[i]}')
            item3.setTextAlignment(Qt.AlignHCenter)
            self.tableWidget.setItem(i, 0, item0)
            self.tableWidget.setItem(i, 1, item1)
            self.tableWidget.setItem(i, 2, item2)
            self.tableWidget.setItem(i, 3, item3)

        self.update_plots()

        self.animationButton.setEnabled(True)
        self.stopButton.setEnabled(True)

    def update_plot(self):
        self.plots_time += (self.timeout/1000.0)
        self.antenna.create_plots(self.plots_time)
        self.update_plots()

    def update_plots(self):
        self.plot_original.refreshPlot(self.antenna.px, self.antenna.probing_signal, "Sygnal oryginalny", self.antenna.time_unit)
        self.plot_reflected.refreshPlot(self.antenna.fx, self.antenna.feedback_signal, "Sygnal odbity", self.antenna.time_unit)
        self.plot_correlation.refreshPlot(self.antenna.px2, self.antenna.correlation_samples, "Korelacja sygnałów", self.antenna.time_unit)

    def start_animation(self):
        self.timer.start(self.timeout)

    def stop_animation(self):
        self.timer.stop()
        self.plots_time = 0

    def connections(self):
        self.createButton.clicked.connect(self.correlation_analysis)
        self.timer.timeout.connect(self.update_plot)
        self.animationButton.clicked.connect(self.start_animation)
        self.stopButton.clicked.connect(self.stop_animation)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app_window = QtWidgets.QMainWindow()
    ui = TransmitterMainAppWindow()
    ui.setupUi(app_window)
    app_window.show()
    sys.exit(app.exec_())