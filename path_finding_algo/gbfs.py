import heapq
import json

def euclidean_distance(node1, node2):
    # Helper function to calculate Euclidean distance between two nodes
    x1, y1 = node1["x"], node1["y"]
    x2, y2 = node2["x"], node2["y"]
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def gbfs(
    start, stop, NODES_FILE="../input/nodes.json", EDGES_FILE="../input/edges.json"
):
    with open(NODES_FILE, "r") as f:
        nodes = json.load(f)["nodes"]

    with open(EDGES_FILE, "r") as f:
        edges = json.load(f)["edges"]
    print('*****************************************')
    new_nodes_data = {}
    for node in nodes:
        new_nodes_data[f"{node['id']}"] = {"x": node["x"], "y": node["y"]}
    graph = {node["id"]: {} for node in nodes}
    pre = {node["id"]: [] for node in nodes}
    for edge in edges:
        graph[edge["u"]][edge["v"]] = edge["length"]
        if edge["oneway"] == False:
            graph[edge["v"]][edge["u"]] = edge["length"]

    distances = {node: float("infinity") for node in graph}
    distances[start] = 0

    priority_queue = [(0 + euclidean_distance(new_nodes_data[f"{start}"], new_nodes_data[f"{stop}"]), 0, start)]

    while priority_queue:
        current_f, current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        if current_node == stop:
            # found a shortest path from start to stop
            print('')
            path = []
            current = stop
            while current != start:
                path.insert(0, current)
                current = pre[current]

            path.insert(0, start)

            coords_list = []
            for node in path:
                coords = [new_nodes_data[f"{node}"]["y"], new_nodes_data[f"{node}"]["x"]]
                coords_list.append(coords)

            return {'coords': coords_list, 'path': path}

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            heuristic = euclidean_distance(new_nodes_data[f"{neighbor}"], new_nodes_data[f"{stop}"])
            f_value = heuristic

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                pre[neighbor] = current_node
                heapq.heappush(priority_queue, (f_value, distance, neighbor))

    return None
