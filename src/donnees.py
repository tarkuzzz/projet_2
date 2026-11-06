import pandas as pd
import matplotlib.pyplot as plt
import os


def lire_fichier_csv(fichier:str):

    chemin = os.path.join("donnees", fichier)
    if os.path.exists(chemin) == False:
        raise FileNotFoundError("Le fichier n'existe pas")
    else:
        return pd.read_csv(chemin,na_values=r"\N")




def creation_donnees():
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

    print(df.head())


    grid_possible = df["grid"] > 0 
    df = df[grid_possible]
    df["top10"] = df["positionOrder"] <= 10




    taux = df.groupby("grid")["top10"].mean() * 100

    plt.bar(taux.index, taux.values)
    plt.title("Taux de top 10 selon la position de départ")
    plt.xlabel("Position de départ")
    plt.ylabel("Taux de top 10 (%)")
    plt.xticks(range(1, taux.index.max() + 1, 2))
    plt.xlim(0.5, taux.index.max() + 0.5)
    plt.savefig("exploration_grid.png")
    return df 


apercu = creation_donnees()
print(apercu.head())
