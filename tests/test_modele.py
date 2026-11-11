import numpy as np
import pytest
from sklearn.metrics import accuracy_score

from modele import exactitude,separation_donnees
from donnees import creation_donnees, nettoyage_donnees

def test_exactitude_cas_usuel():
    """Avec 3 bonnes réponses sur 5, l'exactitude vaut 0,6."""
    vrai = np.array([True, False, True, False, False])
    predit = np.array([True, True, True, False, True])
    resultat = exactitude(vrai, predit)
    assert resultat == pytest.approx(0.6)

def test_exactitude_tout_juste():
    """Si toutes les prédictions sont justes, l'exactitude vaut 1."""
    vrai = np.array([True, False, True, False, False])
    predit = np.array([True, False, True, False, False])
    resultat = exactitude(vrai, predit)
    assert resultat==pytest.approx(1.0)

def test_exactitude_comme_scikit_learn():
    """Sur nos vraies données, notre exactitude donne le même résultat que scikit-learn."""
    df = creation_donnees()
    df = nettoyage_donnees(df)
    X_train, X_test, y_train, y_test = separation_donnees(df)
    predictions_reference = np.full(len(y_test), False)
    notre_resultat = exactitude(y_test, predictions_reference)
    resultat_sklearn = accuracy_score(y_test, predictions_reference)
    assert notre_resultat == pytest.approx(resultat_sklearn)