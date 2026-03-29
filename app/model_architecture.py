import torch as th
import torch.nn as nn
import torch.nn.functional as F
import dgl.function as fn

class SAGELayer(nn.Module):
    def __init__(self, ndim_in, edim, ndim_out, activation):
        super().__init__()
        self.W_msg = nn.Linear(ndim_in + edim, ndim_out)
        self.W_apply = nn.Linear(ndim_in + ndim_out, ndim_out)
        self.activation = activation

    def message_func(self, edges):
        return {'m': self.W_msg(th.cat([edges.src['h'], edges.data['h']], dim=2))}

    def forward(self, g, nfeats, efeats):
        with g.local_scope():
            g.ndata['h'] = nfeats
            g.edata['h'] = efeats
            g.update_all(self.message_func, fn.mean('m', 'h_neigh'))
            h = th.cat([g.ndata['h'], g.ndata['h_neigh']], dim=2)
            return self.activation(self.W_apply(h))

class SAGE(nn.Module):
    def __init__(self, ndim_in, ndim_out, edim, activation, dropout):
        super().__init__()
        self.layers = nn.ModuleList([
            SAGELayer(ndim_in, edim, 128, activation),
            SAGELayer(128, edim, ndim_out, activation)
        ])
        self.dropout = nn.Dropout(dropout)

    def forward(self, g, nfeats, efeats):
        for i, layer in enumerate(self.layers):
            if i > 0:
                nfeats = self.dropout(nfeats)
            nfeats = layer(g, nfeats, efeats)
        return nfeats.sum(1)

class MLPPredictor(nn.Module):
    def __init__(self, in_feats, num_classes):
        super().__init__()
        self.W = nn.Linear(in_feats * 2, num_classes)

    def apply_edges(self, edges):
        return {'score': self.W(th.cat([edges.src['h'], edges.dst['h']], dim=1))}

    def forward(self, g, h):
        with g.local_scope():
            g.ndata['h'] = h
            g.apply_edges(self.apply_edges)
            return g.edata['score']

class Model(nn.Module):
    def __init__(self, ndim_in, ndim_out, edim, activation, dropout, num_classes):
        super().__init__()
        self.gnn = SAGE(ndim_in, ndim_out, edim, activation, dropout)
        self.pred = MLPPredictor(ndim_out, num_classes)

    def forward(self, g, nfeats, efeats):
        h = self.gnn(g, nfeats, efeats)
        return self.pred(g, h)
