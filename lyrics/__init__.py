import requests
from bs4 import BeautifulSoup
import json
import os


cache = json.loads(open("cache.json").read())\
    if os.path.isfile("cache.json") else {}

SEARCH_URL = "https://search.azlyrics.com/search.php?q={artist}+{title}"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}


def gethash(artist, title):
    return artist.lower() + title.lower()


def get_lyrics_from_link(link):
    r = requests.get(link, headers=HEADERS)
    doc = BeautifulSoup(r.text, 'html.parser')
    center = doc.select_one(".col-xs-12.col-lg-8.text-center")
    if not center:
        return None
    div = center.select_one("div:nth-of-type(5)")
    if not div:
        return None
    return { 'lyrics': div.text.strip() }
    # body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center > div:nth-child(8)

def search(artist, title):
    h = gethash(artist, title)
    
    if h in cache:
        return cache[h]

    r = requests.get(SEARCH_URL.format(artist=artist, title=title), headers=HEADERS)
    doc = BeautifulSoup(r.text, 'html.parser')
    table = doc.select_one(".table.table-condensed")

    if not table:
        return []
    links = table.select("tr a")

    if not links:
        return []

    data = list(map(get_lyrics_from_link, list(filter(lambda x: "http" in x, [a.get("href") for a in links]))))

    if not data:
        r = requests.get("https://www.lyricsmode.com/lyrics/a/{artist}/{title}.html".format(artist=artist.replace(' ', '_'), title=title.replace(' ', '_')), headers=HEADERS)
        doc = BeautifulSoup(r.text, 'html.parser')
        div = doc.select_one("#lyrics_text")
        data = div.text if div else None
        data = { 'lyrics': data } if data else []

    cache[h] = data

    return data
