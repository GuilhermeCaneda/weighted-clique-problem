import random
import time
from deap import base, creator, tools, algorithms

import csv
import numpy as np

def read_csv(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    
    n = len(data) - 1  # Ignorando a linha de cabeçalho
    graph = np.zeros((n, n))
    
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            value = data[i][j]
            if value == 'NULL':
                graph[i-1][j-1] = 0
            else:
                graph[i-1][j-1] = float(value)
                #write_csv([i-1, j-1], graph[i-1][j-1]) #escreve no arquivo csv os vértices e o peso da aresta que foi lida do arquivo csv
    
    return graph

# Define the fitness function
def evaluate(individual, graph): #a função de fitness é a soma dos pesos das arestas do grafo que estão presentes no subgrafo induzido pelo indivíduo.
    subset = [index for index in range(len(individual)) if individual[index] == 1] #seleciona os vértices que estão presentes no subgrafo induzido pelo indivíduo
    
    if len(subset) < 2: #se o subgrafo induzido pelo indivíduo tiver menos de 2 vértices
        return 0, #retorna 0 como valor de fitness
    
    # Check if the subset is a clique
    for i in range(len(subset)): #para cada par de vértices do subgrafo induzido pelo indivíduo
        for j in range(i + 1, len(subset)): #para cada par de vértices do subgrafo induzido pelo indivíduo
            if graph[subset[i]][subset[j]] == 0: #se os vértices não forem adjacentes
                return 0, #retorna 0 como valor de fitness
    
    # Calculate the weight of the clique
    fitness = sum(graph[i][j] for i in subset for j in subset if i != j) / 2 #calcula a função de fitness do indivíduo    
    # write_csv(subset, fitness, len(subset))

    return fitness, #retorna o valor de fitness

def write_csv(subset, fitness, len_subset):
    with open('cliques.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([subset, fitness, len_subset])
        
def main(graph): #a função principal do algoritmo genético, que recebe um grafo e retorna o melhor indivíduo encontrado pelo algoritmo genético.
    n = len(graph) #o número de vértices do grafo
    
    # Remove a função de fitness e o tipo de indivíduo, se eles já existirem
    if hasattr(creator, 'FitnessMax'):
        del creator.FitnessMax
    if hasattr(creator, 'Individual'):
        del creator.Individual

    # Create types
    creator.create("FitnessMax", base.Fitness, weights=(1.0,)) # o 1.0 é o peso da função de fitness, pode ser alterado para testar diferentes valores e ver qual é o melhor para o problema em questão.
    creator.create("Individual", list, fitness=creator.FitnessMax) # o FitnessMax é o tipo de fitness que foi criado na linha anterior, Significa que o indivíduo é uma lista e tem um atributo fitness que é do tipo FitnessMax.
    
    # Create toolbox
    toolbox = base.Toolbox() # é uma caixa de ferramentas que contém todas as funções que serão usadas no algoritmo genético.
    
    # Attribute generator
    toolbox.register("attr_bool", random.randint, 0, 1) # é uma função que gera um número aleatório entre 0 e 1, para ser usado como atributo do indivíduo.
    
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n) # é uma função que cria um indivíduo, que é uma lista de tamanho n, onde cada elemento é gerado pela função attr_bool.
    toolbox.register("population", tools.initRepeat, list, toolbox.individual) # é uma função que cria uma população, que é uma lista de indivíduos, onde cada indivíduo é gerado pela função individual.
    
    # Operators
    toolbox.register("evaluate", evaluate, graph=graph) # tem por objetivo calcular a função de fitness de um indivíduo.
    toolbox.register("mate", tools.cxTwoPoint) # tem por objetivo cruzar dois indivíduos para tentar gerar um novo indivíduo que tenha características dos dois pais.
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05) # tem por objetivo alterar um indivíduo de forma aleatória, para tentar melhorar a solução.
    toolbox.register("select", tools.selTournament, tournsize=3) # tem por objetivo selecionar os indivíduos que vão sobreviver para a próxima geração.
    
    population = toolbox.population(n=300)
    NGEN = 40 #tem por objetivo definir o número de gerações que o algoritmo genético vai rodar, pode ser alterado para testar diferentes valores e ver qual é o melhor para o problema em questão.
    CXPB = 0.5 #isso é a probabilidade de crossover (é um hiperparâmetro), pode ser alterado para testar diferentes valores e ver qual é o melhor para o problema em questão.
    MUTPB = 0.2 #isso é a probabilidade de mutação (é um hiperparâmetro), pode ser alterado para testar diferentes valores e ver qual é o melhor para o problema em questão.
    
    # Algorithm
    for gen in range(NGEN): #para cada geração
        offspring = toolbox.select(population, len(population)) #seleciona os indivíduos que vão sobreviver para a próxima geração
        offspring = list(map(toolbox.clone, offspring)) #clona os indivíduos selecionados
        
        for child1, child2 in zip(offspring[::2], offspring[1::2]): #para cada par de indivíduos
            if random.random() < CXPB: #se a probabilidade de crossover for atendida
                toolbox.mate(child1, child2) #cruza os dois indivíduos
                del child1.fitness.values #deleta o valor da função de fitness dos dois indivíduos
                del child2.fitness.values #deleta o valor da função de fitness dos dois indivíduos
        
        for mutant in offspring: #para cada indivíduo
            if random.random() < MUTPB: #se a probabilidade de mutação for atendida
                toolbox.mutate(mutant) #muta o indivíduo
                del mutant.fitness.values #deleta o valor da função de fitness do indivíduo
        
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid] #seleciona os indivíduos que não tiveram a função de fitness calculada
        fitnesses = map(toolbox.evaluate, invalid_ind) #calcula a função de fitness dos indivíduos selecionados
        for ind, fit in zip(invalid_ind, fitnesses): #para cada indivíduo e seu valor de fitness
            ind.fitness.values = fit #atribui o valor de fitness ao indivíduo
        
        population[:] = offspring #atualiza a população com os indivíduos da próxima geração
    
    top_ind = tools.selBest(population, 1)[0] #seleciona o melhor indivíduo da população
    print("Best individual is %s, %s" % (top_ind, top_ind.fitness.values)) #imprime o melhor indivíduo e seu valor de fitness
    
    return top_ind #retorna o melhor indivíduo

def run_genetic_algorithm(file_name, num_runs):
    tempos = []
    graph = read_csv(file_name)

    for _ in range(num_runs):
        tempo_inicial = time.time()

        best_clique = main(graph)

        tempo_final = time.time()
        tempos.append(tempo_final - tempo_inicial)

        print(f"Maior clique encontrada: {best_clique}\n")
        print(f"Tempo de execução: {tempo_final - tempo_inicial:.3f} segundos")
    print(f"Tempo médio de execução: {np.mean(tempos):.3f} segundos\n")

    # Imprime os tempos de execução
    tempos_formatados = [f"{tempo:.3f}" for tempo in tempos]
    print("Tempos de execução totais:", tempos_formatados)

# Exemplo de uso:
run_genetic_algorithm('employees_interactions.csv', 1)


