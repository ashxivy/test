import sys 
sys.path.append("delivery_network")

import unittest
from graph import Graph, graph_from_file, kruskal

class TestMinPowerKruskal(unittest.TestCase):
    def setUp(self):
        self.g = graph_from_file("input/network.00.in")

    def test_min_power_kruskal(self):
        src = 1
        dest = 7
        expected_path = [1, 2, 5, 7]
        expected_power = 11

        # Calculate path and power
        power, path = self.g.min_power_kruskal(src, dest)

        # Check if expected path and power are equal to the calculated ones
        self.assertEqual(path, expected_path)
        self.assertEqual(power, expected_power)

if __name__ == '__main__':
    unittest.main()
