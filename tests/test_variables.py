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


def test_variable_numerique():

    variable_test = Variable_numerique('test',26,1)
    assert variable_test.verfifier_variable('11') == 11
    assert variable_test.verfifier_variable('26') == 26
    assert variable_test.verfifier_variable('1')  == 1
    


    with pytest.raises(DonneeInvalide):
        variable_test.verfifier_variable('x')
    with pytest.raises(DonneeInvalide):
        variable_test.verfifier_variable('-1')
    with pytest.raises(DonneeInvalide):
        variable_test.verfifier_variable('0.4')
    with pytest.raises(DonneeInvalide):
        variable_test.verfifier_variable('0')
    with pytest.raises(DonneeInvalide):
        variable_test.verfifier_variable('27')



def test_variable_non_numerique():
    mot_possible_test = ['ferrari', 'mclaren', 'mercedes', 'red_bull', 'williams']

    variable_test = Variable_non_numerique('test',mot_possible_test)
    assert variable_test.verfifier_variable('ferrari') == 'ferrari'
    assert variable_test.verfifier_variable('mercedes') == 'mercedes'
    assert variable_test.verfifier_variable('mclaren') == 'mclaren'
    assert variable_test.verfifier_variable('red_bull') == 'red_bull'
    assert variable_test.verfifier_variable('williams') == 'williams'


    with pytest.raises(DonneeInvalide):
        variable_test.verfifier_variable('')
    with pytest.raises(DonneeInvalide):
        variable_test.verfifier_variable('7')
    with pytest.raises(DonneeInvalide):
        variable_test.verfifier_variable('   ')
    with pytest.raises(DonneeInvalide):
        variable_test.verfifier_variable('testttttt')
    
        


    

   

