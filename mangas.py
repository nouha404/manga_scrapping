from pathlib import Path
from tinydb import TinyDB
from pprint import pprint

from bs4 import BeautifulSoup
import requests

# on bypass le status_code 403 thanks india youtuber
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36 Edg/105.0.1343.33'
}

array_chapters = []
CHAPTERS_LINKS = []
db = TinyDB('data.json', indent=4)


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

    # Recuperer les range(10) des mangas dans la liste
    for link in range(10):
        response = requests.get(all_links[link], headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        chaptres_link = soup.find('h5', class_='chapter-title-rtl')
        extrate_link = chaptres_link.find('a')
        link_extrated = extrate_link['href']
        CHAPTERS_LINKS.append(link_extrated)
        # chapter name
        get_scan_name = soup.find('h2', class_='widget-title').text

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
    return array_chapters.extend(CHAPTERS)


main_link()
pprint('Recuperation de tous les chapitres...')

GLOBAL_CHAPTERS = []


def get_all_chapters(url: list):
    for src in url:
        response = requests.get(src, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # search
        chapters = soup.find('ul', class_='chapters')
        all_chapters = chapters.findAll('a')
        get_scan_name = soup.find('h2', class_='widget-title').text

        for link in all_chapters:
            links = link['href']
            GLOBAL_CHAPTERS.append(links)
            # searching images
            response_of_picture = requests.get(links, headers=headers)
            soup_of_picture = BeautifulSoup(response_of_picture.content, 'html.parser')
            # get class
            container_image = soup_of_picture.findAll('img', class_='img-responsive')
            IMAGES = []
            for img_src in container_image:
                image_extracted = img_src.get('data-src')
                IMAGES.append(image_extracted)
                pprint('Extraction de tous les images...')
            # insert on database
            db.insert({'manga_name': get_scan_name, 'last_chapter': GLOBAL_CHAPTERS[0], 'images': IMAGES})
    return pprint('Tous les chapitres sont sauvegarder...')


get_all_chapters(array_chapters)