from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QFrame, QTabWidget, QGroupBox, QLabel, QGridLayout, QSpinBox, QCheckBox, QPushButton                      )
from PySide6.QtGui import (QCursor, QPixmap)
from PySide6.QtCore import Qt
import os

class SetupWidget(QWidget):
    def __init__(self, simulator):
        self.simulator = simulator
        self.layout = QVBoxLayout()
        super().__init__()
        self.IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'images', 'a_modifier.jpg')
        self.init_ui()
    
    def validate_edition(self):
        self.simulator["object"].update_battery(self.capacity.value(), self.charge_box.value())
        self.edit_button.toggle()
        print(self.simulator["object"].get_state())
        
    def init_ui(self):
        result = QGroupBox("Setup Simulator")
        welcomeText = QLabel("<h1>Smart Grid Simulator<h1>")
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
        
        layout = QVBoxLayout(result)
        layout.addWidget(welcomeText)
        
        # Add Batterry Image
        image_label = QLabel(self)
        pixmap = QPixmap(self.IMAGE_PATH)
        image_label.setPixmap(pixmap)
        image_label.resize(pixmap.width(), pixmap.height())
        layout.addWidget(image_label)
        
        v_battery_frame = QFrame(self)
        v_battery_layout = QHBoxLayout(v_battery_frame)
        v_battery_layout.addWidget(battery_label)
        v_battery_layout.addWidget(self.capacity)
        v_battery_layout.addWidget(charge_label)
        v_battery_layout.addWidget(self.charge_box)
        layout.addWidget(v_battery_frame)
        v_edition_frame = QFrame(self)
        v_edition_layout = QHBoxLayout(v_edition_frame)
        v_edition_layout.addWidget(self.edit_button)
        v_edition_layout.addWidget(validate_button)
        layout.addWidget(v_edition_frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(result)
        self.setLayout(layout)
