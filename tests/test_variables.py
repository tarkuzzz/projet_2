import pytest

from exceptions import DonneeInvalide
from variables import Variable_non_numerique, Variable_numerique


def test_numerique_saisie_valide():
    """Une saisie entière dans l'intervalle est acceptée et convertie en int."""
    grid = Variable_numerique("grid", 24, 1)
    assert grid.verfifier_variable("5") == 5


def test_numerique_bornes_acceptees():
    """Le minimum et le maximum font partie de l'intervalle accepté."""
    grid = Variable_numerique("grid", 24, 1)
    assert grid.verfifier_variable("1") == 1
    assert grid.verfifier_variable("24") == 24


def test_numerique_texte_refuse():
    """Du texte à la place d'un nombre lève DonneeInvalide."""
    grid = Variable_numerique("grid", 24, 1)
    with pytest.raises(DonneeInvalide):
        grid.verfifier_variable("abc")


def test_numerique_hors_intervalle():
    """Une valeur au-dessus du maximum lève DonneeInvalide."""
    grid = Variable_numerique("grid", 24, 1)
    with pytest.raises(DonneeInvalide):
        grid.verfifier_variable("25")


def test_non_numerique_valeur_inconnue():
    """Une écurie qui n'est pas dans la liste lève DonneeInvalide."""
    ecurie = Variable_non_numerique("constructorRef", ["ferrari", "haas", "mercedes"])
    with pytest.raises(DonneeInvalide):
        ecurie.verfifier_variable("minardi")