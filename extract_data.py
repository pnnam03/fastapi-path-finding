import osmnx as ox
import json

osm_file_path = "./data/hangbai.osm"
G = ox.graph_from_xml(osm_file_path)
nodes, edges = ox.graph_to_gdfs(G)

def print_nodes_to_file(file_name) :
    nodes_data = []

    for id, node in nodes.iterrows():
        nodes_data.append({
            'id': id,
            'x': node['x'],
            'y': node['y']
        })

    print('Nodes: ',len(nodes))
    with open(file_name, 'w') as f:
        json.dump({"nodes": nodes_data}, f)

def print_edges_to_file(file_name):
    edges_data = []
    for u,v,data in G.edges(data=True):
        if 'highway' in data and data['highway'] == 'footway':
            continue
        
        to_append = {
            'u': u,
            'v': v,
            'oneway': data['oneway'],
            'length': data['length'],
        }
        edges_data.append(to_append)

    print('Edges: ',len(edges_data))
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump({"edges": edges_data}, f)
        
print_nodes_to_file('./input/nodes.json')
print_edges_to_file('./input/edges.json')

# print(edges['highway'].to_list())