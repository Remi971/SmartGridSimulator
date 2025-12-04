#pragma once
#include <vector>
#include <string>
#include <random>
#include <ctime>
#include <cmath>
#include <iostream>
#include <string>
#include "json.hpp"

using json = nlohmann::json;

class EnergyProducer {
public:
    int id;
    std::string type;  // "solar", "wind", "grid"
    double capacity;   // Capacité maximale (kW)
    double current_output;  // Production actuelle (kW)

    EnergyProducer(int id, std::string type, double capacity)
        :id(id), type(type), capacity(capacity), current_output(0.0) {}

    void update_output(double current_time) {
        if (type == "solar") {
            double solar_factor = std::max(0.0, 1.0 - std::abs((current_time - 12.0) / 6.0)); // Pic à midi
            current_output = capacity * solar_factor * (0.8 + 0.2 * (((double) rand() / (RAND_MAX)) + 1)); // Variation aléatoire légère
        } else if (type == "wind") {
            double wind_factor = 0.3 + 0.7 * (((double) rand() / (RAND_MAX)) + 1); // Vent entre 30% et 100% de sa capacité
            current_output = capacity * wind_factor;
        } else {  // Grid (réseau principal)
            current_output = capacity;
        }
    }
    
    bool isEqual(int producerId) {
        return producerId == id;
    }
};

class EnergyConsumer {
public:
    int id;
    std::string type;  // "household", "industry"
    double demand;     // Demande actuelle (kW)

    EnergyConsumer(int id, std::string type, double base_demand)
        :id(id), type(type), demand(base_demand) {}

    void update_demand(double current_time) {
        // Variation de la demande selon l'heure
        if (type == "household") {
            //Pic le matin (7h - 9h) et le soir (18h - 22h)
            demand = 2.0 + 5.0 * (
                std::exp(-0.5 * std::pow((current_time - 8) / 2, 2)) + // Pic le matin
                std::exp(-0.5 * std::pow((current_time - 20) / 2, 2)) // Pic le soir
            );
        } else {  // Industry
            demand = 50.0 + 30.0 * std::exp(-0.5 * std::pow((current_time - 12) / 6, 2));  // Demande constante avec un léger pic en journée
        }
    }
    
    bool isEqual(int consumerId) {
        return id == consumerId;
    }
};

class Battery {
public:
    double capacity;   // Capacité totale (kWh)
    double stored_energy;  // Énergie stockée (kWh)
    double max_charge_rate;  // Puissance max de charge (kW)
    double max_discharge_rate;  // Puissance max de décharge (kW)

    Battery(double capacity, double charge_rate)
        : capacity(capacity), stored_energy(capacity / 2),
          max_charge_rate(charge_rate), max_discharge_rate(charge_rate) {}
    
    void update(double newCapacity, double newCharge_rate) {
        capacity = newCapacity;
        stored_energy = newCapacity / 2;
        max_charge_rate = newCharge_rate;
        max_discharge_rate = newCharge_rate;
    };

    void charge(double energy, double delta_time) {
        double max_energy = max_charge_rate * delta_time / 3600;  // kWh
        double energy_to_store = std::min(energy, max_energy);
        stored_energy = std::min(stored_energy + energy_to_store, capacity);
    }
    
    void reset() {
        stored_energy = capacity / 2;
    }

    double discharge(double energy_needed, double delta_time) {
        double max_energy = max_discharge_rate * delta_time / 3600;  // kWh
        double energy_to_release = std::min(std::min(energy_needed, max_energy), stored_energy);
        stored_energy -= energy_to_release;
        return energy_to_release;
    }
};

class SmartGrid {
private:
    std::vector<EnergyProducer> producers;
    std::vector<EnergyConsumer> consumers;
    Battery battery;
    double time_step;  // Secondes
    double current_time;  // Heures (0-24)

public:
    SmartGrid(double battery_capacity, double charge_rate, double time_step=3600)
    : battery(battery_capacity, charge_rate), time_step(time_step), current_time(0.0) {}

    void add_producer(EnergyProducer producer) {
        producers.push_back(producer);
    }
    
    void remove_producer(int id) {
        producers.erase(producers.begin() + id);
        std::cout << id << " Removed !" << std::endl;
    }

    void add_consumer(EnergyConsumer consumer) {
        consumers.push_back(consumer);
    }
    void remove_consumer(int id) {
        consumers.erase(consumers.begin() + id);
        std::cout << id << " Removed !" << std::endl;
    }
    
    void updateBattery(double capacity, double charge_rate) {
        battery.update(capacity, charge_rate);
    }
    
    void reset() {
        producers.clear();
        consumers.clear();
        battery.reset();
        current_time = 0.0;
    }

    double update() {
        current_time += time_step / 3600.0;
        if (current_time >= 24.0) current_time -= 24.0;  // Cycle de 24h

        // Mettre à jour la production et la demande
        double time_factor = 0.5 * (1.0 + sin(M_PI * current_time / 12.0));  // Variation journalière
        for (auto& producer : producers) {
            producer.update_output(current_time);
        }
        for (auto& consumer : consumers) {
            consumer.update_demand(current_time);
        }

        // Calculer l'équilibre offre/demande
        double total_production = 0.0;
        for (const auto& producer : producers) {
            total_production += producer.current_output;
        }

        double total_demand = 0.0;
        for (const auto& consumer : consumers) {
            total_demand += consumer.demand;
        }

        double imbalance = total_production - total_demand;
        double energy = 0.0;
        if (imbalance > 0) {
            // Excédent : stocker dans la batterie
            battery.charge(imbalance * (time_step / 3600.0), time_step);
            energy = imbalance;
        } else {
            // Déficit : utiliser la batterie
            double energy_needed = -imbalance * (time_step / 3600.0);
            double energy_from_battery = battery.discharge(energy_needed, time_step);
            if (energy_from_battery < energy_needed) {
                energy = energy_from_battery < energy_needed;
                // Acheter de l'énergie au réseau principal
                std::cout << "Achat d'énergie supplémentaire au réseau : "
                          << (energy_needed - energy_from_battery) << " kWh" << std::endl;
            }
        }
        return energy;
    }

    json get_state() const {
        json state;
        state["time"] = current_time;
        state["battery"] = {
            {"stored_energy", battery.stored_energy},
            {"capacity", battery.capacity}
        };

        json producers_state;
        for (const auto& producer : producers) {
            producers_state[producer.type] = producer.current_output;
        }
        state["producers"] = producers_state;

        json consumers_state;
        for (const auto& consumer : consumers) {
            consumers_state[consumer.type] = consumer.demand;
        }
        state["consumers"] = consumers_state;
        return state;
    }
};

