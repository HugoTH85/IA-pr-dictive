import sys
import math
import numpy as np
from random import random, sample


#____________________________________________________________________________________________________________________________________________________________________________
# INITIALISATION DES VALEURS POUR L'INSTANCE DONNEE
#____________________________________________________________________________________________________________________________________________________________________________
def tab_poids(input):
    instance=open(input, 'r')
    lignes=instance.readlines()
    # On détermine le nombre de convives potentiels dans l'instance choisie
    n=2
    while lignes[n+1][0]!="0":
        if n>=10 and n<100 and lignes[n+1][0]+lignes[n+1][1]!=str(n):
            break
        elif n>=100 and lignes[n+1][0]+lignes[n+1][1]+lignes[n+1][2]!=str(n):
            break
        n+=1
    L=[]
    for i in range(1,n+1):
        j=0
        while lignes[i][j]!=" ":
            j+=1
        j+=1
        val=""
        while lignes[i][j]!="\n":
            val+=lignes[i][j]
            j+=1
        L.append(int(val))
    instance.close()
    return L

def tab_connaissances(input):
    instance=open(input, 'r')
    lignes=instance.readlines()
    n=2
    while lignes[n+1][0]!="0":
        if n>=10 and n<100 and lignes[n+1][0]+lignes[n+1][1]!=str(n):
            break
        elif n>=100 and lignes[n+1][0]+lignes[n+1][1]+lignes[n+1][2]!=str(n):
            break
        n+=1
    # On passe les connaissances du dernier convive
    d=n+1
    # Création de la matrice des connaissances
    L = [[0] * n for _ in range(n)]

    while lignes[d][0]+lignes[d][1]+lignes[d][2]==str(n-1):
        d+=1
    # On configure la matrice des connaissances
    for i in range(d,len(lignes)):
        j=0
        # On récupère le convive dans num
        num=""
        while lignes[i][j]!=" ":
            num+=lignes[i][j]
            j+=1    
        j+=1
        # On récupère la connaissance du convive dans var
        var=""
        while lignes[i][j]!="\n":
            var+=lignes[i][j]
            j+=1
        # On passe à 1 la bonne case de la matrice
        L[int(num)][int(var)]=1
        L[int(var)][int(num)]=1
    #on complète par les connaissances du dernier convive en s'appuyant sur les autres
    for i in range (len(L[-1])-1):
        if L[i][-1]==1:
            L[-1][i]=1
    L[-1][-1]=1
    instance.close()
    return L


#____________________________________________________________________________________________________________________________________________________________________________
# FONCTIONS UTILES POUR LA SUITE
#____________________________________________________________________________________________________________________________________________________________________________
def check_Connaissances(solution,connaissances):
    for i in range(len(solution)):
        if solution[i]==1:
            for j in range(len(solution)):
                if solution[j]==1 and i!=j and connaissances[i][j]==0:
                    return False
    return True

# Calcul de la somme des poids pour une solution
def evaluation_solution(result_convives, poids):
    val=0
    for i in range(len(result_convives)):
        val+=result_convives[i]*poids[i]
    return val


#____________________________________________________________________________________________________________________________________________________________________________
# ALGORITHME GLOUTON POUR GENERER UNE SOLUTION INITIALE
#____________________________________________________________________________________________________________________________________________________________________________
def solution_initiale(nb_convives,connaissances,poids):
    print("")
    print("Début du glouton")
    print("...")
    solution = []
    guest_eligible = []
    guest_restant = set(range(nb_convives))
    iterations = 0
    invitation = np.zeros(nb_convives, dtype=int)



    # Ajouter manuellement le premier convive potentiel à la solution (celui avec le plus d'amis)
    if guest_restant:
        guest_friend = max(guest_restant, key=lambda guest: np.sum(connaissances[guest]) * poids[guest])
        solution.append(guest_friend)
        invitation[guest_friend] = 1
        guest_restant.remove(guest_friend)



    while guest_restant:
        scores = np.zeros(nb_convives)

        for guest in guest_restant:
            friends_solution = np.logical_and(connaissances[guest], invitation)
            scores[guest] = poids[guest] * np.sum(friends_solution)


        iterations+= 1

        for guest in guest_restant:
            guest_f = list(connaissances[guest])  # Convertir en liste car guest_f est maintenant une liste de 0 et 1
            if all(guest_f[i] == 1 for i in solution):  # Vérifier si tous les amis de guest sont présents dans la solution
                guest_eligible.append(guest)


        if guest_eligible:
            #Score le plus élevé
            guest_selectionne = max(guest_eligible, key=lambda guest: scores[guest])

            invitation[guest_selectionne] = 1
            solution.append(guest_selectionne)
            guest_restant.remove(guest_selectionne)
            guest_eligible.clear()

        else:
            break
    print("Fin du glouton")
    print("")
    return invitation

#____________________________________________________________________________________________________________________________________________________________________________
# ALGORITHME DES LUCIOLES
#____________________________________________________________________________________________________________________________________________________________________________
def mouvement_lucioles(solution, poids, attractivite_lucioles,connaissances):
    solution2=solution.copy()
    lucioles = len(solution2)
    for i in range(lucioles):
        # Recherche d'une luciole
        if solution2[i]==1:
            for j in range(lucioles):
                if poids[j] > poids[i]:
                    # Si la luciole j est plus lumineuse que la luciole i
                    attractivite_i = attractivite_lucioles*math.exp(-abs(solution2[i]-solution2[j]))
                    # Déplacement de la luciole i
                    if random() < attractivite_i:
                        var=solution2[i]
                        solution2[i] = solution2[j]
                        solution2[j] = var
    if check_Connaissances(solution2,connaissances)==False:
        solution2=mouvement_lucioles(solution2,poids,attractivite_lucioles,connaissances)
    return solution2

