# Fiche de décisions

| Choix | Options envisagées | Choix retenu et justification | Validé par l'auxiliaire (date) |
|---|---|---|---|
| Domaine | Aucun autre envisagé | **Formule 1** : nous sommes passionnés de Formule 1 depuis tout petits, et c'est motivant d'utiliser une passion pour un projet d'école. Question claire pour un utilisateur : une voiture finira-t-elle dans le top 10 ? | Facultatif |
| Jeu de données | Aucun entre envisagé | **Kaggle Formula 1 World Championship** (results, races, constructors, circuits) : CSV, colonnes numériques et catégorielles, aucune donnée personnelle | Facultatif |
| Nettoyage | Garder ou retirer les départs depuis les stands | **Retirer les lignes avec grid = 0** : ces voitures n'ont pas de vraie position de départ | Facultatif |
| Période | Toutes les saisons (1950–2024) ; depuis 2010 | **Depuis 2010** : le top 10 marque des points sur toute la période, donc la cible a le même sens partout. 6 351 lignes (contre 25 121). Arbre : 77,3 % (contre 68,0 % avec toutes les saisons) | Facultatif |
| Cible | Position exacte (régression), podium, top 10 | **top10** (classification) : positionOrder <= 10 ; classes presque équilibrées (environ 48 % de top 10) ; le podium ne concerne qu'environ 15 % des lignes | Facultatif |
| Colonnes d'entrée (X) | Toutes les colonnes du tableau fusionné | **grid, year, round, constructorRef, circuitRef** : infos connues avant le départ. Retirées : raceId et les Id (simples identifiants), country (même info que le circuit), positionOrder (c'est la réponse) | Facultatif |
| Séparation | 75/25 (défaut), 80/20, 70/30 | **80 % / 20 %** (5 080 / 1 271 lignes), random_state = 0 : convention courante, assez d'exemples pour apprendre et pour tester | Facultatif |
| Référence | Classe majoritaire, réponse au hasard | **Classe majoritaire** (toujours « hors top 10 ») : 53,8 % d'exactitude sur le test, la note à battre | Facultatif |
| Métrique | Exactitude, F1, précision, rappel | **Exactitude**, avec le F1 en complément : classes équilibrées, donc l'exactitude n'est pas trompeuse, et elle est facile à comprendre pour un non-informaticien | Facultatif |
| Modèle | Arbre de décision, régression logistique, k plus proches voisins | **Arbre de décision** : facile à expliquer (questions oui/non), gère les nombres et le texte, donne une probabilité. La régression logistique demande plus de préparation du texte ; les k plus proches voisins demandent de mettre les colonnes à la même échelle | Facultatif |
| Encodage du texte | OneHotEncoder, OrdinalEncoder | **OneHotEncoder** dans un Pipeline : une colonne de 0/1 par écurie et par circuit ; handle_unknown="ignore" pour ne pas planter sur une valeur inconnue | Facultatif |
| Profondeur de l'arbre | 3, 4, 5, 6, 8 | **5** : meilleur résultat en validation croisée sur l'entraînement (testé avec l'aide de Claude) ; sans limite, l'arbre apprend les données par cœur | Facultatif |
| Organisation du code | Classes de variables dans donnees.py, ou dans un module séparé | **Module variables.py séparé** : chaque module a une seule responsabilité | Facultatif |
| Logique de l'application | Logique dans interface.py, ou dans un module séparé | **Classe Application dans application.py** : l'interface appelle la logique sans la contenir, ce qui permet de la tester sans fenêtre | Facultatif |
| Historique | Fichier JSON, fichier CSV | **CSV** (historique.py) : une ligne par prédiction, ajoutée sans relire tout le fichier, lisible comme un tableau | Facultatif |
| Technologie d'interface | Tkinter, Streamlit, Gradio | **Tkinter** : inclus dans Python, fonctionne en local, exemple officiel pour intégrer Matplotlib | Facultatif |
| Graphique dans l'interface | Importance des variables, matrice de confusion, jauge de probabilité | **Matrice de confusion + jauge de probabilité** : la matrice montre la fiabilité du modèle, la jauge montre la prédiction en cours | Facultatif |
