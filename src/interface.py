import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

from application import LIBELLES, Application
from exceptions import DonneeInvalide

# Palette du thème : fond sombre, rouge course, vert et rouge pour le résultat.
COULEURS = {
    "fond": "#0f1117",
    "panneau": "#181b23",
    "champ": "#242833",
    "bordure": "#343a46",
    "texte": "#f1f3f7",
    "discret": "#9aa3b2",
    "accent": "#ff3b30",
    "accent_clair": "#ff6a5f",
    "vert": "#22c55e",
    "rouge": "#ef4444",
}
POLICE = "Helvetica"
LARGEUR = 420  # largeur du panneau de gauche, en pixels

# Les champs, regroupés par thème dans le formulaire.
SECTIONS = [
    ("🏎️  LA VOITURE", ["grid", "constructorRef"]),
    ("🏁  LA COURSE", ["circuitRef", "year", "round"]),
]


class FenetrePrincipale:
    """Fenêtre principale : formulaire, bouton Prédire, résultat, graphique et historique."""

    def __init__(self, racine: tk.Tk, application: Application):
        """Construit la fenêtre à partir des métadonnées de l'application."""
        self.racine = racine
        self.application = application
        self.champs: dict[str, tk.StringVar] = {}

        racine.title("🏁 Prédicteur de top 10 en Formule 1")
        self._appliquer_style()

        formulaire = ttk.Frame(racine, padding=24, style="Carte.TFrame")
        formulaire.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)
        zone_graphique = ttk.Frame(racine, padding=16, style="Carte.TFrame")
        zone_graphique.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=16)

        self._creer_champs(formulaire)
        self._creer_boutons_et_resultat(formulaire)
        self._creer_graphique(zone_graphique)

    def _appliquer_style(self) -> None:
        """Applique un thème sombre et moderne, avec le rouge course comme couleur d'accent."""
        self.racine.configure(background=COULEURS["fond"])
        style = ttk.Style(self.racine)
        style.theme_use("clam")

        style.configure(".", background=COULEURS["panneau"], foreground=COULEURS["texte"],
                        font=(POLICE, 13))
        style.configure("Carte.TFrame", background=COULEURS["panneau"])
        style.configure("TLabel", background=COULEURS["panneau"], foreground=COULEURS["texte"])
        style.configure("Titre.TLabel", font=(POLICE, 20, "bold"), foreground=COULEURS["accent"])
        style.configure("Discret.TLabel", font=(POLICE, 11), foreground=COULEURS["discret"])
        style.configure("Erreur.TLabel", foreground=COULEURS["rouge"])
        style.configure("Section.TLabel", font=(POLICE, 12, "bold"), foreground=COULEURS["accent"])
        style.configure("Resultat.TFrame", background=COULEURS["champ"])
        style.configure("Pourcentage.TLabel", background=COULEURS["champ"], font=(POLICE, 44, "bold"),
                        foreground=COULEURS["discret"])
        style.configure("DansCarte.TLabel", background=COULEURS["champ"], font=(POLICE, 13))
        style.configure("Badge.TLabel", background=COULEURS["accent"], foreground="white",
                        font=(POLICE, 11, "bold"), padding=(10, 4))
        style.configure("BadgeDiscret.TLabel", background=COULEURS["champ"], foreground=COULEURS["discret"],
                        font=(POLICE, 11, "bold"), padding=(10, 4))

        style.configure("TEntry", fieldbackground=COULEURS["champ"], foreground=COULEURS["texte"],
                        insertcolor=COULEURS["texte"], bordercolor=COULEURS["bordure"],
                        lightcolor=COULEURS["bordure"], darkcolor=COULEURS["bordure"], padding=6)
        style.configure("TCombobox", fieldbackground=COULEURS["champ"], background=COULEURS["champ"],
                        foreground=COULEURS["texte"], arrowcolor=COULEURS["texte"],
                        bordercolor=COULEURS["bordure"], lightcolor=COULEURS["bordure"],
                        darkcolor=COULEURS["bordure"], padding=6)
        style.map("TCombobox",
                  fieldbackground=[("readonly", COULEURS["champ"])],
                  foreground=[("readonly", COULEURS["texte"])],
                  selectbackground=[("readonly", COULEURS["champ"])],
                  selectforeground=[("readonly", COULEURS["texte"])])
        self.racine.option_add("*TCombobox*Listbox.background", COULEURS["champ"])
        self.racine.option_add("*TCombobox*Listbox.foreground", COULEURS["texte"])
        self.racine.option_add("*TCombobox*Listbox.selectBackground", COULEURS["accent"])

        style.configure("Accent.TButton", background=COULEURS["accent"], foreground="white",
                        font=(POLICE, 13, "bold"), borderwidth=0, padding=(18, 8))
        style.map("Accent.TButton", background=[("active", COULEURS["accent_clair"])])
        style.configure("Secondaire.TButton", background=COULEURS["champ"], foreground=COULEURS["texte"],
                        borderwidth=0, padding=(18, 8))
        style.map("Secondaire.TButton", background=[("active", COULEURS["bordure"])])

        style.configure("Treeview", background=COULEURS["panneau"], fieldbackground=COULEURS["panneau"],
                        foreground=COULEURS["texte"], rowheight=26, borderwidth=0)
        style.configure("Treeview.Heading", background=COULEURS["champ"], foreground=COULEURS["texte"],
                        font=(POLICE, 12, "bold"))
        style.map("Treeview", background=[("selected", COULEURS["accent"])])

    def _dessiner_damier(self, cadre: ttk.Frame) -> None:
        """Dessine une bande en damier, comme un drapeau d'arrivée, en haut du panneau."""
        taille = 8
        damier = tk.Canvas(cadre, width=LARGEUR, height=2 * taille, background=COULEURS["panneau"],
                           highlightthickness=0)
        for colonne in range(LARGEUR // taille):
            for rangee in range(2):
                couleur = "white" if (colonne + rangee) % 2 == 0 else "black"
                damier.create_rectangle(colonne * taille, rangee * taille, (colonne + 1) * taille,
                                        (rangee + 1) * taille, fill=couleur, outline="")
        damier.grid(row=0, column=0, columnspan=2, sticky="w")

    def _creer_champs(self, cadre: ttk.Frame) -> None:
        """Crée l'en-tête, puis les champs regroupés en deux sections : la voiture et la course."""
        self._dessiner_damier(cadre)
        ttk.Label(cadre, text="Prédicteur de top 10", style="Titre.TLabel").grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(14, 0))
        ttk.Label(cadre, text="Décrivez une voiture sur la grille de départ : le modèle estime "
                              "ses chances de finir dans le top 10 et de marquer des points.",
                  style="Discret.TLabel", wraplength=LARGEUR).grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(4, 8))

        numeriques = self.application.metadonnees["numeriques"]
        categorielles = self.application.metadonnees["categorielles"]
        ligne = 3
        for titre, noms in SECTIONS:
            ttk.Label(cadre, text=titre, style="Section.TLabel").grid(
                row=ligne, column=0, columnspan=2, sticky="w", pady=(14, 6))
            ligne += 1
            for nom in noms:
                self.champs[nom] = tk.StringVar()
                if nom in numeriques:
                    intervalle = numeriques[nom]
                    texte = f"{LIBELLES[nom]} ({intervalle['min']} à {intervalle['max']})"
                    champ = ttk.Entry(cadre, textvariable=self.champs[nom], width=24)
                else:
                    texte = LIBELLES[nom]
                    champ = ttk.Combobox(cadre, textvariable=self.champs[nom], values=categorielles[nom],
                                         state="readonly", width=22)
                ttk.Label(cadre, text=texte).grid(row=ligne, column=0, sticky="w", pady=5)
                champ.grid(row=ligne, column=1, sticky="e", pady=5, padx=(16, 0))
                ligne += 1

        self._ligne_suivante = ligne

    def _creer_boutons_et_resultat(self, cadre: ttk.Frame) -> None:
        """Crée les boutons, la carte du résultat, le message d'erreur et les scores du modèle."""
        ligne = self._ligne_suivante
        boutons = ttk.Frame(cadre, style="Carte.TFrame")
        boutons.grid(row=ligne, column=0, columnspan=2, sticky="w", pady=(20, 16))
        ttk.Button(boutons, text="🏁 Prédire", style="Accent.TButton",
                   command=self.predire).pack(side="left")
        ttk.Button(boutons, text="📋 Historique", style="Secondaire.TButton",
                   command=self.ouvrir_historique).pack(side="left", padx=10)

        carte = ttk.Frame(cadre, style="Resultat.TFrame", padding=16)
        carte.grid(row=ligne + 1, column=0, columnspan=2, sticky="ew")
        self.pourcentage = tk.StringVar(value="– %")
        self.label_pourcentage = ttk.Label(carte, textvariable=self.pourcentage, style="Pourcentage.TLabel")
        self.label_pourcentage.pack(anchor="w")
        self.resultat = tk.StringVar(value="Remplissez les champs, puis cliquez sur « Prédire ».")
        ttk.Label(carte, textvariable=self.resultat, style="DansCarte.TLabel",
                  wraplength=LARGEUR - 32).pack(anchor="w")

        self.erreur = tk.StringVar()
        ttk.Label(cadre, textvariable=self.erreur, style="Erreur.TLabel", wraplength=LARGEUR).grid(
            row=ligne + 2, column=0, columnspan=2, sticky="w", pady=(8, 0))

        resultats = self.application.metadonnees["resultats"]
        badges = ttk.Frame(cadre, style="Carte.TFrame")
        badges.grid(row=ligne + 3, column=0, columnspan=2, sticky="w", pady=(16, 4))
        ttk.Label(badges, text=f"Notre modèle : {resultats['exactitude']:.0%}",
                  style="Badge.TLabel").pack(side="left")
        ttk.Label(badges, text=f"Référence : {resultats['exactitude_reference']:.0%}",
                  style="BadgeDiscret.TLabel").pack(side="left", padx=8)
        ttk.Label(cadre, text="de bonnes réponses sur des courses que le modèle n'avait jamais vues "
                              "(la référence répond toujours « hors top 10 »).",
                  style="Discret.TLabel", wraplength=LARGEUR).grid(
            row=ligne + 4, column=0, columnspan=2, sticky="w")

    def _creer_graphique(self, cadre: ttk.Frame) -> None:
        """Intègre une figure Matplotlib : matrice de confusion et probabilité de la prédiction."""
        self.figure = Figure(figsize=(5.5, 6), dpi=100, facecolor=COULEURS["panneau"])
        self.axe_matrice = self.figure.add_subplot(2, 1, 1)
        self.axe_probabilite = self.figure.add_subplot(2, 1, 2)

        self._dessiner_matrice()
        self._dessiner_probabilite(None)
        self.figure.tight_layout()

        self.toile = FigureCanvasTkAgg(self.figure, master=cadre)
        widget = self.toile.get_tk_widget()
        widget.configure(background=COULEURS["panneau"], highlightthickness=0)
        widget.pack()

    @staticmethod
    def _styliser_axe(axe) -> None:
        """Applique les couleurs du thème sombre à un graphique Matplotlib."""
        axe.set_facecolor(COULEURS["champ"])
        axe.tick_params(colors=COULEURS["texte"])
        axe.xaxis.label.set_color(COULEURS["texte"])
        axe.yaxis.label.set_color(COULEURS["texte"])
        axe.title.set_color(COULEURS["texte"])
        for bord in axe.spines.values():
            bord.set_color(COULEURS["bordure"])

    def _dessiner_matrice(self) -> None:
        """Dessine la matrice de confusion du modèle sur les données de test."""
        matrice = self.application.metadonnees["resultats"]["matrice_confusion"]
        axe = self.axe_matrice
        degrade = LinearSegmentedColormap.from_list("course", [COULEURS["champ"], COULEURS["accent"]])
        axe.imshow(matrice, cmap=degrade)
        for i in range(2):
            for j in range(2):
                axe.text(j, i, matrice[i][j], ha="center", va="center", fontsize=13,
                         fontweight="bold", color="white")
        axe.set_xticks([0, 1], labels=["Hors top 10", "Top 10"])
        axe.set_yticks([0, 1], labels=["Hors top 10", "Top 10"])
        axe.set_xlabel("Prédiction du modèle")
        axe.set_ylabel("Résultat réel")
        axe.set_title("Matrice de confusion (données de test)", fontweight="bold")
        self._styliser_axe(axe)

    def _dessiner_probabilite(self, probabilite: float | None) -> None:
        """Dessine une jauge de 0 à 100 % avec la probabilité de la dernière prédiction."""
        axe = self.axe_probabilite
        axe.clear()
        axe.set_xlim(0, 100)
        axe.set_ylim(-1, 1)
        axe.set_yticks([])
        for i, y in enumerate((-1, -0.5, 0, 0.5)):
            for j, x in enumerate((48, 50)):
                couleur_case = "black" if (i + j) % 2 == 0 else "white"
                axe.add_patch(Rectangle((x, y), 2, 0.5, facecolor=couleur_case,
                                        edgecolor="black", zorder=3))
        axe.plot([], [], color="white", linewidth=6, label="Ligne d'arrivée : seuil de 50 %")
        if probabilite is not None:
            couleur = COULEURS["vert"] if probabilite >= 0.5 else COULEURS["rouge"]
            axe.barh([0], [probabilite * 100], height=0.6, color=couleur, label="Probabilité prédite")
        axe.set_title("Probabilité de finir dans le top 10", fontweight="bold")
        axe.set_xlabel("Probabilité (%)")
        axe.legend(loc="lower right", fontsize=8, facecolor=COULEURS["panneau"],
                   edgecolor=COULEURS["bordure"], labelcolor=COULEURS["texte"])
        self._styliser_axe(axe)

    def predire(self) -> None:
        """Appelé par le bouton Prédire : envoie les saisies à l'application et affiche le résultat."""
        saisies = {nom: valeur.get() for nom, valeur in self.champs.items()}
        try:
            resultat = self.application.predire(saisies)
        except DonneeInvalide as erreur:
            self.erreur.set(str(erreur))
            self.resultat.set("Corrigez le champ indiqué, puis cliquez à nouveau sur « Prédire ».")
            self.pourcentage.set("– %")
            self.label_pourcentage.configure(foreground=COULEURS["discret"])
            self._dessiner_probabilite(None)
            self.toile.draw()
            return
        self.erreur.set("")
        self.resultat.set(resultat["message"])
        couleur = COULEURS["vert"] if resultat["top10"] else COULEURS["rouge"]
        self.pourcentage.set(f"{resultat['probabilite']:.0%}")
        self.label_pourcentage.configure(foreground=couleur)
        self._dessiner_probabilite(resultat["probabilite"])
        self.toile.draw()

    def ouvrir_historique(self) -> None:
        """Ouvre une fenêtre avec toutes les prédictions enregistrées."""
        lignes = self.application.lire_historique()
        fenetre = tk.Toplevel(self.racine)
        fenetre.title("📋 Historique des prédictions")
        fenetre.configure(background=COULEURS["panneau"])
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
        tableau.pack(fill="both", expand=True, padx=12, pady=12)


def lancer(application: Application) -> None:
    """Ouvre la fenêtre principale et attend les actions de l'utilisateur."""
    racine = tk.Tk()
    FenetrePrincipale(racine, application)
    racine.mainloop()