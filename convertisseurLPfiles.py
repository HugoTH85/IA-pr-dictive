import sys

def convertTXTtoLP(input,output):
    instance=open(input, 'r')
    LPfile=open(output, 'w')
    
    lignes=instance.readlines()

    # On détermine le nombre de convives potentiels dans l'instance choisie
    n=2
    while lignes[n+1][0]!="0":
        if n>=10 and n<100 and lignes[n+1][0]+lignes[n+1][1]!=str(n):
            break
        elif n>=100 and lignes[n+1][0]+lignes[n+1][1]+lignes[n+1][2]!=str(n):
            break
        n+=1

    # Ecriture de la partie "Maximize" du fichier lp
    LPfile.write("Maximize\n")
    LPfile.write("z: ")
    for i in range(1,n+1):
        j=0
        while lignes[i][j]!=" ":
            j+=1
        j+=1
        while lignes[i][j]!="\n":
            LPfile.write(lignes[i][j])
            j+=1
        LPfile.write(" x")
        LPfile.write(str(i))
        if i<n:
            LPfile.write(" + ")
        else:
            LPfile.write("\n")

    # Ecriture des contraintes
    LPfile.write("Subject To\n")
    # On passe les connaissances du dernier convive
    d=n+1
    # Création de la matrice des connaissances
    L = [[0] * n for _ in range(n)]

    while lignes[d][0]+lignes[d][1]+lignes[d][2]==str(n-1):
        d+=1

    # On parcours le reste des connaissances
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

    for i in range(len(L)-1):
        for j in range(len(L[i])):
            # Si 2 convives ne se connaissent pas
            if L[i][j]!=1 and i!=j:
                LPfile.write("x"+str(i+1)+" + x"+str(j+1)+" <= 1\n")
                # On passe ses valeurs à autre que 0 pour éviter des redondances
                L[j][i]=1
                L[i][j]=1

    # Ecriture des variables xi
    LPfile.write("Binaries\n")
    for i in range(1,n+1):
        LPfile.write("x")
        LPfile.write(str(i))
        LPfile.write("\n")

    LPfile.write("End")

    instance.close()
    LPfile.close()

if __name__ == "__main__":
    # Vérifier si les arguments nécessaires sont fournis
    if len(sys.argv) != 3:
        print("Usage: python myfile.py input_file.txt output_file.png")
        sys.exit(1)

    # Récupérer les noms de fichiers à partir des arguments de la ligne de commande
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # fonction à exécuter
    convertTXTtoLP(input_file,output_file)

    #Méthode pour exécuter la fonction : php code1.py InstanceX.txt InstanceX.lp
    # avec InstanceX.txt le fichier texte de l'instance choisie et InstanceX.lp le fichier lp généré par la suite