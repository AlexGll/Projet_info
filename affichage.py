import webbrowser

code_vide = ['<!DOCTYPE html>\n', '<html lang="fr">\n', '<head>\n', '    <meta charset="UTF-8">\n', '    <meta name="viewport" content="width=device-width, initial-scale=1" />\n', '    <title>Titre</title>\n', '    <link rel="stylesheet" href="rendu.css">\n', '</head>\n', '<body> \n', '\n', '<table class="table-style">\n', '    <thead>\n', '        <tr>\n', '            <th>Saison X</th>\n', '        </tr>\n', '    </thead>\n', '    <tbody>\n', '        <tr>\n', '            <td>Note</td>\n', '        </tr>\n', '        \n', '        </tr>\n', '    </tbody>\n', '</table></body></html>']
episodes_tries = [[8.2, 8.2, 7.6, 8.0, 7.9, 8.3, 8.0, 8.2, 7.8, 8.3, 8.2, 8.0, 8.0, 8.2, 8.3, 8.5, 8.1, 6.5], [7.7, 9.1, 7.9, 7.9, 8.0, 8.8, 8.1, 8.1, 8.1, 8.1, 8.0, 7.9, 8.5, 8.1, 8.7, 7.9, 8.3, 8.2, 8.6, 8.1, 8.1, 8.2, 8.2], [8.3, 8.1, 7.8, 7.5, 8.0, 8.3, 7.8, 8.9, 8.3, 8.5, 8.3, 8.3, 8.0, 8.4, 8.0, 8.3, 8.4, 7.9, 8.4, 8.6, 8.1, 8.1, 9.0], [8.7, 7.7, 8.7, 7.6, 8.2, 7.7, 7.7, 7.9, 7.9, 8.1, 8.0, 8.3, 8.2, 8.2, 7.8, 8.0, 7.9, 8.0, 7.7, 8.0, 8.0, 8.1, 8.4, 8.5], [8.0, 8.0, 7.7, 7.8, 8.0, 7.5, 8.5, 7.6, 8.1, 7.9, 7.3, 7.6, 8.1, 8.2, 7.7, 7.6, 7.8, 8.2, 8.1, 8.1, 8.5, 7.7, 8.1, 8.5], [7.6, 7.9, 7.6, 8.2, 8.0, 7.8, 7.7, 8.4, 8.2, 8.0, 7.8, 8.4, 8.4, 8.2, 7.8, 7.8, 7.6, 7.7, 8.1, 8.0, 7.9, 8.0, 8.1, 7.7], [8.0, 7.8, 8.7, 7.9, 7.6, 8.4, 7.7, 7.6, 8.8, 8.1, 7.4, 7.5, 7.6, 7.9, 8.2, 7.6, 7.4, 7.4, 8.1, 8.0, 7.5, 7.7, 7.8, 8.0], [7.2, 7.5, 7.0, 7.2, 7.4, 7.2, 8.0, 7.7, 7.5, 7.0, 7.4, 7.2, 7.4, 8.0, 8.0, 7.8, 7.5, 7.3, 7.5, 7.5, 7.0, 7.3, 7.5, 7.9], [6.8, 7.3, 7.7, 7.4, 7.4, 7.9, 7.2, 7.9, 7.8, 8.3, 9.0, 7.4, 7.4, 7.5, 7.5, 7.4, 7.5, 7.5, 7.4, 7.8, 7.4, 7.4, 7.4, 7.3], [7.7, 7.4, 7.3, 7.2, 7.9, 7.4, 7.9, 8.0, 7.4, 7.3, 7.5, 7.3, 6.9, 7.2, 7.3, 7.1, 7.4, 7.1, 7.1, 7.1, 7.2, 6.7, 7.1, 8.5], [7.5, 7.6, 7.2, 8.9, 7.4, 7.1, 7.1, 6.8, 7.2, 7.1, 7.4, 7.2, 7.2, 7.4, 7.1, 7.3, 7.7, 7.1, 7.4, 7.2, 7.3, 7.1, 7.0, 7.2], [7.1, 7.6, 7.0, 7.2, 6.8, 7.3, 7.2, 7.3, 8.2, 7.2, 7.1, 7.4, 7.0, 7.1, 7.4, 7.9, 6.9, 7.1, 7.0, 7.1, 7.9, 7.2, 9.0, 9.5]]

def ecrire_html(code_vide,episodes_tries,nom_fichier):
    with open(nom_fichier +".html", 'w') as f:
        f.writelines(code_vide[:13])
        f.write( '            <th>Episodes\Saisons</th>\n')
        for j in range(len(episodes_tries)) :
            f.write( '            <th>'+str(j+1)+'</th>\n')
        f.writelines(code_vide[15:17])
        taille_max = max(len(episodes_tries[i]) for i in range(len(episodes_tries)))
        for k in range(taille_max) :
            f.write('        <tr>\n')
            debut=True
            for j in range(len(episodes_tries)) :
                if debut :
                    f.write('            <td>'+str(k+1)+'</td>\n')
                    debut = False
                try :
                    f.write('            <td>'+str(episodes_tries[j][k])+'</td>\n')
                except IndexError :
                    f.write('            <td></td>\n')
            f.write('        </tr>\n')
        f.writelines(code_vide[22:])
        
page = "affichage_test"
ecrire_html(code_vide,episodes_tries,page)
webbrowser.open_new_tab(page+".html")
