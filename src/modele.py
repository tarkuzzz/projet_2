from donnees import creation_donnees, nettoyage_donnees


if __name__ == "__main__":
    df = creation_donnees()
    df = nettoyage_donnees(df)
    print(df.head())