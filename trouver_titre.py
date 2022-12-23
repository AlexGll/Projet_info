import pandas as pd
import numpy as np 
import matplotlib as plt

tmp = pd.read_csv('data\\title.basics.tsv', sep='\t', low_memory=False)
#on selectionne que les séries TV et on enllève les colonnes inutiles  
serie = tmp[tmp['titleType'] == 'tvSeries'].drop(['isAdult','startYear', 'endYear', 'runtimeMinutes', 'genres'], axis=1)
titre = input("Quel titre ?\n")
#avoir le ou LES index correspondant au titre. Le [0] permet d'accéder à la premièere valeur, il faudra donc fiare une verrification que c'est bien celui demandé par l'utilisateur.
index = serie[serie['primaryTitle'] == titre].index[0]
#récupère toutes les infos sur le titre sélectionné. infos[0] correspont au code tconst
infos = serie.loc[index]
print(infos[0])