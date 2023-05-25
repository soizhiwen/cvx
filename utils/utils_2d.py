import networkx as nx
import plotly.graph_objects as go


def create_graph(positions, edges):
    G = nx.Graph()
    G.add_nodes_from(positions.keys())
    G.add_edges_from(edges)

    for n, p in positions.items():
        G.nodes[n]["pos"] = p
    return G


def load_graph(path):
    positions = dict()
    edges = []
    flag = None
    with open(path, "r") as f:
        idx = 0
        for line in f:
            line = line.strip()
            if line == "a" or line == "b":
                flag = line
                continue

            if flag == "a":
                positions[idx] = list(map(float, line.split()))
                idx += 1
            else:
                edges.append(list(map(int, line.split())))

    assert len(positions.keys()) == len(edges) + 1

    return create_graph(positions, edges)


def get_edge_trace(G, color="#888"):
    edge_x = []
    edge_y = []
    for u, v in G.edges():
        pos_u = G.nodes[u]["pos"]
        pos_v = G.nodes[v]["pos"]
        edge_x.extend([pos_u[0], pos_v[0], None])
        edge_y.extend([pos_u[1], pos_v[1], None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color=color),
        mode="lines",
        showlegend=False,
    )
    return edge_trace


def get_node_trace(G, color="#0000FF", size=20, name="Original", text=True):
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]["pos"]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        name=name,
        marker=dict(
            color=color,
            size=size,
            opacity=1.0 if text else 0.6,
        ),
        text=list(G.nodes()) if text else None,
        textfont=dict(size=8, color="#FFF"),
    )
    return node_trace


def plot_graph(g1, g2, alpha, save_name):
    e1 = get_edge_trace(g1)
    e2 = get_edge_trace(g2, color="#000")
    n1 = get_node_trace(g1)
    n2 = get_node_trace(g2, color="#FF0000", size=10, name="Optimized", text=False)

    fig = go.Figure(
        data=[e1, n1, e2, n2],
        layout=go.Layout(
            title=f"Original and Optimized Graphs, alpha={alpha}",
        ),
    )
    fig.write_html(save_name)
    fig.show()
