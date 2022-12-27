import pandas as pd
import numpy as np 
import webbrowser 

titre = input("Quel titre ?\n")

def trouver_titre(titre) :
    tmp = pd.read_csv('data\\title.basics.tsv', sep='\t', low_memory=False)
#on selectionne que les séries TV et on enllève les colonnes inutiles  
    serie = tmp[tmp['titleType'] == 'tvSeries'].drop(['isAdult', 'endYear', 'runtimeMinutes', 'genres'], axis=1)
#avoir le ou LES index correspondant au titre. Le [0] permet d'accéder à la premièere valeur, il faudra donc fiare une verrification que c'est bien celui demandé par l'utilisateur.
    index = serie[serie['primaryTitle'] == titre].index[0]
#récupère toutes les infos sur le titre sélectionné. infos[0] correspont au code tconst
    infos = serie.loc[index]
    return infos[0]

def trouver_episodes(tconst_serie):
    tab_ep = pd.read_csv('data\\title.episode.tsv', sep='\t')
    episodes = tab_ep[tab_ep['parentTconst']== tconst_serie]
    #index_ep = episodes.index
    return episodes

def trier_episodes(episodes):
    episodes_tries = {}
    for ep in episodes['tconst'] :
        index_ep = episodes[episodes['tconst'] == ep].index[0]
        episodes_tries[ep] = [int(episodes['episodeNumber'][index_ep]),int(episodes['seasonNumber'][index_ep])]
    return episodes_tries
trouver_episode = trouver_episodes('tt0898266')
episodes_tries = trier_episodes(trouver_episode) #The Big Bang Theory

def nombre(episodes_tries,i):
    nbr = []
    for ep in episodes_tries :
        nbr.append(episodes_tries[ep][i])
    return len(set(nbr))

def notes(episodes_tries):
    tab_notes = pd.read_csv('data\\title.ratings.tsv', sep='\t')
    notes=[[] for _ in range(nombre(episodes_tries,1))]
    for tconst_ep in episodes_tries :
        saison = episodes_tries[tconst_ep][1]
        numero = episodes_tries[tconst_ep][0]
        index_note = tab_notes[tab_notes['tconst'] == tconst_ep].index
        if str(index_note) == "Int64Index([], dtype='int64')" :
            note = 'Na'
        else: 
            note = float(tab_notes['averageRating'].loc[index_note].values)
        notes[saison-1].append(note)
    return notes

code_vide = ['<!DOCTYPE html>\n', '<html lang="fr">\n', '<head>\n', '    <meta charset="UTF-8">\n', '    <meta name="viewport" content="width=device-width, initial-scale=1" />\n', '    <title>Titre</title>\n', '    <link rel="stylesheet" href="rendu.css">\n', '</head>\n', '<body> \n', '\n', '<table class="table-style">\n', '    <thead>\n', '        <tr>\n', '            <th>Saison X</th>\n', '        </tr>\n', '    </thead>\n', '    <tbody>\n', '        <tr>\n', '            <td>Note</td>\n', '        </tr>\n', '        \n', '        </tr>\n', '    </tbody>\n', '</table></body></html>']

def ecrire_html(code_vide,notes,nom_fichier):
    with open(nom_fichier +".html", 'w') as f:
        f.writelines(code_vide[:13])
        f.write( '            <th>Episodes\Saisons</th>\n')
        for j in range(len(notes)) :
            f.write( '            <th>'+str(j+1)+'</th>\n')
        f.writelines(code_vide[15:17])
        taille_max = max(len(notes[i]) for i in range(len(notes)))
        for k in range(taille_max) :
            f.write('        <tr>\n')
            debut=True
            for j in range(len(notes)) :
                if debut :
                    f.write('            <td>'+str(k+1)+'</td>\n')
                    debut = False
                try :
                    f.write('            <td>'+str(notes[j][k])+'</td>\n')
                except IndexError :
                    f.write('            <td></td>\n')
            f.write('        </tr>\n')
        f.writelines(code_vide[22:])


page = "affichage_test2"
ecrire_html(code_vide,notes(trier_episodes(trouver_episodes(trouver_titre(titre)))),page )
webbrowser.open_new_tab(page+".html")