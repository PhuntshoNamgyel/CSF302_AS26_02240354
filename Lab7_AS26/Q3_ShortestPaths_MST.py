
import heapq
import random
from time import perf_counter


# 1. Read a weighted directed graph from a file
def read_graph(filename):
    with open(filename, encoding="utf-8") as file:
        n, m = map(int, file.readline().split())
        graph = [[] for _ in range(n)]

        for _ in range(m):
            u, v, weight = map(int, file.readline().split())
            graph[u].append((v, weight))

    return graph


# Dijkstra's algorithm using a binary heap
def dijkstra(graph, source):
    n = len(graph)
    dist = [float("inf")] * n
    parent = [None] * n
    visited = [False] * n

    dist[source] = 0
    heap = [(0, source)]

    while heap:
        distance, u = heapq.heappop(heap)

        if visited[u]:
            continue

        visited[u] = True

        for v, weight in graph[u]:
            new_dist = distance + weight

            if not visited[v] and new_dist < dist[v]:
                dist[v] = new_dist
                parent[v] = u
                heapq.heappush(heap, (new_dist, v))

    return dist, parent


# Reconstruct the shortest path
def get_path(parent, vertex):
    path = []

    while vertex is not None:
        path.append(vertex)
        vertex = parent[vertex]

    return path[::-1]


# 2. Kruskal's algorithm using union-find
def kruskal(n, edges):
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    total = 0
    selected = 0

    for weight, u, v in sorted(edges):
        root_u, root_v = find(u), find(v)

        if root_u == root_v:
            continue

        if rank[root_u] < rank[root_v]:
            root_u, root_v = root_v, root_u

        parent[root_v] = root_u

        if rank[root_u] == rank[root_v]:
            rank[root_u] += 1

        total += weight
        selected += 1

        if selected == n - 1:
            break

    return total


# Prim's algorithm using a binary heap
def prim(n, edges):
    graph = [[] for _ in range(n)]

    for weight, u, v in edges:
        graph[u].append((weight, v))
        graph[v].append((weight, u))

    best = [float("inf")] * n
    visited = [False] * n
    best[0] = 0

    heap = [(0, 0)]
    total = 0

    while heap:
        weight, u = heapq.heappop(heap)

        if visited[u]:
            continue

        visited[u] = True
        total += weight

        for w, v in graph[u]:
            if not visited[v] and w < best[v]:
                best[v] = w
                heapq.heappush(heap, (w, v))

    return total


# Generate a random connected undirected graph
def random_connected_graph(n, m, rng):
    edges = []
    used = set()

    # Create a spanning tree to ensure connectivity
    for v in range(1, n):
        u = rng.randrange(v)
        edges.append((rng.randint(1, 1000), u, v))
        used.add((u, v))

    # Add random edges without duplicates
    while len(edges) < m:
        u, v = rng.randrange(n), rng.randrange(n)

        if u == v:
            continue

        a, b = sorted((u, v))

        if (a, b) not in used:
            used.add((a, b))
            edges.append((rng.randint(1, 1000), a, b))

    return edges


# 1. Print shortest distances and paths
graph = read_graph("graph.txt")
source = 0

distances, parents = dijkstra(graph, source)

print("Dijkstra's Shortest Paths")
print("Source:", source)

for vertex, distance in enumerate(distances):
    if distance == float("inf"):
        print(f"Vertex {vertex}: Unreachable")
    else:
        path = " -> ".join(map(str, get_path(parents, vertex)))
        print(f"Vertex {vertex}: Distance = {distance}, Path = {path}")


# 3. Verify Kruskal and Prim on random connected graphs
rng = random.Random(42)

print("\nRandom MST Verification")
print(f"{'V':>5} {'E':>6} {'Kruskal':>12} {'Prim':>12} {'Result':>10}")

for n in [10, 20, 50, 100, 200]:
    m = 3 * n
    edges = random_connected_graph(n, m, rng)

    k_weight = kruskal(n, edges)
    p_weight = prim(n, edges)

    result = "PASS" if k_weight == p_weight else "FAIL"

    print(f"{n:>5} {m:>6} {k_weight:>12} {p_weight:>12} {result:>10}")


# 4. Benchmark sparse and dense graphs
print("\nMST Performance Comparison (V = 1000)")
print(
    f"{'Graph':>8} {'Edges':>8} {'Kruskal (s)':>14} "
    f"{'Prim (s)':>12} {'Winner':>10}"
)

winners = {}

for label, m in [("Sparse", 3000), ("Dense", 250000)]:
    edges = random_connected_graph(1000, m, rng)

    start = perf_counter()
    k_weight = kruskal(1000, edges)
    k_time = perf_counter() - start

    start = perf_counter()
    p_weight = prim(1000, edges)
    p_time = perf_counter() - start

    assert k_weight == p_weight

    winner = "Kruskal" if k_time < p_time else "Prim"
    winners[label] = winner

    print(
        f"{label:>8} {m:>8} {k_time:>14.4f} "
        f"{p_time:>12.4f} {winner:>10}"
    )


# 5. Negative-edge counterexample for Dijkstra
negative_graph = [
    [(1, 2), (2, 5)],
    [],
    [(1, -4)]
]

negative_dist, _ = dijkstra(negative_graph, 0)

print("\nDijkstra Negative-Edge Counterexample")
print("Edges: 0 -> 1 (2), 0 -> 2 (5), 2 -> 1 (-4)")
print("Source: 0, Destination: 1")
print("Dijkstra Distance:", negative_dist[1])
print("Actual Shortest Distance: 1")
print("Actual Shortest Path: 0 -> 2 -> 1")
print("Dijkstra Correct:", negative_dist[1] == 1)


# Performance explanation based on actual results
print("\nPerformance Explanation:")
print(f"Sparse: {winners['Sparse']} was faster in this run.")
print(f"Dense: {winners['Dense']} was faster in this run.")
print("Kruskal sorts all edges and uses union-find.")
print("Prim uses a heap to grow the minimum spanning tree.")
print("Performance varies with graph density and execution overhead.")
