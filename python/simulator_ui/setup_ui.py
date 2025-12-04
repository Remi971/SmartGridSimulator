from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QGroupBox, QLabel, QGridLayout, QSpinBox, QCheckBox, QPushButton                      )
from PySide6.QtGui import (QCursor)
from PySide6.QtCore import Qt

class SetupWidget(QWidget):
    def __init__(self, simulator):
        self.simulator = simulator
        self.layout = QVBoxLayout()
        super().__init__()
        self.init_ui()
    
    def validate_edition(self):
        self.simulator["object"].update_battery(self.capacity.value(), self.charge_box.value())
        self.edit_button.toggle()
        print(self.simulator["object"].get_state())
        
    def init_ui(self):
        result = QGroupBox("Setup Simulator")
        welcomeText = QLabel("<h1>Bienvenue dans le simulateur de réseau intelligent!<h1>")
        battery_label = QLabel("Battery Capacity (kWh):")
        battery_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.capacity = QSpinBox()
        self.capacity.setMaximum(1000.0)
        self.capacity.setValue(200.0)
        
        charge_label = QLabel("Charge Rate (kW):")
        charge_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.charge_box = QSpinBox()
        self.charge_box.setMaximum(100.0)
        self.charge_box.setValue(20.0)
        
        self.edit_button = QCheckBox("Edition disabled", self)
        self.edit_button.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.edit_button.toggled.connect(self.charge_box.setDisabled)
        self.edit_button.toggled.connect(self.capacity.setDisabled)
        
        validate_button = QPushButton("validate edition", self)
        validate_button.setCursor(QCursor(Qt.PointingHandCursor))
        validate_button.clicked.connect(lambda : self.validate_edition())
        self.edit_button.toggled.connect(validate_button.setDisabled)
        self.edit_button.toggle()
        
        layout = QGridLayout(result)
        layout.addWidget(welcomeText, 0, 0, 1, 4)
        layout.addWidget(battery_label, 1, 0)
        layout.addWidget(self.capacity, 1, 1, 1, 1)
        layout.addWidget(charge_label, 1, 2)
        layout.addWidget(self.charge_box, 1, 3, 1, 1)
        layout.addWidget(self.edit_button, 2, 1, 1, 1)
        layout.addWidget(validate_button, 2, 2, 1, 1)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(result)
        self.setLayout(layout)



# class SetupUI:
#     def __init__(self, simulator, tabs, label):
#         self.simulator = simulator
#         self.tabs = tabs
#         self.label = label
#         self.initiate()
        
#     def initiate(self):
#         widget = SetupWidget(self.simulator)
#         self.tabs.addTab(widget, self.label)
      
    