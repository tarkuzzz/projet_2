import pandas as pd
import pytest

from donnees import lire_fichier_csv, nettoyage_donnees,creation_donnees


def test_lire_fichier_introuvable():
    """Un fichier qui n'existe pas lève FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        lire_fichier_csv("fichier_qui_n_existe_pas.csv")


def test_nettoyage_donnees():
    """Le nettoyage retire grid = 0 et les saisons avant 2010, et crée top10."""
    df = pd.DataFrame({
        "grid": [1, 0, 5, 12],
        "year": [2015, 2015, 2005, 2020],
        "positionOrder": [10, 3, 2, 11],
    })
    propre = nettoyage_donnees(df)
    assert len(propre) == 2
    assert list(propre["top10"]) == [True, False]





def test_cololmne_df():
    df = creation_donnees()
    assert "raceId" in df.columns
    assert "constructorId" in df.columns
    assert "grid" in df.columns
    assert "positionOrder" in df.columns
    assert "year" in df.columns
    assert "round" in df.columns
    assert "circuitId" in df.columns
    assert "constructorRef" in df.columns
    assert "circuitRef" in df.columns
    assert "country" in df.columns
    assert 'weather' not in df.columns 
    assert len(df.columns) == 10

def test_cololmne_df_nettoyer():
    df_1 = creation_donnees()
    df =  nettoyage_donnees(df_1)
    assert len(df.columns) == 11
    assert 'top10' in df.columns


