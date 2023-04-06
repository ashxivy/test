import sys 
sys.path.append("delivery_network")

import unittest
from graph import Graph, graph_from_file


class TestMinPowerKruskal(unittest.TestCase):
    def setUp(self):
        self.g = graph_from_file("input/network.00.in")

    def test_min_power_kruskal(self):
        src = 2
        dest = 4
        expected_power = 10

        # Calculate path and power
        power, path = self.g.min_power_kruskal(src, dest)

        # Check if expected path and power are equal to the calculated ones
        self.assertEqual(power, expected_power)

if __name__ == '__main__':
    unittest.main()
