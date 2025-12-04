import random
from enum import Enum
from PySide6.QtWidgets import (QWidget, QFrame, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QPushButton)
from PySide6.QtCore import (Qt)
from PySide6.QtGui import (QCursor, QPixmap)
from PySide6 import QtCharts
import os
import pyqtgraph as pg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

BATTERY_IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'images', 'Battery.png')

class StopButtonLabel(Enum):
    STOP_SIMULATION = "Stop Simulation"
    RESET_SIMULATION = "Reset Simulation"
    

class ResultsWidget(QWidget):
    def __init__(self, simulator):
        super().__init__()
        self.simulator = simulator["object"]
        self.layout = QVBoxLayout()
        self.state = simulator['state']
        self.timer = simulator['timer']
        self.plot_linear_data = simulator['plot_linear_data']
        self.plot_graph = pg.PlotWidget(title="Energy Balance Over Time")
        self.table_producer = simulator['table']['producer']
        self.table_consumer = simulator['table']['consumer']
        self.donut_chart = QWidget()
        self.init_ui()
    
    #Override    
    def resizeEvent(self, event):
        self.draw_donut_battery()
        
    def update_results(self):
        #def fetch_and_update():
        if 'producers' in self.state:
            weather_factor = random.uniform(0.0, 1.0)
            energy_update = self.simulator.update()
            #TODO: If energy_update < 0, enregistrer le montant d'énergie manquante et le temps pour en faire un graphique
            self.state = self.simulator.get_state()
            
            #Update Donut Data
            self.ax.clear()
            charge = (self.state["battery"]["stored_energy"] / self.state["battery"]["capacity"]) * 100
            self.sizes = [round(charge), round(100 - charge)]
            
            self.draw_donut_battery()
            self.plot_linear_data['time'].append(len(self.plot_linear_data['time']))
            self.plot_linear_data['battery'].append(self.state['battery']['stored_energy'])
            if 'solar' not in self.state['producers']:
                self.state['producers']['solar'] = 0
            self.plot_linear_data['solar'].append(self.state['producers']['solar'])
            if 'wind' not in self.state['producers']:
                self.state['producers']['wind'] = 0
            self.plot_linear_data['wind'].append(self.state['producers']['wind'])
            total_demand = 0
            if 'industry' in self.state['consumers']:
                total_demand += self.state['consumers']['industry']
            if 'household' in self.state['consumers']:
                total_demand += self.state['consumers']['household']
            self.plot_linear_data['demand'].append(total_demand)
            self.solar_curve.setData(self.plot_linear_data['time'], self.plot_linear_data['solar'])
            self.wind_curve.setData(self.plot_linear_data['time'], self.plot_linear_data['wind'])
            self.demand_curve.setData(self.plot_linear_data['time'], self.plot_linear_data['demand'])
            self.battery_level_curve.setData(self.plot_linear_data['time'], self.plot_linear_data['battery'])
        #return fetch_and_update
        
    def stop_reset(self):
        if self.stop_button.text() == StopButtonLabel.STOP_SIMULATION.value and self.timer.isActive():
            self.timer.stop()
            self.stop_button.setText(StopButtonLabel.RESET_SIMULATION.value)
            print(StopButtonLabel.STOP_SIMULATION.value)
        elif self.stop_button.text() == StopButtonLabel.RESET_SIMULATION.value:
            self.simulator.reset()
            self.plot_linear_data['time'].clear()
            self.plot_linear_data['battery'].clear()
            self.plot_linear_data['solar'].clear()
            self.plot_linear_data['wind'].clear()
            self.plot_linear_data['demand'].clear()
            self.state = {
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
                }
            self.table_producer.clear()
            self.table_producer.setRowCount(0)
            self.table_consumer.clear()
            self.table_consumer.setRowCount(0)
            self.solar_curve.setData(self.plot_linear_data['time'], self.plot_linear_data['solar'])
            self.wind_curve.setData(self.plot_linear_data['time'], self.plot_linear_data['wind'])
            self.demand_curve.setData(self.plot_linear_data['time'], self.plot_linear_data['demand'])
            self.battery_level_curve.setData(self.plot_linear_data['time'], self.plot_linear_data['battery'])
            self.draw_donut_battery()
            self.stop_button.setText(StopButtonLabel.STOP_SIMULATION.value)
    
    def add_image_overlay(self, layout):
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter) 
        pixmap = QPixmap(BATTERY_IMAGE_PATH)
        image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        layout.addWidget(image_label, 1, 2, 1, 1)
     
    def draw_donut_battery(self):
        def value(val):
            return f'{round(val)}%'
        print("SIZES : ", self.sizes)
        
        self.ax.pie(self.sizes, colors=self.colors, wedgeprops=dict(width=0.3), autopct=value)
        
        img = plt.imread(BATTERY_IMAGE_PATH)
        self.ax.imshow(img, extent=(-0.3, 0.3, -0.3, 0.3), aspect='auto', zorder=10)
        self.ax.set_aspect('equal')
        self.canvas.draw()
        
    def init_ui(self):
        result = QGroupBox("Simulation Results")
        infoText = QLabel("<h2>Visualization<h2>")
        infoText.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.plot_graph.setLabel('left', 'Power (kW)')
        self.plot_graph.setLabel('bottom', 'Time (h)')
        self.plot_graph.addLegend()
        self.solar_curve = self.plot_graph.plot(pen='y', name='Solar Output')
        self.wind_curve = self.plot_graph.plot(pen='b', name='Wind Output')
        self.demand_curve = self.plot_graph.plot(pen='r', name='Total Demand')
        self.battery_level_curve = self.plot_graph.plot(pen='g', name='Battery Level')
        # self.simulator['plot_linear_data'] = {'time': [], 'battery': [], 'solar': [], 'wind': [], 'demand': []}
        
        #Button to stop simulation
        self.stop_button = QPushButton(StopButtonLabel.STOP_SIMULATION.value, self)
        self.stop_button.setCursor(QCursor(Qt.PointingHandCursor))
        
        #Donut Chart
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.labels = ["Charge", "Discharge"]
        self.sizes = [50, 50]
        self.colors = ['#2ABf9E', '#9e9d9dff']
        self.draw_donut_battery()
        
        layout = QVBoxLayout(result)
        h_frame = QFrame(self)
        h_layout = QHBoxLayout(h_frame)
        h_layout.addWidget(self.plot_graph)
        h_layout.addWidget(self.canvas)
        layout.addWidget(infoText)
        layout.addWidget(h_frame)
        layout.addWidget(self.stop_button)
        
        
        self.layout.addWidget(result)
        self.setLayout(layout)
        
        # Mettre à jour les résultats toutes les secondes
        self.timer.timeout.connect(lambda : self.update_results())
        self.stop_button.clicked.connect(self.stop_reset)