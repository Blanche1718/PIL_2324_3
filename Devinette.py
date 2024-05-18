import random
def dessin():
    if categorie_choisie == "Informatique":
       image = """
               O  
              /|\\
              / \\ 
        """
       return image
    elif categorie_choisie == "Medecine":
       image = """
            +
          +++++
            +
            +
            +  
        """
       return image
    elif categorie_choisie == "Basketball":
       image = """
               O 
              /| 
               |\/O
               |
              / \\
        """
       return image 
   

chemin = r"C:\Users\DELL\OneDrive\Bureau\New folder\mots.txt" 
categories = {}
# je veux ouvrir le fichier de mots en mode lecture
with open(chemin,"r") as f:
#On va lire toutes les lignes du fichier et les stocker dans une liste lignes
   lignes = f.readlines()
#instructions à l'utilisateur
print("\nPour pouvoir jouer vous devez entrez le numéro de la catégorie dans laquelle vous souhaitez deviner des mots.")
#parcourir la liste lignes et enregistrer les categories ainsi que les mots de la catégories sous formes de clés-valeurs dans un dictionnaire
i = 13
for ligne in lignes :
   if ligne.strip().endswith(":"):
      categorie = ligne.strip()[:-1]
      categories[categorie] = []
      i += 1
   elif ligne == " ":
         continue
   else:
      if categorie: 
         categories[categorie].append(ligne.strip())
#affichage des categories
print("\nVoici les categories disponibles")
for i , categorie in enumerate(categories, 1):
   print(f'{i}: {categorie}')
#instruction à l'utilisateur
choix = int(input("\nEntrez le numéro de la catégorie de votre choix : "))
#verifier si le numero entré correspond à celui d'une catégorie dans le dictionnaire et selectionner les mots de cette catégorie puis le mot à deviner
if choix in range(1 , len(categories)+1 ):#range s'arrete à l'avant dernier indice 
   categorie_choisie = list(categories.keys())[choix-1]#les indices dans le dictionnaire commence par 0 
   mots_categorie = categories[categorie_choisie]

   mot = random.choice(mots_categorie)
   mot_miniscule = mot.lower()
   print(mot)
   lettres_du_mot = set(mot_miniscule)
   lettres_devinées = set()
   longueur_du_mot = len(mot)
   tentatives = longueur_du_mot + 3
   print(f"\nLe mot contient {longueur_du_mot} letrres\n" )
   while tentatives >0 :
      mot_display = ' '.join(lettre if lettre in lettres_devinées else '*'for lettre in mot_miniscule)
      print (mot_display)
      lettre_entrée = input("\n Devinez une lettre du mot : ").lower()
      if lettre_entrée in lettres_du_mot and lettres_du_mot != set():
         lettres_devinées.add(lettre_entrée)
         lettres_du_mot.remove(lettre_entrée)
         tentatives -= 1 
         if lettres_du_mot != set():
             print( "\n Il vous reste {} tentatives.".format(tentatives))
   
      elif lettre_entrée in lettres_devinées:
          print("\n Vous aviez dejà deviné cette lettre")
          tentatives -= 1
          print( "\n Il vous reste {} tentatives.".format(tentatives))
   
      else:
            print("\nMauvaise lettre!")
            tentatives -= 1
            print( "\n Il vous reste {} tentatives.".format(tentatives))
   
      
      if lettres_du_mot == set():
            print(f"\nFélicitations, vous avez deviné le mot :{mot} .")
            print(dessin())
            break      
   # Si le joueur a épuisé toutes les tentatives
   if tentatives == 0:
      print("\nDésolé, vous avez épuisé toutes vos tentatives. Le mot était :", mot)      

else:
   print("\n Choix invalide.Le numéro entré doit correspondre à celui d'une des catégories affichées")
