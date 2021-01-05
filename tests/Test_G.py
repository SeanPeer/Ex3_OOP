from DiGraph import DiGraph


def build_graph(name="g"):

    print(f"Creating Graph {name}:")
    g = DiGraph()

    print("adding nodes [0,4] \n"
          "adding edges: [0,1], [0,2], [1,2], [2,3] ,[3,4]")
    for i in range(5):
        g.add_node(i)

    g.add_edge(0, 1, 1)
    g.add_edge(0, 2, 1)
    g.add_edge(1, 2, 2)

    g.add_edge(2, 3, 3)
    g.add_edge(3, 4, 5)

    return g


def test_g():

    g = build_graph()

    print(f"Test: add existing node -> (false) = {g.add_node(0)}")
    print(f"Test: add existing edge -> (false) = {g.add_edge(0, 1, 1)}")

    print("removing edge 0 -> 1")
    g.remove_edge(0, 1)

    print(f"Test: remove non-existing edge -> (false) = {g.remove_edge(0, 1)}")
    print(f"Test: edge to a non-existing node -> (false) = {g.add_edge(0, 50, 5)}")

    print("removing node 0")
    g.remove_node(0)

    print(f"Test: add node after node removal -> (true) = {g.add_node(0)}")
    print(f"Test: add edge after node removal -> (true) = {g.add_edge(0, 1, 2)}")

    print(f"Test: print graph -> (|V|=5 , |E|=4) -> = {g}")

    g = build_graph()
    g_copy = build_graph("g_copy")

    print(f"Test: copy of graph -> (|V|=5 , |E|=5) -> = {g_copy}")

    print(f"Test: equals for a copy -> (true) = {g == g_copy}")

    g_copy.remove_node(0)
    print(f"Test: equals after change -> (false) = {g == g_copy}")


if __name__ == '__main__':
    test_g()
