# =================================================
# Actions on Wiktionary page
# =================================================
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import quote


# =================================================
# url delay if error
def make_request(url):

    headers = {
        "User-Agent": "GermanAnkiCardGenerator/1.0"
    }

    while True:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code == 429:
            print("Too many requests. Waiting 30 seconds...")
            time.sleep(30)
            continue

        return response

# =================================================
# Downloads Wiktionary page
def get_page(word):
    url = "https://de.wiktionary.org/wiki/" + quote(word)
    headers = {
        "User-Agent": "GermanAnkiCardGenerator/1.0"
    }
    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )
    if response.status_code == 404:
        print("Nicht gefunden:", word)
        return None
    
    response.raise_for_status()

    return BeautifulSoup(response.text, "html.parser")


# ==================================================
# Takes page html, returns word class and its html section
def get_word_class(soup):
    section = soup.find(
        "section",
        {"data-mw-section-id": "2"}
    )
    if section is None:
        return None, None

    heading = section.find("h3")
    if heading is None:
        return None, section
    
    word_class = heading.get_text(" ", strip=True).split(",")[0].strip()
    return word_class, section


# =================================================
# Takes section html and returns subsection html by name
def find_subsection_content(name, section):
    if section is None:
        return None

    for p in section.find_all("p"):
        text = p.get_text(" ", strip=True)
        if text == name + ":":
            return p.find_next_sibling("dl")

    return None


# =================================================
# Takes subsection html and gets its text
def get_subsection_content(subsection):
    if subsection is None:
        return None

    content = []
    for dd in subsection.find_all("dd"):
        content.append(
            "".join(str(element) for element in dd.contents)
        )

    return content


# =================================================
# Takes Aussprache subsection html and gets its text
def get_aussprache(aussprache):
    if aussprache is None:
        return None

    ipa = aussprache.find("span", class_="ipa")
    if ipa is None:
        return None
    return "[" + ipa.get_text(" ", strip=True) + "]"


# ==================================================
# Gets aussprache from url
def get_ipa_from_url(url):
    if url is None:
        return None
    
    response = requests.get(
        url,
        headers={
            "User-Agent": "GermanAnkiCardGenerator/1.0"
        },
        timeout=10
    )
    response.raise_for_status()
    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )
    ipa = soup.find(
        "span",
        class_="ipa"
    )

    if ipa is None:
        return None
    return "[" + ipa.get_text(strip=True) + "]"