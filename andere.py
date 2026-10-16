from wiktionary import (
    find_subsection_content,
    get_subsection_content,
    get_aussprache
)


# ==================================================
# Create content for Adverb section
def andere_content(word, word_class, section):
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
        "Front": word_class,
        "Andere": word,
        "Aussprache": aussprache,
        **content
    }