import csv
import numpy as np

# Função para ler um arquivo CSV e convertê-lo em uma matriz de adjacência
def read_csv(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    
    n = len(data) - 1
    graph = np.zeros((n, n))
    
    # Preenche a matriz de adjacência com os valores do CSV
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            value = data[i][j]
            if value == 'NULL':
                graph[i-1][j-1] = 0
            else:
                graph[i-1][j-1] = int(value)

   # Retorna a matriz de adjacência 
    return graph

# Função para encontrar o clique de peso máximo em um grafo
def max_weighted_clique(graph):
    n = len(graph)
    
    max_edges = -1
    start_node = None
    for i in range(n):
        positive_edges = sum(1 for j in range(n) if graph[i][j] > 0)
        if positive_edges > max_edges:
            max_edges = positive_edges
            start_node = i
    
    # Inicializa o clique com o nó de início
    clique = [start_node]
    candidates = {i for i in range(n) if i != start_node and graph[start_node][i] > 0}
    
    # Expande o clique adicionando nós que maximizam o ganho de peso
    while candidates:
        max_gain = -1
        best_candidate = None
        
        for candidate in candidates:
            gain = sum(graph[node][candidate] for node in clique)
            if gain > max_gain:
                max_gain = gain
                best_candidate = candidate
        
        if best_candidate is not None:
            clique.append(best_candidate)
            candidates.remove(best_candidate)
            candidates = {v for v in candidates if all(graph[v][u] > 0 for u in clique)}
        else:
            break
    
    # Retorna o clique de peso máximo
    return clique

# Leitura do arquivo CSV e construção do grafo
graph = read_csv('employees_interactions.csv')

# Encontra o clique de peso máximo no grafo
clique = max_weighted_clique(graph)

# Imprime a matriz de adjacência do grafo e o clique de peso máximo encontrado
print(graph)
print("")
print("Clique de peso máximo encontrado:", clique)