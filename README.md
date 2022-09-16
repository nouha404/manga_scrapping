# manga_scrapping
For Sensei  :- [@MedouneSGB](https://github.com/MedouneSGB)

```python
 pprint('Be sure to download only the main branch file (manga_extractor _v2 ) to test the script')
```

### Mini function to try download the image of a chapter

```python
def download_images(url):
    # Comme d'hab ca bypass le status code 403
    response = requests.get(url, headers=headers, stream = True)
    name = 'image.jpg'

    # Empecher la taille de l'image d'etre nulle Thiey google.
    response.raw.decode_content = True

    with open(name, 'wb') as f:
        shutil.copyfileobj(response.raw, f)
    pprint('Telechargement reussi babinks')
    
   """
      La méthode shutil.copyfileobj() en Python est utilisée pour copier le contenu d’un objet de type fichier vers un autre objet de type fichier. Par défaut,                cette méthode copie les données en morceaux et, si vous le souhaitez, nous pouvons également spécifier la taille de la mémoire tampon via le paramètre de longueur.
     Cette méthode copie le contenu du fichier de la position actuelle du fichier jusqu’à la fin du fichier.
   """


download_images('https://www.scan-vf.net/uploads/manga/one_piece/chapters/chapitre-1059/16.jpg')
```
