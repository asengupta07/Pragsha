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

# Example usage:
if __name__ == "__main__":
    # Create a list of vertices
    vertices = ["A", "B", "C", "D", "E"]

    # Create a graph and add edges with their weights
    graph = Graph(vertices)
    graph.add_edge("A", "B", 3)
    graph.add_edge("A", "C", 2)
    graph.add_edge("B", "D", 2)
    graph.add_edge("C", "B", 1)
    graph.add_edge("D", "C", 1)
    graph.add_edge("E", "A", 1)
    graph.add_edge("E", "D", 4)

    start_vertex = "E"

    try:
        shortest_distances = graph.bellman_ford(start_vertex)
        for vertex, distance in shortest_distances.items():
            print(f"Shortest distance from {start_vertex} to {vertex}: {distance}")
    except Exception as e:
        print(e)

