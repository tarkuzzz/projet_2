from donnees import creation_donnees, nettoyage_donnees
from sklearn.model_selection import train_test_split


if __name__ == "__main__":
    df = creation_donnees()
    df = nettoyage_donnees(df)
    X=df[["grid","year","round","constructorRef","circuitRef"]]
    y=df["top10"]
    print(df.head())
    print(X)
    print(y)

X_train, X_test, y_train, y_test = train_test_split(X , y, random_state=0, test_size=0.2)

print("----")
print(len(X_train))
print(len(X_test))
print(len(y_train))
print(len(y_test))