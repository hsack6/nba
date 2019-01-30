import numpy as np

def load_graphs_from_file(path):
    graph_data = np.load(path)
    # nodes           = graph_data[:][0] (192, 2, 45)
    # edges           = graph_data[:][1] (192, 576)
    # label_attribute = grpah_data[:][2] (192, 4)
    # label_lost      = graph_data[:][3] (192,)
    # label_return    = graph_data[:][4] (192,)
    return graph_data[:, :5]

def find_edge_type_num(all_data):
    return all_data[0][1].shape[1] / all_data[0][1].shape[0]

def find_max_node_num(all_data):
    n_examples = len(all_data)
    max_node_num = 0
    for i in range(n_examples):
        if all_data[i][0].shape[0] > max_node_num:
            max_node_num = all_data[i][0].shape[0]
    return max_node_num

def zero_padding(all_data, n_node, n_edge_types):
    n_examples = len(all_data)
    expanded_nodes = np.zeros((n_examples, n_node, all_data[0][0].shape[1], all_data[0][0].shape[2]))
    for i in range(n_examples):
        n_node_i = all_data[i][0].shape[0]
        expanded_nodes[i, 0:n_node_i] = all_data[i][0]
    # print(expanded_nodes.shape) (63, 860, 2, 45)
    expanded_edges = np.zeros((n_examples, n_node, n_edge_types * n_node))
    for i in range(n_examples):
        a_i = all_data[i][1]
        n_node_i = all_data[i][1].shape[0]
        for j in range(n_edge_types):
            expanded_edges[i, 0:n_node_i, j*n_node : j*n_node+n_node_i] = a_i[:, j*n_node_i:(j+1)*n_node_i]
    # print(expanded_edges.shape) (63, 860, 2580)
    expanded_label_attribute = np.zeros((n_examples, n_node, all_data[0][2].shape[1]))
    for i in range(n_examples):
        n_node_i = all_data[i][2].shape[0]
        expanded_label_attribute[i, 0:n_node_i] = all_data[i][2]
    # print(expanded_label_attribute.shape) (63, 860, 4)
    expanded_label_lost = np.zeros((n_examples, n_node))
    for i in range(n_examples):
        n_node_i = all_data[i][3].shape[0]
        expanded_label_lost[i, 0:n_node_i] = all_data[i][3]
    expanded_label_return = np.zeros((n_examples, n_node))
    for i in range(n_examples):
        n_node_i = all_data[i][4].shape[0]
        expanded_label_lost[i, 0:n_node_i] = all_data[i][4]
    # print(expanded_label_lost.shape, expanded_label_return.shape) ((63, 860), (63, 860))
    return [[expanded_nodes[i], expanded_edges[i], expanded_label_attribute[i], expanded_label_lost[i], expanded_label_return[i]] for i in range(n_examples)]

def split_set(data_list):
    n_examples = len(data_list)
    idx = range(n_examples)
    return data_list[:50], data_list[-10:]

class NBADataset():
    """
    Load NBA dataset for GGNN
    """
    def __init__(self, path, is_train):
        all_data = load_graphs_from_file(path)
        self.n_edge_types =  find_edge_type_num(all_data)
        self.n_node = find_max_node_num(all_data)
        all_data = zero_padding(all_data, self.n_node, self.n_edge_types)

        all_task_train_data, all_task_val_data = split_set(all_data)

        if is_train:
            self.data = all_task_train_data
        else:
            self.data = all_task_val_data

    def __getitem__(self, index):
        annotation = self.data[index][0]
        am = self.data[index][1]
        label_attribute = self.data[index][2]
        label_lost = self.data[index][3]
        label_return = self.data[index][4]
        return annotation, am, label_attribute, label_lost, label_return

    def __len__(self):
        return len(self.data)
