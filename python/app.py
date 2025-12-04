import sys
import os
from PySide6.QtWidgets import QApplication
from simulator_gui import Widgets


if __name__ == '__main__':
    app = QApplication()
    simulator = Widgets()
    style_path = os.path.join(os.path.dirname(__file__), 'simulator_ui', 'style.qss')
    with open(style_path, "r") as f:
        style_file = f.read()
        simulator.setStyleSheet(style_file)
    simulator.show()
    sys.exit(app.exec())