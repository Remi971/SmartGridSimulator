from PySide6.QtWidgets import (QGridLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem)
import numpy as np

class GeneratorUI:
    def __init__(self, simulator):
        self.simulator = simulator
        self.generated_data = []
        self.table_layout = QTableWidget()

    def init_ui(self, widget):
        layout = QGridLayout()
        
        infoText = QLabel("This tab allows you to generate synthetic data for testing the simulator.")
        infoText.setWordWrap(True)
        
        generate_button = QPushButton("Generate 24h Simulation Data")
        generate_button.clicked.connect(lambda: self.generate_data())
        
       
        header = ["hour", "time", "household_demand", "industry_demand", "solar_production", "wind_production", "weather_factor"]
        self.table_layout.setColumnCount(len(header))
        self.table_layout.setHorizontalHeaderLabels(header)
        self.table_layout.setRowCount(0)
        self.table_layout.setColumnCount(len(header))

        layout.addWidget(infoText, 0, 0, 1, 2)
        layout.addWidget(generate_button, 1, 0, 1, 2)
        layout.addWidget(self.table_layout, 2, 0, 1, 2)
        widget.setLayout(layout)

    def generate_data(self):
        """
        Génère des données simulées pour 24 heures :
        - Consommation (ménages + industries)
        - Production solaire (basée sur l'heure de la journée)
        - Production éolienne (variations aléatoires réalistes)
        """
        hours = list(range(24))
        data = []

        for hour in hours:
            # Heure en format décimal (ex: 7.5 pour 7h30)
            time = hour

            # 1. Consommation (kW)
            # - Ménages : pic le matin (7h-9h) et le soir (18h-22h)
            household_demand = 2.0 + 5.0 * (
                np.exp(-0.5 * ((time - 8) / 2)**2) +  # Pic le matin
                np.exp(-0.5 * ((time - 20) / 2)**2)   # Pic le soir
            )
            # - Industries : demande constante avec un léger pic en journée
            industry_demand = 50.0 + 30.0 * np.exp(-0.5 * ((time - 12) / 6)**2)

            # 2. Production solaire (kW) - dépend de l'heure (0 = nuit, 12 = midi)
            solar_factor = max(0.0, 1.0 - abs((time - 12.0) / 6.0))  # Pic à midi
            solar_production = 50.0 * solar_factor * (0.8 + 0.2 * np.random.random())  # Variation aléatoire légère

            # 3. Production éolienne (kW) - variations aléatoires réalistes
            wind_factor = 0.3 + 0.7 * np.random.random()  # Vent entre 30% et 100% de sa capacité
            wind_production = 30.0 * wind_factor

            data.append({
                "hour": hour,
                "time": f"{hour:02d}:00",
                "household_demand": max(0.0, household_demand),
                "industry_demand": max(0.0, industry_demand),
                "solar_production": max(0.0, solar_production),
                "wind_production": max(0.0, wind_production),
                "weather_factor": {
                    "solar": solar_factor,
                    "wind": wind_factor
                }
            })
        print(data)
        self.generated_data = data
        for row_idx, entry in enumerate(data):
            self.table_layout.insertRow(row_idx)
            self.table_layout.setItem(row_idx, 0, QTableWidgetItem(str(entry["hour"])))
            self.table_layout.setItem(row_idx, 1, QTableWidgetItem(entry["time"]))
            self.table_layout.setItem(row_idx, 2, QTableWidgetItem(f"{entry['household_demand']:.2f}"))
            self.table_layout.setItem(row_idx, 3, QTableWidgetItem(f"{entry['industry_demand']:.2f}"))
            self.table_layout.setItem(row_idx, 4, QTableWidgetItem(f"{entry['solar_production']:.2f}"))
            self.table_layout.setItem(row_idx, 5, QTableWidgetItem(f"{entry['wind_production']:.2f}"))
            weather_str = f"Solar: {entry['weather_factor']['solar']:.2f}, Wind: {entry['weather_factor']['wind']:.2f}"
            self.table_layout.setItem(row_idx, 6, QTableWidgetItem(weather_str))