from abc import ABC, abstractmethod
from exceptions import DonneeInvalide



class Variable_general(ABC):
    """Classe parente abstraite : une variable que l'utilisateur doit saisir dans l'interface."""

    def __init__(self,nom:str):
        """Reçoit le nom de la variable (ex. "grid")."""
        self._nom = nom

    def __str__(self)-> str:
        """Renvoie le nom de la variable."""
        return self._nom

    @abstractmethod
    def verfifier_variable(self,input_utilisateur:str)-> int | str:
        """Vérifie la saisie et la renvoie convertie ; lève DonneeInvalide si elle est invalide."""
        pass

    

class Variable_numerique(Variable_general):
    """Une variable entière comprise entre un minimum et un maximum (ex. la position de départ)."""

    def __init__(self, nom:str,maximum:int,minimum:int):
        """Reçoit le nom de la variable, puis son maximum et son minimum (dans cet ordre)."""
        super().__init__(nom)
        self._maximum = maximum 
        self._minimum = minimum

    

    def verfifier_variable(self,input_utilisateur:str)-> int:
        """Vérifie que la saisie est un entier dans l'intervalle accepté.

        Reçoit : le texte saisi par l'utilisateur.
        Renvoie : la saisie convertie en entier.
        Échoue : DonneeInvalide si la saisie n'est pas un entier ou est hors de l'intervalle.
        """
        
        
        try:
            valeur = int(input_utilisateur)

        except ValueError:

            raise DonneeInvalide("mettre un nombre entier")

    

        if valeur > self._maximum or valeur < self._minimum:
            raise DonneeInvalide(f"mettre une donnée comprise entre {self._minimum} et {self._maximum} ")
            
        else:
            self._valeur = valeur 
            return self._valeur


class Variable_non_numerique(Variable_general):
    """Une variable texte qui doit faire partie d'une liste de valeurs (ex. l'écurie)."""

    def __init__(self, nom:str,liste_mot_possible:list):
        """Reçoit le nom de la variable et la liste des valeurs acceptées."""
        super().__init__(nom)
        self._liste_nom_possible =  liste_mot_possible

    

    def verfifier_variable(self,input_utilisateur:str)-> str:
        """Vérifie que la saisie fait partie de la liste des valeurs acceptées.

        Reçoit : le texte saisi par l'utilisateur.
        Renvoie : la saisie, sans les espaces au début et à la fin.
        Échoue : DonneeInvalide si la saisie est vide, est un nombre, ou n'est pas dans la liste.
        """
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


    
        


