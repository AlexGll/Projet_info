from tkinter import *
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) #Pandas renvoie une erreur préventive pour ses prochaines versions, qui ne modifie donc pas le résultat obtenu.
import pandas as pd
import numpy as np 
import webbrowser 


def main(question):
    titre = demander(question)
    page = "affichage_notes_"+str(titre)
#Le résultat final état affiché sur une page HTML, nous avons fait en sorte de coder ce fichier .html depuis notre programme Python. 
    code_vide = ['<!DOCTYPE html>\n', '<html lang="fr">\n', '<head>\n', '    <meta charset="UTF-8">\n', '    <meta name="viewport" content="width=device-width, initial-scale=1" />\n', '    <title>Notes IMDB \t Karl LIEBEL et Alexandre GILLES</title>\n', '    <link rel="stylesheet" href="rendu.css">\n', '</head>\n', '<body> \n', '\n', '<table class="table-style">\n', '    <thead>\n', '        <tr>\n', '            <th>'+titre+'</th>\n', '        </tr>\n', '    </thead>\n', '    <tbody>\n', '        <tr>\n', '            <td>Note</td>\n', '        </tr>\n', '        \n', '        </tr>\n', '    </tbody>\n', '</table></body></html>']
    ecrire_html(code_vide,notes(trier_episodes(trouver_episodes(trouver_titre(titre)))),page)
    webbrowser.open_new_tab(page+".html") #permet d'ouvrir le fichier HTML créé dans  


            #Cette fonction ouvre une page tkinter en posant une question en argument et renvoyant la valeur donnée.
def demander(question):
    global reponse
    reponse=''
    #Initialisation de la page
    page1 = Tk ()
    page1.title("Notes IMDb Séries")
    page1.geometry("1080x720")
    page1.iconbitmap()
    page1.config(background="#f5c518")
    page1.state('zoomed')

    def get_input():
        global reponse
        reponse= reponse_input.get()
        return(reponse)

    #Cadre d'affichage
    cadre= Frame (page1, bg='#f5c518')
    cadre.pack(expand=YES)
    #Titre Principal
    label_Titre=Label(cadre, text=question, font=('Bauhaus 93',40), bg='#f5c518', fg='black')
    label_Titre.grid(row=0, column=0)
    #Bouton de lancement
    bouton_lancement = Button(cadre, text='Valider',font=('Bauhaus 93',20), bg='black', fg='#f5c518', command=lambda:[f for f in [get_input(),page1.destroy()]])
    bouton_lancement.grid(row=1, column=1)
    #Boutton de saisie
    reponse_input= Entry(cadre,font=('Bauhaus 93',20), bg='black', fg='#f5c518')
    reponse_input.grid(row=1, column=0)

    page1.mainloop()
    return reponse

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
        annees_str =''
        for k in annees_serie :
            annees_str += str(k)+', '
        annees_str = annees_str[:-2]
        date = 0
        while not(date in annees_serie):
            date = demander('Plusieurs séries portent ce nom.\nVoici l\'année de leur première diffusion respective :\n'+annees_str)
        for i in range(len(annees_serie)) :
            if annees_serie[i] == date : 
                return tconst_serie[i]
#Il faut aussi gérer le cas où la série n'est pas trouvée dans la liste fournie par IMDB
    elif len(tconst_serie) == 0 : 
        main("Nous sommes désolé mais cette série\nn'est pas dans notre base de donnée, veuillez réessayer :")
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
    pilote = False #pour traiter le cas où il y a des épisodes pilote, ie indexé par 0. On récupère à la fois l'information de la présence d'épisodes pilote dans la série et les saisons où c'est le cas
    for ep in episodes['tconst'] :
        index_ep = episodes[episodes['tconst'] == ep].index[0]
        if episodes['episodeNumber'][index_ep] == '\\N' or episodes['seasonNumber'][index_ep]== '\\N' :
            continue
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
def ecrire_html(code_vide,note_pilote,nom_fichier):
    notes = note_pilote[0]
    print(notes)
    pilote = note_pilote[1]
    with open(nom_fichier +".html", 'w') as f:
        f.writelines(code_vide[:14])
        for j in range(len(notes)) :
            f.write( '            <th>'+str(j+1)+'</th>\n')
        f.writelines(code_vide[15:17])
        taille_max = 0 
        for l in notes :
            long = len(l)
            if long > taille_max : 
                taille_max = long
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

main('Quel est le titre\nde la série dont vous souhaitez les notes IMDB ?\n(merci de mettre le titre en anglais avec les majuscules)')
