import pandas as pd
import matplotlib.pyplot as plt
import os
 


def lire_fichier_csv(fichier:str):
    """Lit un fichier CSV du dossier donnees/.

    Reçoit : le nom du fichier (ex. "results.csv").
    Renvoie : un DataFrame où les valeurs "\\N" sont considérées comme manquantes.
    Échoue : FileNotFoundError si le fichier n'existe pas.
    """

    chemin = os.path.join("donnees", fichier)
    if os.path.exists(chemin) == False:
        raise FileNotFoundError("Le fichier n'existe pas")
    else:
        return pd.read_csv(chemin,na_values=r"\N")




def creation_donnees():
    """Réunit les 4 fichiers CSV en un seul tableau.

    Renvoie : un DataFrame avec une ligne par voiture dans une course
              (résultat, course, écurie et circuit).
    Échoue : FileNotFoundError si un des fichiers CSV est introuvable.
    """
    resultats = lire_fichier_csv('results.csv')
    resultats = resultats[["raceId", "constructorId", "grid", "positionOrder"]]

    courses = lire_fichier_csv('races.csv')
    courses = courses[["raceId", "year", "round", "circuitId"]]
    df = resultats.merge(courses, on="raceId")


    ecuries = lire_fichier_csv('constructors.csv')
    ecuries = ecuries[["constructorId", "constructorRef"]]
    df = df.merge(ecuries, on="constructorId")

    circuits = lire_fichier_csv("circuits.csv")
    circuits = circuits[["circuitId", "circuitRef", "country"]]
    df = df.merge(circuits, on="circuitId")

    return df 




def nettoyage_donnees(df:pd.DataFrame):
    """Nettoie le tableau et crée la colonne cible top10.

    - retire les départs depuis les stands (grid = 0) ;
    - garde seulement les saisons depuis 2010 (le top 10 marque des points) ;
    - crée top10 = True si la voiture finit dans les 10 premiers.

    Reçoit : le tableau créé par creation_donnees.
    Renvoie : un nouveau DataFrame nettoyé (l'original n'est pas modifié).
    Échoue : KeyError si une des colonnes grid, year ou positionOrder manque.
    """
    grid_possible = df["grid"] > 0 
    df = df[grid_possible].copy()
    df = df[df["year"] >= 2010]
    df["top10"] = df["positionOrder"] <= 10
    return df 




def creation_graphique(df:pd.DataFrame):
    """Trace le taux de top 10 selon la position de départ et l'enregistre en image.

    Reçoit : le tableau nettoyé et le chemin de l'image à créer.
    Échoue : KeyError si les colonnes grid ou top10 manquent.
    """
    taux = df.groupby("grid")["top10"].mean() * 100
    
    plt.bar(taux.index, taux.values)
    plt.title("Taux de top 10 selon la position de départ")
    plt.xlabel("Position de départ")
    plt.ylabel("Taux de top 10 (%)")
    plt.xticks(range(1, taux.index.max() + 1, 2))
    plt.xlim(0.5, taux.index.max() + 0.5)
    plt.savefig("exploration_grid.png")




if __name__ == "__main__":
    df = creation_donnees()
    df = nettoyage_donnees(df)
    print(df.head())
    creation_graphique(df)


