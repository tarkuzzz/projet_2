from application import Application
from exceptions import ModeleIntrouvable
from interface import lancer


def main() -> None:
    """Charge l'application et ouvre la fenêtre, ou affiche un message clair si le modèle manque."""
    try:
        application = Application()
    except ModeleIntrouvable as erreur:
        print(f"Erreur : {erreur}")
        return
    lancer(application)


if __name__ == "__main__":
    main()