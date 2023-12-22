import json

def ids(start, stop, NODES_FILE="../input/nodes.json", EDGES_FILE="../input/edges.json"):
    with open(NODES_FILE, "r") as f:
        nodes = json.load(f)["nodes"]

    with open(EDGES_FILE, "r") as f:
        edges = json.load(f)["edges"]

    new_nodes_data = {}
    for node in nodes:
        new_nodes_data[f"{node['id']}"] = {"x": node["x"], "y": node["y"]}

    graph = {node["id"]: {} for node in nodes}
    for edge in edges:
        graph[edge["u"]][edge["v"]] = edge["length"]
        if edge["oneway"] == False:
            graph[edge["v"]][edge["u"]] = edge["length"]

    def dfs(node, depth, visited):
        if depth == 0 and node == stop:
            return [node]
        
        if depth > 0 and node not in visited:
            visited.add(node)
            for neighbor, _ in graph[node].items():
                path = dfs(neighbor, depth - 1, visited.copy())
                if path:
                    return [node] + path

        return None

    max_depth = 0
    while True:
        path = dfs(start, max_depth, set())
        if path:
            coords_list = [[new_nodes_data[f"{node}"]["y"], new_nodes_data[f"{node}"]["x"]] for node in path]
            return {'coords': coords_list, 'path': path}
        max_depth += 1

        if max_depth > len(nodes):  # Stop if the depth limit exceeds the number of nodes
            break

    return None
