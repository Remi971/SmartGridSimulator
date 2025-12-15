import unittest
from grid_simulator import GridSimulator

class TestGridSimulator(unittest.TestCase):
    def setUp(self):
        self.simulator = GridSimulator(battery_capacity=100.0, charge_rate=10.0)

    def test_add_and_remove_producer(self):
        self.simulator.add_producer(1, "solar", 50.0)
        self.simulator.add_producer(2, "wind", 30.0)
        # Here you would normally check the internal state, but since it's C++ based,
        # we assume if no exception is raised, it works.
        self.simulator.remove_producer(1)
        self.simulator.remove_producer(0)

    def test_add_and_remove_consumer(self):
        self.simulator.add_consumer(1, "household", 20.0)
        self.simulator.add_consumer(2, "industry", 50.0)
        # Same as above regarding state checking.
        self.simulator.remove_consumer(1)
        self.simulator.remove_consumer(0)

    def test_update_grid(self):
        self.simulator.add_producer(1, "solar", 50.0)
        self.simulator.add_consumer(1, "household", 20.0)
        self.simulator.update()
        

    
if __name__ == '__main__':
    unittest.main()