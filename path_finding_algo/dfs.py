import json

def dfs(current_node, graph, visited, pre):
    visited[current_node] = True
        
    for neighbor in graph[current_node]:
        if not visited[neighbor]:
            pre[neighbor] = current_node
            dfs(neighbor, graph, visited, pre)
    pass

def dfs_wrapper(start, stop, NODES_FILE = '../input/nodes.json',
EDGES_FILE = '../input/edges.json'):
    
    with open(NODES_FILE,'r') as f:
        nodes = json.load(f)['nodes']
    
    new_nodes_data = {}
    for node in nodes:
        new_nodes_data[f"{node['id']}"] = {
            'x': node['x'],
            'y': node['y']
        }

    with open(EDGES_FILE, 'r') as f:
        edges = json.load(f)['edges']
    
    graph = {node['id']: [] for node in nodes}
    visited = {node['id']: False for node in nodes}
    pre = {node['id']: [] for node in nodes}

    for edge in edges:
        graph[edge['u']].append(edge['v'])
        if edge['oneway'] == False:
            graph[edge['v']].append(edge['u'])

    dfs(start, graph, visited, pre)

    if stop not in visited:
        return None
    
    path = []
    current = stop
    while current != start:
        path.insert(0, current)
        current = pre[current]

    path.insert(0, start)

    coords_list = []
    for node in path:
        coords = [new_nodes_data[f'{node}']['y'], new_nodes_data[f'{node}']['x']]
        coords_list.append(coords)
    
    return {'coords': coords_list, 'path': path}
