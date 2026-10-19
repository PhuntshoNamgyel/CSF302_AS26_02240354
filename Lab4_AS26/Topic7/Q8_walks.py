from Q4_binary import matrix_pow_binary


def count_walks(adj, u, v, k, m):
    """Count walks with exactly k edges from vertex u to vertex v, mod m."""
    # Entry (i, j) of adj^k is the number of walks of length k from i to j.
    # A walk may repeat vertices and edges, which is why a matrix power works.
    powered = matrix_pow_binary(adj, k, m)
    return powered[u][v]


if __name__ == "__main__":
    # Directed graph with 4 vertices. adj[i][j] = 1 means an edge i -> j.
    #   0 -> 1, 0 -> 2, 1 -> 2, 2 -> 0, 2 -> 3, 3 -> 1
    adj = [
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 0, 0],
    ]
    MOD = 10**9 + 7

    print(count_walks(adj, 0, 3, 3, MOD))       # 1
    print(count_walks(adj, 0, 0, 5, MOD))       # 3
    print(count_walks(adj, 1, 3, 1, MOD))       # no direct edge, so 0
    print(count_walks(adj, 0, 3, 10**12, MOD))  # huge k is still fast