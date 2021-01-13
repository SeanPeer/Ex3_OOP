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

    def __sconnect(self, v: int):
        id = 0
        low = dict()
        onStack = dict()
        stack = []

        for n in self.graph.get_all_v().keys():
            low.update({n:0})
            onStack.update({n: False})

        work = [(v, 0)]  # NEW: Recursion stack.
        while work:
            v, i = work[-1]  # i is next successor to process.
            del work[-1]
            if i == 0:  # When first visiting a vertex:
                stack.append(v)
                onStack.update({v: True})
                id += 1
                self.ids.update({v: id})
                low.update({v: id})
            recurse = False
            j=0
            for to in self.graph.all_out_edges_of_node(v).keys():
                w = to
                if self.ids.get(w)==0:
                    # CHANGED: Add w to recursion stack.
                    work.append((v, j + 1))
                    work.append((w, 0))
                    recurse = True
                    j += 1
                    break
                elif onStack.get(to) is True:
                    j += 1
                    low.update({v:min(low.get(v),low.get(to))})

            if recurse: continue  # NEW
            if self.ids.get(v) is low.get(v):
                list_path = []
                while stack:
                    node = stack.pop()
                    list_path.insert(0, node)
                    onStack.update({node: False})
                    low.update({node: (self.ids.get(v))})
                    if node == v: break
                self.lists_path.insert(0, list_path)
            if work:  # NEW: v was recursively visited.
                w = v
                v, _ = work[-1]
                low.update({v:min(low.get(v),low.get(w))})

    def SCCUtil(self, u, low, disc, stackMember, st):

        # Initialize discovery time and low value
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
        stackMember[u] = True
        st.append(u)

        # Go through all vertices adjacent to this
        for v in self.graph.all_out_edges_of_node(u):

            # If v is not visited yet, then recur for it
            if disc[v] == -1:

                self.SCCUtil(v, low, disc, stackMember, st)

                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                # Case 1 (per above discussion on Disc and Low value)
                low[u] = min(low[u], low[v])

            elif stackMember[v]:

                '''Update low value of 'u' only if 'v' is still in stack 
                (i.e. it's a back edge, not cross edge). 
                Case 2 (per above discussion on Disc and Low value) '''
                low[u] = min(low[u], disc[v])

                # head node found, pop the stack and print an SCC
        w = -1  # To store stack extracted vertices
        if low[u] == disc[u]:
            while w != u:
                w = st.pop()
                # print(w)
                # self.sccs.append(w)
                self.component.append(w)
                stackMember[w] = False

            # print("")
            self.sccs.append(self.component)
            self.component = []

            # The function to do DFS traversal.

    # It uses recursive SCCUtil()
    def SCC(self):

        # Mark all the vertices as not visited
        # and Initialize parent and visited,
        # and ap(articulation point) arrays
        disc = [-1] * (self.graph.v_size())
        low = [-1] * (self.graph.v_size())
        stackMember = [False] * (self.graph.v_size())
        st = []

        # Call the recursive helper function
        # to find articulation points
        # in DFS tree rooted with vertex 'i'
        for i in range((self.graph.v_size())):
            if disc[i] == -1:
                self.SCCUtil(i, low, disc, stackMember, st)

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @param id1: The node id
        @return: The list of nodes in the SCC
        """
        self.sccs = []
        self.component = []
        # Mark all the vertices as not visited
        # and Initialize parent and visited,
        # and ap(articulation point) arrays
        disc = [-1] * (self.graph.v_size())
        low = [-1] * (self.graph.v_size())
        stackMember = [False] * (self.graph.v_size())
        st = []

        # Call the recursive helper function
        # to find articulation points
        # in DFS tree rooted with vertex 'i'

        self.SCCUtil(id1, low, disc, stackMember, st)

        return self.sccs

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC
        """
        self.sccs = []
        self.component = []
        self.SCC()
        return self.sccs
        # for v in self.graph.nodes:
        #     self.graph.nodes[v].tag = False
        #
        # sccs = []
        # for v in self.graph.get_all_v():
        #     c = self.dfs_with_stack(v, self.graph)
        #     if c:
        #         sccs.append(c)
        #
        # return sccs
        #
        # stack = []
        #
        # # visited = {i: False for i in self.graph.get_all_v()}
        #
        # for v in self.graph.get_all_v():
        #     # if not visited[v]:
        #     if not self.graph.nodes[v].tag:
        #         # self.fillStack(self.graph.get_all_v(), v, visited, stack)
        #         self.fillStack_tag(self.graph.get_all_v(), v, stack)
        #
        # transposed = DiGraph.transpose(self.get_graph())
        #
        # # visited = {i: False for i in self.graph.get_all_v()}
        #
        # res = []
        # while stack:
        #     v = stack.pop()
        #     final = set()
        #     if not transposed.nodes[v].tag:
        #         # component = self.dfs(transposed.get_all_v(), v, final)
        #         component = self.dfs_with_stack(v, transposed)
        #         res.append(component)
        #
        # return res

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
