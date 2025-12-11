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

/**
 * @class EnergyProducer
 * @brief Energy Producer in the Smart Grid
 * This class represents an energy producer such as solar panels, wind turbines, or the main grid.
 */
class EnergyProducer {
public:
    int id;
    std::string type;  // "solar", "wind", "grid"
    double capacity;   // Maximum capacity (kW)
    double current_output;  // Current Production (kW)

    /**
     * @brief Constructor for EnergyProducer
     * @param id Unique identifier for the producer
     * @param type Type of producer ("solar", "wind", or "grid")
     * @param capacity Maximum capacity of the producer in kW
     */
    EnergyProducer(int id, std::string type, double capacity)
        :id(id), type(type), capacity(capacity), current_output(0.0) {}

    /**
     * @brief Update output based on time of day and randomness
     * @param current_time Current time in hours (0-24)
     */
    void update_output(double current_time) {
        if (type == "solar") {
            double solar_factor = std::max(0.0, 1.0 - std::abs((current_time - 12.0) / 6.0)); // Peak at noon
            current_output = capacity * solar_factor * (0.8 + 0.2 * (((double) rand() / (RAND_MAX)) + 1)); // Random varation between 80% and 100%
        } else if (type == "wind") {
            double wind_factor = 0.3 + 0.7 * (((double) rand() / (RAND_MAX)) + 1); // Wind between 30% and 100% of its capacity
            current_output = capacity * wind_factor;
        } else {  // Grid (Main grid)
            current_output = capacity;
        }
    }
    
    /**
     * @brief Check if the producer ID matches
     * @param producerId ID to compare
     * @return true if IDs match, false otherwise
     */
    bool isEqual(int producerId) {
        return producerId == id;
    }
};

/**
 * @class EnergyConsumer
 * @brief Energy Consumer in the Smart Grid
 * This class represents an energy consumer such as households or industries.
 */
class EnergyConsumer {
public:
    int id;
    std::string type;  // "household", "industry"
    double demand;     // Actual Demand (kW)

    /**
     * @brief Constructor for EnergyConsumer
     * @param id Unique identifier for the consumer
     * @param type Type of consumer ("household" or "industry")
     * @param base_demand Base demand of the consumer in kW
     */
    EnergyConsumer(int id, std::string type, double base_demand)
        :id(id), type(type), demand(base_demand) {}

    /**
     * @brief Update demand based on time of day
     * @param current_time Current time in hours (0-24)
     */
    void update_demand(double current_time) {
        // Demand variation over time 
        if (type == "household") {
            //Peak in the morning (7h - 9h) and in the evening (18h - 22h)
            demand = 2.0 + 5.0 * (
                std::exp(-0.5 * std::pow((current_time - 8) / 2, 2)) + // Peak the morning
                std::exp(-0.5 * std::pow((current_time - 20) / 2, 2)) // Peak the evening
            );
        } else {  // Industry
            demand = 50.0 + 30.0 * std::exp(-0.5 * std::pow((current_time - 12) / 6, 2));  // Constant demand with a slight peak at midday
        }
    }
    
    /**
     * @brief Check if the consumer ID matches
     * @param consumerId ID to compare
     * @return true if IDs match, false otherwise
     */
    bool isEqual(int consumerId) {
        return id == consumerId;
    }
};

/**
 * @class Battery
 * @brief Battery Storage in the Smart Grid
 * This class represents a battery storage system for storing excess energy and supplying energy during deficits.
 */
class Battery {
public:
    double capacity;   // Total Capacity (kWh)
    double stored_energy;  // Stored Energy (kWh)
    double max_charge_rate;  // Maximum charging power (kW)
    double max_discharge_rate;  // Maximum discharge power (kW)

    /**
     * @brief Constructor for Battery
     * @param capacity Capacity or the battery in kWh
     * @param charge_rate Maximum charge/discharge rate of the battery in kW
     */
    Battery(double capacity, double charge_rate)
        : capacity(capacity), stored_energy(capacity / 2),
          max_charge_rate(charge_rate), max_discharge_rate(charge_rate) {}
    
          /**
     * @brief Update battery parameters
     * @param newCapacity New capacity of the battery in kWh
     * @param newCharge_rate New charge/discharge rate of the battery in kW
     */
    void update(double newCapacity, double newCharge_rate) {
        capacity = newCapacity;
        stored_energy = newCapacity / 2;
        max_charge_rate = newCharge_rate;
        max_discharge_rate = newCharge_rate;
    };

