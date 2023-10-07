from collections import deque
import json


def bfs(
    start, stop, NODES_FILE="../input/nodes.json", EDGES_FILE="../input/edges.json"
):
    with open(NODES_FILE, "r") as f:
        nodes = json.load(f)["nodes"]

    new_nodes_data = {}
    for node in nodes:
        new_nodes_data[f"{node['id']}"] = {"x": node["x"], "y": node["y"]}

    with open(EDGES_FILE, "r") as f:
        edges = json.load(f)["edges"]

    graph = {node["id"]: [] for node in nodes}

    for edge in edges:
        graph[edge["u"]].append(edge["v"])
        if edge["oneway"] == False:
            graph[edge["v"]].append(edge["u"])

    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current_node, path = queue.popleft()

        if current_node == stop:
            break

        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    if stop not in visited:
        return None

    coords_list = []
    for node in path:
        coords = [new_nodes_data[f"{node}"]["y"], new_nodes_data[f"{node}"]["x"]]
        coords_list.append(coords)

    return {'coords': coords_list, 'path': path}

