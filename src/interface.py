import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from application import LIBELLES, Application
from exceptions import DonneeInvalide

class FenetrePrincipale:
    """Fenêtre principale : formulaire, bouton Prédire, résultat, graphique et historique."""

    def __init__(self, racine: tk.Tk, application: Application):
        """Construit la fenêtre à partir des métadonnées de l'application."""
        self.racine = racine
        self.application = application
        self.champs: dict[str, tk.StringVar] = {}

        racine.title("Prédicteur de top 10 en Formule 1")

        formulaire = ttk.Frame(racine, padding=16)
        formulaire.grid(row=0, column=0, sticky="n")
        zone_graphique = ttk.Frame(racine, padding=16)
        zone_graphique.grid(row=0, column=1)

        self._creer_champs(formulaire)
        self._creer_boutons_et_resultat(formulaire)
        self._creer_graphique(zone_graphique)

    def _creer_champs(self, cadre: ttk.Frame) -> None:
        """Crée un champ texte par variable numérique et une liste déroulante par variable texte."""
        ttk.Label(cadre, text="Décrivez la voiture au départ", font=("", 14, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        ligne = 1
        for nom, intervalle in self.application.metadonnees["numeriques"].items():
            texte = f"{LIBELLES[nom]} ({intervalle['min']} à {intervalle['max']})"
            ttk.Label(cadre, text=texte).grid(row=ligne, column=0, sticky="w", pady=4)
            self.champs[nom] = tk.StringVar()
            ttk.Entry(cadre, textvariable=self.champs[nom], width=22).grid(
                row=ligne, column=1, pady=4, padx=(8, 0))
            ligne += 1

        for nom, valeurs in self.application.metadonnees["categorielles"].items():
            ttk.Label(cadre, text=LIBELLES[nom]).grid(row=ligne, column=0, sticky="w", pady=4)
            self.champs[nom] = tk.StringVar()
            ttk.Combobox(cadre, textvariable=self.champs[nom], values=valeurs,
                         state="readonly", width=20).grid(row=ligne, column=1, pady=4, padx=(8, 0))
            ligne += 1

        self._ligne_suivante = ligne

    def _creer_boutons_et_resultat(self, cadre: ttk.Frame) -> None:
        """Crée les boutons Prédire et Historique, la zone de résultat et le message d'erreur."""
        ligne = self._ligne_suivante
        boutons = ttk.Frame(cadre)
        boutons.grid(row=ligne, column=0, columnspan=2, sticky="w", pady=12)
        ttk.Button(boutons, text="Prédire", command=self.predire).pack(side="left")
        ttk.Button(boutons, text="Historique", command=self.ouvrir_historique).pack(side="left", padx=8)

        self.resultat = tk.StringVar(value="Remplissez les champs, puis cliquez sur « Prédire ».")
        ttk.Label(cadre, textvariable=self.resultat, wraplength=320, font=("", 12)).grid(
            row=ligne + 1, column=0, columnspan=2, sticky="w")

        self.erreur = tk.StringVar()
        ttk.Label(cadre, textvariable=self.erreur, foreground="red", wraplength=320).grid(
            row=ligne + 2, column=0, columnspan=2, sticky="w", pady=(8, 0))

        resultats = self.application.metadonnees["resultats"]
        fiabilite = (f"Fiabilité du modèle : {resultats['exactitude']:.0%} de bonnes réponses "
                     f"sur des courses jamais vues (contre {resultats['exactitude_reference']:.0%} "
                     "en répondant toujours « hors top 10 »).")
        ttk.Label(cadre, text=fiabilite, wraplength=320, foreground="gray").grid(
            row=ligne + 3, column=0, columnspan=2, sticky="w", pady=(16, 0))

    def _creer_graphique(self, cadre: ttk.Frame) -> None:
        """Intègre une figure Matplotlib : matrice de confusion et probabilité de la prédiction."""
        self.figure = Figure(figsize=(5.5, 6), dpi=100)
        self.axe_matrice = self.figure.add_subplot(2, 1, 1)
        self.axe_probabilite = self.figure.add_subplot(2, 1, 2)

        self._dessiner_matrice()
        self._dessiner_probabilite(None)
        self.figure.tight_layout()

        self.toile = FigureCanvasTkAgg(self.figure, master=cadre)
        self.toile.get_tk_widget().pack()

    def _dessiner_matrice(self) -> None:
        """Dessine la matrice de confusion du modèle sur les données de test."""
        matrice = self.application.metadonnees["resultats"]["matrice_confusion"]
        axe = self.axe_matrice
        axe.imshow(matrice, cmap="Blues")
        plus_grand = max(max(ligne) for ligne in matrice)
        for i in range(2):
            for j in range(2):
                couleur = "white" if matrice[i][j] > plus_grand / 2 else "black"
                axe.text(j, i, matrice[i][j], ha="center", va="center", fontsize=12, color=couleur)
        axe.set_xticks([0, 1], labels=["Hors top 10", "Top 10"])
        axe.set_yticks([0, 1], labels=["Hors top 10", "Top 10"])
        axe.set_xlabel("Prédiction du modèle")
        axe.set_ylabel("Résultat réel")
        axe.set_title("Matrice de confusion (données de test)")

    def _dessiner_probabilite(self, probabilite: float | None) -> None:
        """Dessine une jauge de 0 à 100 % avec la probabilité de la dernière prédiction."""
        axe = self.axe_probabilite
        axe.clear()
        axe.set_xlim(0, 100)
        axe.set_ylim(-1, 1)
        axe.set_yticks([])
        axe.axvline(50, color="gray", linestyle="--", label="Seuil de décision (50 %)")
        if probabilite is not None:
            couleur = "green" if probabilite >= 0.5 else "red"
            axe.barh([0], [probabilite * 100], height=0.6, color=couleur, label="Probabilité prédite")
        axe.set_title("Probabilité de finir dans le top 10")
        axe.set_xlabel("Probabilité (%)")
        axe.legend(loc="lower right", fontsize=8)

    def predire(self) -> None:
        """Appelé par le bouton Prédire : envoie les saisies à l'application et affiche le résultat."""
        saisies = {nom: valeur.get() for nom, valeur in self.champs.items()}
        try:
            resultat = self.application.predire(saisies)
        except DonneeInvalide as erreur:
            self.erreur.set(str(erreur))
            return
        self.erreur.set("")
        self.resultat.set(resultat["message"])
        self._dessiner_probabilite(resultat["probabilite"])
        self.toile.draw()

    def ouvrir_historique(self) -> None:
        """Ouvre une fenêtre avec toutes les prédictions enregistrées."""
        lignes = self.application.lire_historique()
        fenetre = tk.Toplevel(self.racine)
        fenetre.title("Historique des prédictions")
        if not lignes:
            ttk.Label(fenetre, text="Aucune prédiction pour l'instant.", padding=16).pack()
            return
        colonnes = ["grid", "year", "round", "constructorRef", "circuitRef", "prediction", "probabilite"]
        tableau = ttk.Treeview(fenetre, columns=colonnes, show="headings", height=15)
        for colonne in colonnes:
            tableau.heading(colonne, text=LIBELLES.get(colonne, colonne.capitalize()))
            tableau.column(colonne, width=130)
        for ligne in lignes:
            tableau.insert("", "end", values=[ligne.get(colonne, "") for colonne in colonnes])
        tableau.pack(fill="both", expand=True, padx=8, pady=8)

def lancer(application: Application) -> None:
    """Ouvre la fenêtre principale et attend les actions de l'utilisateur."""
    racine = tk.Tk()
    FenetrePrincipale(racine, application)
    racine.mainloop()