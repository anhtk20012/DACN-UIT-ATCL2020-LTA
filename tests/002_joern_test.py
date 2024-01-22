from importlib import reload
from graphviz import Digraph
import random

import sastvd as svd
import sastvd.helpers.joern as svdj
import os
test_func = """\
short add (short b) {
    short a = 32767;
    if (b > 0) {
        a = a + b;
    }
    return a;
}
"""


def test_joern_graph():
    """Test 1."""
    reload(svdj)
    svdj.full_run_joern_from_string(test_func, "test", "test")
    filepath = svd.interim_dir() / "test" / "test.c"
    nodes, edges = svdj.get_node_edges(filepath)
    assert len(nodes) == 53
    assert len(edges) == 116


# Bigvul suspicious Joern IDs
# 178958, 179986, 180111, 180254, 180256
# 183008, 186024, 186854, 185466, 186856
# 179552, 185465, 117854, 182671, 183185
# 179986, 179989, 180109, 180110, 180187
# 180244, 180249, 180249, 180252, 180253

# print(before_func)
# df = svdd.bigvul()
# before_func = df.iloc[1].before
# after_func = df.iloc[3].after
# test_joern_graph()
# path = svd.interim_dir() / f"{items[iid]['dataset']}/{items[iid]['id']}.c"
# path = svd.interim_dir() / f"test/test.c"
path = svd.processed_dir() / "bigvul/after/24370.c"
# print(svdj.get_node_edges(path)[0])

def nodelabel2line(label: str):
    """Given a node label, return the line number.

    Example:
    s = "METHOD_1.0: static long main()..."
    nodelabel2line(s)
    >>> '1.0'
    """
    try:
        return str(int(label))
    except:
        return label.split(":")[0].split("_")[-1]


def randcolor():
    """Generate random color."""

    def r():
        return random.randint(0, 255)

    return "#%02X%02X%02X" % (r(), r(), r())

def get_digraph(nodes, edges, edge_label=True):
    """Plote digraph given nodes and edges list."""
    dot = Digraph(comment="Combined PDG")

    nodes = [n + [nodelabel2line(n[1])] for n in nodes]
    colormap = {"": "white"}
    for n in nodes:
        if n[2] not in colormap:
            colormap[n[2]] = randcolor()

    for n in nodes:
        style = {"style": "filled", "fillcolor": colormap[n[2]]}
        dot.node(str(n[0]), str(n[1]), **style)
    for e in edges:
        style = {"color": "black"}
        if e[2] == "CALL":
            style["style"] = "solid"
            style["color"] = "purple"
        elif e[2] == "AST":
            style["style"] = "solid"
            style["color"] = "black"
        elif e[2] == "CFG":
            style["style"] = "solid"
            style["color"] = "red"
        elif e[2] == "CDG":
            style["style"] = "solid"
            style["color"] = "blue"
        elif e[2] == "REACHING_DEF":
            style["style"] = "solid"
            style["color"] = "orange"
        elif "DDG" in e[2]:
            style["style"] = "dashed"
            style["color"] = "darkgreen"
        else:
            style["style"] = "solid"
            style["color"] = "black"
        style["penwidth"] = "1"
        if edge_label:
            dot.edge(str(e[0]), str(e[1]), e[2], **style)
        else:
            dot.edge(str(e[0]), str(e[1]), **style)
    return dot

def plot_node_edges(filepath: str, lineNumber: int = -1):
    nodes, edges = svdj.get_node_edges(filepath)
    if lineNumber > 0:
        nodesforline = set(nodes[nodes.lineNumber == lineNumber].id.tolist())
    else:
        nodesforline = set(nodes.id.tolist())

    # edges_new = edges[
    #     (edges.outnode.isin(nodesforline)) | (edges.innode.isin(nodesforline))
    # ]
    # accepted_etypes = ["DDG"] #, "CDG", "CFG", "AST"]
    # accepted_etypes = ["CDG", "CFG"]
    #         (edges['etype'].isin(accepted_etypes)) & 
        
    edges_new = edges[
        ((edges['outnode'].isin(nodesforline)) | (edges['innode'].isin(nodesforline)))
    ]
    nodes_new = nodes[
        nodes.id.isin(set(edges_new.outnode.tolist() + edges_new.innode.tolist()))
    ]
    dot = get_digraph(
        nodes_new[["id", "node_label"]].to_numpy().tolist(),
        edges_new[["outnode", "innode", "etype"]].to_numpy().tolist(),
    )
    dot.render("/home/ubuntu/linevd/tests/tmp.gv", format='png')
    
# plot_node_edges(path)
if os.path.exists(path):
    plot_node_edges(path)