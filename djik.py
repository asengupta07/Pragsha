class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = []

    def add_edge(self, u, v, w):
        self.edges.append([u, v, w])

    def bellman_ford(self, start):
        # Initialize distances
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[start] = 0

        # Relax edges repeatedly
        for _ in range(len(self.vertices) - 1):
            for u, v, w in self.edges:
                if distances[u] != float('inf') and distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w

        # Check for negative weight cycles
        for u, v, w in self.edges:
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                raise Exception("Graph contains a negative weight cycle")

        return distances

    import math

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        return distance

import networkx as nx
G = nx.Graph()
G.add_node("Node1", lat=latitude1, lon=longitude1)
G.add_node("Node2", lat=latitude2, lon=longitude2)
distance = haversine(latitude1, longitude1, latitude2, longitude2)
if distance < threshold_distance:
    G.add_edge("Node1", "Node2", weight=distance)

    try:
        shortest_distances = graph.bellman_ford(start_vertex)
        for vertex, distance in shortest_distances.items():
            print(f"Shortest distance from {start_vertex} to {vertex}: {distance}")
    except Exception as e:
        print(e)

