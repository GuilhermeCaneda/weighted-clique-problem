import pulp
from itertools import combinations
import csv
import json

def extractEdges(headers, reader):
    edges = {}
    for i, row in enumerate(reader):
            node1 = headers[i + 1]
            for j, weight in enumerate(row[1:]):
                node2 = headers[j + 1]
                if weight != 'NULL' and weight != '0':  
                    # tupla ordenada para garantir que aresta não direcional seja única
                    edge = tuple(sorted((node1, node2)))
                    weight_float = float(weight.replace(',', '.'))
                    edges[edge] = weight_float 
    return edges

def extractVertices(headers):
    return headers[1:]

def read_csv(filename):
    vertices = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        vertices = extractVertices(headers)
        edges = extractEdges(headers, reader)

    print("Vertex:")
    print(vertices)
    print("Edges")
    for edge, weight in edges.items():
        print(f"    {edge}: {weight},")
        
    return vertices, edges

def write_json(filename, status, objective_value, clique_vertices, clique_edges):
    data = {
        "status": status,
        "objective_value": objective_value,
        "clique_vertices": clique_vertices,
        "clique_edges": clique_edges
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def linear_solution(vertices, edges):
    prob = pulp.LpProblem("Weighted_Clique_Problem_Linear", pulp.LpMaximize)
    # Definindo as variáveis de decisão para os vértices e arestas
    x = pulp.LpVariable.dicts("x", vertices, lowBound=0, upBound=1, cat='Continuous')
    y = pulp.LpVariable.dicts("y", edges, lowBound=0, upBound=1, cat='Continuous')
    # Definindo a função objetivo
    prob += pulp.lpSum(edges[(i, j)] * y[(i, j)] for (i, j) in edges)
    # Adicionando as restrições para garantir que as arestas só são incluídas se ambos os vértices estiverem no clique
    for (i, j) in edges:
        prob += y[(i, j)] <= x[i]
        prob += y[(i, j)] <= x[j]
        prob += y[(i, j)] >= x[i] + x[j] - 1
    # Adicionando restrições de clique (não adicione vértices desconectados)
    for (i, j) in combinations(vertices, 2):
        if (i, j) not in edges and (j, i) not in edges:
            prob += x[i] + x[j] <= 1
    prob.solve()
    if pulp.LpStatus[prob.status] == "Optimal":
        print("Linear Problem:")
        print("Status:", pulp.LpStatus[prob.status])
        print("Objective Value:", pulp.value(prob.objective))
        print("Clique Vertices:", [v for v in vertices if pulp.value(x[v]) == 1])
        print("Clique Edges:", [(i, j) for (i, j) in edges if pulp.value(y[(i, j)]) == 1])
        for v in vertices:
            print(f"x[{v}] = {x[v].varValue}")

        for a in edges:
            print(f"y[{a}] = {y[a].varValue}")

        status = pulp.LpStatus[prob.status]
        objective_value = pulp.value(prob.objective)
        clique_vertices = [v for v in vertices if pulp.value(x[v]) > 0]
        clique_edges = [(i, j) for (i, j) in edges if pulp.value(y[(i, j)]) > 0]
        return status, objective_value, clique_vertices, clique_edges

def integer_solution(vertices, edges):
    prob_int = pulp.LpProblem("Weighted_Clique_Problem_Integer", pulp.LpMaximize)
    # Redefinindo as variáveis de decisão para os vértices e arestas como inteiras
    x_int = pulp.LpVariable.dicts("x", vertices, lowBound=0, upBound=1, cat='Integer')
    y_int = pulp.LpVariable.dicts("y", edges, lowBound=0, upBound=1, cat='Integer')
    # Definindo a função objetivo
    prob_int += pulp.lpSum(edges[(i, j)] * y_int[(i, j)] for (i, j) in edges)
    # Adicionando as restrições para garantir que as arestas só são incluídas se ambos os vértices estiverem no clique
    for (i, j) in edges:
        prob_int += y_int[(i, j)] <= x_int[i]
        prob_int += y_int[(i, j)] <= x_int[j]
        prob_int += y_int[(i, j)] >= x_int[i] + x_int[j] - 1
    # Adicionando restrições de clique (não adicione vértices desconectados)
    for (i, j) in combinations(vertices, 2):
        if (i, j) not in edges and (j, i) not in edges:
            prob_int += x_int[i] + x_int[j] <= 1
    prob_int.solve()
    if pulp.LpStatus[prob_int.status] == "Optimal":
        print("Integer Problem:")
        print("Status:", pulp.LpStatus[prob_int.status])
        print("Objective Value:", pulp.value(prob_int.objective))
        print("Clique Vertices:", [v for v in vertices if pulp.value(x_int[v]) == 1])
        print("Clique Edges:", [(i, j) for (i, j) in edges if pulp.value(y_int[(i, j)]) == 1])

        for v in vertices:
            print(f"x[{v}] = {x_int[v].varValue}")

        for a in edges:
            print(f"y[{a}] = {y_int[a].varValue}")

        status = pulp.LpStatus[prob_int.status]
        objective_value = pulp.value(prob_int.objective)
        clique_vertices = [v for v in vertices if pulp.value(x_int[v]) == 1]
        clique_edges = [(i, j) for (i, j) in edges if pulp.value(y_int[(i, j)]) == 1]
        return status, objective_value, clique_vertices, clique_edges

def main(filename):
    vertices, edges = read_csv(filename) 

    status, objective_value, clique_vertices, clique_edges = linear_solution(vertices, edges)
    write_json("Clique_PL.json", status, objective_value, clique_vertices, clique_edges)

    status_int, objective_value_int, clique_vertices_int, clique_edges_int = integer_solution(vertices, edges)
    write_json("Clique_PI.json", status_int, objective_value_int, clique_vertices_int, clique_edges_int)

main('employees_interactions.csv')