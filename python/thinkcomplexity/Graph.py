import string
import random
import math

from itertools import chain

try:
    from Gui import Gui, GuiCanvas
except ImportError:
    from swampy.Gui import Gui, GuiCanvas

class Graph(dict):
    '''
    A Graph is a dictionary of dictionaries. The out
    dictionary maps from a vertex to an inner dictionary.
    The inner dictionary maps from other vertices to edges.

    For vertices a and b, Graph[a][b] maps
    to the edge that connects a->b if it exists.
    '''

    def __init__(self, vs=[], es=[]):
        '''
        Create a new graph.
        (vs) is a list of vertices.
        (es) is a list of edges.
        '''
        for v in vs:
            self.add_vertex(v)

        for e in es:
            self.add_edge(e)

    def add_vertex(self, v):
        '''add (v) to the graph'''
        self[v] = {}

    def add_edge(self, e):
        '''
        Add (e) to the graph by adding an entry in both directions.

        If there is already an edge connecting these Vertices, the
        new edge replaces it.
        '''
        v, w = e
        self[v][w] = e
        self[w][v] = e

    def get_edge(self, v, w):
        '''get edge between (v, w) if it exists, else None'''
        try:
            return self[v][w]
        except KeyError:
            return None

    def remove_edge(self, e):
        '''remove Edge (e) from all Vertices'''
        v, w = e
        try:
            del self[v][w]
        except:
            pass
        try:
            del self[w][v]
        except:
            pass

    def vertices(self):
        '''return a list of all Vertices in the Graph'''
        return self.keys()

    def edges(self):
        '''return a list of all Edges in the Graph'''
        return list(set(self[i][j] for i in self for j in self[i]))

    def out_vertices(self, v):
        '''return a list of Vertices adjacent to (v)'''
        return [k for k in self[v]]

    def out_edges(self, v):
        '''return a list of edges connected to Vertex (v)'''
        return [self[v][k] for k in self[v]]

    def add_all_edges(self):
        '''complete a graph by adding edges between all pairs Vertices'''
        l = self.vertices()
        self._handshake(lambda g,x,y: g.add_edge(Edge(x,y)), l[0], l[1:])

    def _handshake(self, f, x, rest):
        if len(rest) == 0:
            return
        for y in rest:
            f(self, x, y)
        self._handshake(f, rest[0], rest[1:])

    def is_connected(self):
        vs = self.vertices()
        if len(vs) < 1: return False
        to_visit = [vs[0]]
        visited = []
        while len(to_visit) > 0:
            v = to_visit.pop()
            visited.append(v)
            for vn in self.out_vertices(v):
                if vn not in visited:
                    to_visit.append(vn)

        return set(visited) == set(vs)

class Vertex(object):
    '''A Vertex is a node in a Graph.'''

    def __init__(self, label=''):
        self.label = label

    def __repr__(self):
        return 'Vertex(%s)' % repr(self.label)

    __str__ = __repr__


class Edge(tuple):
    '''An Edge is a tuple of two Vertices'''

    def __new__(cls, e1, e2):
        return tuple.__new__(cls, (e1, e2))

    def __repr__(self):
        return 'Edge(%s, %s)' % (repr(self[0]), repr(self[1]))

    __str__ = __repr__

def show_graph(script, n='10', *args):
    import GraphWorld

    # create n Vertices
    n = int(n)
    labels = string.ascii_lowercase + string.ascii_uppercase
    vs = [Vertex(c) for c in labels[:n]]

    # create a graph and a layout
    g = Graph(vs)
    g.add_all_edges()
    layout = GraphWorld.CircleLayout(g)

    # draw the graph
    gw = GraphWorld.GraphWorld()
    gw.show_graph(g, layout)
    gw.mainloop()

    # is it connected?
    print("Graph connected: " + str(g.is_connected()))

if __name__ == '__main__':
    import sys
    show_graph(*sys.argv) 
