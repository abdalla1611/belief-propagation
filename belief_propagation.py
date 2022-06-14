from factor_graph import *
from factor import *


def normalize_msg(message):
    return factor(message.get_variables(), message.get_distribution() / np.sum(message.get_distribution()))


class belief_propagation:
    def __init__(self, fgraph):
        if type(fgraph) is not factor_graph:
            raise Exception('fgraph is not factor graph')
        if not (fgraph.is_connected() and not fgraph.is_loop()):
            raise Exception('this graph is not a tree')

        self.msg = {}
        self.fgraph = fgraph

    def belief(self, v_name):
        incoming_messages = []
        for f_name_neighbor in self.fgraph.get_graph().vs[self.fgraph.get_graph().neighbors(v_name)]['name']:
            incoming_messages.append(self.get_factor2variable_msg(f_name_neighbor, v_name))
        return normalize_msg(joint_distribution(incoming_messages))


    def get_variable2factor_msg(self,v_name , f_name):
        key = (v_name, f_name)
        if key not in self.msg:
            self.msg[key] = self.compute_variable2factor_msg(v_name, f_name)

        return self.msg[key]


    def compute_variable2factor_msg(self, v_name, f_name):
        incoming_messages = []
        for f_name_neighbor in self.fgraph.get_graph().vs[self.fgraph.get_graph().neighbors(v_name)]['name']:
            if f_name_neighbor != f_name:
                incoming_messages.append(self.get_factor2variable_msg(f_name_neighbor, v_name))

        if not incoming_messages:
            # if the variable does not have its own distribution
            return factor([v_name], np.array([1.] * self.fgraph.get_graph().vs.find(name=v_name)['rank']))
        else:
            return normalize_msg(joint_distribution(incoming_messages))


    def get_factor2variable_msg(self, f_name, v_name):
        key = (f_name, v_name)
        if key not in self.msg:
            self.msg[key] = self.compute_factor2variable_msg(f_name, v_name)

        return self.msg[key]

    def compute_factor2variable_msg(self, f_name, v_name):
        incoming_msgs = [self.fgraph.get_graph().vs.find(f_name)['factor_f']]
        marginal_variables = []
        for v_neighbor in self.fgraph.get_graph().vs[self.fgraph.get_graph().neighbors(f_name)]['name']:
            if v_neighbor != v_name:
                incoming_msgs.append(self.get_variable2factor_msg(v_neighbor, f_name))
                marginal_variables.append(v_neighbor)
        return normalize_msg(factor_marginal(joint_distribution(incoming_msgs), marginal_variables))
