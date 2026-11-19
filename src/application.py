import pandas as pd

from exceptions import DonneeInvalide
from modele import charger_modele
from variables import Variable_non_numerique, Variable_numerique
from historique import ajouter_historique, lire_historique
import os

LIBELLES = {
    "grid": "Position de départ",
    "year": "Saison",
    "round": "Numéro de la course",
    "constructorRef": "Écurie",
    "circuitRef": "Circuit",
}

class Application:
    """Réunit le modèle, les variables d'entrée et l'historique des prédictions."""

    def __init__(self, dossier: str = "modeles",chemin_historique: str = os.path.join("modeles", "historique.csv")):
        """Charge le modèle sauvegardé et crée une variable par colonne d'entrée."""
        self._modele, self.metadonnees = charger_modele(dossier)
        self._chemin_historique = chemin_historique
        self.variables = []
        for nom, intervalle in self.metadonnees["numeriques"].items():
            self.variables.append(Variable_numerique(nom, intervalle["max"], intervalle["min"]))
        for nom, valeurs in self.metadonnees["categorielles"].items():
            self.variables.append(Variable_non_numerique(nom, valeurs))

    def valider(self, saisies: dict[str, str]) -> dict:
        """Vérifie chaque saisie avec sa variable et renvoie les valeurs converties."""
        valeurs = {}
        for variable in self.variables:
            nom = str(variable)
            try:
                valeurs[nom] = variable.verfifier_variable(saisies.get(nom, ""))
            except DonneeInvalide as erreur:
                raise DonneeInvalide(f"{LIBELLES[nom]} : {erreur}") from erreur
        return valeurs

    def predire(self, saisies: dict[str, str]) -> dict:
        """Valide les saisies, prédit le résultat et l'ajoute à l'historique."""
        valeurs = self.valider(saisies)
        ligne = pd.DataFrame([valeurs])
        probabilites = self._modele.predict_proba(ligne)[0]
        classes = list(self._modele.classes_)
        probabilite = float(probabilites[classes.index(True)])
        top10 = probabilite >= 0.5

        if top10:
            message = f"Cette voiture devrait finir dans le top 10 : {probabilite:.0%} de chances."
        else:
            message = f"Cette voiture devrait finir hors du top 10 : {probabilite:.0%} de chances d'y entrer."

        ajouter_historique(valeurs, top10, round(probabilite, 3), self._chemin_historique)
        return {"top10": top10, "probabilite": probabilite, "message": message}

    def lire_historique(self) -> list[dict]:
        """Renvoie les prédictions enregistrées, de la plus récente à la plus ancienne."""
        return lire_historique(self._chemin_historique)[::-1]

    def __str__(self) -> str:
        """Résumé lisible de l'application et du score du modèle."""
        exactitude = self.metadonnees["resultats"]["exactitude"]
        return f"Application F1 : {len(self.variables)} variables, modèle à {exactitude:.1%} d'exactitude"

if __name__ == "__main__":
    application = Application()
    print(application)
    print(application.predire({"grid": "1", "year": "2023", "round": "5",
                               "constructorRef": "red_bull", "circuitRef": "monaco"}))
    try:
        application.predire({"grid": "abc", "year": "2023", "round": "5",
                             "constructorRef": "red_bull", "circuitRef": "monaco"})
    except DonneeInvalide as erreur:
        print("Erreur attendue :", erreur)
    print(application.lire_historique())