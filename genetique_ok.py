import random
import numpy as np
import time
import sys

def initialize_population(N, T):
    return [generate_individual(N) for _ in range(T)]

def generate_individual(N):
    return np.random.randint(2, size=N)

def evaluate_solution(solution, friendships, interests):
    active_persons = set(np.nonzero(solution)[0])
    active_friendships = [(i, j) for i, j in friendships if i in active_persons and j in active_persons]
    
    score = np.sum(solution * interests) - len(active_friendships)
    
    return score


def selection_reproduction(P, T_prime):
    return random.sample(P, T_prime)

def crossover(M, pc):
    C = []
    for parent1, parent2 in zip(M[::2], M[1::2]):
        if random.uniform(0, 1) < pc:
            crossover_point = random.randint(1, len(parent1) - 1)
            child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
            child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))
            C.extend([child1, child2])
    return C

def mutation(C, pm):
    for i in range(len(C)):
        if random.uniform(0, 1) < pm:
            mutation_point = random.randint(0, len(C[i]) - 1)
            C[i][mutation_point] = 1 - C[i][mutation_point]
    return C

def reparation(C, friendships):
    for solution in C:
        inactive_persons = set(np.nonzero(solution == 0)[0])
        inactive_friendships = [(i, j) for i, j in friendships if i in inactive_persons and j in inactive_persons]
        
        if inactive_friendships:
            i, j = random.choice(inactive_friendships)
            person_to_invite = np.random.choice([i, j])
            solution[person_to_invite] = 1
    
    return C


def selection_survival(P, T, friendships, interests):
    evals = [(evaluate_solution(S, friendships, interests), S) for S in P]
    evals.sort(reverse=True, key=lambda x: x[0])
    return [S for _, S in evals[:T]]

def genetique_opti(time_limit, N, friendships, interests):
    T = 400  # Population size
    T_prime = 100  # Selection size
    pc = 0.8  # Crossover probability
    pm = 2 / N  # Mutation probability

    P = initialize_population(N, T)

    best_solution = None
    best_fitness = float('-inf')
    iterations = 0

    start_time = time.time()

    while not stop_condition(start_time, time_limit):
        M = selection_reproduction(P, T_prime)
        C = crossover(M, pc)
        C = mutation(C, pm)
        C = reparation(C, friendships)
        P = P + C

        P = selection_survival(P, T, friendships, interests)
        current_best_solution = max(P, key=lambda x: evaluate_solution(x, friendships, interests))
        current_best_fitness = evaluate_solution(current_best_solution, friendships, interests)

        if current_best_fitness > best_fitness:
            best_solution = current_best_solution
            best_fitness = current_best_fitness

        iterations += 1

    return best_solution, best_fitness, iterations

def stop_condition(start_time, time_limit):
    elapsed_time = time.time() - start_time
    return elapsed_time >= float(time_limit)


def main():
    # ouverture du fichier instance
    instance = open(input_file, 'r')
    # Lecture des deux premières lignes
    N, M = map(int, instance.readline().split())

    # Lecture des interests
    interests = np.array([int(instance.readline().split()[1]) for _ in range(N)])

    # Lecture des connaissances des convives
    friendships = [tuple(map(int, instance.readline().split())) for _ in range(M)]

    # Exécution de l'algorithme
    best_solution, best_fitness, iterations = genetique_opti(time_limit, N, friendships, interests)

    # Écriture des résultats dans le fichier de sortie
    with open(output_file_path, 'w') as output_file:
        output_file.write("Convives invités: {}\n".format([i for i, inv in enumerate(best_solution) if inv > 0.5]))
        output_file.write("Score optimal de la soirée: {}\n".format(-best_fitness))
        output_file.write("Nombre d'itérations: {}\n".format(iterations))


if __name__ == "__main__":
    # Vérifier si les arguments nécessaires sont fournis
    if len(sys.argv) != 4:
        print("Utilisation: python main.py temps input_file.txt output_file.txt")
        sys.exit(1)

    # Récupérer les noms de fichiers à partir des arguments de la ligne de commande
    time_limit = sys.argv[1]
    input_file = sys.argv[2]
    output_file_path = sys.argv[3]
    main()

