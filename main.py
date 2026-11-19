import csv
import sys
from pathlib import Path

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

GITHUB_URL = "https://github.com/GalG1007/HomeWork4-iceCream"


class IceCreamApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ice Cream Profits Analyzer")
        self.resize(800, 620)

        self.temperatures = []
        self.revenues = []

        self._setup_ui()
        self.plot_data() 

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)

        top_layout = QHBoxLayout()
        title_label = QLabel("Ice Cream Sales & Temperature")
        title_label.setObjectName("titleLabel")
        top_layout.addWidget(title_label)

        top_layout.addStretch()

        self.load_button = QPushButton("Load CSV File")
        self.load_button.clicked.connect(self.load_file)
        top_layout.addWidget(self.load_button)

        main_layout.addLayout(top_layout)

        
        self.figure = Figure(figsize=(7, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas)

        bottom_layout = QHBoxLayout()
        self.about_button = QPushButton("About")
        self.about_button.setObjectName("aboutButton")
        self.about_button.clicked.connect(self.show_about)
        bottom_layout.addWidget(self.about_button)
        bottom_layout.addStretch()

        main_layout.addLayout(bottom_layout)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Ice Cream CSV", "", "CSV Files (*.csv);;All Files (*)"
        )
        if not file_path:
            return

        self.temperatures.clear()
        self.revenues.clear()

        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row:
                    self.temperatures.append(float(row[0]))
                    self.revenues.append(float(row[1]))

        self.plot_data()

    def plot_data(self):
        self.ax.clear()

       
        self.ax.plot([0, 1, 2, 3], [10, 30, 20, 40], label="Temporary Data")
        self.ax.set_title("Temporary Graph - Load CSV to update")
        self.ax.legend()



        self.canvas.draw()

    def show_about(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("About")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(
            "<h3>Ice Cream Profits Analyzer</h3>"
            "<p>A PySide6 & Matplotlib application analyzing ice cream revenue vs. temperature.</p>"
            f'<p><b>GitHub Repository:</b> <a href="{GITHUB_URL}">{GITHUB_URL}</a></p>'
        )
        msg.exec()


def load_stylesheet(app: QApplication):
    qss_path = Path(__file__).parent / "style.qss"
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    load_stylesheet(app)
    window = IceCreamApp()
    window.show()
    sys.exit(app.exec())