def algorithme_luciole(solution, poids, attractivite_lucioles, max_iterations,connaissances):
    print("début algo lucioles")
    print("...")
    solution2 = solution.copy()
    L=[]
    for iteration in range(max_iterations):
        solution2=mouvement_lucioles(solution2,poids,attractivite_lucioles,connaissances)
        L.append([solution2,evaluation_solution(solution2,poids)])
    print("fin algo lucioles")
    print("")
    return L


#____________________________________________________________________________________________________________________________________________________________________________
# Algorithme Immunitaire
#____________________________________________________________________________________________________________________________________________________________________________
def select_parents(solutions, pression_selection):
    num_parents = int(len(solutions) * pression_selection)
    parents_selectionnes = sample(solutions, num_parents)
    return parents_selectionnes

def mutation_solution(solution, taux_mutation,connaissances):
    for i in range(len(solution)):
        solution2=solution.copy()
        if random()<taux_mutation:
            solution2[i]=1-solution2[i]
    if check_Connaissances(solution2,connaissances)==False:
        mutation_solution(solution,taux_mutation,connaissances)
    else:
        return solution2

def algorithme_immunitaire(solutions, poids, taux_mutation, pression_selection, max_generations,connaissances):
    print("début algo génétique")
    print("...")
    solutions2 = solutions.copy()

    for generation in range(max_generations):
        parents = select_parents(solutions2, pression_selection)
        enfants = []

        for parent in parents:
            enfant_mute = mutation_solution(parent, taux_mutation,connaissances)
            enfants.append([enfant_mute,evaluation_solution(enfant_mute)])

        solutions2 += enfants

        # Trier les solutions possibles
        solutions2=sorted(solutions2, key=lambda x: x[1], reverse=True)

        # Tronquer la population pour maintenir sa taille
        solutions2 = solutions2[:len(solutions)]

    # Retourner la meilleure solution trouvée dans l'ensemble
    best_solution=solutions2[0][1]
    for i in range(len(solutions2)):
        if solutions2[i][1]>best_solution:
            best_solution=solutions2[i]
    print("fin algo génétique")
    print("")
    return best_solution


#____________________________________________________________________________________________________________________________________________________________________________
# Algorithme Hybride
#____________________________________________________________________________________________________________________________________________________________________________
def hybride(input, attractivite_lucioles, taux_mutation, pression_selection, max_iterations, max_generations):
    # Initialisation des connaissances et poids des convives
    connaissances=tab_connaissances(input)
    poids=tab_poids(input)
    nb_convives=len(poids)

    # Coordonne l'exécution des deux algorithmes, utilisant les solutions générées par les lucioles comme point de départ pour l'algorithme immunitaire.
    # Génération d'une solution initiale (liste de convives)
    solution1 = solution_initiale(nb_convives,connaissances,poids)

    # Application de l'algorithme des lucioles pour explorer l'espace des solutions
    solutions = algorithme_luciole(solution1, poids, attractivite_lucioles, max_iterations,connaissances)

    # Application de l'algorithme immunitaire pour améliorer les solutions trouvées par les lucioles
    solution_finale = algorithme_immunitaire(solutions, poids, taux_mutation, pression_selection, max_generations,connaissances)

    sol=[]
    for i in range(len(solutions)):
        sol.append(solutions[i][1])

    print("Solution initiale : ",evaluation_solution(solution1,poids))
    print("Solutions des lucioles : ",sol)
    print("solution finale :",solution_finale)


if __name__ == "__main__":
    # Vérifier si les arguments nécessaires sont fournis
    if len(sys.argv) != 2:
        print("Usage: python myfile.py instance_file.txt")
        sys.exit(1)

    # Récupérer le fichier d'instance à partir des arguments de la ligne de commande
    file = sys.argv[1]

    # Demander à l'utilisateur de renseigner les valeurs souhaitées pour les paramètres suivants :
    taux_mutation=float(input("Veuillez saisir le taux de mutation souhaité (entre 0 et 1) : "))
    if taux_mutation<0 or taux_mutation>1:
        print("Valeur incorrecte")
        sys.exit(1)
    pression_selection=float(input("Veuillez saisir la pression de sélection souhaité pour l'algorithme immunitaire (entre 0 et 1) : "))
    if pression_selection<0 or pression_selection>1:
        print("Valeur incorrecte")
        sys.exit(1)
    attractivite_lucioles=float(input("Veuillez saisir l'intensité d'attractivité des lucioles : "))
    if attractivite_lucioles<0:
        print("Valeur incorrecte")
        sys.exit(1)
    max_iterations=int(input("Veuillez saisir le nombre maximum d'itérations pour l'algorithme des lucioles : "))
    if max_iterations<0:
        print("Valeur incorrecte")
        sys.exit(1)
    max_generations=int(input("Veuillez saisir le nombre maximum de générations créées pour l'algorithme immunitaire : "))
    if max_generations<0:
        print("Valeur incorrecte")
        sys.exit(1)

    # Exécution de l'algorithme
    hybride(file,attractivite_lucioles,taux_mutation,pression_selection,max_iterations,max_generations)