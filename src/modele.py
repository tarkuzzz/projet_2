from donnees import creation_donnees, nettoyage_donnees
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, f1_score
import json
import os
import joblib



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
    """Calcule l'exactitude (part de bonnes réponses) de façon vectorisée avec NumPy.

    Reçoit : les vraies réponses et les prédictions, de même longueur.
    Renvoie : un nombre entre 0 et 1
    """
    juste= y_vrai==y_predit
    return (np.mean(juste))




def creer_modele(profondeur_max: int=5) -> Pipeline:
    """Crée le modèle : encodage des colonnes texte, puis arbre de décision."""
    preparation= ColumnTransformer([ 
    ("texte", OneHotEncoder(handle_unknown="ignore"), ["constructorRef", "circuitRef"]),
    ("nombres", "passthrough", ["grid", "year", "round"]),
    ])
    arbre=DecisionTreeClassifier(max_depth=profondeur_max,random_state=0)
    return Pipeline([("preparation", preparation), ("arbre", arbre )])



def evaluer_modele(modele: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """Calcule l'exactitude, le F1 et la matrice de confusion du modèle sur le test."""
    predictions = modele.predict(X_test)
    reference = np.full(len(y_test), False)
    return {
        "exactitude": float(exactitude(y_test, predictions)),
        "exactitude_reference": float(exactitude(y_test, reference)),
        "f1": float(f1_score(y_test, predictions)),
        "matrice_confusion": confusion_matrix(y_test, predictions).tolist(),
    }




def creer_metadonnees(df: pd.DataFrame, resultats: dict) -> dict:
    """Décrit les colonnes d'entrée et le score du modèle, pour construire l'interface."""
    return {
        "colonnes": ["grid", "year", "round", "constructorRef", "circuitRef"],
        "numeriques": {
            colonne: {"min": int(df[colonne].min()), "max": int(df[colonne].max())}
            for colonne in ["grid", "year", "round"]
        },
        "categorielles": {
            colonne: sorted(df[colonne].unique().tolist())
            for colonne in ["constructorRef", "circuitRef"]
        },
        "resultats": resultats,
    }




def sauvegarder_modele(modele: Pipeline, metadonnees: dict, dossier: str = "modeles") -> None:
    """Enregistre le modèle (joblib) et ses métadonnées (JSON) dans le dossier donné."""
    os.makedirs(dossier,exist_ok=True)
    joblib.dump(modele, os.path.join(dossier, "modele.joblib"))
    with open(os.path.join(dossier, "metadonnees.json"), "w", encoding="utf-8") as fichier:
        json.dump(metadonnees, fichier, indent=2, ensure_ascii=False)




if __name__ == "__main__":
    df = creation_donnees()
    df = nettoyage_donnees(df)
    X_train , X_test , y_train ,y_test= separation_donnees(df)
    predictions_reference=np.full(len(y_test),False)
    modele=creer_modele()
    modele.fit(X_train,y_train)
    resultats=evaluer_modele(modele, X_test, y_test)
    metadonnes=creer_metadonnees(df,resultats)
    sauvegarder_modele(modele,metadonnes)


   




    