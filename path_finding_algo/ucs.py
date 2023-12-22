import heapq
import json


def ucs(
    start, stop, NODES_FILE="../input/nodes.json", EDGES_FILE="../input/edges.json"
):
    with open(NODES_FILE, "r") as f:
        nodes = json.load(f)["nodes"]

    with open(EDGES_FILE, "r") as f:
        edges = json.load(f)["edges"]

    new_nodes_data = {}
    for node in nodes:
        new_nodes_data[f"{node['id']}"] = {"x": node["x"], "y": node["y"]}

    graph = {node["id"]: {} for node in nodes}
    pre = {node["id"]: [] for node in nodes}
    for edge in edges:
        graph[edge["u"]][edge["v"]] = edge["length"]
        if edge["oneway"] == False:
            graph[edge["v"]][edge["u"]] = edge["length"]

    # Initialize distances with infinity
    distances = {node: float("infinity") for node in graph}
    distances[start] = 0

    # Use a priority queue to store nodes with their respective costs
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == stop:
            # found a path to the stop node
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

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                pre[neighbor] = current_node
                # Use cumulative cost as priority
                heapq.heappush(priority_queue, (distance, neighbor))

    return None
