utiliation 1:
outil:Claude
question: comment faire pour push le projet sur git et garder le repo le  plus propre possible
reponse recu: creation du fichier .gitignore avec les commandes a l'interieur
verification faite: sur le github du projet lors des push il y a aucun fichier indesirables
decision: garde

utiliation 2:
outil:Claude
question: comment faire pour avoir des test qui verifie mon code a chaques fois que je push le code?
repoonse recu: creation d'un fichier test.yml avec du code qui installe et roule pytest automatiquement 
decision: garde mais il y avait une erreur quelque part

utilisation 3:
outil:Claude
question:comment enlever l'erreur 'exit code 127'?
reponse recue: remplacer pip et pytest par python -m pip et python -m pytest
verification: en relisant le code j'ai remarque une erreur de syntaxe qui c'etait glisser dans le code 
decision: rejete car l'erreur ne venait pas des test eux memes mais plutot d'une erreur de syntaxe


utilisation 4:
outil:Claude
question: quelle donnees je dois utiliser et comment je mets ces donnees sous un seul tableau
reponse recu: utiliser results.csv, races.csv, constructors.csv et circuits.csv puis les réunir avec merge une étape à la fois
verification: disscusion avec l auxielliere
decision: garde etant onne que les donnes correspondes aux consignes qui nous on ete donne


utilisation 5:
outil:Claude
question: comment utiliser merge pour mettre resultats et courses ensembles
reponse recu: resultats.merge(courses, on="raceId"),  on="raceId" est la cololmne commune a partir de laquelle on merge 
verification: avec print(df.head()) il y a un tableau avec year,round et circuitId qui apparait
decision: garde et j'ai repeter le processus pour les autres donnees (claude m'a dit de separer en fonction)

Utilisation 7 :
Outil : Claude
Question : comment faire le graphique du taux de top 10 selon la position de départ avec maplotlib?
Réponse reçue : la fonction creation_graphique, Claude a aussi proposé un bloc if à la fin du fichier, pour que le code ne s'exécute pas quand on appele le fichier 
Vérification faite : exécution du code l'image du graphique est créée, mais l'axe affichait une position 0 qui n'existe pas
Décision : garde mais j'ai ajoute    plt.xticks et plt.xlim pour que l'axe commence à 1 et nous avons aussi garde le bloc if 


