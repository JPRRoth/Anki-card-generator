# ==================================================
# All Substantiv content
# ==================================================
import requests
from bs4 import BeautifulSoup
from wiktionary import (
    find_subsection_content,
    get_subsection_content,
    get_aussprache,
    get_ipa_from_url
)
from urllib.parse import urljoin

# ==================================================
# Create content for Substantiv section
def substantiv_content(section):
    substantiv, substantiv_plural, aussprache_plural = find_substantiv_table(
        section
    )


    aussprache_html = find_subsection_content(
        "Aussprache",
        section
    )
    aussprache = get_aussprache(aussprache_html)

    subsections_list = [
        "Bedeutungen",
        "Sinnverwandte Wörter",
        "Synonyme",
        "Beispiele",
        "Gegenwörter",
        "Herkunft"
    ]
    content = {}

    for name in subsections_list:
        subsection_html = find_subsection_content(
            name,
            section
        )
        content[name] = get_subsection_content(
            subsection_html
        )

    return {
        "Front": "Substantiv",
        "Substantiv": substantiv,
        "Aussprache": aussprache,
        "Substantiv Plural": substantiv_plural,
        "Aussprache Plural": aussprache_plural,
        **content
    }


# ==================================================
# Takes section html, finds and gets substantiv text and gets plural_aussprache text
def find_substantiv_table(section):
    if section is None:
        return None

    table = section.find("table")
    if table is None:
        return None, None, None

    for row in table.find_all("tr"):
        header = row.find("th")
        
        if header is None:
            continue

        if header.get_text(strip=True) == "Nominativ":
            cells = row.find_all("td")
            
            singular = "".join(
                str(element) for element in cells[0].contents
            ).strip()
            
            plural = "".join(
                str(element) for element in cells[1].contents
            ).strip()

            plural_link = cells[1].find("a")
            if plural_link is None:
                plural_aussprache = None
            else:
                plural_url = urljoin(
                "https://de.wiktionary.org",
                plural_link.get("href")
            )
                plural_aussprache = get_ipa_from_url(
                plural_url
            )
            return singular, plural, plural_aussprache
    return None, None, None