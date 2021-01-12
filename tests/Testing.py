import unittest
from GraphAlgo import GraphAlgo
import json
import networkx as nx
import timeit
import time


class Testing(unittest.TestCase):

    def test_runtimes(self):
        algo = GraphAlgo()

        G_10_80_0 = '../data/G_10_80_0.json'
        G_100_800_0 = '../data/G_100_800_0.json'
        G_1000_8000_0 = '../data/G_1000_8000_0.json'
        G_10000_80000_0 = '../data/G_10000_80000_0.json'
        G_20000_160000_0 = '../data/G_20000_160000_0.json'
        G_30000_240000_0 = '../data/G_30000_240000_0.json'

        G_10_80_1 = '../data/G_10_80_1.json'
        G_100_800_1 = '../data/G_100_800_1.json'
        G_1000_8000_1 = '../data/G_1000_8000_1.json'
        G_10000_80000_1 = '../data/G_10000_80000_1.json'
        G_20000_160000_1 = '../data/G_20000_160000_1.json'
        G_30000_240000_1 = '../data/G_30000_240000_1.json'

        G_10_80_2 = '../data/G_10_80_2.json'
        G_100_800_2 = '../data/G_100_800_2.json'
        G_1000_8000_2 = '../data/G_1000_8000_2.json'
        G_10000_80000_2 = '../data/G_10000_80000_2.json'
        G_20000_160000_2 = '../data/G_20000_160000_2.json'
        G_30000_240000_2 = '../data/G_30000_240000_2.json'

        files = [G_10_80_0, G_100_800_0, G_1000_8000_0, G_10000_80000_0, G_20000_160000_0, G_30000_240000_0,
                 G_10_80_1, G_100_800_1, G_1000_8000_1, G_10000_80000_1, G_20000_160000_1, G_30000_240000_1,
                 G_10_80_2, G_100_800_2, G_1000_8000_2, G_10000_80000_2, G_20000_160000_2, G_30000_240000_2]

        result = []
        result_shortest_path = []
        result_scc = []

        for i in files:
            start = timeit.default_timer()
            start_ = time.perf_counter()

            algo.load_from_json(i)

            stop = timeit.default_timer() - start
            stop_ = time.perf_counter() - start_

            # print(f"loading {i} took {stop} with timeit default_timer()")
            # print(f"loading {i} took {stop_} with time perf_counter()")

            result.append((stop + stop_) / 2)

            start = timeit.default_timer()
            start_ = time.perf_counter()

            algo.shortest_path(0, 3)

            stop = timeit.default_timer() - start
            stop_ = time.perf_counter() - start_

            result_shortest_path.append((stop + stop_) / 2)

            # start = timeit.default_timer()
            # start_ = time.perf_counter()
            #
            # algo.connected_components()
            #
            # stop = timeit.default_timer() - start
            # stop_ = time.perf_counter() - start_
            #
            # result_scc.append((stop + stop_) / 2)

        print("Algo load results: ", result)
        print("Algo shortest path results: ", result_shortest_path)
        print("Algo scc results: ", result_scc)

    def test_runtimes_networkx(self):
        algo = GraphAlgo()

        G_10_80_0 = '../data/G_10_80_0.json'
        G_100_800_0 = '../data/G_100_800_0.json'
        G_1000_8000_0 = '../data/G_1000_8000_0.json'
        G_10000_80000_0 = '../data/G_10000_80000_0.json'
        G_20000_160000_0 = '../data/G_20000_160000_0.json'
        G_30000_240000_0 = '../data/G_30000_240000_0.json'

        G_10_80_1 = '../data/G_10_80_1.json'
        G_100_800_1 = '../data/G_100_800_1.json'
        G_1000_8000_1 = '../data/G_1000_8000_1.json'
        G_10000_80000_1 = '../data/G_10000_80000_1.json'
        G_20000_160000_1 = '../data/G_20000_160000_1.json'
        G_30000_240000_1 = '../data/G_30000_240000_1.json'

        G_10_80_2 = '../data/G_10_80_2.json'
        G_100_800_2 = '../data/G_100_800_2.json'
        G_1000_8000_2 = '../data/G_1000_8000_2.json'
        G_10000_80000_2 = '../data/G_10000_80000_2.json'
        G_20000_160000_2 = '../data/G_20000_160000_2.json'
        G_30000_240000_2 = '../data/G_30000_240000_2.json'

        files = [G_10_80_0, G_100_800_0, G_1000_8000_0, G_10000_80000_0, G_20000_160000_0, G_30000_240000_0,
                 G_10_80_1, G_100_800_1, G_1000_8000_1, G_10000_80000_1, G_20000_160000_1, G_30000_240000_1,
                 G_10_80_2, G_100_800_2, G_1000_8000_2, G_10000_80000_2, G_20000_160000_2, G_30000_240000_2]

        result = []
        result_shortest_path = []

        for i in files:
            start = timeit.default_timer()
            start_ = time.perf_counter()

            # networkx load graph logic here
            nodes = []
            edges = []

            with open(i) as f:
                data = json.load(f)

                for n in data['Nodes']:
                    nodes.append(n['id'])

                for e in data['Edges']:
                    edges.append((e['src'], e['dest'], e['w']))

            g_nx = nx.DiGraph()

            g_nx.add_nodes_from(nodes)
            g_nx.add_weighted_edges_from(edges)

            stop = timeit.default_timer() - start
            stop_ = time.perf_counter() - start_

            # print(f"loading {i} took {stop} with timeit default_timer()")
            # print(f"loading {i} took {stop_} with time perf_counter()")

            result.append((stop + stop_) / 2)

            start = timeit.default_timer()
            start_ = time.perf_counter()

            sp = nx.shortest_path(g_nx, 0, 3, weight='weight')

            stop = timeit.default_timer() - start
            stop_ = time.perf_counter() - start_

            result_shortest_path.append((stop + stop_) / 2)

        print("networkx load results: ", result)
        print("networkx shortest path results: ", result_shortest_path)


if __name__ == '__main__':
    unittest.main()
