# python/grid_simulator.py
import ctypes
import json
import os

# Définir la structure JsonString
class JsonString(ctypes.Structure):
    _fields_ = [("data", ctypes.c_char_p)] 

# Charger la librairie C++
lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), "/Users/remi.bhagalou/Documents/Remi/projets/SmartGridSimulator/build/libsmart_grid.dylib"))

# Définir les types de retour et arguments
lib.create_grid.argtypes = [ctypes.c_double, ctypes.c_double]
lib.create_grid.restype = ctypes.c_void_p

lib.add_producer.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_double]

lib.remove_producer.argtypes = [ctypes.c_void_p, ctypes.c_int]

lib.add_consumer.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_double]

lib.remove_consumer.argtypes = [ctypes.c_void_p, ctypes.c_int]

lib.update_grid.argtypes = [ctypes.c_void_p]

lib.update_battery.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double]

lib.reset.argtypes = [ctypes.c_void_p]

lib.get_grid_state.argtypes = [ctypes.c_void_p]
lib.get_grid_state.restype = ctypes.POINTER(JsonString)

lib.free_state.argtypes = [ctypes.POINTER(JsonString)]

lib.delete_grid.argtypes = [ctypes.c_void_p]

class GridSimulator:
    def __init__(self, battery_capacity=100.0, charge_rate=10.0):
        self.grid_ptr = lib.create_grid(battery_capacity, charge_rate)

    def add_producer(self, id, producer_type, capacity):
        lib.add_producer(
            self.grid_ptr,
            ctypes.c_int(id),
            producer_type.encode('utf-8'),
            ctypes.c_double(capacity)
        )
    
    def remove_producer(self, id):
        lib.remove_producer(
            self.grid_ptr,
            ctypes.c_int(id)
        )

    def add_consumer(self, id, consumer_type, base_demand):
        lib.add_consumer(
            self.grid_ptr,
            ctypes.c_int(id),
            consumer_type.encode('utf-8'),
            ctypes.c_double(base_demand)
        )
    
    def remove_consumer(self, id):
        lib.remove_consumer(
            self.grid_ptr,
            ctypes.c_int(id)
        )

    def update(self):
        lib.update_grid(self.grid_ptr)
        
    def update_battery(self, capacity, charge_rate):
        lib.update_battery(
            self.grid_ptr, 
            ctypes.c_double(capacity),
            ctypes.c_double(charge_rate)
            )
        
    def reset(self):
        lib.reset(self.grid_ptr)

    def get_state(self):
        state_ptr = lib.get_grid_state(self.grid_ptr)
        state_str = state_ptr.contents.data.decode('utf-8')
        state = json.loads(state_str)
        # Libérer la mémoire allouée par C++
        lib.free_state(state_ptr)
        
        return state

    def __del__(self):
        lib.delete_grid(self.grid_ptr)