    /**
     * @brief Charge the battery with excess energy
     * @param energy Amount of energy to charge (kWh)
     * @param delta_time Time step for charging (seconds)
     */
    void charge(double energy, double delta_time) {
        double max_energy = max_charge_rate * delta_time / 3600;  // kWh
        double energy_to_store = std::min(energy, max_energy);
        stored_energy = std::min(stored_energy + energy_to_store, capacity);
    }
    
    /**
     * @brief Reset the battery to initial state
     */
    void reset() {
        stored_energy = capacity / 2;
    }

    /**
     * @brief Discharge the battery to supply energy
     * @param energy_needed Amount of energy needed (kWh)
     * @param delta_time Time step for discharging (seconds)
     * @return Amount of energy actually discharged (kWh)
     */
    double discharge(double energy_needed, double delta_time) {
        double max_energy = max_discharge_rate * delta_time / 3600;  // kWh
        double energy_to_release = std::min(std::min(energy_needed, max_energy), stored_energy);
        stored_energy -= energy_to_release;
        return energy_to_release;
    }
};
/**
 * @class SmartGrid
 * @brief Smart Grid electric system simulator
 * This class simulates a smart grid electric system with energy producers, consumers and a battery storage.
 */
class SmartGrid {
private:
    std::vector<EnergyProducer> producers;
    std::vector<EnergyConsumer> consumers;
    Battery battery;
    double time_step;  // Secondes
    double current_time;  // Heures (0-24)
    double purchase_energy; // kWh purchased from the main grid

public:
    /**
     * @brief Constructor for SmartGrid
     * @param battery_capacity Capacity or the battery in kWh
     * @param charge_rate Maximum charge/discharge rate of the battery in kW
     * @param time_step Time step for the simulation in seconds (default is 3600s)
     */
    SmartGrid(double battery_capacity, double charge_rate, double time_step=3600)
    : battery(battery_capacity, charge_rate), time_step(time_step), current_time(0.0), purchase_energy(0.0) {}

    /**
     * @brief Add an energy producer to the smart grid
     * @param producer EnergyProducer object to add
     */
    void add_producer(EnergyProducer producer) {
        producers.push_back(producer);
    }
    
    /**
     * @brief Remove an energy producer from the smart grid
     * @param id ID of the producer to remove
     */
    void remove_producer(int id) {
        producers.erase(producers.begin() + id);
        std::cout << id << " Removed !" << std::endl;
    }

    /**
     * @brief Add an energy consumer to the smart grid
     * @param consumer EnergyConsumer object to add
     */
    void add_consumer(EnergyConsumer consumer) {
        consumers.push_back(consumer);
    }
    /**
     * @brief Remove an energy consumer from the smart grid
     * @param id ID of the consumer to remove
     */
    void remove_consumer(int id) {
        consumers.erase(consumers.begin() + id);
        std::cout << id << " Removed !" << std::endl;
    }
    /**
     * @brief Update battery parameters
     * @param capacity New capacity of the battery in kWh
     * @param charge_rate New charge/discharge rate of the battery in kW
     */
    void updateBattery(double capacity, double charge_rate) {
        battery.update(capacity, charge_rate);
    }
    
    /**
     * @brief Reset the smart grid to initial state
     */
    void reset() {
        producers.clear();
        consumers.clear();
        battery.reset();
        current_time = 0.0;
    }

    /**
     * @brief Simulate one time step of the smart grid
     * @return Amount of energy bought from the main grid (kWh)
     */
    void update() {
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
            purchase_energy = 0.0;
        } else {
            // Déficit : utiliser la batterie
            double energy_needed = -imbalance * (time_step / 3600.0);
            double energy_from_battery = battery.discharge(energy_needed, time_step);
            if (energy_from_battery < energy_needed) {
                energy = energy_needed - energy_from_battery;
                purchase_energy = energy;
                // Acheter de l'énergie au réseau principal
                std::cout << "Purchasing additional energy from the grid : "
                          << energy << " kWh" << std::endl;
            }
        }
    }

    /**
     * @brief Get the current state of the smart grid
     * @return JSON object representing the current state of the smart grid
     */
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
        state["purchase_energy"] = purchase_energy;
        return state;
    }
};

