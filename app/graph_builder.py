import dgl
import torch
import networkx as nx

def build_graph(df, h, device):

    G = nx.from_pandas_edgelist(
        df, "src_ip", "dst_ip", create_using=nx.MultiDiGraph()
    )

    G = dgl.from_networkx(G)

    # 🔥 FIX: move graph to device
    G = G.to(device)

    G.ndata["h"] = torch.ones(G.num_nodes(), 1, len(h[0]), device=device)
    G.edata["h"] = torch.tensor(h, dtype=torch.float32, device=device).unsqueeze(1)

    return G