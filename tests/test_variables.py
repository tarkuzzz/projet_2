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


@pytest.mark.parametrize("saisie", ["", "abc", "3.5"])
def test_numerique_saisie_pas_un_entier(saisie):
    """Une saisie vide, du texte ou un nombre à virgule lève DonneeInvalide."""
    grid = Variable_numerique("grid", 24, 1)
    with pytest.raises(DonneeInvalide):
        grid.verfifier_variable(saisie)


@pytest.mark.parametrize("saisie", ["0", "25"])
def test_numerique_hors_intervalle(saisie):
    """Une valeur juste en dessous du minimum ou au-dessus du maximum lève DonneeInvalide."""
    grid = Variable_numerique("grid", 24, 1)
    with pytest.raises(DonneeInvalide):
        grid.verfifier_variable(saisie)


def test_non_numerique_saisie_valide():
    """Une valeur de la liste est acceptée, sans les espaces autour."""
    ecurie = Variable_non_numerique("constructorRef", ["ferrari", "haas", "mercedes"])
    assert ecurie.verfifier_variable(" ferrari ") == "ferrari"


@pytest.mark.parametrize("saisie", ["", "12", "minardi"])
def test_non_numerique_saisie_invalide(saisie):
    """Une saisie vide, un nombre ou une valeur hors de la liste lève DonneeInvalide."""
    ecurie = Variable_non_numerique("constructorRef", ["ferrari", "haas", "mercedes"])
    with pytest.raises(DonneeInvalide):
        ecurie.verfifier_variable(saisie)


def test_str_renvoie_le_nom():
    """__str__ renvoie le nom de la variable."""
    assert str(Variable_numerique("grid", 24, 1)) == "grid"