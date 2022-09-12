from pprint import pprint
from pathlib import Path
from tinydb import TinyDB

from bs4 import BeautifulSoup
import requests

# on bypass le status_code 403 thanks india youtuber
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36 Edg/105.0.1343.33'
}
# Creation du fichier Json
db = TinyDB('manga.json', indent=4)


def main_link(url='https://www.scan-vf.net/'):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    manga_liste = soup.find('div', class_='mangalist')

    all_links = []
    for _ in manga_liste:
        manga_items = soup.findAll('div', 'manga-item')
        for link in manga_items:
            books_name = link.find('a')
            links = books_name['href']
            all_links.append(links)

    CHAPTERS_LINKS = []
    # Limiter le nombre d'item a 10
    for link in range(10):
        response = requests.get(all_links[link], headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        chaptres_link = soup.find('h5', class_='chapter-title-rtl')
        extrate_link = chaptres_link.find('a')
        link_extrated = extrate_link['href']
        CHAPTERS_LINKS.append(link_extrated)

        if response.status_code == 200:
            print(f'Chargement de {link_extrated} ...')
    # Partie 2 : Le lien d'un scan spécifique avec son nom
    CHAPTERS = []
    for i in CHAPTERS_LINKS:
        pprint(f'Chargement du scan spécifique...')
        extrate_number_chapters = Path(i)
        # recuperer le lien avec seulement le nom du scan sans les chapitres
        CHAPTERS.append(
            f'{extrate_number_chapters.parts[0]}//{extrate_number_chapters.parts[1]}/{extrate_number_chapters.parts[2]}')

    # Partie 3 : recuperer tout les chapitres
    for chaptre_url in CHAPTERS:
        RESPONSE = requests.get(chaptre_url, headers=headers)
        SOUP = BeautifulSoup(RESPONSE.content, 'html.parser')

        chapters = SOUP.find('ul', class_='chapters')
        all_chapters = chapters.findAll('a')

        ALL_CHAPTERS = []
        for chapter in all_chapters:
            # extraire les lien
            links_of_all_chapters = chapter['href']
            ALL_CHAPTERS.append(links_of_all_chapters)
        get_scan_name = SOUP.find('h2', class_='widget-title')

        db.insert({'names': get_scan_name.text, 'chapters': ALL_CHAPTERS})


main_link()