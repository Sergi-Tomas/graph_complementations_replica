import graph as gph

if __name__ == "__main__":
    graph = gph.Graph()

    node0 = gph.Node(0)
    node1 = gph.Node(1)
    node2 = gph.Node(2)
    node3 = gph.Node(3)

    graph.add_node(node0)
    graph.add_node(node1)
    graph.add_node(node2)
    graph.add_node(node3)

    qbit0 = gph.Qbit(0)
    qbit1 = gph.Qbit(1)
    qbit2 = gph.Qbit(2)
    qbit3 = gph.Qbit(3)
    qbit4 = gph.Qbit(4)
    qbit5 = gph.Qbit(5)

    node0.add_qbit(qbit0)
    node0.add_qbit(qbit1)
    node0.add_qbit(qbit2)
    node1.add_qbit(qbit3)
    node2.add_qbit(qbit4)
    node3.add_qbit(qbit5)

    graph.add_edge(qbit0, qbit3)
    graph.add_edge(qbit1, qbit4)
    graph.add_edge(qbit2, qbit5)
    
    graph.draw()

    graph.subgraph_complementation(node0)

    graph.draw()