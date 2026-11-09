from abc import ABC, abstractmethod
from exceptions import DonneeInvalide



class Variable_general(ABC):

    def __init__(self,nom:str):
        self._nom = nom

    def __str__(self):
        return self._nom

    @abstractmethod
    def verfifier_variable(self,input_utilisateur:str):
        pass

    

class Variable_numerique(Variable_general):

    def __init__(self, nom:str,maximum:int,minimum:int):
        super().__init__(nom)
        self._maximum = maximum 
        self._minimum = minimum

    

    def verfifier_variable(self,input_utilisateur:str):
        
        try:
            valeur = int(input_utilisateur)

        except ValueError:

            raise DonneeInvalide("mettre un nombre entier")

    

        if valeur > self._maximum or valeur < self._minimum:
            raise DonneeInvalide(f"mettre une donnée comprise dans l'intervalle {self._minimum} et {self._maximum} ")
            
        else:
            self._valeur = valeur 
            return self._valeur


class Variable_non_numerique(Variable_general):

    def __init__(self, nom:str,liste_mot_possible:list):
        super().__init__(nom)
        self._liste_nom_possible =  liste_mot_possible

    

    def verfifier_variable(self,input_utilisateur:str):

        mot = input_utilisateur.strip()

        if mot == '':

            raise DonneeInvalide('entrez un mot')
        elif mot.isdigit() == True:

            raise DonneeInvalide('entrez un mot')

        elif mot not in self._liste_nom_possible:

            raise DonneeInvalide('entrez un mot de la liste')
        else:
            self._mot = mot
            return self._mot 


    
        


