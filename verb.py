# ==================================================
# All Verb content
# ==================================================
from wiktionary import (
    find_subsection_content,
    get_subsection_content,
    get_aussprache,
    get_ipa_from_url
)


# ==================================================
# Takes section html, gives perfekt/präteritum text and its aussprache text
def find_verb_forms(section):
    table = section.find(
        "table",
        class_="inflection-table"
    )
    if table is None:
        return None, None, None, None, None, None, None

    praeteritum = None
    praeteritum_url = None
    perfekt = None
    perfekt_url = None
    hilfsverb = None
    dritte_person = None
    dritte_url = None

    for row in table.find_all("tr"):
        header = row.find("th")

        # ------------------------------------------
        # 3rd person singular Präsens
        cells = row.find_all("td")
        if len(cells) >= 2:
            dritte = cells[0].get_text(" ", strip=True)

            if dritte == "er, sie, es":
                link = cells[1].find("a")
                
                if link is not None:
                    dritte_person = link.get_text(" ", strip=True)
                    dritte_url = link.get("href")


        if header is None:
            continue
        header_text = header.get_text(
            " ",
            strip=True
        )

        # ------------------------------------------
        # Präteritum
        if header_text == "Präteritum":
            cells = row.find_all("td")
            if cells:
                link = cells[-1].find("a")
                if link is not None:
                    praeteritum = link.get_text(
                        " ",
                        strip=True
                    )
                    praeteritum_url = link.get(
                        "href"
                    )

        # ------------------------------------------
        # Perfekt
        elif header_text == "Perfekt":
            next_row = row.find_next_sibling("tr")
            if next_row is not None:
                links = next_row.find_all("a")
                if len(links) >= 2:
                    # Partizip II
                    perfekt = links[0].get_text(
                        " ",
                        strip=True
                    )
                    perfekt_url = links[0].get(
                        "href"
                    )
                    # Hilfsverb
                    hilfsverb = links[1].get_text(
                        " ",
                        strip=True
                    )

    return (
        praeteritum,
        praeteritum_url,
        perfekt,
        perfekt_url,
        hilfsverb,
        dritte_person,
        dritte_url
    )


# ==================================================
# Takes verb section html, returns verb dictionary
def verb_content(word, section):
    (
        praeteritum,
        praeteritum_url,
        perfekt,
        perfekt_url,
        hilfsverb,
        dritte_person,
        dritte_url
    ) = find_verb_forms(section)
    
    aussprache_praeteritum = get_ipa_from_url(
        praeteritum_url
    )


    aussprache_perfekt = get_ipa_from_url(
        perfekt_url
    )


    aussprache_dritte = get_ipa_from_url(
        dritte_url
    )
    

    aussprache_html = find_subsection_content(
        "Aussprache",
        section
    )
    aussprache = get_aussprache(
        aussprache_html
    )


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
        "Front": "Verb",
        "Verb": word,
        "Aussprache": aussprache,

        "Präteritum": praeteritum,
        "Präteritum Aussprache": aussprache_praeteritum,

        "Perfekt": " ".join(
            x for x in [perfekt, hilfsverb]
            if x is not None
        ),
        "Perfekt Aussprache": aussprache_perfekt,
        
        "3. Singular": dritte_person,
        "3. Singular Aussprache": aussprache_dritte,

        **content
    }