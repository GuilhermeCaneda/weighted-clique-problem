def max_weighted_clique(graph):
    # graph is represented as an adjacency matrix where graph[i][j] is the weight of the edge between i and j
    n = len(graph)
    
    # Step 1: Find the node with the most positive edges
    max_edges = -1
    start_node = None
    for i in range(n):
        positive_edges = sum(1 for j in range(n) if graph[i][j] > 0)
        if positive_edges > max_edges:
            max_edges = positive_edges
            start_node = i
    
    # Initialize the clique with the start node
    clique = [start_node]
    candidates = {i for i in range(n) if i != start_node and graph[start_node][i] > 0}
    
    # Step 2: Build the clique by adding the best candidate iteratively
    while candidates:
        # Calculate the gain of adding each candidate to the clique
        max_gain = -1
        best_candidate = None
        
        for candidate in candidates:
            gain = sum(graph[node][candidate] for node in clique)
            if gain > max_gain:
                max_gain = gain
                best_candidate = candidate
        
        if best_candidate is not None:
            # Add the best candidate to the clique
            clique.append(best_candidate)
            # Update the candidates
            candidates.remove(best_candidate)
            # Only keep candidates that are adjacent to all nodes in the clique
            candidates = {v for v in candidates if all(graph[v][u] > 0 for u in clique)}
        else:
            break
    
    return clique

# Example usage:
# Graph represented as an adjacency matrix
graph = [
    [0, 2, 3, 2, 0],
    [2, 0, 4, -1, 0],
    [3, 4, 0, 5, 0],
    [2, -1, 5, 0, 2],
    [0, 0, 0, 2, 0]
]

clique = max_weighted_clique(graph)
print("Clique de peso máximo encontrado:", clique)