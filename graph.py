import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    '''
    Basic graph operations
    '''

    def add_node(self, node):
        self.nodes.append(node)
        node.set_graph(self)

    def add_edge(self, qbit1, qbit2):
        self.edges.append((qbit1, qbit2))
        qbit1.add_connection(qbit2)
        qbit2.add_connection(qbit1)

    def remove_edge(self, qbit1, qbit2):
        self.edges.remove((qbit1, qbit2))
        qbit1.remove_connection(qbit2)
        qbit2.remove_connection(qbit1)

    def remove_qbit(self, qbit):
        # Remove all connections to this qbit
        for connection in list(qbit.get_connections()):
            self.remove_edge(qbit, connection)
        
        # Remove qbit from its node
        if qbit.get_node() is not None:
            qbit.get_node().remove_qbit(qbit)
            
    def get_all_nodes(self):
        return self.nodes

    def get_all_edges(self):
        return self.edges

    '''
    Node operations
    '''
    def cz(self, qbit1, qbit2):
        if (qbit1, qbit2) in self.edges or (qbit2, qbit1) in self.edges:
            self.remove_edge(qbit1, qbit2)
        else:
            self.add_edge(qbit1, qbit2)

    def lc(self, qbit):
        comb = combinations(qbit.get_connections(), 2)

        for pair in comb:
            self.cz(pair[0], pair[1])
    '''
    Algorithms
    '''
    def subgraph_complementation(self, node, clique_distr = False):
        target = node.get_qbits()[0]
        nodeqbs = node.get_qbits()[1:]

        #Step 1
        for qbit in nodeqbs:
            self.cz(target, qbit)
        self.draw()
        #Step 2
        for qbit in nodeqbs:    
            self.lc(qbit)
        self.draw()

        #Step 3
        for qbit in nodeqbs:
            self.cz(target, qbit)
        self.draw()

        #Step 4
        self.lc(target)

        #Measurement of the nodeqbs in orden to deliver a k-clique graph state. (see pg. 3 bottom left paragraph)
        if clique_distr:
            for qbit in nodeqbs:
                self.remove_qbit(qbit)

    def edge_reset(self, node):
        target = node.get_qbits()[0]
        nodeqbs = node.get_qbits()[1:]

        #Step 3
        for qbit in nodeqbs:
            self.cz(target, qbit)

        #Step 2
        for qbit in nodeqbs:
            self.lc(qbit)

        #Step 1
        for qbit in nodeqbs:
            self.cz(target, qbit)

    def draw(self):
        G = nx.Graph()
        color_map = []
        color_index = 0
        node_colors = {}

        # Assign colors to nodes
        for node in self.nodes:
            node_color = plt.cm.tab10(color_index % 10)
            node_colors[node] = node_color
            color_index += 1

        # Add nodes and edges to the graph
        for node in self.nodes:
            for qbit in node.get_qbits():
                G.add_node(qbit.get_id(), label=f'Qbit {qbit.get_id()}')
                color_map.append(node_colors[node])
                for connection in qbit.get_connections():
                    G.add_edge(qbit.get_id(), connection.get_id())
        
        pos = nx.spring_layout(G)
        labels = nx.get_node_attributes(G, 'label')
        nx.draw(G, pos, with_labels=True, labels=labels, node_size=500, node_color=color_map, font_size=10, font_weight="bold", edge_color="gray")
        plt.show()

class Node:
    def __init__(self, id):
        self.id = id
        self.qbits = []
        self.graph = None

    def add_qbit(self, qbit):
        self.qbits.append(qbit)
        qbit.set_node(self)

    def set_graph(self, graph):
        self.graph = graph

    def get_qbits(self):
        return self.qbits

    def get_id(self):
        return self.id
        

class Qbit:
    def __init__(self, id):
        self.id = id
        self.connections = []
        self.node = None

    def add_connection(self, qbit):
        self.connections.append(qbit)

    def remove_connection(self, qbit):
        if qbit in self.connections:
            self.connections.remove(qbit)

    def set_node(self, node):
        self.node = node

    def get_connections(self):
        return self.connections

    def get_node(self):
        return self.node

    def get_id(self):
        return self.id


