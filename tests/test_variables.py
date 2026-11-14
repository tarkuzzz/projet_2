from variables import Variable_general,Variable_non_numerique,Variable_numerique
from exceptions import DonneeInvalide
import pytest

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
    
        


    

   

