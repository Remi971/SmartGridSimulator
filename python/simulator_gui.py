from PySide6.QtCore import (Qt, QTimer)
from PySide6.QtGui import (QCursor, QDoubleValidator)
from PySide6.QtWidgets import (QDialog, QWidget, QLabel, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QTabWidget, QLineEdit, QTableWidget)
from grid_simulator import GridSimulator
from simulator_ui.setup_ui import SetupWidget
from simulator_ui.setting_ui import SettingWidget
from simulator_ui.results_ui import ResultsWidget
from simulator_ui.generator_ui import GeneratorUI


MENU_ITEMS = [
    {"id": "setup", "label": "Setup Simulator", "class": SetupWidget},
    {"id": "settings", "label": "Settings", "class": SettingWidget},
    {"id": "results", "label": "Results", "class": ResultsWidget},
    # {"id": "generator", "label": "Data Generator", "class": GeneratorUI},
]

class Widgets(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Grid Simulator")
        self.setMinimumSize(800, 600)
        self.layout = QVBoxLayout(self)
        self.simulator = {
            "object": GridSimulator(battery_capacity=200.0, charge_rate=20.0), 
            "state": {
                'battery': {
                    'capacity': 'N/A', 
                    'stored_energy': 'N/A'
                    }, 
                'producers': {
                    'solar': 'N/A', 
                    'wind': 'N/A', 
                    'grid': 'N/A'
                    }, 
                'consumers': {
                    'household': 'N/A', 
                    'industry': 'N/A'
                    }
                },
            "plot_linear_data": {
                "time": [],
                "battery": [],
                "solar": [],
                "wind": [],
                "demand": []
            },
            "timer": QTimer(),
            "table": {
                "producer": QTableWidget(),
                "consumer": QTableWidget()
            }
        }
        
        self.tabs = QTabWidget()
        
        for item in MENU_ITEMS:
            if 'class' in item:
                self.addTab(self.simulator, self.tabs, item["label"], item["class"])
              
        self.layout.addWidget(self.tabs)
        
    def addTab(self, simulator: dict[str, any], tabs: QTabWidget, label: str, Widget: QWidget) -> None:
        widget = Widget(simulator)
        tabs.addTab(widget, label)         
       
    def condition_simulator(self):
        condition = QWidget()
        self.tabs.addTab(condition, "Conditions de Simulation")
        condition.layout = QVBoxLayout(self)
        
        result = QGroupBox("Run Simulation")
        infoText = QLabel("<h2>Simuler les conditions.<h2>")
        infoText.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        header = [str(x) for x in range(24)]
        simulation_table = QTableWidget(self)
        simulation_table.setColumnCount(len(header))
        simulation_table.setHorizontalHeaderLabels(header)
        simulation_table.setRowCount(0)
        simulation_table.setColumnCount(len(header))
        
        weather_label = QLabel("Weather Factor (0.0 to 1.0):")
        weather_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        weather_input = QDoubleValidator(0.0, 1.0, 2)
        weather_line_edit = QLineEdit()
        weather_line_edit.setValidator(weather_input)
        weather_line_edit.setText("0.5")
        
        simulate_button = QPushButton("Simulate Condition", self)
        simulate_button.setCursor(QCursor(Qt.PointingHandCursor))
        
        layout = QGridLayout(result)
        layout.addWidget(infoText, 0, 0, 1, 2)
        layout.addWidget(simulation_table, 1, 0, 1, 2)
        layout.addWidget(weather_label, 2, 0)
        layout.addWidget(weather_line_edit, 2, 1)
        layout.addWidget(simulate_button, 3, 0, 1, 2)
        condition.layout.addWidget(result)
        condition.setLayout(layout)
        
 
    