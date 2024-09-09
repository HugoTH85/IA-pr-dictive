from calendar import c
import sys
import time
import numpy as np

def Glouton(N, friendships, interests):
    solution = []
    c_eligible = []
    c_restant = set(range(N))
    iterations = 0
   
    # Ajouter manuellement le premier convive potentiel à la solution
    if c_restant:
        premier_c = max(c_restant, key=lambda convive: len(friendships[convive]) * interests[convive])
        solution.append(premier_c)
        c_restant.remove(premier_c)
        
       
        
    while c_restant:
        scores = np.zeros(N)
        
        for convive in c_restant:
            friends = set(friendships[convive])
            friends_solution = friends.intersection(solution)
            scores[convive] = interests[convive] * len(friends_solution)
        
        iterations+= 1
        
    
        #Convive éligible(connais tout le monde)
        for convive in c_restant:
            convive_f = set(friendships[convive])
            if convive_f.issuperset(solution):
                c_eligible.append(convive)
        
        
        
        if c_eligible:
            #Score le plus élevé
            c_selectionne = max(c_eligible, key=lambda convive: scores[convive])
            solution.append(c_selectionne)
            c_restant.remove(c_selectionne)
            c_eligible.clear()

        else:
            print("Fin de l'algorithme.")
            break
    

    return solution

def main():
    start_time =time.time()
    fic = open(file_path, 'r')
    
    #Deux premières lignes
    N, M = map(int, fic.readline().split())

    #Lecture des interets des convives
    interests = np.array([int(fic.readline().split()[1]) for _ in range(N)])

    #Amis
    friendships = [[] for _ in range(N)]

    #Amitier
    for _ in range(M):
        i, j = map(int, fic.readline().split())
        friendships[i].append(j)
        friendships[j].append(i)

    fic.close()
    
    solution = Glouton(N, friendships, interests)
    
    #Resultats
    somme = sum(interests[convive] for convive in solution)
    print("Somme:",somme)    
    print("Solution :",solution)
    end_time = time.time()
    execution_time =end_time - start_time
    print("Temps d'execution :",execution_time)
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Glouton.py instance_file.txt")
        sys.exit(1)

    file_path = sys.argv[1]
    main()
