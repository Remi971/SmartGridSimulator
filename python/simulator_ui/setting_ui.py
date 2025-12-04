import random
from PySide6.QtCore import Qt
from PySide6.QtGui import (QCursor)
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QGroupBox, QLabel, QGridLayout, QComboBox, QSpinBox, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout)


class SettingWidget(QWidget):
    def __init__(self, simulator):
        self.simulator = simulator
        super().__init__()
        self.producer_table = simulator['table']['producer']
        self.consumer_table = simulator['table']['consumer']
        self.simulator = simulator['object']
        self.timer = simulator['timer']
        self.state = simulator['state']
        self.layout = QVBoxLayout()
        self.init_ui()
         
    def init_ui(self):
        result = QGroupBox("Settings")
        infoText = QLabel("<h2>Configurez vos producteurs et consommateurs ici.<h2>")
        infoText.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        # Producer Section
        add_producer_box = QGroupBox()
        add_producer_box.setTitle("Add Producer")
        producer_type = QComboBox()
        producer_type.addItems(["solar", "wind", "grid"])
        capacity_input = QSpinBox()
        capacity_input.setMaximum(1000.0)
        capacity_input.setValue(50.0)
        add_producer_button = QPushButton("+", self)
        add_producer_button.setCursor(QCursor(Qt.PointingHandCursor))
        h_p_layout = QHBoxLayout()
        h_p_layout.addWidget(producer_type)
        h_p_layout.addWidget(capacity_input)
        h_p_layout.addWidget(add_producer_button)
        add_producer_box.setLayout(h_p_layout)
        
        header = ["Type", "Capacity (kW)", "Action"]
        self.producer_table.setColumnCount(len(header))
        self.producer_table.setHorizontalHeaderLabels(header)
        self.producer_table.setRowCount(0)
        self.producer_table.setColumnCount(len(header))
       
        add_producer_button.clicked.connect(lambda: self.add_producer_row(producer_type.currentText(), capacity_input.value()))
        
        #Consumer Section 
        add_consumer_box = QGroupBox()
        add_consumer_box.setTitle("Add Consumer")
        consumer_type = QComboBox()
        consumer_type.addItems(["household", "industry"])
        demand_input = QSpinBox()
        demand_input.setMaximum(1000.0)
        demand_input.setValue(50.0)
        add_consumer_button = QPushButton("+", self)
        add_consumer_button.setCursor(QCursor(Qt.PointingHandCursor))
        h_c_layout = QHBoxLayout()
        h_c_layout.addWidget(consumer_type)
        h_c_layout.addWidget(demand_input)
        h_c_layout.addWidget(add_consumer_button)
        add_consumer_box.setLayout(h_c_layout)
        
        header_consumer = ["Type", "Base Demand (kW)", "Action"]
        self.consumer_table.setColumnCount(len(header_consumer))
        self.consumer_table.setHorizontalHeaderLabels(header_consumer)
        self.consumer_table.setRowCount(0)
        self.consumer_table.setColumnCount(len(header_consumer))
        
        add_consumer_button.clicked.connect(lambda: self.add_consumer_row(consumer_type.currentText(), demand_input.value()))
        
        confirm_button = QPushButton("Confirm Settings", self)
        confirm_button.setCursor(QCursor(Qt.PointingHandCursor))
        confirm_button.clicked.connect(self.get_simulator_state)
        
        layout = QGridLayout(result)
        layout.addWidget(infoText, 0, 0, 1, 2)
        layout.addWidget(add_producer_box, 1, 0)
        layout.addWidget(self.producer_table, 2, 0 )
        layout.addWidget(add_consumer_box, 1, 1)
        layout.addWidget(self.consumer_table, 2, 1)
        layout.addWidget(confirm_button, 3, 0, 1, 2)
        self.layout.addWidget(result)
        self.setLayout(layout)
        
    def delete_producer_row(self):
        button = self.delete_producer_button.sender()
        if button:
            row = self.producer_table.indexAt(button.pos()).row()
            self.simulator.remove_producer(row)
            self.producer_table.removeRow(row)
    
    def delete_consumer_row(self):
        button = self.delete_consumer_button.sender()
        if button:
            row = self.consumer_table.indexAt(button.pos()).row()
            self.simulator.remove_consumer(row)
            self.consumer_table.removeRow(row)
        
    def add_producer_row(self, producer_type, capacity):
        row = self.producer_table.rowCount()
        self.producer_table.setRowCount(row + 1)
        print("Adding producer:", row, producer_type, capacity)
        self.producer_table.setItem(row, 0, QTableWidgetItem(producer_type))
        self.producer_table.setItem(row, 1, QTableWidgetItem(str(capacity)))
        self.simulator.add_producer(row, producer_type, capacity)
        self.delete_producer_button = QPushButton("Delete")
        self.delete_producer_button.clicked.connect(self.delete_producer_row)
        self.delete_producer_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.delete_producer_button.setProperty("class", "small_button")
        #delete_button.setDisabled(True)
        self.producer_table.setCellWidget(row, 2, self.delete_producer_button)
        
    def add_consumer_row(self, consumer_type, capacity):
        row = self.consumer_table.rowCount()
        self.consumer_table.setRowCount(row + 1)
        print("Adding consumer:", row, consumer_type, capacity)
        self.consumer_table.setItem(row, 0, QTableWidgetItem(consumer_type))
        self.consumer_table.setItem(row, 1, QTableWidgetItem(str(capacity)))
        self.simulator.add_consumer(row, consumer_type, capacity)
        self.delete_consumer_button = QPushButton("Delete")
        self.delete_consumer_button.clicked.connect(self.delete_consumer_row)
        self.delete_consumer_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.delete_consumer_button.setProperty("class", "small_button")
        #delete_consumer_button.setDisabled(True)
        self.consumer_table.setCellWidget(row, 2, self.delete_consumer_button)
        
    def get_simulator_state(self):
        self.state = self.simulator.get_state()
        if self.state['producers'] and self.state['consumers']:
            weather_factor = random.uniform(0.0, 1.0)
            self.simulator.update()
            self.state = self.simulator.get_state()
            self.timer.start(1000)
        print(self.state)
        #print("Current Simulator State:", self.simulator["state"]) 