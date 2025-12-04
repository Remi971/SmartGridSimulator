//
//  smart_grid.cpp
//  Energy_Simulator
//
//  Created by Remi Bhagalou on 18/11/2025.
//
#include "../include/smart_grid.h"
#include <iostream>
#include <fstream>

struct JsonString {
    char* data;
};


extern "C" {
    void* create_grid(double battery_capacity, double charge_rate) {
        return new SmartGrid(battery_capacity, charge_rate);
    }

    void add_producer(void* grid_ptr, int id, const char* type, double capacity) {
        SmartGrid* grid = static_cast<SmartGrid*>(grid_ptr);
        grid->add_producer(EnergyProducer(id, std::string(type), capacity));
    }

    void remove_producer(void* grid_ptr, int id) {
        SmartGrid* grid = static_cast<SmartGrid*>(grid_ptr);
        grid->remove_producer(id);
    }

    void add_consumer(void* grid_ptr, int id, const char* type, double base_demand) {
        SmartGrid* grid = static_cast<SmartGrid*>(grid_ptr);
        grid->add_consumer(EnergyConsumer(id, std::string(type), base_demand));
    }

    void remove_consumer(void* grid_ptr, int id) {
        SmartGrid* grid = static_cast<SmartGrid*>(grid_ptr);
        grid->remove_consumer(id);
    }

    void update_grid(void* grid_ptr) {
        SmartGrid* grid = static_cast<SmartGrid*>(grid_ptr);
        grid->update();
    }

    void update_battery(void* grid_ptr, double capacity, double charge_rate) {
        SmartGrid* grid = static_cast<SmartGrid*>(grid_ptr);
        grid->updateBattery(capacity, charge_rate);
    }

    void reset(void* grid_ptr) {
        SmartGrid* grid = static_cast<SmartGrid*>(grid_ptr);
        grid->reset();
    }

    JsonString* get_grid_state(void* grid_ptr) {
        SmartGrid* grid = static_cast<SmartGrid*>(grid_ptr);
        json state = grid->get_state();
        std::string state_str = state.dump();
        JsonString* cstr = new JsonString;
        cstr->data = new char[state_str.size() + 1];
        strcpy(cstr->data, state_str.c_str());
        return cstr;
    }

    void free_state(JsonString* cstr_ptr) {
        if (cstr_ptr) {
            delete[] cstr_ptr->data;
            delete cstr_ptr;
        }
    }

    void delete_grid(void* grid_ptr) {
        delete static_cast<SmartGrid*>(grid_ptr);
    }
}

