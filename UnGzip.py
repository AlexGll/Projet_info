import gzip
import shutil
from os import listdir
from os.path import isfile, join
import requests 


fichiers = [f for f in listdir('data') if isfile(join('data', f))]
print(fichiers)
for fichier in fichiers : 
   with gzip.open('data\\'+fichier, 'rb') as f_in:
       with open('data\\'+fichier[:-3], 'wb') as f_out:
           shutil.copyfileobj(f_in, f_out)
