from tests import Test_G
from GraphAlgo import GraphAlgo
import os


def test_a():

    graph = Test_G.build_graph("graph_algo")
    algo = GraphAlgo(graph)

    print("graph: {0}".format(graph))
    print("nodes: {0}".format(graph.get_all_v()))

    # edges [0,1], [0,2], [1,2], [2,3] ,[3,4]

    print(f"Test: shortest path 0 to 4 -> (9, [0, 2, 3, 4]) = {algo.shortest_path(0, 4)} ")
    print(f"Test: shortest path 0 to 2 -> (1, [0, 2]) = {algo.shortest_path(0, 2)} ")
    print(f"Test: shortest path 0 to 0 -> (inf, []) = {algo.shortest_path(0, 0)} ")
    print(f"Test: shortest path 2 to 1 -> (inf, []) = {algo.shortest_path(2, 1)} ")
    print(f"Test: shortest path 0 to 4 -> (inf, []) = {algo.shortest_path(0, 7)} ")


def test_save_load():
    graph = Test_G.build_graph("graph_algo")
    algo = GraphAlgo(graph)

    print("graph: {0}".format(graph))
    print("nodes: {0}".format(graph.get_all_v()))

    path = '../data/test_save_to_json'
    print(f"Test: save to json -> (true, path: {path}) = {algo.save_to_json(path)}")

    algo_load = GraphAlgo()
    print(f"Test: load from json -> (true) = {algo_load.load_from_json(path)}")

    print(f"Test: graph after load -> (|V|=5 , |E|=5) -> = {algo_load.get_graph()}")
    print(f"Test: nodes: (0: 0: |edges out| 0 |edges in| 2, 1: 1: |edges out| 1 |edges in| 1,"
          f" 2: 2: |edges out| 2 |edges in| 1, 3: 3: |edges out| 1 |edges in| 1, 4: 4: |edges out| 1 |edges in| 0)"
          f"\n -> {algo_load.get_graph().get_all_v()}")
    print(f"Test: in edges to node {1}: -> (2: 2) = {algo_load.get_graph().all_in_edges_of_node(1)}")
    print(f"Test: out edges from node {1}: -> (0: 1) = {algo_load.get_graph().all_out_edges_of_node(1)}")


if __name__ == '__main__':
    test_a()
    test_save_load()
