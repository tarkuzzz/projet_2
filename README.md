# Prédicteur de top 10 en Formule 1

Projet 2 d'INF1007 (Polytechnique Montréal, automne 2026), réalisé en équipe de deux.

## Description

L'application estime si une voiture de Formule 1 finira dans le top 10 d'une course, à partir de 5 informations connues avant le départ : la position de départ, la saison, le numéro de la course, l'écurie et le circuit.

Un arbre de décision a été entraîné sur les courses de 2010 à 2024. L'utilisateur décrit une voiture dans une interface Tkinter et obtient une prédiction en langage simple, avec une probabilité. L'application affiche aussi un graphique et garde l'historique des prédictions.

On peut l'utiliser par exemple après les qualifications, quand la position de départ est connue, pour estimer le résultat de la course.

## Jeu de données

- **Source :** Formula 1 World Championship (1950 - 2024) sur Kaggle : https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020
- **Licence :** CC0: Public Domain
- **Fichiers utilisés :** `results.csv`, `races.csv`, `constructors.csv` et `circuits.csv`, dans le dossier `donnees/`
- **Après nettoyage :** 6 351 lignes (saisons 2010 à 2024, sans les départs depuis la voie des stands), environ 48 % de top 10
- **Colonnes d'entrée :** `grid`, `year`, `round` (numériques) ; `constructorRef`, `circuitRef` (catégorielles)
- Aucune donnée personnelle : on n'utilise ni le nom ni l'identifiant des pilotes.

## Installation et lancement

Depuis la racine du projet :

```bash
pip install -r requirements.txt
python src/modele.py   # entraîne le modèle et le sauvegarde dans modeles/ (déjà fait)
python src/main.py     # ouvre l'interface
```

L'interface utilise **Tkinter**, inclus avec Python. Le modèle est déjà sauvegardé dans `modeles/` : il n'est pas réentraîné à chaque lancement.

## Structure du code

| Fichier | Rôle |
|---|---|
| `src/donnees.py` | Lecture des CSV, fusion, nettoyage, graphique d'exploration |
| `src/modele.py` | Séparation, entraînement, évaluation, sauvegarde et chargement du modèle |
| `src/variables.py` | Classes `Variable_general`, `Variable_numerique` et `Variable_non_numerique`, qui valident les saisies |
| `src/exceptions.py` | Exceptions personnalisées `DonneeInvalide` et `ModeleIntrouvable` |
| `src/historique.py` | Enregistrement et lecture de l'historique des prédictions (CSV) |
| `src/application.py` | Classe `Application` : la logique (validation, prédiction, historique), sans fenêtre |
| `src/interface.py` | Fenêtre Tkinter : elle affiche et appelle `Application`, sans faire de calcul |
| `src/main.py` | Point d'entrée |
| `tests/` | Tests pytest |

## Résultat du modèle

- **Modèle :** arbre de décision (`max_depth=5`), avec un encodage one-hot des colonnes texte
- **Métrique :** exactitude, avec le F1 en complément
- **Évaluation :** sur 20 % des données (1 271 voitures), jamais vues pendant l'entraînement

| | Exactitude |
|---|---|
| Référence (toujours « hors top 10 ») | 53,8 % |
| **Arbre de décision** | **77,3 %** |

F1 : 0,757. Matrice de confusion : 535 vrais négatifs, 149 fausses alertes, 139 ratés, 448 vrais positifs.

**Limites :** le modèle se trompe environ une fois sur quatre. Il ne connaît ni la météo, ni les abandons, ni les pénalités, ni la forme du pilote. Il n'a vu que les saisons 2010 à 2024. Enfin, la séparation mélange les années au hasard : le test ne porte pas strictement sur des courses « futures ».

## Tests et couverture

```bash
pytest
coverage run --source=src -m pytest
coverage report
```

20 tests : cas usuels, cas limites et cas d'erreur.

Couverture : **51 %** du code de `src/`. L'interface (`interface.py`) et `main.py` ne sont pas testés, comme le prévoit l'énoncé : toute la logique est dans `Application`, qui est testée. Sans ces deux fichiers, la couverture est de **82 %**.

## Outil du chapitre 7

Une **`lambda`** sert de clé de tri dans `creer_metadonnees` (`modele.py`) : elle classe les écuries et les circuits par ordre alphabétique, sans tenir compte des majuscules.

## Documentation consultée

- pandas, `DataFrame.merge` : https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
- scikit-learn, `train_test_split` : https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
- scikit-learn, `DecisionTreeClassifier` : https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
- Tkinter : https://docs.python.org/3/library/tkinter.html
- Matplotlib dans Tkinter : https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html