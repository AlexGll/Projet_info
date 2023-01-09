def main():
    global titre
    titre=''
    page1 = Tk ()
    page1.title("Notes IMDb Séries")
    page1.geometry("1080x720")
    page1.iconbitmap()
    page1.config(background="#f5c518")

    def get_input():
        global titre
        titre= titre_input.get()
        return(titre)

    #Cadre d'affichage
    cadre= Frame (page1, bg='#f5c518')
    cadre.pack(expand=YES)
    #Titre Principal
    label_Titre=Label(cadre, text='Quel est le titre de la série ?', font=('Bauhaus 93',40), bg='#f5c518', fg='black')
    label_Titre.grid(row=0, column=0)

    #Bouton de lancement
    bouton_lancement = Button(cadre, text='Chercher',font=('Bauhaus 93',20), bg='black', fg='#f5c518', command=get_input)
    bouton_lancement.grid(row=1, column=1)

    #Boutton de saisie
    titre_input= Entry(cadre,font=('Bauhaus 93',20), bg='black', fg='#f5c518')
    titre_input.grid(row=1, column=0)
    #Bouton exit
    bouton_exit= Button(cadre, text='fermer', font=('Bauhaus 93',20), bg='black', fg='#f5c518', command=page1.destroy)
    bouton_exit.grid(row=1, column=2)

    page1.mainloop() 
    print(titre)
    page = "affichage_notes_"+str(titre)
#Le résultat final état affiché sur une page HTML, nous avons fait en sorte de coder ce fichier .html depuis notre programme Python. 
    code_vide = ['<!DOCTYPE html>\n', '<html lang="fr">\n', '<head>\n', '    <meta charset="UTF-8">\n', '    <meta name="viewport" content="width=device-width, initial-scale=1" />\n', '    <title>Notes IMDB \t Karl LIEBEL et Alexandre GILLES</title>\n', '    <link rel="stylesheet" href="rendu.css">\n', '</head>\n', '<body> \n', '\n', '<table class="table-style">\n', '    <thead>\n', '        <tr>\n', '            <th>'+titre+'</th>\n', '        </tr>\n', '    </thead>\n', '    <tbody>\n', '        <tr>\n', '            <td>Note</td>\n', '        </tr>\n', '        \n', '        </tr>\n', '    </tbody>\n', '</table></body></html>']
    ecrire_html(code_vide,notes(trier_episodes(trouver_episodes(trouver_titre(titre)))),page)
    webbrowser.open_new_tab(page+".html") #permet d'ouvrir le fichier HTML créé dans  

            #Cette fonction détermine le tconst, identifiant unique utilisé par IMDB, de la série à partir de son titre
def trouver_titre(titre) :
    tmp = pd.read_csv('Desktop/title.basics.tsv', sep='\t', low_memory=False)
#on selectionne que les séries TV et on enlève les colonnes inutiles  
    serie = tmp[tmp['titleType'] == 'tvSeries'].drop(['isAdult', 'endYear', 'runtimeMinutes', 'genres'], axis=1)
#avoir le ou LES index correspondant au titre. Il faudra donc faire une verrification que c'est bien celui demandé par l'utilisateur.
    index = serie[serie['primaryTitle'] == titre]
    annees_serie = index['startYear'].values.tolist() #On récupère seulement la première année de diffusion des série ayant le bon nom. Le .value permet d'extraire les données sous for de ndarray de Numpy puis le .tolist permet de le convertir en liste.
    tconst_serie = index['tconst'].values.tolist()
    global date
    date='T'
#Il faut gérer le cas où il existe plusieurs séries avec le même nom. Nous avons décidé d'utiliser la date de leur première diffusion comme élément distinguant (la probablité pour que deux séries du même nom sortent la même année étant très faible)
    if len(tconst_serie) > 1: 
        page2 = Tk ()
        page2.title("Année de Sortie")
        page2.geometry("1080x720")
        page2.config(background="#f5c518")

        def get_input():
            global date
            date= date_input.get()
            return(date)

        #Cadre d'affichage
        cadre= Frame (page2, bg='#f5c518')
        cadre.pack(expand=YES)
        #Titre Principal
        label_Titre=Label(cadre, text='Plusieurs séries portent ce nom', font=('Bauhaus 93',40), bg='#f5c518', fg='black')
        label_Titre.grid(row=0, column=0)
        label_Titre2=Label(cadre, text='voici l\'année de leur première diffusion respective :', font=('Bauhaus 93',40), bg='#f5c518', fg='Black')
        label_Titre2.grid(row=1, column=0)
        label_Titre3=Label(cadre, text=f'{annees_serie}', font=('Bauhaus 93',40), bg='#f5c518', fg='Black')
        label_Titre3.grid(row=2, column=0)


        #Bouton de lancement
        bouton_lancement = Button(cadre, text='Chercher',font=('Bauhaus 93',20), bg='#f5c518', fg='Black', command=get_input)
        bouton_lancement.grid(row=3, column=0, sticky=E)

        #Boutton de saisie
        date_input= Entry(cadre,font=('Bauhaus 93',20), bg='#f5c518', fg='Black')
        date_input.grid(row=3, column=0)
        #Bouton exit
        bouton_exit= Button(cadre, text='fermer', font=('Bauhaus 93',20), bg='#f5c518', fg='black', command=page2.destroy)
        bouton_exit.grid(row=3, column=1)

        page2.mainloop()
        print(date)
        for i in range(len(annees_serie)) :
            if annees_serie[i] == date : 
                return tconst_serie[i]
#Il faut aussi gérer le cas où la série n'est pas trouvée dans la liste fournie par IMDB
    elif len(tconst_serie) == 0 : 
        print("Nous sommes désolé mais cette série n'est pas dans notre base de donnée, veuillez réessayer :")
        main()
    else :
        return tconst_serie[0]
