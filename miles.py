import csv
import sys

def initialise_graph():
    graph = Graph()
    with open("connections.RGD") as f:
        for i in range(5):
            next(f)
        reader = csv.reader(f, delimiter=',')
        for station in reader:
            try:
                graph.add_edge(station[0], station[1], float(station[2]))
            except IndexError:
                break
    return graph

def algorithm(graph, start):
    unvisited = list(graph.get_vertices())
    shortest_path = {}
    previous_nodes = {}
    max_value = float('inf')
    for node in unvisited:
        shortest_path[node] = max_value
        shortest_path[start] = 0
    while unvisited:
        current_min = None
        for node in unvisited:
            if current_min == None:
                current_min = graph.get_vertex(node)
            elif shortest_path[node] < shortest_path[current_min.get_id()]:
                current_min = graph.get_vertex(node)
        
        neighbours = current_min.get_connections()
        for neighbour in neighbours:
            tentative = shortest_path[current_min.get_id()] + current_min.get_weight(neighbour)
            if tentative < shortest_path[neighbour.get_id()]:
                shortest_path[neighbour.get_id()] = tentative
                previous_nodes[neighbour.get_id()] = current_min.get_id()
        unvisited.remove(current_min.get_id())
    
    return previous_nodes, shortest_path

def print_result(graph, previous_nodes, shortest_path, start, target):
    path = []
    node = target

    while node != start:
        path.append(node)
        node = previous_nodes[node]

    path.append(start)

    print("The best path is as follows with a value of {} miles:".format(round(shortest_path[target], 2)))
    print(" -> ".join(reversed(path)))

def calculate():
    start = input("Enter starting station: ")
    target = input("Enter destination station: ")
    graph = initialise_graph()
    previous_nodes, shortest_path = algorithm(graph, start)
    print_result(graph, previous_nodes, shortest_path, start=start, target=target)

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbour(self, neighbour, weight=0):
        self.adjacent[neighbour] = weight

    def get_connections(self):
        return self.adjacent.keys() 

    def get_id(self):
        return self.id

    def get_weight(self, neighbour):
        return self.adjacent[neighbour]

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbour(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbour(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()