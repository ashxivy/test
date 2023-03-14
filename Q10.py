from graph import Graph, graph_from_file, kruskal
import time 

g = graph_from_file("input/network.00.in")
for i in range (1,11):
    temps=temps.append(time.perf_counter(g.min_power()))

    def test_min_power_kruskal(self):
        src = 2
        dest = 4
        expected_power = 10

        # Calculate path and power
        power, path = self.g.min_power_kruskal(src, dest)
