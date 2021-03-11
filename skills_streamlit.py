import streamlit as st
import networkx as nx
import pandas as pd
import random
from streamlit_agraph import agraph, Node, Edge, Config

st.set_page_config(layout="centered")

def generate_colors(n, random_seed=10):
    random.seed(random_seed)
    rgb_values = []
    hex_values = []
    r = int(random.random() * 256)
    g = int(random.random() * 256)
    b = int(random.random() * 256)
    step = 256 / n
    for _ in range(n):
        r += step
        g += step
        b += step
        r = int(r) % 256
        g = int(g) % 256
        b = int(b) % 256
        r_hex = hex(r)[2:]
        g_hex = hex(g)[2:]
        b_hex = hex(b)[2:]
        hex_values.append('#' + r_hex + g_hex + b_hex)
        rgb_values.append((r, g, b))

    return rgb_values, hex_values

st.title('Skills Taxonomy Network Tool')
st.markdown('## Investigate skills in different skill areas - Select area to explore:')

#graph data
skill_edges = pd.read_csv('df_edge.csv')
skill_nodes = pd.read_csv('df_node.csv')

#select from the different skills clusters 
option = st.selectbox(label = '', 
	options = list(skill_nodes['cluster_subgroup0_name'].unique()))

nodes = []
edges = []

#subsubgroup colors
subgraph = skill_nodes[skill_nodes['cluster_subgroup0_name'] == option]
subsubgroup	= subgraph['cluster_group'].unique().tolist()
subsubgroupname = subgraph['cluster_subgroup2_name'].unique().tolist()
subsubname_dict = dict(zip(subsubgroup, subsubgroupname))

subsub_colorlist = generate_colors(len(subsubgroup), random_seed = 42)[1]
subsub_dict = dict(zip(subsubgroup, subsub_colorlist))

subnode_names = list(subgraph['preferredLabel'])
subgraph_edges = skill_edges[skill_edges['target'].isin(subnode_names)]
subgraph_edges = subgraph_edges[subgraph_edges['source'].isin(subnode_names)]

length_of_nodes = str(len(subnode_names))
st.markdown('**Number of Skills in Cluster: **' + length_of_nodes)

for i, r in subgraph.iterrows():
	sub_color = subsub_dict[r['cluster_group']]
	nodes.append(Node(id = r['preferredLabel'], color = sub_color, size = 50))

for i, r in subgraph_edges.iterrows():
	edges.append(Edge(source = r['source'], target=r['target'], color = 'silver', weight=r['weight']))

config = Config(width = 800, height = 500, directed = False, nodeHighlightBehavior=True, highlightColor="#F7A7A6", collapsible=True) 

return_value = agraph(nodes = nodes, 
                      edges = edges, 
                      config = config)

st.subheader("Sub clusters:")

subcluster_list_sorted = sorted(list(set(subsubgroup)))
for sub_cluster in (list(set(subcluster_list_sorted))):
    sub_colour_select = subsub_dict[sub_cluster]
    sub_cluster_label = subsubname_dict[sub_cluster]
    st.markdown(f""" <font color={sub_colour_select} style='bold'> {sub_cluster} : {sub_cluster_label} </font>""", unsafe_allow_html = True)

