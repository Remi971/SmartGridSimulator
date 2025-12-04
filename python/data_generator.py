import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt

def generate_24h_simulation() -> list:
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

    return data

def save_to_json(data, filename="simulation_24h.json"):
    """Sauvegarde les données générées dans un fichier JSON."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Données sauvegardées dans {filename}")

def save_to_csv(data, filename="simulation_24h.csv"):
    """Sauvegarde les données générées dans un fichier CSV."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Données sauvegardées dans {filename}")

def plot_simulation(data):
    """Affiche un graphique des données générées."""
    df = pd.DataFrame(data)

    plt.figure(figsize=(12, 6))

    # Consommation
    plt.plot(df["hour"], df["household_demand"] + df["industry_demand"],
             label="Consommation Totale", color="red", linewidth=2)

    # Production
    plt.plot(df["hour"], df["solar_production"], label="Solaire", color="orange")
    plt.plot(df["hour"], df["wind_production"], label="Éolien", color="blue")

    plt.xlabel("Heure de la journée")
    plt.ylabel("Puissance (kW)")
    plt.title("Simulation de la Consommation et Production sur 24h")
    plt.legend()
    plt.grid(True)
    plt.xticks(range(24), [f"{h:02d}:00" for h in range(24)], rotation=45)
    plt.tight_layout()
    plt.savefig("simulation_24h.png")
    plt.show()

def run_simulation_with_data(data, grid_simulator):
    """
    Lance une simulation avec les données générées.
    `grid_simulator` doit être une instance de ton simulateur (ex: GridSimulator).
    """
    for hour_data in data:
        weather_factor = (hour_data["weather_factor"]["solar"] + hour_data["weather_factor"]["wind"]) / 2.0
        grid_simulator.update(weather_factor)

        # Récupérer et afficher l'état du réseau
        state = grid_simulator.get_state()
        print(f"Heure {hour_data['time']}:")
        print(f"  Consommation: {hour_data['household_demand'] + hour_data['industry_demand']:.1f} kW")
        print(f"  Production: Solaire={hour_data['solar_production']:.1f}kW, Éolien={hour_data['wind_production']:.1f}kW")
        print(f"  Batterie: {state['battery']['stored_energy']:.1f}/{state['battery']['capacity']:.1f} kWh")
        print("---")

if __name__ == "__main__":
    # Générer les données
    simulation_data = generate_24h_simulation()

    # Sauvegarder les données
    save_to_json(simulation_data)
    save_to_csv(simulation_data)

    # Afficher un graphique
    plot_simulation(simulation_data)

    # Exemple d'utilisation avec ton simulateur (à décommenter une fois intégré)
    # from grid_simulator import GridSimulator
    # simulator = GridSimulator(battery_capacity=200.0, charge_rate=20.0)
    # simulator.add_producer(b"solar", 50.0)
    # simulator.add_producer(b"wind", 30.0)
    # simulator.add_consumer(b"household", 5.0)
    # simulator.add_consumer(b"industry", 100.0)
    # run_simulation_with_data(simulation_data, simulator)
