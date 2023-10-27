import random
import math

def euclidean_distance(point1, point2):
    return sum((a - b) ** 2 for a, b in zip(point1, point2)) ** 0.5

def calculate_radius(cluster, centroid):
    return max(euclidean_distance(point, centroid) for point in cluster)

def initialize_centroids(data, k):
    return random.sample(data, k)

def assign_clusters(data, centroids):
    clusters = [[] for _ in range(len(centroids))]
    for point in data:
        closest_centroid = min(centroids, key=lambda centroid: euclidean_distance(point, centroid))
        cluster_index = centroids.index(closest_centroid)
        clusters[cluster_index].append(point)
    return clusters

def update_centroids(clusters):
    new_centroids = []
    for cluster in clusters:
        if cluster:
            new_centroid = [sum(x) / len(cluster) for x in zip(*cluster)]
            new_centroids.append(new_centroid)
        else:
            new_centroids.append(cluster[0])
    return new_centroids

def kmeans(data, k, max_iterations=100):
    centroids = initialize_centroids(data, k)
    for _ in range(max_iterations):
        clusters = assign_clusters(data, centroids)
        new_centroids = update_centroids(clusters)
        if new_centroids == centroids:
            return clusters, centroids
        centroids = new_centroids
    return clusters, centroids

if __name__ == "__main__":
    data = [
        [45.24575, 23.22643],
        [46.12055, 24.32123],
        [44.56321, 23.54321],
        [47.65432, 22.98765],
        [46.98765, 23.09876],
        [45.12345, 22.87654],
        [47.87654, 24.23456],
        [44.65432, 23.98765],
        [45.98765, 24.87654],
        [46.56789, 22.98765]
    ]

    k = 3
    clusters, centroids = kmeans(data, k)

    for i, cluster in enumerate(clusters):
        print(f"Cluster {i + 1}: {cluster}")
        if cluster:
            centroid = centroids[i]
            radius = calculate_radius(cluster, centroid)
            print(f"Radius of Cluster {i + 1}: {radius:.5f}")
    
    print(f"Centroids: {centroids}")
