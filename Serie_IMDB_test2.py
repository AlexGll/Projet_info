import pandas as pd
import numpy as np 


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

episodes_tries = trier_episodes(trouver_episodes('tt0050013'))

def nombre(episodes_tries,i):
    nbr = []
    for ep in episodes_tries :
        nbr.append(episodes_tries[ep][i])
    return len(set(nbr))

def notes(episodes_tries):
    tab_notes = pd.read_csv('Desktop/title.ratings.tsv', sep='\t')
    notes=[[] for _ in range(nombre(episodes_tries,1))]
    for tconst_ep in episodes_tries :
        saison = episodes_tries[tconst_ep][1]
        numero = episodes_tries[tconst_ep][0]
        index_note = tab_notes[tab_notes['xtconst'] == tconst_ep].index
        if index_note== ([],'int64') :
            note= 'Na'
        else: note =tab_notes['averageRating'].loc[index_note]
        notes[saison-1].append(note)
    return notes

print(notes(episodes_tries))
