import numpy as np
import sys, time

def fitness_function(x, interests):
    # On minimise le négatif de la somme des intérêts
    return -np.sum(interests[x>0.5])  

def logistic_function(x):
    # fonction logistique
    return 1 / (1 + np.exp(-x))

def chaotic_system(x, friendships, interests):
    # Système dynamique chaotique
    N = len(x)
    result = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i != j and i in friendships[j] and j in friendships[i]:
                result[i] += logistic_function(interests[i])

    return result


def chaotic_optimization(time_limit, population_size, friendships, interests):
    # Fonction d'optimisation basée sur le temps
    start_time = time.time()
    current_time = start_time
    iterations = 0

    time_limit = float(time_limit)

    # Initialisation de la population
    N = len(interests)
    

    while current_time - start_time < time_limit:
        population = np.random.rand(population_size, N)
        # Évolution chaotique
        for i in range(population_size):
            population[i] += chaotic_system(population[i], friendships, interests)

        # Évaluation des solutions
        fitness_values = [fitness_function(ind, interests) for ind in population]

        # Sélection des meilleures solutions
        indices = np.argsort(fitness_values)
        selected_population = population[indices[:population_size]]

        # filtre des individus qui connaissent tous les autres
        filtered_population = []
        for ind in selected_population:
            if all(any(friend in invited_indices for friend in friendships[i]) for i, invited_indices in enumerate(filtered_population)):
                filtered_population.append(ind)
        population[:len(filtered_population)] = filtered_population

        # Mise à jour du temps et du nombre d'itérations
        current_time = time.time()
        iterations += 1


    # Meilleure solution trouvée
    best_solution = population[0]
    best_fitness = fitness_function(best_solution, interests)

    return best_solution, best_fitness, iterations



def main():
    # ouverture du fichier instance
    instance=open(input_file,'r')
    # Lecture des deux premières lignes
    N, M = map(int, instance.readline().split())

    # Lecture des interests
    interests = np.array([int(instance.readline().split()[1]) for _ in range(N)])

    # Lecture des connaissences des convives
    friendships = [tuple(map(int, instance.readline().split())) for _ in range(M)]

    # Exécution de l'algorithme
    best_solution, best_fitness, iterations = chaotic_optimization(time_limit, N, friendships, interests)

    # Écriture des résultats dans le fichier de sortie
    output_file = sys.argv[3]
    with open(output_file, 'w') as output_file:
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
    output_file = sys.argv[3]
    main()