import pandas as pd
import numpy as np 

titre = input("Quel titre ?\n")

def trouver_titre(titre) :
    tmp = pd.read_csv('data\\title.basics.tsv', sep='\t', low_memory=False)
#on selectionne que les séries TV et on enllève les colonnes inutiles  
    serie = tmp[tmp['titleType'] == 'tvSeries'].drop(['isAdult', 'endYear', 'runtimeMinutes', 'genres'], axis=1)
#avoir le ou LES index correspondant au titre. Le [0] permet d'accéder à la premièere valeur, il faudra donc fiare une verrification que c'est bien celui demandé par l'utilisateur.
    index = serie[serie['primaryTitle'] == titre].index[0]
#récupère toutes les infos sur le titre sélectionné. infos[0] correspont au code tconst
    infos = serie.loc[index].values('tconst')
    return infos

def trouver_titre(titre) :
    tmp = pd.read_csv('Desktop/title.basics.tsv', sep='\t', low_memory=False)
#on selectionne que les séries TV et on enllève les colonnes inutiles  
    serie = tmp[tmp['titleType'] == 'tvSeries'].drop(['isAdult', 'endYear', 'runtimeMinutes', 'genres'], axis=1)
#avoir le ou LES index correspondant au titre. Le [0] permet d'accéder à la premièere valeur, il faudra donc fiare une verrification que c'est bien celui demandé par l'utilisateur.
    index = serie[serie['primaryTitle'] == titre].index
    infos = serie.loc[index]   
#récupère toutes les infos sur le titre sélectionné. infos[0] correspont au code tconst
    if len(index) != 1: 
       date = input("Quelle est la date du début de la série?\n")
       for i in range(len(index)):
        if int(date) == int(infos.iloc[i,4]):
            infos = infos.loc[infos.index[i]]
            break
    return infos[0]

tconst_serie = trouver_titre(titre)

print(tconst_serie)
