import json
import heapq

class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.pos = (x, y)

# dùng để tính khoảng cách giữa 2 node bất kì
def cost(node1, node2):
    x1, y1 = node1.pos
    x2, y2 = node2.pos
    return abs(x1 - x2) + abs(y1 - y2) 

def a_star(start_id, goal_id, NODES_FILE, EDGES_FILE):
    with open(NODES_FILE) as f:
        nodes = json.load(f)['nodes']
        # tạo dictionary để lưu node
        node_dict = {node['id']: Node(node['id'], node['x'], node['y']) for node in nodes}

    with open(EDGES_FILE) as f:
        edges = json.load(f)['edges']
        graph = {}
        for edge in edges:
            u = node_dict[edge['u']]
            v = node_dict[edge['v']]
            if u not in graph:
                graph[u] = {}
            graph[u][v] = edge['length']

    start = node_dict[start_id]
    goal = node_dict[goal_id]

    # heap hiệu năng với priority queue tốt hơn list, có pop, push
    open_list = []
    # open_list gồm f_score nếu đi qua nút đó và nút đó
    heapq.heappush(open_list, (0, start))
    # lưu lại những nút đã chọn
    before = {}
    # g_score dùng để lưu chi phí từ nút start đến nút đang xét
    g_score = {start: 0}
    # f_score dùng để ước lượng chi phí tổng cộng của đường đi nếu đi qua nút đó
    f_score = {start: cost(start, goal)}

    # ý tưởng của A* same same Dijikstra, với nút kề với nút đang xét và không thuộc before thì chọn nút có g_score + f_score min, sau đó update các nút khác
    while open_list:
        # heap tự động sắp xếp theo thứ tự tăng dần theo f_score nên auto pop thằng thứ nhất để có được khoảng cách min
        current = heapq.heappop(open_list)[1]

        if current == goal:
            data = []
            while current in before:
                data.append(current)
                current = before[current]
            data.reverse()
            return data
        
        # cái này same same Dijikstra
        for neighbour in graph[current]:
            current_g_score = g_score[current] + graph[current][neighbour]
            if neighbour not in g_score or current_g_score < g_score[neighbour]:
                before[neighbour] = current
                g_score[neighbour] = current_g_score
                f_score[neighbour] = current_g_score + cost(neighbour, goal)
                heapq.heappush(open_list, (f_score[neighbour], neighbour))
    
    return None

if __name__ == '__main__':
    path = a_star(8189781671,11112265409, '../input/nodes.json', '../input/edges.json')
    print(path)
