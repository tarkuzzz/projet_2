from donnees import creation_donnees, nettoyage_donnees


if __name__ == "__main__":
    df = creation_donnees()
    df = nettoyage_donnees(df)
    X=df[["grid","year","round","constructorRef","circuitRef"]]
    y=df["top10"]
    print(df.head())
    print(X)
    print(y)

