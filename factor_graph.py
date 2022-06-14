import igraph as ig

from factor import *
import pyvis.network as net


def string2factor_graph(str_):
    res_factor_graph = factor_graph()
    str_ = [i.split('(') for i in str_.split(')') if i != '']
    for i in range(len(str_)):
        str_[i][1] = str_[i][1].split(',')

    for i in str_:
        res_factor_graph.add_factor_node(i[0], factor(i[1]))

    return res_factor_graph


'''draw the factor graph'''


def plot_factor_graph(g):
    graph = net.Network(notebook=True, width="100%")
    graph.toggle_physics(False)
    # Vertices
    label = g.get_graph().vs['name']
    color = ['black' if i is True else 'gray' for i in g.get_graph().vs['is_factor']]
    shape = ['square' if i is True else 'circle' for i in g.get_graph().vs['is_factor']]
    graph.add_nodes(range(len(g.get_graph().vs)), label=label, color=color, shape=shape)

    # Edges
    graph.add_edges(g.get_graph().get_edgelist())
    return graph.show("graph.html")


class factor_graph:
    def __init__(self):
        self._graph = ig.Graph()

    def add_factor_node(self, name_f, factor_f):
        for v_name in factor_f.get_variables():
            if self.get_node_status(v_name) == False:
                self.create_variable_node(v_name)

        self.set_variable_ranks(factor_f)
        self.create_factor_node(name_f, factor_f)

    def change_factor_distribution(self, name_f, factor_f):
        self.set_variable_ranks(factor_f)
        self._graph.vs.find(name=name_f)['factor_f'] = factor_f

    def create_factor_node(self, name_f, factor_f):
        self._graph.add_vertex(name_f)
        self._graph.vs.find(name=name_f)['is_factor'] = True
        self._graph.vs.find(name=name_f)['factor_f'] = factor_f
        # create the edges
        start = self._graph.vs.find(name=name_f).index
        edge_list = [tuple([start, self._graph.vs.find(name=v_name).index]) for v_name in factor_f.get_variables()]
        self._graph.add_edges(edge_list)

    def set_variable_ranks(self, factor_f):
        for i, v_name in enumerate(factor_f.get_variables()):
            if factor_f.is_none():
                self._graph.vs.find(name=v_name)['rank'] = None
            else:
                self._graph.vs.find(name=v_name)['rank'] = factor_f.get_shape()[i]

    def add_variable_node(self, v_name):
        self.create_variable_node(v_name)

    def create_variable_node(self, v_name, rank=None):
        self._graph.add_vertex(v_name)
        self._graph.vs.find(name=v_name)['is_factor'] = False
        self._graph.vs.find(name=v_name)['rank'] = rank

    def get_node_status(self, name):
        if len(self._graph.vs) == 0:
            return False
        elif len(self._graph.vs.select(name_eq=name)) == 0:
            return False
        else:
            if self._graph.vs.find(name=name)['is_factor']:
                return 'factor'
            else:
                return 'variable'

    def get_graph(self):
        return self._graph

    def is_connected(self):
        return self._graph.is_connected()

    def is_loop(self):
        return any(self._graph.is_loop())
