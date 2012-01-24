import random
import string

from Graph import Graph, Vertex, Edge

class RandomGraph(Graph):

    def add_random_edges(self, p=0.05):
        def random_add(g, x, y):
            if random.random() < p:
                g.add_edge(Edge(x, y))
        vs = self.vertices()
        self._handshake(random_add, vs[0], vs[1:])


def show_graph(script, n='15', *args):
    import GraphWorld

    # create n Vertices
    n = int(n)
    labels = string.ascii_lowercase + string.ascii_uppercase
    vs = [Vertex(c) for c in labels[:n]]

    # create a graph and a layout
    g = RandomGraph(vs)
    g.add_random_edges(0.7)
    layout = GraphWorld.CircleLayout(g)

    # draw the graph
    gw = GraphWorld.GraphWorld()
    gw.show_graph(g, layout)
    gw.mainloop()

    # is connected?
    print("Is connected? " + str(g.is_connected()))


if __name__ == '__main__':
    import sys
    show_graph(*sys.argv) 
