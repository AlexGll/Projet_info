import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) #Pandas renvoie une erreur préventive pour ses prochaines versions, qui ne modifie donc pas le résultat obtenu.
import pandas as pd
import numpy as np 
import webbrowser 

def main():
    titre = input("Quel est le titre de la série dont vous souhaitez les notes IMDB ?\n") 
    page = "affichage_notes_"+str(titre)
#Le résultat final état affiché sur une page HTML, nous avons fait en sorte de coder ce fichier .html depuis notre programme Python. 
    code_vide = ['<!DOCTYPE html>\n', '<html lang="fr">\n', '<head>\n', '    <meta charset="UTF-8">\n', '    <meta name="viewport" content="width=device-width, initial-scale=1" />\n', '    <title>Notes IMDB \t Karl LIEBEL et Alexandre GILLES</title>\n', '    <link rel="stylesheet" href="rendu.css">\n', '</head>\n', '<body> \n', '\n', '<table class="table-style">\n', '    <thead>\n', '        <tr>\n', '            <th>'+titre+'</th>\n', '        </tr>\n', '    </thead>\n', '    <tbody>\n', '        <tr>\n', '            <td>Note</td>\n', '        </tr>\n', '        \n', '        </tr>\n', '    </tbody>\n', '</table></body></html>']
    ecrire_html(code_vide,notes(trier_episodes(trouver_episodes(trouver_titre(titre)))),page)
    webbrowser.open_new_tab(page+".html") #permet d'ouvrir le fichier HTML créé dans  

            #Cette fonction détermine le tconst, identifiant unique utilisé par IMDB, de la série à partir de son titre
def trouver_titre(titre) :
    tmp = pd.read_csv('data\\title.basics.tsv', sep='\t', low_memory=False)
#on selectionne que les séries TV et on enlève les colonnes inutiles  
    serie = tmp[tmp['titleType'] == 'tvSeries'].drop(['isAdult', 'endYear', 'runtimeMinutes', 'genres'], axis=1)
#avoir le ou LES index correspondant au titre. Il faudra donc faire une verrification que c'est bien celui demandé par l'utilisateur.
    index = serie[serie['primaryTitle'] == titre]
    annees_serie = index['startYear'].values.tolist() #On récupère seulement la première année de diffusion des série ayant le bon nom. Le .value permet d'extraire les données sous for de ndarray de Numpy puis le .tolist permet de le convertir en liste.
    tconst_serie = index['tconst'].values.tolist()
#Il faut gérer le cas où il existe plusieurs séries avec le même nom. Nous avons décidé d'utiliser la date de leur première diffusion comme élément distinguant (la probablité pour que deux séries du même nom sortent la même année étant très faible)
    if len(tconst_serie) > 1: 
        print('Plusieurs séries portent ce nom, voici l\'année de leur première diffusion respective : ')
        for an in annees_serie :
            print(an, end='  ',)
        while not(date in annees_serie) :
            date = input("\nQuelle est la date du début de votre série?\n")
            for i in range(len(annees_serie)) :
                if annees_serie[i] == date : 
                    return tconst_serie[i]
#Il faut aussi gérer le cas où la série n'est pas trouvée dans la liste fournie par IMDB
    elif len(tconst_serie) == 0 : 
        print("Nous sommes désolé mais cette série n'est pas dans notre base de donnée, veuillez réessayer :")
        main()
    else :
        return tconst_serie[0]

            #Cette fonction prend le tconst d'une série et récupère tous les episodes correspondant à cette série
def trouver_episodes(tconst_serie):
    tab_ep = pd.read_csv('data\\title.episode.tsv', sep='\t')
    episodes = tab_ep[tab_ep['parentTconst'] == tconst_serie]
    return episodes

            #Cette fonction renvoie un dictionnaire ayant pour clé le tconst d'un épisode et comme valeur une liste [numéro d'épisode, numéro de la saison], et ce pour tous les épisodes d'une série
def trier_episodes(episodes):
    episodes_tries = {}
    pilote = False#pour traiter le cas où il y a des épisodes pilote, ie indexé par 0. On récupère à la fois l'information de la présence d'épisodes pilote dans la série et les saisons où c'est le cas
    for ep in episodes['tconst'] :
        index_ep = episodes[episodes['tconst'] == ep].index[0]
        episodes_tries[ep] = [int(episodes['episodeNumber'][index_ep]),int(episodes['seasonNumber'][index_ep])]
        if int(episodes['episodeNumber'][index_ep]) == 0 :
            pilote = True
    return episodes_tries,pilote

            #Cette fonction calcule le nombre d'éléments différents dans une liste. Pour nous, le nombre maximale d'épisodes, pour toutes les saisons, afin de connaitre la dimension du tableau affichant les résultats
def nombre(episodes_tries,i):
    nbr = []
    for ep in episodes_tries :
        nbr.append(episodes_tries[ep][i])
    return len(set(nbr))

            #Cette fonction récupère les notes de tous les épisodes 
def notes(episodes_tries):
    pilote = episodes_tries[1]
    episodes_tries = episodes_tries[0]
    tab_notes = pd.read_csv('data\\title.ratings.tsv', sep='\t')
    dimension_episodes = nombre(episodes_tries,0)
    dimension_saison = nombre(episodes_tries,1)
    notes=[['' for _ in range(dimension_episodes)] for _ in range(dimension_saison)]
    if pilote :
            for l in notes :
                l.append('')
    for tconst_ep in episodes_tries :
        saison = episodes_tries[tconst_ep][1]
        numero = episodes_tries[tconst_ep][0]
        index_note = tab_notes[tab_notes['tconst'] == tconst_ep].index
        if str(index_note) == "Int64Index([], dtype='int64')" :
            note = 'Na'
        else:
            note = float(tab_notes['averageRating'].loc[index_note].values)
        if pilote :
            notes[saison-1][numero] = note
        else : notes[saison-1][numero-1] = note
    return notes,pilote

            #Cette fonction écrit le code HTML à partir d'un code déjà existant en ajoutant les lignes liées aux notes précédemment déterminées
def ecrire_html(code_vide,note,nom_fichier):
    notes = note[0]
    pilote = note[1]
    with open(nom_fichier +".html", 'w') as f:
        f.writelines(code_vide[:14])
        for j in range(len(notes)) :
            f.write( '            <th>'+str(j+1)+'</th>\n')
        f.writelines(code_vide[15:17])
        taille_max = max(len(notes[i]) for i in range(len(notes)))
        for k in range(taille_max) :
            f.write('        <tr>\n')
            debut=True
            for j in range(len(notes)) :
                if debut and not(pilote) :
                    f.write('            <td>'+str(k+1)+'</td>\n')
                    debut = False
                elif debut and pilote : 
                    f.write('            <td>'+str(k)+'</td>\n')
                    debut = False
                try :
                    f.write('            <td>'+str(notes[j][k])+'</td>\n')
                except IndexError :
                    f.write('            <td></td>\n')
            f.write('        </tr>\n')
        f.writelines(code_vide[22:])

main()
