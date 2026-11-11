# Journal d'utilisation de l'IA

| # | Outil | Question | Réponse reçue | Vérification faite | Décision |
|---|---|---|---|---|---|
| 1 | Claude | Comment envoyer le projet sur GitHub en gardant le dépôt le plus propre possible ? | Créer un fichier .gitignore contenant la liste des fichiers à ignorer | Sur le GitHub du projet, aucun fichier indésirable n'apparaît après les push | Gardé |
| 2 | Claude | Comment avoir des tests qui vérifient mon code à chaque push ? | Créer un fichier tests.yml qui installe les bibliothèques et lance pytest automatiquement | La CI a d'abord échoué, puis est passée après la correction d'une erreur de syntaxe (voir l'utilisation 3) | Gardé |
| 3 | Claude | Comment corriger l'erreur « exit code 127 » ? | Remplacer pip et pytest par python -m pip et python -m pytest | En relisant le code, j'ai remarqué une erreur de syntaxe qui s'y était glissée | Rejeté, car l'erreur ne venait pas des tests, mais d'une erreur de syntaxe |
| 4 | Claude | Quelles données utiliser, et comment les réunir en un seul tableau ? | Utiliser results.csv, races.csv, constructors.csv et circuits.csv, puis les réunir avec merge, une étape à la fois | Discussion avec l'auxiliaire | Gardé, car les données respectent les consignes du projet |
| 5 | Claude | Comment utiliser merge pour réunir les résultats et les courses ? | resultats.merge(courses, on="raceId") ; on="raceId" indique la colonne commune utilisée pour la fusion | Avec print(df.head()), les colonnes year, round et circuitId apparaissent dans le tableau | Gardé ; j'ai répété le processus pour les autres données (Claude m'a conseillé de séparer le code en fonctions) |
| 6 | Claude | Comment faire le graphique du taux de top 10 selon la position de départ avec Matplotlib ? | La fonction creation_graphique ; Claude a aussi proposé un bloc if à la fin du fichier, pour que le code ne s'exécute pas quand un autre fichier l'importe et pour ne pas qu'on génère une image à chaque fois | En exécutant le code, l'image du graphique est créée, mais l'axe affichait une position 0, qui n'existe pas en réalité | Modifié : ajout de plt.xticks et plt.xlim pour que l'axe commence à 1 ; bloc if gardé |
| 7 | Claude | M'expliquer le projet et les bases du machine learning (données, indices, cible, entraînement, test) | Explications simples avec nos données F1, sans écrire notre code | Relu l'énoncé et les fichiers CSV ; compris assez pour choisir moi-même les colonnes X et y | Gardé |
| 8 | Claude | Me servir de tuteur pendant que je code modele.py | Questions et indices pour me guider, sans donner les réponses (imports, X et y, erreurs de dossier, de pandas et de git push) | J'ai écrit et lancé le code moi-même ; le tableau, X et y s'affichent correctement | Gardé |


