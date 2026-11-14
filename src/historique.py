import csv 
import os 
COLONNES = ["grid", "year", "round", "constructorRef", "circuitRef",
            "country", "prediction", "probabilite"]

def ajouter_historique(entre:dict, prediciton_top10:bool,probabilite_top10:float, chemin_historique:str):

    dict_historique = entre.copy()
    dict_historique['probabilite'] = probabilite_top10

    if prediciton_top10 == True:
        dict_historique['prediction'] = 'fini dans le Top 10'

    else: 
        dict_historique['prediction'] = 'ne fini pas dans le Top 10'


    if os.path.exists(chemin_historique) == False:
        with open(chemin_historique,'w',newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f,fieldnames=COLONNES)
            writer.writeheader()
            writer.writerow(dict_historique)

        

    else:
        with open(chemin_historique,'a',newline='', encoding='utf-8') as f:

            writer = csv.DictWriter(f,fieldnames=COLONNES)
            writer.writerow(dict_historique)



def lire_historique(chemin_historique:str):

    if os.path.exists(chemin_historique) == False:

        return []

    else:

        with open(chemin_historique,'r',newline='', encoding='utf-8') as f:

            reader = csv.DictReader(f)
            historique = list(reader)

        return historique


