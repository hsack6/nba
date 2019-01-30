import torch
import torch.nn as nn

class AttrProxy(object):
    def __init__(self, module, prefix):
        self.module = module
        self.prefix = prefix

    def __getitem__(self, i):
        return getattr(self.module, self.prefix + str(i))


class OutputLayer(nn.Module):
    def __init__(self, state_dim, n_timesteps, n_node):
        super(OutputLayer, self).__init__()
        self.state_dim = state_dim
        self.n_timesteps = n_timesteps
        self.n_node = n_node
        self.out = nn.Sequential(
            nn.Linear(self.n_timesteps * self.state_dim, 31)
        )
        self._initialization()

    def _initialization(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                m.weight.data.normal_(0.0, 0.02)
                m.bias.data.fill_(0)

    def forward(self, prop_state):
        flatten_state = prop_state.view(-1, self.n_node,  self.n_timesteps * self.state_dim)
        output = self.out(flatten_state)
        return output


class Propogator(nn.Module):
    def __init__(self, state_dim, n_node, n_edge_types, n_timesteps):
        super(Propogator, self).__init__()
        self.n_node = n_node
        self.n_edge_types = n_edge_types
        self.n_timesteps = n_timesteps
        self.state_dim = state_dim
        self.reset_gate = nn.Sequential(
            nn.Linear(state_dim * 2, state_dim),
            nn.Sigmoid()
        )
        self.update_gate = nn.Sequential(
            nn.Linear(state_dim * 2, state_dim),
            nn.Sigmoid()
        )
        self.transform = nn.Sequential(
            nn.Linear(state_dim * 2, state_dim),
            nn.Tanh()
        )


    def forward(self, state_in, state_cur, A):
        a_in = []
        for i in range(self.n_timesteps):
            a_in.append(torch.bmm(A, state_in.transpose(0, 2).transpose(1, 2)[i]))
        a_in = torch.stack(a_in).transpose(0, 2).transpose(0, 1).contiguous()
        a = torch.cat((a_in, state_cur), 3)
        r = self.reset_gate(a)
        z = self.update_gate(a)
        joined_input = torch.cat((a_in, r * state_cur), 3)
        h_hat = self.transform(joined_input)
        output = (1 - z) * state_cur + z * h_hat
        return output


class GGNN(nn.Module):
    def __init__(self, state_dim, annotation_dim, n_edge_types, n_timesteps, n_node, n_steps, model):
        super(GGNN, self).__init__()
        assert state_dim >= annotation_dim,  'state_dim must be no less than annotation_dim'
        self.state_dim = state_dim
        self.annotation_dim = annotation_dim
        self.n_edge_types = n_edge_types
        self.n_timesteps = n_timesteps
        self.n_node = n_node
        self.n_steps = n_steps
        self.is_output = 1 if model == 0 else 0
        for i in range(self.n_edge_types):
            in_fc = nn.Linear(self.state_dim, self.state_dim)
            self.add_module("in_{}".format(i), in_fc)
        self.in_fcs = AttrProxy(self, "in_")
        self.propogator = Propogator(self.state_dim, self.n_node, self.n_edge_types, self.n_timesteps)
        self.annotation_join = nn.Sequential(
            nn.Linear((self.state_dim + self.annotation_dim), self.state_dim),
            nn.Tanh(),
        )
        self.output = OutputLayer(self.state_dim, self.n_timesteps, self.n_node)
        self._initialization()

    def _initialization(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                m.weight.data.normal_(0.0, 0.02)
                m.bias.data.fill_(0)

    def forward(self, prop_state, annotation, A):
        for i_step in range(self.n_steps):
            in_states = []
            for i in range(self.n_edge_types):
                in_states.append(self.in_fcs[i](prop_state))
            in_states = torch.stack(in_states).transpose(0, 1).contiguous()
            in_states = in_states.view(-1, self.n_node*self.n_edge_types, self.n_timesteps, self.state_dim)
            prop_state = self.propogator(in_states, prop_state, A)
        join_state = torch.cat((prop_state, annotation), 3)
        output = self.annotation_join(join_state)
        if self.is_output:
            output = self.output(output)
        return output

class CNN(nn.Module):
    def __init__(self, state_dim, batchSize, n_node, n_timesteps, model):
        super(CNN, self).__init__()
        self.state_dim = state_dim
        self.batch_size = batchSize
        self.n_node = n_node
        self.n_timesteps = n_timesteps
        self.conv = nn.Conv2d(in_channels=1, out_channels=self.state_dim, kernel_size=(2, self.state_dim), stride=1, padding=0)
        self.is_output = 1 if model == 1 else 0
        self.output = OutputLayer(state_dim, self.n_timesteps-1, n_node)
        self._initialization()

    def _initialization(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                m.weight.data.normal_(0.0, 0.02)
                m.bias.data.fill_(0)

    def forward(self, x, dummy0, dummy1):
        output = x.view(self.batch_size*self.n_node, self.n_timesteps, self.state_dim, 1).transpose(1, 3).transpose(2, 3)
        output = self.conv(output)
        output = output.view(output.size()[0],output.size()[1],output.size()[2]).transpose(1, 2).contiguous()
        output = output.view(self.batch_size, self.n_node, output.size()[1], output.size()[2])
        if self.is_output:
            output = self.output(output)
        return output

class GatedCNN(nn.Module):
    def __init__(self, state_dim, batchSize, n_node, n_timesteps, model):
        super(GatedCNN, self).__init__()
        self.state_dim = state_dim
        self.batch_size = batchSize
        self.n_node = n_node
        self.n_timesteps = n_timesteps
        self.is_output = 1 if model == 2 else 0
        self.cnn0 = CNN(state_dim, batchSize, n_node, n_timesteps, model)
        self.cnn1 = CNN(state_dim, batchSize, n_node, n_timesteps, model)
        self.sigmoid = nn.Sigmoid()
        self.output = OutputLayer(state_dim, self.n_timesteps-1, n_node)
        self._initialization()

    def _initialization(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                m.weight.data.normal_(0.0, 0.02)
                m.bias.data.fill_(0)

    def forward(self, x, dummy0, dummy1):
        x0 = self.cnn0(x, dummy0, dummy1)
        x1 = self.cnn1(x, dummy0, dummy1)
        output = x0 * self.sigmoid(x1)
        if self.is_output:
            output = self.output(output)
        return output

class STGCBlock(nn.Module):
    def __init__(self, state_dim, annotation_dim, n_edge_types, n_timesteps, n_node, n_steps, batchSize, model):
        super(STGCBlock, self).__init__()
        assert state_dim >= annotation_dim,  'state_dim must be no less than annotation_dim'
        self.state_dim = state_dim
        self.annotation_dim = annotation_dim
        self.n_edge_types = n_edge_types
        self.n_timesteps = n_timesteps
        self.n_node = n_node
        self.n_steps = n_steps
        self.is_output = 1 if model == 3 else 0
        self.ggnn = GGNN(state_dim, annotation_dim, n_edge_types, n_timesteps-1, n_node, n_steps, model)
        self.gcnn0 = GatedCNN(state_dim, batchSize, n_node, n_timesteps, model)
        self.gcnn1 = GatedCNN(state_dim, batchSize, n_node, n_timesteps-1, model)
        self.output = OutputLayer(self.state_dim, self.n_timesteps-2, self.n_node)
        self._initialization()

    def _initialization(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                m.weight.data.normal_(0.0, 0.02)
                m.bias.data.fill_(0)

    def forward(self, prop_state, annotation, A):
        dummy = 0
        output = self.gcnn0(prop_state, dummy, dummy)
        output = self.ggnn(output, output, A)
        output = self.gcnn1(output, dummy, dummy)
        if self.is_output:
            output = self.output(output)
        return output
