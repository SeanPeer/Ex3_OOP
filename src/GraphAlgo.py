from typing import List
import DiNode
from src import GraphInterface
import heapq
from DiGraph import DiGraph
import json as js
import sys
import matplotlib.pyplot as plt
import random
import threading


class GraphAlgo:

    def __init__(self, graph=None):
        self.graph = graph
        self.Time = 0
        self.sccs = []
        self.component = []

        self.ids = {}
        self.list_path = []
        self.lists_path = []
        # sys.setrecursionlimit(6_000)


    def get_graph(self) -> GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """

        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """

        loaded_graph = DiGraph()
        try:
            with open(file_name, 'r') as json_f:
                data = js.load(json_f)

            for n in data['Nodes']:
                try:
                    pos = n['pos'].split(',')
                    x, y, z = float(pos[0]), float(pos[1]), float(pos[2])
                    loaded_graph.add_node(n['id'], (x, y, z))
                except:
                    loaded_graph.add_node(n['id'])

            for e in data['Edges']:
                loaded_graph.add_edge(e['src'], e['dest'], e['w'])

            self.graph = loaded_graph
            return True

        except OSError as err:
            print("OS error: {0}".format(err))
            return False
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, Flase o.w.

        note: data will be saved as {Edges: [], Nodes: []}
        """

        nodes = self.graph.get_all_v()

        data = {'Edges': [], 'Nodes': []}

        for n in nodes:
            node = nodes[n]

            data['Nodes'].append({
                'id': node.id,
                'pos': node.pos
            })

            for o in node.outs:
                data['Edges'].append({
                    'src': o,
                    'w': node.outs[o],
                    'dest': node.id
                })

        try:
            with open(file_name, 'w') as out:
                js.dump(data, out)
                return True

        except OSError as err:
            print("OS error: {0}".format(err))
            return False
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, the path as a list
        Example:
#      >>> from GraphAlgo import GraphAlgo
#       >>> g_algo = GraphAlgo()
#        >>> g_algo.addNode(0)
#        >>> g_algo.addNode(1)
#        >>> g_algo.addNode(2)
#        >>> g_algo.addEdge(0,1,1)
#        >>> g_algo.addEdge(1,2,4)
#        >>> g_algo.shortestPath(0,1)
#        (1, [0, 1])
#        >>> g_algo.shortestPath(0,2)
#        (5, [0, 1, 2])
        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """

        nodes = self.graph.get_all_v()
        if id1 not in nodes or id2 not in nodes\
                or id1 == id2:
            return float('inf'), []

        parents = {i: None for i in nodes}
        distances = {i: float('inf') for i in nodes}
        distances[id1] = 0

        min_distance = [(0, id1)]
        visited = set()

        while min_distance:

            cur_dist, cur = heapq.heappop(min_distance)

            if cur in visited: continue
            visited.add(cur)

            for ni in self.graph.all_out_edges_of_node(cur):
                if ni in visited: continue

                alt = cur_dist + self.graph.all_out_edges_of_node(cur)[ni]

                if alt < distances[ni]:
                    distances[ni] = alt
                    parents[ni] = cur

                    heapq.heappush(min_distance, (alt, ni))

        cur = id2
        path = [cur]

        while cur:
            path.append(parents[cur])
            cur = parents[cur]

            if cur == id1:
                break

            if cur is None:
                return distances[id2], []

        return distances[id2], path[::-1]

    def bfs_util(self, v, nodes, stack):
        q = [v]
        nodes[v].tag = True

        while q:
            indx = q.pop()

            for i in self.graph.all_out_edges_of_node(indx):
                if not nodes[i].tag:
                    nodes[i].tag = True
                    q.append(i)
            stack.append(indx)

    def bfs(self, v, graph, final):
        q = [v]
        final.append(v)
        graph.nodes[v].tag = True

        while q:
            indx = heapq.heappop(q)

            for i in graph.all_out_edges_of_node(indx):

                if not graph.nodes[i].tag:
                    graph.nodes[i].tag = True
                    q.append(i)
                    final.append(i)

        return final

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        used Kosaraju's algorithm with BFS

        @param id1: The node id
        @return: The list of nodes in the SCC
        """

        nodes = self.graph.get_all_v()

        for n in nodes:
            nodes[n].tag = False

        stack = []

        self.bfs_util(id1, nodes, stack)

        # transpose graph
        transpose_graph = self.graph.transpose()

        scc_path = []

        self.bfs(id1, transpose_graph, scc_path)

        return list(set(stack).intersection(scc_path))

    def connected_components(self) -> List[list]:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        used Kosaraju's altered with BFS to avoid recursive overflow

        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC
        """

        for n in self.graph.get_all_v():
            self.graph.get_all_v()[n].tag = False

        result = []

        for n in self.graph.get_all_v():

            flag = False
            for i in result:
                if n in i: flag = True

            if flag: continue

            for x in self.graph.get_all_v():
                self.graph.get_all_v()[x].tag = False

            stack = []

            self.bfs_util(n, self.graph.get_all_v(), stack)

            # transpose graph
            transpose_graph = self.graph.transpose()

            scc_path = []

            self.bfs(n, transpose_graph, scc_path)

            result.append(list(set(stack).intersection(scc_path)))

        return result

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """

        nodes = self.graph.get_all_v()

        x_, y_, z_ = [], [], []
        xy_id = []

        ax = plt.axes()
        for n in nodes:
            node_ = nodes[n]
            if node_.pos is None:
                node_.update_position(self.graph.v_size())
                # x, y, z = random.randint(0, self.graph.v_size()), random.uniform(0, self.graph.v_size()), 0

            (x, y, z) = node_.pos

            for out in node_.outs:

                o_ = self.graph.nodes[out]

                if o_.pos is None:
                    o_.update_position(self.graph.v_size())
                    # o_x, o_y, o_z = random.randint(0, self.graph.v_size()), random.uniform(0, self.graph.v_size()), 0

                (o_x, o_y, o_z) = o_.pos

                # print(f"x:{x}, y:{y}, dx:{o_x-x}, dy:{o_y-y}")

                # plot arrows between nodes
                ax.quiver(x, y, o_x-x, o_y-y, angles='xy', scale_units='xy', scale=1, width=0.005)

            xy_id.append((x, y, node_.id))
            x_.append(x)
            y_.append(y)
            z_.append(z)

        # plt.xlim(left=min(x_), right=max(x_))
        # plt.ylim(bottom=min(y_), top=max(y_))

        # plot node id's
        for i, (x, y, id_) in enumerate(xy_id):
            plt.annotate(id_, (x, y), fontsize='xx-large', color='red')

        # plot nodes
        plt.plot(x_, y_, 'bo')
        plt.show()
