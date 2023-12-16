import json
import math

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from path_finding_algo.a_star import a_star
from path_finding_algo.bfs import bfs
from path_finding_algo.dfs import dfs_wrapper
from path_finding_algo.dijkstra import dijkstra

app = FastAPI()

origins = [
    "https://vite-path-finding.vercel.app",
    "http://localhost:5174",
]

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods like ["GET", "POST"]
    allow_headers=["*"],  # You can specify specific HTTP headers like ["Authorization"]
)

with open("./input/nodes.json", "r") as f:
    nodes = json.load(f)["nodes"]

with open("./input/edges.json", "r") as f:
    edges = json.load(f)["edges"]

new_nodes_data = {}
for node in nodes:
    new_nodes_data[f"{node['id']}"] = {"x": node["x"], "y": node["y"]}


@app.get("/")
def index():
    return {"hello": "world"}


@app.post("/find_path/")
async def receive_post(request_body: dict):
    start = find_id_of_node(request_body["start"]["lat"], request_body["start"]["lng"])
    stop = find_id_of_node(request_body["stop"]["lat"], request_body["stop"]["lng"])
    algorithm = request_body["algorithm"]

    result = {}
    if algorithm == "bfs":
        result = bfs(
            start=start,
            stop=stop,
            NODES_FILE="./input/nodes.json",
            EDGES_FILE="./input/edges.json",
        )
    elif algorithm == "dfs":
        result = dfs_wrapper(
            start=start,
            stop=stop,
            NODES_FILE="./input/nodes.json",
            EDGES_FILE="./input/edges.json",
        )
    elif algorithm == "dijkstra":
        result = dijkstra(
            start=start,
            stop=stop,
            NODES_FILE="./input/nodes.json",
            EDGES_FILE="./input/edges.json",
        )
    elif algorithm == "a*":
        result = a_star(
            start=start,
            stop=stop,
            NODES_FILE="./input/nodes.json",
            EDGES_FILE="./input/edges.json",
        )
    elif algorithm == "bellman-ford":
        pass

    return {"path": result['coords'], 'length': get_path_length(result['path'])}


@app.post("/find_nearest_node")
async def receive_post(request_body: dict):
    lat = request_body["lat"]
    lng = request_body["lng"]

    min_distance = 1000000000
    nearest_node = None

    for edge in edges:
        node = new_nodes_data[f"{edge['u']}"]
        distance = math.sqrt((node["x"] - lng) ** 2 + (node["y"] - lat) ** 2)
        if distance < min_distance:
            nearest_node = node
            min_distance = distance

        node = new_nodes_data[f"{edge['v']}"]
        distance = math.sqrt((node["x"] - lng) ** 2 + (node["y"] - lat) ** 2)
        if distance < min_distance:
            nearest_node = node
            min_distance = distance

    if nearest_node is None:
        return None
    return {"lat": nearest_node["y"], "lng": nearest_node["x"]}


def find_id_of_node(lat, lng):
    for edge in edges:
        node = new_nodes_data[f"{edge['u']}"]
        if node["x"] == lng and node["y"] == lat:
            return edge["u"]

        node = new_nodes_data[f"{edge['v']}"]
        if node["x"] == lng and node["y"] == lat:
            return edge["v"]
    return -1


def get_path_length(path):
    graph = {node["id"]: {} for node in nodes}
    for edge in edges:
        graph[edge["u"]][edge["v"]] = edge["length"]
        if not edge["oneway"]:
            graph[edge["v"]][edge["u"]] = edge["length"]

    total_length = 0
    for i, node in enumerate(path):
        if i + 1 == len(path):
            break
        total_length += graph[node][path[i + 1]]

    return total_length
