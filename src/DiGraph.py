from DiNode import DiNode


class DiGraph:

    def __init__(self):
        self.nodes = {}

        self.edges = []

        self.edges_size = 0
        self.node_size = 0
        self.operations = 0

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """

        return self.node_size

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """

        return self.edges_size

    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair  (key, node_data)
        """

        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (key, weight)
         """

        return self.nodes.get(id1).ins

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair (key,
        weight)
        """

        return self.nodes.get(id1).outs

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        return self.operations

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """

        if id1 in self.nodes and id2 in self.nodes:

            node1 = self.nodes.get(id1)
            node2 = self.nodes.get(id2)

            if not node1.check_edge_out(id2) and weight >= 0 and id1 is not id2:
                b1 = node1.add_outo(id2, w=weight)
                b2 = node2.add_into(id1, w=weight)

                self.edges_size += 1
                self.operations += 1

                self.edges.append((id1, id2, weight))

                return True

        return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        Note: if the node id already exists the node will not be added
        """

        if node_id not in self.nodes:

            self.nodes[node_id] = DiNode(id_=node_id, pos=pos)
            self.node_size += 1

            return True

        return False

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.
        Note: if the node id does not exists the function will do nothing
        """
        if node_id in self.nodes:
            node = self.nodes.get(node_id)

            for o in node.outs:
                del self.nodes[o].ins[node_id]
                self.edges_size -= 1
                self.operations += 1

            for n in node.ins:
                del self.nodes[n].outs[node_id]

            self.node_size -= 1
            self.operations += 1
            del self.nodes[node_id]

            return True

        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        Note: If such an edge does not exists the function will do nothing
        """

        if node_id1 in self.nodes and node_id2 in self.nodes:

            node1 = self.nodes.get(node_id1)
            node2 = self.nodes.get(node_id2)

            if node1.check_edge_out(node_id2) and node_id1 is not node_id2:

                node1.disconnect_out(node_id2)
                node2.disconnect_in(node_id1)

                self.edges_size -= 1
                self.operations += 1
                return True

        return False

    def transpose(self):
        """
        builds a transposed graph
        :param graph:
        :return: transposed graph
        """

        transposed = DiGraph()

        for node in self.get_all_v():
            transposed.add_node(node)

        for node in self.get_all_v():
            for ni in self.nodes[node].outs:
                transposed.add_edge(ni, node, self.nodes[node].outs[ni])

        return transposed

    def __str__(self):
        return "|V|="+str(self.node_size)+" , |E|="+str(self.edges_size)

    def __repr__(self):
        return "|V|="+str(self.node_size)+" , |E|="+str(self.edges_size)

    def __eq__(self, other):
        return other.edges_size == self.edges_size \
               and other.node_size == self.node_size
