import osmnx as ox
from matplotlib import pyplot as plt
import json
# Load the .osm file
osm_file_path = "./data/hangbai.osm"
G = ox.graph_from_xml(osm_file_path)
nodes, edges = ox.graph_to_gdfs(G)



bidirectional_edges = [(u, v) for u, v, k, data in G.edges(keys=True, data=True) if data.get('oneway') == False]
edge_colors = ['yellow' if edge in bidirectional_edges else 'white' for edge in G.edges()]

ox.plot_graph_route(G, route = [8178544971, 8173724278],)
plt.plot()
