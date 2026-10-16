# ==================================================
# All Adjektiv content
# ==================================================
from wiktionary import (
    find_subsection_content,
    get_subsection_content,
    get_aussprache,
    get_ipa_from_url
)


# ==================================================
# Create content for Adjektiv section
def find_adjektiv_table(section):
    table = section.find(
        "table",
        class_="inflection-table"
    )
    if table is None:
        return None, None, None, None, None

    rows = table.find_all("tr")
    if len(rows) < 2:
        return None, None, None, None, None

    cells = rows[1].find_all("td")
    if len(cells) < 3:
        return None, None, None, None, None

    # ------------------------------------------
    # Positiv
    positiv = cells[0].get_text(
        " ",
        strip=True
    )


    # ------------------------------------------
    # Komparativ
    komparativ_link = cells[1].find("a")
    if komparativ_link is None:
        komparativ = cells[1].get_text(
            " ",
            strip=True
        )
        komparativ_aussprache = None

    else:
        komparativ = komparativ_link.get_text(
            " ",
            strip=True
        )
        komparativ_aussprache = get_ipa_from_url(
            komparativ_link.get("href")
        )


    # ------------------------------------------
    # Superlativ
    superlativ = cells[2].get_text(
        " ",
        strip=True
    )
    superlativ_link = cells[2].find("a")
    if superlativ_link is None:
        superlativ_aussprache = None

    else:
        superlativ_aussprache = get_ipa_from_url(
            superlativ_link.get("href")
        )

    return (
        positiv,
        komparativ,
        komparativ_aussprache,
        superlativ,
        superlativ_aussprache
    )


# ==================================================
# Takes Adjektiv content html, returns dictionary
def adjektiv_content(section):
    (
        positiv,
        komparativ,
        komparativ_aussprache,
        superlativ,
        superlativ_aussprache
    ) = find_adjektiv_table(section)


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
        "Front": "Adjektiv",
        "Adjektiv": positiv,
        "Aussprache": aussprache,
        "Komparativ": komparativ,
        "Komparativ Aussprache": komparativ_aussprache,
        "Superlativ": superlativ,
        "Superlativ Aussprache": superlativ_aussprache,

        **content
    }