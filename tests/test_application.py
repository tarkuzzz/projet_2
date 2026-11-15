import pytest

from application import Application
from exceptions import DonneeInvalide, ModeleIntrouvable

SAISIE_VALIDE = {"grid": "1", "year": "2023", "round": "5",
                 "constructorRef": "red_bull", "circuitRef": "monaco"}


def test_prediction_valide(tmp_path):
    """Une saisie valide donne une probabilité entre 0 et 1 et un message lisible."""
    application = Application(chemin_historique=str(tmp_path / "historique.csv"))
    resultat = application.predire(SAISIE_VALIDE)
    assert 0 <= resultat["probabilite"] <= 1
    assert "top 10" in resultat["message"]


def test_saisie_invalide(tmp_path):
    """Une saisie invalide lève DonneeInvalide, avec le nom du champ dans le message."""
    application = Application(chemin_historique=str(tmp_path / "historique.csv"))
    saisie = {**SAISIE_VALIDE, "grid": "abc"}
    with pytest.raises(DonneeInvalide, match="Position de départ"):
        application.predire(saisie)


def test_historique(tmp_path):
    """Chaque prédiction est ajoutée à l'historique, puis relue."""
    application = Application(chemin_historique=str(tmp_path / "historique.csv"))
    assert application.lire_historique() == []
    application.predire(SAISIE_VALIDE)
    application.predire(SAISIE_VALIDE)
    historique = application.lire_historique()
    assert len(historique) == 2
    assert historique[0]["constructorRef"] == "red_bull"


def test_modele_introuvable(tmp_path):
    """Si le modèle n'existe pas dans le dossier, Application lève ModeleIntrouvable."""
    with pytest.raises(ModeleIntrouvable):
        Application(dossier=str(tmp_path))