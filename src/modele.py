from donnees import creation_donnees, nettoyage_donnees
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np


def separation_donnees(df:pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Sépare le tableau nettoyé en données d'entraînement et de test.

    Reçoit : le tableau nettoyé, qui contient les colonnes d'entrée et la colonne top10.
    Renvoie : X_train, X_test, y_train, y_test (80 % entraînement, 20 % test).
    Échoue : KeyError si une des colonnes attendues manque dans le tableau.
    """
    X=df[["grid", "year", "round", "constructorRef", "circuitRef"]]
    y=df["top10"]
    X_train, X_test, y_train, y_test = train_test_split(X , y, random_state=0, test_size=0.2)
    return X_train, X_test, y_train, y_test

def exactitude(y_vrai,y_predit):
    juste= y_vrai==y_predit
    return (np.mean(juste))

if __name__ == "__main__":
    df = creation_donnees()
    df = nettoyage_donnees(df)
    X_train , X_test , y_train ,y_test= separation_donnees(df)
    predictions_reference=np.full(len(y_test),False)
    print(exactitude(y_test,predictions_reference))


   




    