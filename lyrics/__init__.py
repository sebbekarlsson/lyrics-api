import requests
from bs4 import BeautifulSoup


SEARCH_URL = "https://search.azlyrics.com/search.php?q={artist}+{title}"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}


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
    r = requests.get(SEARCH_URL.format(artist=artist, title=title), headers=HEADERS)
    doc = BeautifulSoup(r.text, 'html.parser')
    table = doc.select_one(".table.table-condensed")
    links = table.select("tr a")

    return list(map(get_lyrics_from_link, list(filter(lambda x: "http" in x, [a.get("href") for a in links]))))



