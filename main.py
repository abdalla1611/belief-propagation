import numpy as np
import igraph as ig
from factor import *
from factor_graph import *
from belief_propagation import *

if __name__ == '__main__':
    mrf = string2factor_graph('Gr(i,d,g)Sa(i,s)Le(g,l)In(i)Di(d)')
    '''draw the graph'''
    plot_factor_graph(mrf)
    Di = factor(['d'], np.array([0.6, 0.4]))
    In = factor(['i'], np.array([0.7, 0.3]))
    Gr = factor(['i', 'd', 'g'], np.array([[[0.3, 0.4, 0.3], [0.05, 0.25, 0.7]], [[0.9, 0.08, 0.02], [0.5, 0.3, 0.2]]]))
    Sa = factor(['i', 's'], np.array([[0.95, 0.05], [0.2, 0.8]]))
    Le = factor(['g', 'l'], np.array([[0.1, 0.9], [0.4, 0.6], [0.99, 0.01]]))
    '''update the factors'''
    mrf.change_factor_distribution('Gr', Gr)
    mrf.change_factor_distribution('Sa', Sa)
    mrf.change_factor_distribution('Le', Le)
    mrf.change_factor_distribution('In', In)
    mrf.change_factor_distribution('Di', Di)
    '''compute'''
    bp = belief_propagation(mrf)
    print('p(i) is ', bp.belief('i').get_distribution())
    print('p(g) is ', bp.belief('g').get_distribution())
    print('p(d) is ', bp.belief('d').get_distribution())
    print('p(s) is ', bp.belief('s').get_distribution())
    print('p(l) is ', bp.belief('l').get_distribution())

