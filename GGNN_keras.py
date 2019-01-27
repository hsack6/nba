from keras import backend as K
from keras.engine.topology import Layer

def split(tensor, axis=0):
    # split tensor at the specified axis.
    tensor_axis = [i for i in range(len(tensor.shape))]
    tensor_axis[0], tensor_axis[axis] = tensor_axis[axis], tensor_axis[0]
    pattern = [tensor_axis[0]]
    pattern.extend(sorted(tensor_axis[1:]))
    tensor = K.permute_dimensions(tensor, tuple(pattern))
    return [tensor[0] for i in range(tensor.shape[0])]

def stack(list_of_tensor, axis=0):
    return K.stack(list_of_tensor, axis)

def activate(h, edges_dict, activate_kernel_dict, activate_bias):
    vertices = split(h, axis=1)
    number_of_vertices = len(vertices)
    state = [[] for _ in range(number_of_vertices)]
    for label in edges_dict.keys():
        edges = edges_dict[label]
        activate_kernel = activate_kernel_dict[label]

        # forward edges
        input_tensor = stack(list(map(lambda x: vertices[x[0]], edges)), axis=0)
        output_tensor = K.dot(input_tensor, activate_kernel)
        output_tensor = split(output_tensor, axis=0)
        for edge, output in zip(edges, output_tensor):
            state[edge[1]].append(output)
        # reverse edges : Omitted for undirected graph

    # assemble state
    state = np.array(state)
    outputs = stack(list(map(lambda x: K.sum(x, axis=0), state)), axis=1)

    # add bias
    outputs = outputs + activate_bias
    return outputs


def propagate(h, edges_dict, activate_kernel_dict, activate_bias, GRU_W_z, GRU_W_r, GRU_W, GRU_U_z, GRU_U_r, GRU_U):
    a = activate(h, edges_dict, activate_kernel_dict, activate_bias)
    z = K.sigmoid(K.dot(a, GRU_W_z) + K.dot(h, GRU_U_z))
    r = K.sigmoid(K.dot(a, GRU_W_r) + K.dot(h, GRU_U_r))
    h_hat = K.tanh(K.dot(a, GRU_W) + K.dot(r * h, GRU_U))
    h_next = ((1 - z) * h) + (z * h_hat)
    return h_next

def node_representation(h, x, representation_kernel, representation_bias):
    return K.dot(K.concatenate([h, x]), representation_kernel) + representation_bias

class GGNN(Layer):
    def __init__(self, edges_dict, vertex_annotations, iter_propagate, **kwargs):
        self.edges_dict = edges_dict
        self.vertex_annotations = vertex_annotations
        self.iter_propagate = iter_propagate
        super(GGNN, self).__init__(**kwargs)

    def build(self, input_shape):
        self.activate_kernel_dict = {label: self.add_weight(name='activate_kernel' + str(label),
                                                            shape=(input_shape[-1], input_shape[-1]),
                                                            initializer='uniform',
                                                            trainable=True) for label in self.edges_dict.keys()}
        self.activate_bias = self.add_weight(name='activate_bias',
                                             shape=(1, input_shape[-1]),
                                             initializer='zeros')
        self.GRU_W_z = self.add_weight(name='GRU_W_z',
                                    shape=(input_shape[-1], input_shape[-1]),
                                    initializer='uniform',
                                    trainable=True)
        self.GRU_W_r = self.add_weight(name='GRU_W_r',
                                    shape=(input_shape[-1], input_shape[-1]),
                                    initializer='uniform',
                                    trainable=True)
        self.GRU_W = self.add_weight(name='GRU_W',
                                 shape=(input_shape[-1], input_shape[-1]),
                                 initializer='uniform',
                                 trainable=True)
        self.GRU_U_z = self.add_weight(name='GRU_U_z',
                                    shape=(input_shape[-1], input_shape[-1]),
                                    initializer='uniform',
                                    trainable=True)
        self.GRU_U_r = self.add_weight(name='GRU_U_r',
                                    shape=(input_shape[-1], input_shape[-1]),
                                    initializer='uniform',
                                    trainable=True)
        self.GRU_U = self.add_weight(name='GRU_U',
                                 shape=(input_shape[-1], input_shape[-1]),
                                 initializer='uniform',
                                 trainable=True)
        self.representation_kernel = self.add_weight(name='representation_kernel',
                                                     shape=(input_shape[-1] + self.vertex_annotations.shape[-1], input_shape[-1]),
                                                     initializer='uniform',
                                                     trainable=True)
        self.representation_bias = self.add_weight(name='representation_bias',
                                                   shape=(1, input_shape[-1]),
                                                   initializer='zeros')
        super(GGNN, self).build(input_shape)

    def call(self, x):
        self.h = x
        self.state_size = self.h.shape[-1]
        for _ in range(self.iter_propagate):
            self.h = propagate(self.h, self.edges_dict, self.activate_kernel_dict, self.activate_bias, self.GRU_W_z, self.GRU_W_r, self.GRU_W, self.GRU_U_z, self.GRU_U_r, self.GRU_U)

        return node_representation(self.h, self.vertex_annotations, self.representation_kernel, self.representation_bias)

    def compute_output_shape(self, input_shape):
        return (input_shape)


print(save_graph_data[0][0])
print(save_graph_data[0][1])
print(save_graph_data[0][2].shape)
print(save_graph_data[0][3].keys())
print(save_graph_data[0][4].shape)
print(save_graph_data[0][5].shape)
print(save_graph_data[0][6].shape)

def h_0(vertex_annotations, h_size):
    h = np.zeros((vertex_annotations.shape[0], vertex_annotations.shape[1], h_size))
    h[:, :, 0:vertex_annotations.shape[-1]] = vertex_annotations
    return h

sample_num = len(save_graph_data)
h_size = 40
iter_propagate = 1
L = save_graph_data[0][0]
year_start = 1951 + L
max_vertex_num = max([save_graph_data[i][2].shape[0] for i in range(len(save_graph_data))])

V = np.array([save_graph_data[i][2] for i in range(len(save_graph_data))])
h = np.zeros((sample_num, max_vertex_num, L, h_size))
vertex_annotations = np.zeros((sample_num, max_vertex_num, L, V[0].shape[-1]))
for sample in range(sample_num):
    #print(V[sample].shape[0])
    h[sample][0:V[sample].shape[0]] = h_0(V[sample], h_size)
    vertex_annotations[sample][0:V[sample].shape[0]] = V[sample]
print(h.shape)
print(vertex_annotations.shape)
#print(np.sum(h[0][190:]))
#print(np.sum(x[0][190:]))

#E = np.zeros((sample_num, L+1, max_vertex_num, max_vertex_num))
#for sample in range(sample_num):
#    for timestep in range(L+1):
        #print(year_start+sample, timestep, len(save_graph_data[sample][3][timestep]))
#        for edge in save_graph_data[sample][3][timestep]:
#            E[sample][timestep][edge[0]][edge[1]] = 1
#        assert np.allclose(E[sample][timestep].T, E[sample][timestep]), 'Not an undirected graph'
#print(E.shape)

edges_dict_list = [save_graph_data[i][3] for i in range(len(save_graph_data))]

E = np.array([i for i in range(V.shape[0])])

h_input = Input(shape=h[0].shape)
E_input = Input(shape=E[0].shape)

print(E.shape)
print(E_input.shape)

ggnn = GGNN(iter_propagate, L+1, 31, edges_dict_list)([h_input, K.variable(edges_dict_list[0])])
model = Model([h_input, E_input], ggnn)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
print(model.summary())

model.fit(x_train, y_train, epochs=20, batch_size=1, shuffle=True)
